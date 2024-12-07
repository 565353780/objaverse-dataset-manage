from objaverse_dataset_manage.Demo.downloader import demo_download, demo_remove_invalid_glb
from objaverse_dataset_manage.Demo.mesh_convertor import demo as demo_convert_mesh

if __name__ == "__main__":
    demo_download()
    demo_remove_invalid_glb()
    demo_convert_mesh()
