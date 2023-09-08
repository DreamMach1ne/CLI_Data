import os
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

def download_file(file_url, destination_folder, downloaded_files):
    file_name = file_url.split('/')[-1]
    local_file_path = os.path.join(destination_folder, file_name)
    
    if os.path.exists(local_file_path):
        print(f"File {file_name} already exists. Skipping.")
        return
    
    if file_url in downloaded_files:
        print(f"File {file_name} already downloaded in this session. Skipping.")
        return

    try:
        print(f"Downloading {file_url}...")
        response = requests.get(file_url, stream=True)
        response.raise_for_status()
        
        with open(local_file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                
        print(f"Downloaded {file_name}")
        downloaded_files.add(file_url)
        
    except requests.RequestException as e:
        print(f"Failed to download {file_url}. Error: {e}")

def extract_folder_name_from_url(url):
    return url.split('/')[-1]

def download_files_from_page(soup, destination_folder, downloaded_files):
    download_links = soup.select('table.table.table-bordered tbody tr td a[href^="https://ftp.cngb.org"]')
    
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(download_file, link['href'], destination_folder, downloaded_files) for link in download_links]
        
        for future in futures:
            future.result()

def fetch_page_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')
    except requests.RequestException as e:
        print(f"Failed to fetch {url}. Error: {e}")
        return None

def main():
    base_url = 'http://gigadb.org/dataset/view/id/100295'
    destination_folder = extract_folder_name_from_url(base_url)
    downloaded_files = set()
    
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    page_number = 1
    while True:
        page_url = f"{base_url}/Sample_page/{page_number}"
        print(f"Scraping page: {page_url}")
        
        soup = fetch_page_content(page_url)
        if soup is None:
            break
        
        download_files_from_page(soup, destination_folder, downloaded_files)
        
        next_page_link = soup.select_one('ul.yiiPager li.next a')
        if next_page_link:
            page_number += 1
        else:
            print("Completed downloading all files.")
            break

if __name__ == '__main__':
    main()

