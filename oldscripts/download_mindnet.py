import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor

def download_file(url, destination_folder, downloaded_files):
    file_name = url.split('/')[-1]
    local_file_path = os.path.join(destination_folder, file_name)
    
    if os.path.exists(local_file_path):
        print(f"File {file_name} already exists. Skipping.")
        return

    if url in downloaded_files:
        print(f"File {file_name} is being downloaded by another thread. Skipping.")
        return

    downloaded_files.add(url)

    try:
        print(f"Downloading {url}...")
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        with open(local_file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                
        print(f"Downloaded {file_name}")
        
    except requests.RequestException as e:
        print(f"Failed to download {url}. Error: {e}")

def create_folder_if_not_exists(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

def main():
    base_folder = "EEG_Datasets"
    create_folder_if_not_exists(base_folder)

    urls = [
        "http://mindbigdata.com/opendb/index.html",
        "http://mindbigdata.com/opendb/imagenet.html",
        "http://mindbigdata.com/opendb/visualmnist.html"
    ]

    downloaded_files = set()

    for url in urls:
        page_folder = url.split('/')[-1]
        destination_folder = os.path.join(base_folder, page_folder)
        create_folder_if_not_exists(destination_folder)

        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
        except requests.RequestException as e:
            print(f"Failed to fetch {url}. Error: {e}")
            continue

        download_links = [urljoin(url, link.get('href')) for link in soup.find_all('a') if link.get('href', '').endswith('.zip')]

        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(download_file, link, destination_folder, downloaded_files) for link in download_links]
            
            for future in futures:
                future.result()

    print("Completed downloading all files.")

if __name__ == '__main__':
    main()
