# kaggle_module.py
import os

def download_kaggle_datasets(kaggle_commands, destination_folder):
    full_path = os.path.join(destination_folder, "Kaggle_Downloads")
    os.makedirs(full_path, exist_ok=True)
    os.chdir(full_path)

    for command in kaggle_commands:
        exit_code = os.system(command)
        if exit_code != 0:
            print(f"[ERROR] Failed to download dataset with command: {command}")
            return False
    return True
