from time import sleep

from objaverse_dataset_manage.Demo.mesh_convertor import demo as demo_convert_mesh

if __name__ == "__main__":
    while True:
        demo_convert_mesh()
        sleep(10)
