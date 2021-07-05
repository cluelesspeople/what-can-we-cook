import os
import json

json_file = "../victor-val.json"
images_dir = "../victor/images/val"
labels_dir = "../victor/labels/val"
save_dir = "../khavin"

with open(json_file) as file:
  data_info = json.load(file)

exts = [".jpg", ".jpeg", ".png", ".webp"]

def readAndSave(file_name, class_name, i, img_read_loc=images_dir, txt_read_loc=labels_dir, save_loc=save_dir):
    ext = 0
    while True:
        try:
            with open(f"{img_read_loc}/{file_name}{exts[ext]}",'rb') as image_file:
                image_string = image_file.read()
                with open(f"{save_loc}/images/{class_name}/{class_name}-{i}.jpg",'wb') as dest_image:
                    dest_image.write(image_string)
            with open(f"{txt_read_loc}/{file_name}.txt",'r') as label_file:
                label_string = label_file.read()
                with open(f"{save_loc}/labels/{class_name}/{class_name}-{i}.txt",'w') as dest_label:
                    dest_label.write(label_string)
                    break
        except FileNotFoundError:
            if ext == 3: 
                print("File Not Found!")
                break;
            ext += 1

for class_name, file_names in data_info.items():
    os.makedirs(f"{save_dir}/images/{class_name}", exist_ok=True)
    os.makedirs(f"{save_dir}/labels/{class_name}", exist_ok=True)
    offset = len(os.listdir(f"{save_dir}/images/{class_name}")) + 1
    for i, file_name in enumerate(file_names):
        readAndSave(file_name, class_name, i + offset)


