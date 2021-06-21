import os
from PIL import Image
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection


split = "test"
start_label = 2100
output_size = 352
max_count = 100

dataset_path = os.path.abspath("../data/kitti")
img_path = os.path.join(dataset_path, "orig", "images")
label_path = os.path.join(dataset_path, "orig", "labels")
labels_list = os.listdir(label_path)
target_path = dataset_path
if not os.path.exists(os.path.join(target_path, "images", split)):
    os.makedirs(os.path.join(target_path, "images", split))
    os.makedirs(os.path.join(target_path, "labels", split))

car_count = 0
pedestrian_count = 0


def plot(img, boxes):
    fig, ax = plt.subplots(1)
    plt.imshow(img[:, :, ::-1])
    rects = [
        Rectangle(
            (box[0], box[1]),
            box[2] - box[0],
            box[3] - box[1],
            linewidth=1,
            edgecolor="r",
            facecolor="none",
        )
        for box in boxes
    ]
    for rect in rects:
        ax.add_patch(rect)

    plt.show()


def crop(img, boxes, classes):
    boxes = np.asarray(boxes)
    classes = np.asarray(classes)
    center = (boxes[:, 2:] + boxes[:, :2]) / 2.0

    h_orig, w_orig, _ = img.shape
    h = output_size
    w = output_size
    y = (h_orig - h) / 2
    x = (w_orig - w) / 2
    h, w, x, y = int(h), int(w), int(x), int(y)

    center = center - np.asarray([[x, y]] * center.shape[0])  # [n, 2]
    mask_x = (center[:, 0] >= 0) & (center[:, 0] < w)  # [n,]
    mask_y = (center[:, 1] >= 0) & (center[:, 1] < h)  # [n,]
    mask = np.expand_dims(
        (mask_x & mask_y), -1
    )  # [n, 1], mask for the boxes within the image after crop.

    boxes_out = np.reshape(boxes[np.tile(mask, 4)], (-1, 4))  # [m, 4]
    if len(boxes_out) == 0:
        return np.asarray([]), np.asarray([]), np.asarray([])
    shift = [[x, y, x, y]] * boxes_out.shape[0]  # [m, 4]

    boxes_out = boxes_out - shift
    boxes_out[:, 0] = np.clip(boxes_out[:, 0], 0, w)
    boxes_out[:, 2] = np.clip(boxes_out[:, 2], 0, w)
    boxes_out[:, 1] = np.clip(boxes_out[:, 1], 0, h)
    boxes_out[:, 3] = np.clip(boxes_out[:, 3], 0, h)

    classes_out = classes[np.squeeze(mask, -1)]

    img_out = img[y : y + h, x : x + w, :]

    return img_out, boxes_out, classes_out


for label_idx, label_file in enumerate(labels_list):
    print(label_idx)
    if label_idx < start_label:
        continue

    with open(os.path.join(label_path, label_file)) as f:
        new_labels = ""
        for line_idx, line in enumerate(f):
            splitted = line.strip().split()

            obj_class = splitted[0]
            x1 = int(float(splitted[4]))
            y1 = int(float(splitted[5]))
            x2 = int(float(splitted[6]))
            y2 = int(float(splitted[7]))
            x = int((x2 - x1) / 2 + x1)
            y = int((y2 - y1) / 2 + y1)
            width = int(x2 - x1)
            height = int(y2 - y1)

            if obj_class == "Car":
                new_class = 0  # Car
                new_labels = (
                    new_labels
                    + str(new_class)
                    + " "
                    + str(x)
                    + " "
                    + str(y)
                    + " "
                    + str(width)
                    + " "
                    + str(height)
                    + "\n"
                )
            if obj_class == "Pedestrian":
                new_class = 1  # Pedestrian
                new_labels = (
                    new_labels
                    + str(new_class)
                    + " "
                    + str(x)
                    + " "
                    + str(y)
                    + " "
                    + str(width)
                    + " "
                    + str(height)
                    + "\n"
                )

    fname = label_file[:-3] + "png"
    img_source_path = os.path.join(img_path, fname)
    img = cv2.imread(img_source_path)

    num_boxes = new_labels.count("\n")
    boxes, classes = [], []
    for line in new_labels.split("\n")[:-1]:
        splitted = line.strip().split()
        c = int(splitted[0])
        x = int(splitted[1])
        y = int(splitted[2])
        width = int(splitted[3])
        height = int(splitted[4])

        x1 = int(x - width / 2)
        x2 = int(x + width / 2)
        y1 = int(y - height / 2)
        y2 = int(y + height / 2)
        boxes.append([x1, y1, x2, y2])
        classes.append(c)

    img, boxes, classes = crop(img, boxes, classes)
    if not img.shape[0]:
        continue
    # plot(img, boxes)

    boxes_list = list()
    for box in boxes:
        x = int((box[2] - box[0]) / 2 + box[0]) / output_size
        y = int((box[3] - box[1]) / 2 + box[1]) / output_size
        width = int(box[2] - box[0]) / output_size
        height = int(box[3] - box[1]) / output_size
        boxes_list.append(list([x, y, width, height]))

    labels_write = ""
    for b, box in enumerate(boxes_list):
        labels_write = (
            labels_write
            + str(int(classes[b]))
            + " "
            + str(box[0])
            + " "
            + str(box[1])
            + " "
            + str(box[2])
            + " "
            + str(box[3])
            + "\n"
        )
        if int(classes[b]) == 0:
            car_count += 1
        if int(classes[b]) == 1:
            pedestrian_count += 1

    if car_count > max_count and pedestrian_count > max_count:
        break
    if car_count > max_count and any(classes) == 0:
        continue
    if pedestrian_count > max_count and any(classes) == 1:
        continue

    img_target_path = os.path.join(target_path, "images", split, fname)
    cv2.imwrite(img_target_path, img)

    with open(os.path.join(target_path, "labels", split, label_file), "a") as f:
        f.write(labels_write)
