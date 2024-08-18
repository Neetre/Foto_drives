import os
from dotenv import load_dotenv
load_dotenv()
from PIL import Image
from os import walk
from icecream import ic
from PIL.ExifTags import TAGS
import shutil
import subprocess


def get_files():
    files = []
    if os.path.exists(os.environ.get("FOLDER_PATH")):
        for (dirpath, dirnames, filenames) in walk(os.environ.get("FOLDER_PATH")):
            for file in filenames:
                if dirpath == os.environ.get("FOLDER_PATH"):
                    if file.endswith('.jpg') or file.endswith('.jpeg') or file.endswith('.JPG') or file.endswith('.JPEG'):
                        files.append(os.path.join(dirpath, file))
                    elif file.endswith('.HEIC') or file.endswith('.heic'):
                        files.append(os.path.join(dirpath, file))
                    elif file.endswith('.mp4'):
                        files.append(os.path.join(dirpath, file))
                    elif file.endswith('.mov') or file.endswith('.MOV'):
                        files.append(os.path.join(dirpath, file))
    return files


def get_date_img(file):
    image = Image.open(file)
    exif_data = image._getexif()
    
    if exif_data is not None:
        for tag_id, value in exif_data.items():
            tag = TAGS.get(tag_id, tag_id)
            if tag == 'DateTimeOriginal':
                return value
    return None


def get_heic_date(file):
    try:
        result = subprocess.run(['exiftool', '-DateTimeOriginal', file], capture_output=True, text=True, check=True)
    except Exception as e:
        print(f"Error while getting date: {e}")
        return None
    return result.stdout.split(": ")[1].strip()


def get_video_metadata(video_path):
    try:
        # Run ffmpeg command to get metadata in JSON format
        result = subprocess.run(['ffmpeg', '-i', video_path, '-f', 'ffmetadata', '-'],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)

    except subprocess.CalledProcessError as e:
        print(f"Error extracting metadata: {e}")
        return None
    
    for line in result.stderr.split('\n'):
        if "creation_time" in line:
            date = line.split(': ')[1].strip().replace('T', ' ').replace('-', ':').split('.')[0]
            print(date)
            return date


def sort_files(data):
    data = dict(sorted(data.items(), key=lambda item: item[1]))
    return data


def move_files(data):
    for file, date in data.items():
        day = date[0]
        shutil.move(file, os.path.join(os.environ.get("FOLDER_PATH"), day, os.path.basename(file)))


def main():
    data = {}
    files = get_files()
    for file in files:
        if file.endswith('.HEIC') or file.endswith('.heic'):
            # continue
            # file = convert_image(file, ".jpg")
            date = get_heic_date(file)
        elif file.endswith('.mp4') or file.endswith('.mov') or file.endswith('.MOV'):
            date = get_video_metadata(file)
        else:
            date = get_date_img(file)
        print(f"{file} - {date}")
        if date is not None:
            date_parts = date.split(" ")[0].split(":")
            date_parts.reverse()
            data[file] = date_parts
    data = sort_files(data)
    days = sorted(list(set([date[0] for date in data.values()])))

    for day in days:
        os.makedirs(os.path.join(os.environ.get("FOLDER_PATH"), day), exist_ok=True)
    move_files(data)


if __name__ == "__main__":
    main()
