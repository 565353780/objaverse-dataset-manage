import os
import json 
from tqdm import tqdm
from multiprocessing import Pool

from objaverse_dataset_manage.Config.url import BASE_URL, METADATA_BASE_URL
from objaverse_dataset_manage.Method.io import getModelSizeList, getExistingModelPathDict, getMetaDataDict, tryLoadGlb, tryLoadGlb
from objaverse_dataset_manage.Method.download import download_kiuiv2_filtered_models, download_metadata
from objaverse_dataset_manage.Method.path import removeFile


class Downloader(object):
    def __init__(self, dataset_root_folder_path: str) -> None:
        self.dataset_root_folder_path = dataset_root_folder_path

        self.save_dir = self.dataset_root_folder_path + 'Objaverse_82K/'
        self.save_metadata_dir = self.dataset_root_folder_path + 'Objaverse_82K/metadata/'
        self.glbs_directory = self.dataset_root_folder_path + 'Objaverse_82K/glbs/'

        os.makedirs(self.save_dir, exist_ok=True)
        os.makedirs(self.save_metadata_dir, exist_ok=True)
        os.makedirs(self.glbs_directory, exist_ok=True)
        return

    def downloadGlbs(self, csv_file_path: str, num_threads: int = 6) -> bool:
        print('[INFO][Downloader::downloadGlbs]')
        print('\t start download_filtered_models...')
        download_kiuiv2_filtered_models(csv_file_path, BASE_URL, self.save_dir, num_threads)

        print('[INFO][Downloader::downloadGlbs]')
        print('\t start download_metadata...')
        download_metadata(METADATA_BASE_URL, self.save_metadata_dir)

        print('[INFO][Downloader::downloadGlbs]')
        print('\t start getExistingModelPathDict...')
        extract_models = getExistingModelPathDict(self.glbs_directory)

        print('[INFO][Downloader::downloadGlbs]')
        print('\t start getMetaDataDict...')
        filtered_metadata = getMetaDataDict(self.save_metadata_dir, extract_models)

        with open(self.save_dir + 'metadata.json'  , 'w') as f:
            json.dump(filtered_metadata, f)

        return True

    def removeInvalidGlb(self, model_id: str) -> bool:
        glb_file_path = self.glbs_directory + model_id + '.glb'

        if not os.path.exists(glb_file_path):
            return True

        if not tryLoadGlb(glb_file_path):
            print('[ERROR][Downloader::removeInvalidGlbs]')
            print('\t tryLoadGlb failed!')

            removeFile(glb_file_path)
            return True

        return True

    def removeInvalidGlbs(self, worker_num: int = 1) -> bool:
        classname_list = os.listdir(self.glbs_directory)
        classname_list.sort()

        for classname in classname_list:
            class_folder_path = self.glbs_directory + classname + "/"

            modelid_list = os.listdir(class_folder_path)
            modelid_list.sort()

            full_model_id_list = [classname + '/' + model_id[:-4] for model_id in modelid_list]

            print("[INFO][MeshConvertor::convertAllShapes]")
            print('\t start convert all shapes in', classname, '...')
            with Pool(worker_num) as pool:
                results = list(tqdm(
                    pool.imap(self.removeInvalidGlb, full_model_id_list),
                    total=len(full_model_id_list),
                    desc="Processing"
                ))

        return True
