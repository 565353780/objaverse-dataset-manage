import os
from objaverse_dataset_manage.Module.mesh_convertor import MeshConvertor

def demo():
    dataset_root_folder_path = '/home/chli/chLi/Dataset/'
    dataset_name = 'Objaverse_82K'
    force_start = False
    worker_num = 1

    mesh_convertor = MeshConvertor(dataset_root_folder_path, dataset_name, force_start)

    mesh_convertor.convertAllShapes(worker_num)
    return True
