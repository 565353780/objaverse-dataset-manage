import os

from objaverse_dataset_manage.Method.path import renameFile

def zipFolder(folders_folder_path: str, zip_folder_path: str) -> bool:
    if not os.path.exists(folders_folder_path):
        print("[ERROR][zip::zipFolder]")
        print("\t folders folder not exist!")
        print("\t folders_folder_path:", folders_folder_path)
        return False

    os.makedirs(zip_folder_path, exist_ok=True)

    folder_name_list = os.listdir(folders_folder_path)
    folder_name_list.sort()

    for folder_name in folder_name_list:
        folder_path = folders_folder_path + folder_name
        if not os.path.isdir(folder_path):
            continue

        zip_file_path = zip_folder_path + folder_name + '.zip'
        if os.path.exists(zip_file_path):
            continue

        tmp_zip_file_path = zip_folder_path + folder_name + '_tmp.zip'

        print("[INFO][zip::zipFolder]")
        print('\t start zip folder:', folder_name, '...')
        command = 'zip -r ' + tmp_zip_file_path + ' ' + folder_path
        valid_command = command.replace('\\', '\\\\')

        status = os.system(valid_command)

        if status != 0:
            print("[ERROR][zip::zipFolder]")
            print("\t zip folder failed!")
            print("\t command:", valid_command)
            return False

        renameFile(tmp_zip_file_path, zip_file_path)

    return True

def unzipFolder(zip_files_folder_path: str, unzip_folder_path: str) -> bool:
    if not os.path.exists(zip_files_folder_path):
        print("[ERROR][zip::unzipFolder]")
        print("\t zip files folder not exist!")
        print("\t zip_files_folder_path:", zip_files_folder_path)
        return False

    zip_filename_list = os.listdir(zip_files_folder_path)
    zip_filename_list.sort()

    for zip_filename in zip_filename_list:
        if zip_filename[:4] != "000-" or zip_filename[-4:] != ".zip":
            continue

        zip_file_path = zip_files_folder_path + zip_filename

        print('[INFO][zip::unzipFolder]')
        print('\t start unzip file:', zip_filename, '...')
        command = 'unzip -u ' + zip_file_path + ' -d ' + unzip_folder_path
        valid_command = command.replace('\\', '\\\\')

        status = os.system(valid_command)

        if status != 0:
            print("[ERROR][zip::unzipFolder]")
            print("\t unzip folder failed!")
            print("\t command:", valid_command)
            return False

    return True
