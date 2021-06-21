import os
from os import listdir
from os.path import isfile, join

"""
Creates a txt file with paths to all images that contain the selected classes for training
Class 0: Car
Class 1: Pedestrian

Input:
classes: list() with classes that should be contained in the dataset

Output:
Saves a .txt file in the dataset folder (data/kitti) with absolute paths to all images 
"""

# USER INPUT
classes = [1]

for split in ["train", "test"]:
    # PATH DEFINITION
    split_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "data", "kitti", "images", split
    )
    img_paths = [
        os.path.join(split_path, f)
        for f in listdir(split_path)
        if isfile(join(split_path, f))
    ]
    label_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(img_paths[0]))), "labels", split
    )

    # CREATE TXT AND SAVE IMAGE PATHS TO THIS TXT
    with open(
        os.path.join(os.path.dirname(os.path.dirname(split_path)), split + ".txt"), "w"
    ) as f:
        for item in img_paths:
            with open(
                os.path.join(label_path, item[-10:-3] + "txt"), "r+"
            ) as label_file:
                lines = label_file.readlines()
                classes_in_img = [int(line[0]) for line in lines]
                if all([elem in classes for elem in classes_in_img]):
                    f.write("%s\n" % item)
