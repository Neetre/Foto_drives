import os
import shutil
import logging
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from dotenv import load_dotenv
load_dotenv()
import logging
from typing import List, Tuple
logging.basicConfig(level=logging.INFO)
from register import get_register


def setup() -> Tuple[List, str, str]:
    """
    Set up the Google Drive connection and prepare local directories.
    
    Returns:
        Tuple containing file list, local path, and duplicate folder path.
    """
    FOLDER_ID = os.environ.get('FOLDER_ID')
    FOLDER_PATH = os.environ.get('FOLDER_PATH')
    DUPLICATE_FOLDER = os.environ.get('DUPLICATE_FOLDER')

    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)

    file_list = drive.ListFile({'q': f"'{FOLDER_ID}' in parents and trashed=false"}).GetList()  # gets a list of files in the specified folder
    local_path = FOLDER_PATH if os.path.exists(FOLDER_PATH) else os.mkdir(FOLDER_PATH)
    duplicate_folder = DUPLICATE_FOLDER if os.path.exists(DUPLICATE_FOLDER) else os.mkdir(DUPLICATE_FOLDER)
    return file_list, local_path, duplicate_folder


def download(local_path: str, duplicate_folder: str, file_list: List):
    """
    Download files from Google Drive to local directory.
    
    Args:
        local_path: Path to store downloaded files.
        duplicate_folder: Path to store duplicate files.
        file_list: List of files to download.
    """
    already_downloaded = get_register()
    for file in file_list:
        try:
            if file['mimeType'] != 'application/vnd.google-apps.folder':  # check if it is not a folder
                if file['title'] in already_downloaded:
                    logging.info(f"Already downloaded: {file['title']}")
                    continue
                file_path = os.path.join(local_path, file['title'])
                if os.path.exists(file_path):
                    #duplicate_folder = duplicate_dir if os.path.exists(duplicate_dir) else os.mkdir(DUPLICATE_FOLDER) # TODO non mi piacciono i duplicati, magari fa solo un check se la foto è già presente nella cartella
                    duplicate_path = os.path.join(duplicate_folder, file['title'])
                    shutil.move(file_path, duplicate_path)
                    logging.info(f"Downloaded: {file['title']}")
                else:
                    file.GetContentFile(file_path)  # download the files
                    print(f"Downloaded: {file['title']}")
        except Exception as e:
            logging.error(f"Error processing {file['title']}: {str(e)}")
    
    logging.info('Download Complete')


if __name__ == "__main__":
    try:
        file_list, local_path, duplicate_folder = setup()
        download(local_path, duplicate_folder, file_list)
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
