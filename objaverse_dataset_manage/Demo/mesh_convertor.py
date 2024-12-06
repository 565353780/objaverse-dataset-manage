import os
from objaverse_dataset_manage.Module.mesh_convertor import MeshConvertor

def demo():
    dataset_root_folder_path = '/home/chli/chLi/Dataset/'
    force_start = False
    worker_num = os.cpu_count()

    mesh_convertor = MeshConvertor(dataset_root_folder_path, force_start)

    mesh_convertor.convertAllShapes(worker_num)
    return True
