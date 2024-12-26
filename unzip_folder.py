import os
from time import sleep

from objaverse_dataset_manage.Method.zip import unzipFolder


if __name__ == "__main__":
    root_list = [
        '/mnt/d/chLi/Dataset/',
        os.environ['HOME'] + '/chLi/Dataset/',
    ]

    root_folder_path = None
    for root in root_list:
        if os.path.exists(root):
            root_folder_path = root
            break
    if root_folder_path is None:
        print("[ERROR][unzip_folder::__main__]")
        print("\t dataset not found!")
        exit()

    target_folder = 'glbs'
    target_folder = 'manifold_sdf_0_25'

    zip_files_folder_path = root_folder_path + 'Objaverse_82K/' + target_folder + '_zip/'
    unzip_folder_path = root_folder_path + 'Objaverse_82K/' + target_folder + '/'

    while True:
        unzipFolder(zip_files_folder_path, unzip_folder_path)
        sleep(60)
