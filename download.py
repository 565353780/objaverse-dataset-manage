import os
from objaverse_dataset_manage.Module.downloader import Downloader

if __name__ == "__main__":
    dataset_root_folder_path = '/home/chli/chLi/Dataset/'
    minKb = 2
    maxKb = 80
    minKb = 2
    maxKb = 1000
    num_threads = os.cpu_count()

    downloader = Downloader(dataset_root_folder_path)

    downloader.downloadGlbs(minKb, maxKb, num_threads)
