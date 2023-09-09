# modules/bnci_module.py
from extract.downloader import download_all_files, prepare_download, fetch_bnci_links

def download_from_bnci(base_url, destination_folder, gcs_bucket=None):
    full_path, downloaded_files = prepare_download(destination_folder, "BNCI_Horizon_MAT_Datasets")
    download_links = fetch_bnci_links(base_url)
    if not download_links:
        print("[ERROR] No download links found.")
        return False

    return download_all_files(download_links, full_path, downloaded_files, gcs_bucket)
