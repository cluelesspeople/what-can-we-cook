import os
import json

os.chdir("../victor/labels/train")
files = os.listdir()

record = {}
for file in files:
    if file.__contains__(".txt"):
        if file == "classes.txt": continue

        file_object = open(file, "r")
        content = file_object.read()
        for bbox in content.strip().split("\n"):
            [class_id, *bbox_info] = bbox.split(" ")
            if class_id in record:
                record[class_id].add(file.replace(".txt", ""))
            else:
                record[class_id] = set({file.replace(".txt", "")})

def convert_set_to_list(obj): 
    # obj = {1: set(), 2: set(),}
    new_obj = {}
    for key, value in obj.items():
        new_obj[key] = list(value)
    return new_obj

os.chdir("../../..")
with open('victor-train.json', 'w') as file:
    json.dump(convert_set_to_list(record), file)