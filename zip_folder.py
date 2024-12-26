import os

from objaverse_dataset_manage.Method.zip import zipFolder


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
        print("[ERROR][zip_folder::__main__]")
        print("\t dataset not found!")
        exit()

    folders_folder_path = root_folder_path + 'Objaverse_82K/manifold_sdf_0_25/'
    zip_folder_path = root_folder_path + 'Objaverse_82K/manifold_sdf_0_25_zip/'

    zipFolder(folders_folder_path, zip_folder_path)
