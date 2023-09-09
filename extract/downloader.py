# extract/downloader.py
import os
import requests
from concurrent.futures import ThreadPoolExecutor
from gcp import upload_to_gcs  # Import the GCS module

def prepare_download(destination_folder, specific_folder):
    """Prepares the download directory and returns the full path and a set of already downloaded files.

    Args:
        destination_folder (str): The root folder where files will be downloaded.
        specific_folder (str): The specific folder within the destination folder.

    Returns:
        tuple: Full path to the specific folder and a set of already downloaded files.
    """
    full_path = os.path.join(destination_folder, specific_folder)
    downloaded_files = set()
    create_folder_if_not_exists(full_path)
    return full_path, downloaded_files

def create_folder_if_not_exists(folder_name):
    """Creates a folder if it doesn't exist.

    Args:
        folder_name (str): The name of the folder to create.
    """
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

def download_and_upload_file(file_url, destination_folder, downloaded_files, gcs_bucket=None):
    """Downloads a file and optionally uploads it to a GCS bucket.

    Args:
        file_url (str): The URL of the file to download.
        destination_folder (str): The folder to download the file to.
        downloaded_files (set): A set of already downloaded files.
        gcs_bucket (str, optional): The GCS bucket to upload the file to.

    Returns:
        bool: True if download is successful, False otherwise.
    """
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
