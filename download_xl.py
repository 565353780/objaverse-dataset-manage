import objaverse.xl as oxl

dataset_root_folder_path = '/home/chli/Dataset/Objaverse_XL/'

print('start get_annotations')
annotations = oxl.get_annotations(download_dir=dataset_root_folder_path)

print(annotations)
