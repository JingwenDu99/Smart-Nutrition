import os
import json
import shutil
from datetime import datetime


image_dir = "p01/food-images"                     
output_root = "processed/p01/food-images"         
json_path = "image_time.json"         

# Load image_time.json
with open(json_path, "r") as f:
    image_info = json.load(f)

# Iterative every record in json
for item in image_info:
    filename = item["filename"]                   # e.g.: IMG_8916.jpeg
    datetime_str = item["datetime"]               # e.g.: 2020:02:01 10:03:41

    # e.g.:20200201 
    date = datetime.strptime(datetime_str, "%Y:%m:%d %H:%M:%S").strftime("%Y%m%d")

    # source path
    src_path = os.path.join(image_dir, filename)

    # Create destination path data/processed/p01/20200201/
    dst_dir = os.path.join(output_root, date)
    os.makedirs(dst_dir, exist_ok=True)

    # Copy image to destination path
    dst_path = os.path.join(dst_dir, filename)
    if os.path.exists(src_path):
        shutil.copy2(src_path, dst_path)
