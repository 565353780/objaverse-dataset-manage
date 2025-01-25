import os
import glob
import json 
import gzip
import trimesh

def extract_models_from_dump(file_path):
    model_sizes = {}
    current_model = None
    with open(file_path, 'r') as file:
        for line in file:
            # Get model path
            if ".glb" in line:
                # Extract model path
                model_path = line.split()[-1].strip()
                model_path = model_path.replace("b/", "")
                current_model = model_path
            # Get current_model size
            elif current_model and "size" in line: 

                size = int(line.split()[-1].strip()) 
                model_sizes[current_model] = size 
                current_model = None
    return model_sizes

def getModelSizeList() -> list:
    with gzip.open("../objaverse-dataset-manage/data/model_sizes.json.gz", 'rb') as gzip_file:
        model_sizes = json.loads(gzip_file.read().decode('utf-8'))

    return model_sizes

def getExistingModelPathDict(glbs_folder_path: str) -> dict:
    existing_models = {}
    for file_path in glob.iglob(glbs_folder_path + '/**/*', recursive=True):
        if os.path.isfile(file_path):
            file_name = os.path.splitext(file_path)[0]
            existing_models[os.path.basename(file_name)] = file_path
    return existing_models

def getMetaDataDict(metadata_folder_path: str, existing_models: dict) -> dict:
    metadata = {}
    filtered_metadata = { }

    metadata_path = metadata_folder_path
    for file_name in os.listdir(metadata_path):
        if file_name.endswith(".gz"):
            file_path = os.path.join(metadata_path, file_name)
            with gzip.open(file_path, 'rt', encoding='utf-8') as f:
                metadata = json.load(f)
                for key, value in existing_models.items():
                    if key in metadata:
                        filtered_metadata[key] = metadata[key]
                        filtered_metadata[key]['file_path'] = value

    return filtered_metadata


def tryLoadGlb(glb_file_path: str) -> bool:
    try:
        trimesh.load(glb_file_path)
        return True
    except Exception as e:
        print('[WARN][io::tryLoadGlb]')
        print('\t load glb file failed!')
        print('\t glb_file_path:', glb_file_path)
        return False
