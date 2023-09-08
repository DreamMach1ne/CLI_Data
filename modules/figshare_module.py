import json
from extract.downloader import prepare_download, handle_pagination
from extract.downloader import download_all_files
import requests

def fetch_figshare_articles(api_url, page):
    collection_url = f"{api_url}?page={page}"
    try:
        response = requests.get(collection_url)
        response.raise_for_status()
        return json.loads(response.text)
    except requests.RequestException as e:
        print(f"[ERROR] Failed to fetch {collection_url}. Error: {e}")
        return None

def fetch_figshare_file_links(article):
    article_id = article['id']
    files_url = f"https://api.figshare.com/v2/articles/{article_id}/files"
    try:
        files_response = requests.get(files_url)
        files_response.raise_for_status()
        files = json.loads(files_response.text)
        if not files:
            print(f"[INFO] No files found for article {article_id}. Skipping.")
            return []
    except requests.RequestException as e:
        print(f"[ERROR] Failed to fetch files for article {article_id}. Error: {e}")
        return []

    return [f"https://api.figshare.com/v2/articles/{article_id}/files/{file['id']}/download" for file in files]

def download_from_figshare(api_url, destination_folder):
    full_path, downloaded_files = prepare_download(destination_folder, "Figshare_Downloads")

    page = 1
    while True:
        articles = fetch_figshare_articles(api_url, page)
        if articles is None or not articles:
            break

        download_links = []
        for article in articles:
            download_links.extend(fetch_figshare_file_links(article))

        if not download_all_files(download_links, full_path, downloaded_files):
            return False

        page += 1

    return True
