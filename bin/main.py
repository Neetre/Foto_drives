from download_photo import setup, download
from order import img_sort
import logging


def main():
    try:
        file_list, local_path, duplicate_folder = setup()
        download(local_path, duplicate_folder, file_list)
    except Exception as e:
        logging.error(f"An error occurred while downloading: {str(e)}")

    try:
        img_sort()
    except Exception as e:
        logging.error(f"An error occurred while sorting the images: {str(e)}")


if __name__ == "__main__":
    main()