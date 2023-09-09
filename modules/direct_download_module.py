from extract.downloader import download_all_files, prepare_download

def download_direct_links(direct_links, destination_folder, gcs_bucket=None):
    full_path, downloaded_files = prepare_download(destination_folder, "Direct_Downloads")
    return download_all_files(direct_links, full_path, downloaded_files, gcs_bucket)
