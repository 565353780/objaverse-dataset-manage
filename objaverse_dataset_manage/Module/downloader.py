import os
import json 

from objaverse_dataset_manage.Config.url import BASE_URL, METADATA_BASE_URL
from objaverse_dataset_manage.Method.io import getModelSizeList, getExistingModelPathDict, getMetaDataDict
from objaverse_dataset_manage.Method.download import download_filtered_models, download_metadata


class Downloader(object):
    def __init__(self, dataset_root_folder_path: str) -> None:
        self.dataset_root_folder_path = dataset_root_folder_path

        self.save_dir = self.dataset_root_folder_path + 'Objaverse/'
        self.save_metadata_dir = self.dataset_root_folder_path + 'Objaverse/metadata/'
        self.glbs_directory = self.dataset_root_folder_path + '/Objaverse/glbs/'

        os.makedirs(self.save_dir, exist_ok=True)
        os.makedirs(self.save_metadata_dir, exist_ok=True)
        os.makedirs(self.glbs_directory, exist_ok=True)
        return

    def downloadGlbs(self, minKb: int = 2, maxKb: int = 80, num_threads: int = 6) -> bool:
        model_sizes = getModelSizeList()
        print('full objaverse dataset model num =', len(model_sizes))

        download_filtered_models(model_sizes, BASE_URL, self.save_dir, minKb, maxKb, num_threads)

        download_metadata(METADATA_BASE_URL, self.save_metadata_dir)

        extract_models = getExistingModelPathDict(self.glbs_directory)

        filtered_metadata = getMetaDataDict(extract_models)

        with open(self.save_dir + 'metadata.json'  , 'w') as f:
            json.dump(filtered_metadata, f)

        return True
