import os
import requests
from tqdm import tqdm  
from concurrent.futures import ThreadPoolExecutor 


def download_model(model_url, save_path):
    try:
        response = requests.get(model_url)
        if response.status_code == 200:
            with open(save_path, 'wb') as f:
                f.write(response.content)
                #print(f"Downloaded: {save_path}")
        else:
            print(f"Failed to download: {model_url}")
    except Exception as e:
        print(f"Error downloading: {model_url}, {e}")

def download_filtered_models(model_sizes, base_url, save_dir, minKb, maxKb,num_threads = os.cpu_count()):
    filtered_models = {model_path: size for model_path, size in model_sizes.items() if minKb < size < maxKb * 1024}
    print('[INFO][download::download_filtered_models]')
    print('\t filtered_models num =', len(filtered_models.keys()))

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = []

        for model_path in filtered_models.keys():
            folder_name = os.path.dirname(model_path)
            sub_folder = os.path.join(save_dir, folder_name)

            file_name = os.path.basename(model_path)
            save_path = os.path.join(sub_folder, file_name)

            if not os.path.exists(save_path):
                os.makedirs(sub_folder, exist_ok=True)
                model_url = f"{base_url}/{model_path}?download=true"
                futures.append(executor.submit(download_model, model_url, save_path))

        for future in tqdm(futures, total=len(futures)):
            future.result()

def download_file(url, folder_path, filename):
    save_file_path = os.path.join(folder_path, filename)

    if os.path.exists(save_file_path):
        return True

    url = url + "?download=true"
    print(url)

    response = requests.get(url, stream=True)

    if response.status_code != 200:
        print(f"Failed to download {filename}")

        return False

    with open(save_file_path, 'wb') as f:
        f.write(response.content) 

    return True
 
def download_metadata(base_url, save_dir,  num_threads=6):
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = []
        for i in range(1, 161):
            filename = f"000-{i:03d}.json.gz"
            file_url = base_url + filename
            futures.append(executor.submit(download_file, file_url, save_dir, filename))

        for future in tqdm(futures, total=len(futures)):
            future.result() 
