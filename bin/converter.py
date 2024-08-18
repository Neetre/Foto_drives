import os
from PIL import Image
from moviepy.editor import VideoFileClip
from pathlib import Path
import shutil
from pillow_heif import register_heif_opener


def convert_image(input_file, suffix=".png"):
    if suffix[0] != ".":
        suffix = "." + suffix
    if input_file.lower().endswith(".heic"):
        register_heif_opener()

    output_file = str(Path(input_file).with_suffix(suffix))
    image = Image.open(input_file)
    image.save(output_file)
    print(f"Converted {input_file} to {output_file}")
    return output_file


def convert_video(input_file, suffix=".mp4", progress_bar=None):
    output_file = str(Path(input_file).with_suffix(suffix))
    video = VideoFileClip(input_file)
    video.write_videofile(output_file, progress_bar=progress_bar)
    print(f"Converted {input_file} to {output_file}")
    
    
def convert(input_folder, output_folder):
    heic_files = [photo for photo in os.listdir(input_folder) if photo.lower().endswith('.heic')]
    for photo in heic_files:
        heic_path = os.path.join(input_folder, photo)
        
        # Check if the file is not an .mp4
        if not photo.lower().endswith('.mp4'):
            temp_img = Image.open(heic_path)
            
            jpg_path = os.path.join(output_folder, photo.lower().replace('.heic', '.jpg'))
            temp_img.save(jpg_path, format="JPEG")
            
            print(f"Converted: {photo} -> {os.path.basename(jpg_path)}")
            
            # Delete the starting .heic photo
            os.remove(heic_path)
            print(f"Deleted: {photo}")
        else:
            mp4_path = os.path.join(output_folder, photo.lower())
            shutil.copy(heic_path, mp4_path)
            print(f"Copied: {photo} -> {os.path.basename(mp4_path)}")
