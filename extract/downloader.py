# extract/downloader.py
import os
import requests
from concurrent.futures import ThreadPoolExecutor
from gcs_module import upload_to_gcs  # Import the GCS module

def prepare_download(destination_folder, specific_folder):
    full_path = os.path.join(destination_folder, specific_folder)
    downloaded_files = set()
    create_folder_if_not_exists(full_path)
    return full_path, downloaded_files

def create_folder_if_not_exists(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

def download_and_upload_file(file_url, destination_folder, downloaded_files, gcs_bucket=None):
    if not file_url.startswith('http'):
        print(f"[ERROR] Invalid URL {file_url}. Skipping.")
        return

    file_name = file_url.split('/')[-1]
    local_file_path = os.path.join(destination_folder, file_name)

    if os.path.exists(local_file_path):
        print(f"[INFO] File {file_name} already exists. Skipping.")
        return

    if file_url in downloaded_files:
        print(f"[INFO] File {file_name} already downloaded in this session. Skipping.")
        return

    try:
        print(f"[INFO] Downloading {file_url}...")
        response = requests.get(file_url, stream=True)
        if response.status_code == 404:
            print(f"[ERROR] File not found: {file_url}")
            return
        response.raise_for_status()

        with open(local_file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"[SUCCESS] Downloaded {file_name}")
        downloaded_files.add(file_url)

        # Upload to GCS if bucket name is provided
        if gcs_bucket:
            upload_success = upload_to_gcs(gcs_bucket, local_file_path, file_name)
            if upload_success:
                print(f"[SUCCESS] Uploaded {file_name} to GCS bucket {gcs_bucket}")

    except requests.RequestException as e:
        print(f"[ERROR] Failed to download {file_url}. Error: {e}")

def download_all_files(download_links, destination_folder, downloaded_files, gcs_bucket=None):
    with ThreadPoolExecutor() as executor:
        try:
            futures = [executor.submit(download_and_upload_file, link, destination_folder, downloaded_files, gcs_bucket) for link in download_links]
            for future in futures:
                future.result()
        except KeyboardInterrupt:
            print("[ERROR] Operation was manually interrupted.")
            return False
    return True
