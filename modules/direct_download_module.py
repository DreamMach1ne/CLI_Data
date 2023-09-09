# direct_downloads_module.py

from urllib.parse import urlparse
from extract.downloader import download_all_files, prepare_download

def download_direct_links(direct_links, destination_folder, gcs_bucket=None):
    """Downloads files from direct links and optionally uploads them to a GCS bucket.

    Args:
        direct_links (list): List of direct URLs.
        destination_folder (str): The folder to download the files to.
        gcs_bucket (str, optional): The GCS bucket to upload the files to.

    Returns:
        bool: True if all downloads are successful, False otherwise.
    """
    for link in direct_links:
        domain = urlparse(link).netloc.replace('.', '_')
        full_path, downloaded_files = prepare_download(destination_folder, domain)
        success = download_all_files([link], full_path, downloaded_files, gcs_bucket)
        if not success:
            return False
    return True
