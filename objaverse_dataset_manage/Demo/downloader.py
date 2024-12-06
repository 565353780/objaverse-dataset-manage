import os

from objaverse_dataset_manage.Module.downloader import Downloader

def demo():
    dataset_root_folder_path = '/home/chli/chLi/Dataset/'
    minKb = 2
    maxKb = 40
    num_threads = os.cpu_count()

    downloader = Downloader(dataset_root_folder_path)

    downloader.downloadGlbs(minKb, maxKb, num_threads)
    return True
