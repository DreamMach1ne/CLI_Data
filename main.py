import argparse
from modules.mindnet_module import download_from_mindnet
from modules.bnci_module import download_from_bnci
from modules.figshare_module import download_from_figshare
from modules.gigadb_module import download_from_gigadb
from modules.direct_download_module import download_direct_links
from modules.kaggle_module import download_kaggle_datasets
from extract.downloader import create_folder_if_not_exists

def main():
    parser = argparse.ArgumentParser(description='Download datasets.')
    parser.add_argument('--source', choices=['gigadb', 'mindbigdata', 'bnci', 'figshare', 'direct', 'kaggle'], default='all', help='Source to download from')
    parser.add_argument('--gcs_bucket', type=str, help='Google Cloud Storage bucket to upload files to')
    args = parser.parse_args()

    destination_folder = "Downloaded_Datasets"
    create_folder_if_not_exists(destination_folder)

    success = False

    if args.source == 'bnci':
        success = download_from_bnci("http://bnci-horizon-2020.eu/database/data-sets", destination_folder, args.gcs_bucket)
    elif args.source == 'figshare':
        success = download_from_figshare("https://api.figshare.com/v2/collections/3917698/articles", destination_folder, args.gcs_bucket)
    elif args.source == 'mindbigdata':
        success = download_from_mindnet(destination_folder, args.gcs_bucket)
    elif args.source == 'gigadb':
        success = download_from_gigadb("http://gigadb.org/dataset/view/id/100295", destination_folder, args.gcs_bucket)
    elif args.source == 'direct':
        direct_links = [
            # Add your direct links here
        ]
        success = download_direct_links(direct_links, destination_folder, args.gcs_bucket)
    elif args.source == 'kaggle':
        kaggle_commands = [
            'kaggle competitions download -c grasp-and-lift-eeg-detection',
            'kaggle competitions download -c inria-bci-challenge'
        ]
        success = download_kaggle_datasets(kaggle_commands, destination_folder, args.gcs_bucket)

    if success:
        print(f"[SUCCESS] Completed downloading all files from {args.source}.")

if __name__ == '__main__':
    main()
