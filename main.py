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
    parser.add_argument('--source', choices=['gigadb', 'mindbigdata', 'bnci', 'figshare', 'direct', 'kaggle', 'all'], default='all', help='Source to download from')
    parser.add_argument('--gcs_bucket', type=str, help='Google Cloud Storage bucket to upload files to')
    args = parser.parse_args()

    destination_folder = "Downloaded_Datasets"
    create_folder_if_not_exists(destination_folder)

    if args.source == 'all':
        sources = ['gigadb', 'mindbigdata', 'bnci', 'figshare', 'direct', 'kaggle']
    else:
        sources = [args.source]

    for source in sources:
        success = False
        if source == 'bnci':
            success = download_from_bnci("http://bnci-horizon-2020.eu/database/data-sets", destination_folder, args.gcs_bucket)
        elif source == 'figshare':
            success = download_from_figshare("https://api.figshare.com/v2/collections/3917698/articles", destination_folder, args.gcs_bucket)
        elif source == 'mindbigdata':
            success = download_from_mindnet(destination_folder, args.gcs_bucket)
        elif source == 'gigadb':
            success = download_from_gigadb("http://gigadb.org/dataset/view/id/100295", destination_folder, args.gcs_bucket)
        elif source == 'direct':
            direct_links = ['https://archive.ics.uci.edu/static/public/457/eeg+steady+state+visual+evoked+potential+signals.zip',
            'https://www-ti.informatik.uni-tuebingen.de/~spueler/eeg_data/cVEP_dataset.rar',
            'https://physionet.org/files/eegmmidb/1.0.0/','https://gin.g-node.org/robintibor/high-gamma-dataset/src/master/data/train/1.edf'
            ,'https://archive.ics.uci.edu/static/public/230/planning+relax.zip',
            'https://figshare.com/collections/A_large_electroencephalographic_motor_imagery_dataset_for_electroencephalographic_brain_computer_interfaces/3917698',
            'http://www.enterface.net/enterface05/docs/results/databases/project1_database.zip',
            'http://www.enterface.net/enterface05/docs/results/databases/project2_database.zip',
            'http://www.enterface.net/enterface05/docs/results/databases/project5_database.zip',
            'http://www.enterface.net/enterface05/docs/results/databases/project7_database.zip',
            'https://headit.ucsd.edu/studies/3316f70e-35ff-11e3-a2a9-0050563f2612.jnlp',
            'https://bcmi.sjtu.edu.cn/~seed/downloads.html#seed-access-anchor',
            'https://bcmi.sjtu.edu.cn/~seed/downloads.html#seed-iv-access-anchor',
            'https://bcmi.sjtu.edu.cn/~seed/downloads.html#seed-vig-access-anchor',
            'https://stacks.stanford.edu/file/druid:xd109qh3109/fhpred.zip',
            "https://utexas.box.com/shared/static/7ab8qm5e3i0vfsku0ee4dc6hzgeg7nyh.zip",
            'https://utexas.box.com/shared/static/3go1g4gcdar2cntjit2knz5jwr3mvxwe.zip',
            "https://openneuro.org/datasets/ds003020/",
            "https://utexas.box.com/shared/static/ae5u0t3sh4f46nvmrd3skniq0kk2t5uh.zip",
            "https://openneuro.org/datasets/ds004510/",
            "https://utexas.box.com/s/ri13t06iwpkyk17h8tfk0dtyva7qtqlz",
            "https://utexas.box.com/s/ri13t06iwpkyk17h8tfk0dtyva7qtqlz"
            ]
            success = download_direct_links(direct_links, destination_folder, args.gcs_bucket)
        elif source == 'kaggle':
            kaggle_commands = [
                    'kaggle competitions download -c grasp-and-lift-eeg-detection',
                    'kaggle competitions download -c inria-bci-challenge'
                ]
            success = download_kaggle_datasets(kaggle_commands, destination_folder, args.gcs_bucket)

        if success:
            print(f"[SUCCESS] Completed downloading all files from {args.source}.")

if __name__ == '__main__':
    main()
