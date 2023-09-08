import os
import requests
from concurrent.futures import ThreadPoolExecutor


def prepare_download(destination_folder, specific_folder):
    full_path = os.path.join(destination_folder, specific_folder)
    downloaded_files = set()
    create_folder_if_not_exists(full_path)
    return full_path, downloaded_files



def download_file(file_url, destination_folder, downloaded_files):
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

    except requests.RequestException as e:
        print(f"[ERROR] Failed to download {file_url}. Error: {e}")



def download_all_files(download_links, destination_folder, downloaded_files):
    with ThreadPoolExecutor() as executor:
        try:
            futures = [executor.submit(download_file, link, destination_folder, downloaded_files) for link in download_links]
            for future in futures:
                future.result()
        except KeyboardInterrupt:
            print("[ERROR] Operation was manually interrupted.")
            return False
    return True

def create_folder_if_not_exists(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)


#bnci_scraper.py
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

def fetch_bnci_links(base_url):
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
    except requests.RequestException as e:
        print(f"[ERROR] Failed to fetch {base_url}. Error: {e}")
        return []

    return [urljoin(base_url, link.get('href')) for link in soup.find_all('a') if link.get('href', '').endswith('.mat')]



def handle_pagination(base_url, page_param, download_all_files_func, full_path, downloaded_files, link_selector):
    page_number = 1
    while True:
        page_url = f"{base_url}/{page_param}/{page_number}"
        print(f"Scraping page: {page_url}")

        try:
            response = requests.get(page_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
        except requests.RequestException as e:
            print(f"[ERROR] Failed to fetch {page_url}. Error: {e}")
            return False

        download_links = [link['href'] for link in soup.select(link_selector)]

        if not download_all_files_func(download_links, full_path, downloaded_files):
            return False

        next_page_link = soup.select_one('ul.yiiPager li.next a')
        if next_page_link:
            page_number += 1
        else:
            print("Completed downloading all files.")
            break
    return True