import os
from objaverse_dataset_manage.Module.mesh_convertor import MeshConvertor

def demo():
    root_list = [
        '/mnt/data/jintian/chLi/Dataset/',
        os.environ['HOME'] + '/chLi/Dataset/',
    ]
    dataset_root_folder_path = None
    for root in root_list:
        if os.path.exists(root):
            dataset_root_folder_path = root
            break
    if dataset_root_folder_path is None:
        print('[ERROR][mesh_convertor::demo]')
        print('\t dataset not found!')
        return False

    dataset_name = 'Objaverse_82K'
    force_start = False
    worker_num = 1

    mesh_convertor = MeshConvertor(dataset_root_folder_path, dataset_name, force_start)

    mesh_convertor.convertAllShapes(worker_num)
    return True
