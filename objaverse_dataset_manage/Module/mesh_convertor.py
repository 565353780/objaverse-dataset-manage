import os
import json
import trimesh
import numpy as np
from tqdm import tqdm
from multiprocessing import Pool

from objaverse_dataset_manage.Method.path import createFileFolder


class MeshConvertor(object):
    def __init__(self,
                 dataset_root_folder_path: str,
                 force_start: bool = False) -> None:
        self.dataset_root_folder_path = dataset_root_folder_path
        self.force_start = force_start

        self.glb_folder_path = self.dataset_root_folder_path + 'Objaverse/glbs/'
        self.mesh_folder_path = self.dataset_root_folder_path + 'Objaverse/mesh/'
        self.tag_folder_path = self.dataset_root_folder_path + "Tag/ObjaverseMesh/"
        return

    def convertOneShape(self, model_id: str) -> bool:
        glb_file_path = self.glb_folder_path + model_id + '.glb'
        if not os.path.exists(glb_file_path):
            print("[ERROR][MeshConvertor::convertOneShape]")
            print("\t glb file not exist!")
            print("\t glb_file_path:", glb_file_path)
            return False

        finish_tag_file_path = self.tag_folder_path + model_id + "/finish.txt"

        if os.path.exists(finish_tag_file_path):
            return True

        start_tag_file_path = self.tag_folder_path + model_id + "/start.txt"

        if os.path.exists(start_tag_file_path):
            if not self.force_start:
                return True

        createFileFolder(start_tag_file_path)

        with open(start_tag_file_path, "w") as f:
            f.write("\n")

        save_mesh_file_path = self.mesh_folder_path + model_id + '.ply'

        createFileFolder(save_mesh_file_path)

        mesh = trimesh.load(glb_file_path)

        if isinstance(mesh, trimesh.Scene):
            sub_mesh_list = [geometry for geometry in mesh.geometry.values() if isinstance(geometry, trimesh.Trimesh)]
            if len(sub_mesh_list) == 0:
                print('[ERROR][MeshConvertor::convertOneShape]')
                print('\t the glb file contains no mesh!')
                print('\t glb_file_path:', glb_file_path)
                return False

            mesh = trimesh.util.concatenate(sub_mesh_list)

        min_bound = np.min(mesh.vertices, axis=0)
        max_bound = np.max(mesh.vertices, axis=0)
        length = np.max(max_bound - min_bound)
        scale = 0.9 / length
        center = (min_bound + max_bound) / 2.0

        mesh.vertices = (mesh.vertices - center) * scale

        mesh.export(save_mesh_file_path)

        with open(finish_tag_file_path, "w") as f:
            f.write("\n")

        return True

    def convertAllShapes(self, worker_num: int = 6) -> bool:
        if self.force_start:
            worker_num = 1

        metadata_json_file_path = self.dataset_root_folder_path + 'Objaverse/metadata.json'
        if not os.path.exists(metadata_json_file_path):
            print('[ERROR][MeshConvertor::convertAllShapes]')
            print('\t metadata json file not exist!')
            print('\t metadata_json_file_path:', metadata_json_file_path)

            return False

        with open(metadata_json_file_path, 'r') as f:
            data = json.load(f)

        keys = list(data.keys())

        model_id_list = []

        for key in tqdm(keys):
            glb_file_path = data[key]['file_path']
            model_id = os.path.relpath(glb_file_path, self.glb_folder_path)[:-4]
            model_id_list.append(model_id)

        model_id_list.sort()

        start_idx = 40000

        model_id_list = model_id_list[start_idx:]

        print("[INFO][MeshConvertor::convertAllShapes]")
        print('\t start convert all shapes...')
        with Pool(worker_num) as pool:
            results = list(tqdm(
                pool.imap(self.convertOneShape, model_id_list),
                total=len(model_id_list),
                desc="Processing"
            ))

        return True
