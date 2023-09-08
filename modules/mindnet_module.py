from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
from extract.downloader import  download_all_files,prepare_download

def download_from_mindnet(destination_folder):
    full_path, downloaded_files = prepare_download(destination_folder, "MindNet_Downloads")


    urls = [
        "http://mindbigdata.com/opendb/index.html",
        "http://mindbigdata.com/opendb/imagenet.html",
        "http://mindbigdata.com/opendb/visualmnist.html"
    ]

    for url in urls:
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
        except requests.RequestException as e:
            print(f"[ERROR] Failed to fetch {url}. Error: {e}")
            continue

        download_links = [urljoin(url, link.get('href')) for link in soup.find_all('a') if link.get('href', '').endswith('.zip')]

        if not download_all_files(download_links, full_path, downloaded_files):
            return False

    return True
