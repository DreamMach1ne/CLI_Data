from extract.downloader import download_all_files, prepare_download, handle_pagination

# Assuming this is in gigadb_module.py or wherever you've defined download_from_gigadb

def download_from_gigadb(base_url, destination_folder, gcs_bucket=None):
    full_path, downloaded_files = prepare_download(destination_folder, "GigaDB_Downloads")
    return handle_pagination(base_url, "Sample_page", download_all_files, full_path, downloaded_files, 'table.table.table-bordered tbody tr td a[href^="https://ftp.cngb.org"]', gcs_bucket)
