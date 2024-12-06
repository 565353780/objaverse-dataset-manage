from objaverse_dataset_manage.Module.mesh_convertor import MeshConvertor

def demo():
    dataset_root_folder_path = '/home/chli/chLi/Dataset/'
    force_start = False

    mesh_convertor = MeshConvertor(dataset_root_folder_path, force_start)

    mesh_convertor.convertAllShapes()
    return True
