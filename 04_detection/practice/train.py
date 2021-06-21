from __future__ import division

import argparse
import datetime
import os
import sys
import time

import torch
import tqdm
from terminaltables import AsciiTable
from torch.autograd import Variable
from torch.utils.data import DataLoader

from evaluate import evaluate
from models import *
from utils.augmentations import *
from utils.datasets import *
from utils.logger import *
from utils.parse_config import *
from utils.utils import *

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--epochs", type=int, default=100, help="number of epochs")
    parser.add_argument(
        "--batch_size", type=int, default=8, help="size of each image batch"
    )
    parser.add_argument(
        "--gradient_accumulations",
        type=int,
        default=2,
        help="number of gradient accums before step",
    )
    parser.add_argument(
        "--model_def",
        type=str,
        default="config/yolov3-kitti-tiny.cfg",
        help="path to model definition file",
    )
    parser.add_argument(
        "--data_config",
        type=str,
        default="config/kitti.data",
        help="path to data config file",
    )
    parser.add_argument(
        "--n_cpu",
        type=int,
        default=8,
        help="number of cpu threads to use during batch generation",
    )
    parser.add_argument(
        "--img_size", type=int, default=352, help="size of each image dimension"
    )
    parser.add_argument(
        "--checkpoint_interval",
        type=int,
        default=1,
        help="interval between saving model weights",
    )
    parser.add_argument(
        "--evaluation_interval",
        type=int,
        default=1,
        help="interval evaluations on validation set",
    )
    parser.add_argument(
        "--compute_map", default=False, help="if True computes mAP every tenth batch"
    )
    parser.add_argument(
        "--multiscale_training", default=True, help="allow for multi-scale training"
    )
    parser.add_argument(
        "--verbose",
        "-v",
        default=False,
        action="store_true",
        help="Makes the training more verbose",
    )
    parser.add_argument(
        "--logdir",
        type=str,
        default="logs",
        help="Defines the directory where the training log files are stored",
    )
    opt = parser.parse_args()
    print(opt)

    logger = Logger(opt.logdir)

    # Check if GPU is available
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Create necessary directories to save checkpoints
    os.makedirs("output", exist_ok=True)
    os.makedirs("checkpoints", exist_ok=True)

    # Get data configuration
    data_config = parse_data_config(opt.data_config)
    train_path = data_config["train"]
    valid_path = data_config["test"]
    class_names = load_classes(data_config["names"])
    num_classes = int(data_config["classes"])

    # Quit training if train.txt and test.txt are not in dataset folder
    try:
        open(train_path)
        open(valid_path)
    except Exception as e:
        print(e)
        print("Run utils/create_split_txt.py first to create train.txt and test.txt!")
        sys.exit()

    # Initiate model
    model = Darknet(opt.model_def).to(device)
    model.apply(weights_init_normal)

    # Get dataloader
    dataset = ListDataset(
        train_path,
        multiscale=opt.multiscale_training,
        img_size=opt.img_size,
        transform=AUGMENTATION_TRANSFORMS,
        num_classes=num_classes,
    )
    dataloader = torch.utils.data.DataLoader(
        dataset,
        batch_size=opt.batch_size,
        shuffle=True,
        num_workers=opt.n_cpu,
        pin_memory=True,
        collate_fn=dataset.collate_fn,
    )

    # Define optimizer
    optimizer = torch.optim.Adam(model.parameters())

    # Define metrics
    metrics = [
        "grid_size",
        "loss",
        "x",
        "y",
        "w",
        "h",
        "conf",
        "cls",
        "cls_acc",
        "recall50",
        "recall75",
        "precision",
        "conf_obj",
        "conf_noobj",
    ]

    # Training loop
    for epoch in tqdm.tqdm(range(opt.epochs), desc="Total Process"):
        model.train()
        start_time = time.time()

        # select smaller batches and train batch-by-batch
        for batch_i, (_, imgs, targets) in enumerate(
            tqdm.tqdm(dataloader, desc=f"Training Epoch {epoch}")
        ):
            batches_done = len(dataloader) * epoch + batch_i

            imgs = Variable(imgs.to(device))
            targets = Variable(targets.to(device), requires_grad=False)

            # Inference and backpropagation
            loss, outputs = model(imgs, targets)
            loss.backward()

            if batches_done % opt.gradient_accumulations == 0:
                # Accumulates gradient before each step
                optimizer.step()
                optimizer.zero_grad()

            # ----------------
            #   Log progress
            # ----------------

            log_str = "\n---- [Epoch %d/%d, Batch %d/%d] ----\n" % (
                epoch,
                opt.epochs,
                batch_i,
                len(dataloader),
            )

            metric_table = [
                ["Metrics", *[f"YOLO Layer {i}" for i in range(len(model.yolo_layers))]]
            ]

            # Log metrics at each YOLO layer
            for i, metric in enumerate(metrics):
                formats = {m: "%.6f" for m in metrics}
                formats["grid_size"] = "%2d"
                formats["cls_acc"] = "%.2f%%"
                row_metrics = [
                    formats[metric] % yolo.metrics.get(metric, 0)
                    for yolo in model.yolo_layers
                ]
                metric_table += [[metric, *row_metrics]]

            log_str += AsciiTable(metric_table).table
            log_str += f"\nTotal loss {to_cpu(loss).item()}"

            # Tensorboard logging
            tensorboard_log = []
            for j, yolo in enumerate(model.yolo_layers):
                for name, metric in yolo.metrics.items():
                    if name != "grid_size":
                        tensorboard_log += [(f"train/{name}_{j + 1}", metric)]
            tensorboard_log += [("train/loss", to_cpu(loss).item())]
            logger.list_of_scalars_summary(tensorboard_log, batches_done)

            # Determine approximate time left for epoch
            epoch_batches_left = len(dataloader) - (batch_i + 1)
            time_left = datetime.timedelta(
                seconds=epoch_batches_left * (time.time() - start_time) / (batch_i + 1)
            )
            log_str += f"\n---- ETA {time_left}"

            if opt.verbose:
                print(log_str)

            model.seen += imgs.size(0)

        # Evaluate model after finishing an epoch
        if epoch % opt.evaluation_interval == 0:
            print("\n---- Evaluating Model ----")
            # Evaluate the model on the validation set
            metrics_output = evaluate(
                model,
                path=valid_path,
                iou_thres=0.5,
                conf_thres=0.5,
                nms_thres=0.5,
                img_size=opt.img_size,
                batch_size=8,
                num_classes=num_classes,
            )

            if metrics_output is not None:
                precision, recall, AP, f1, ap_class = metrics_output
                evaluation_metrics = [
                    ("validation/precision", precision.mean()),
                    ("validation/recall", recall.mean()),
                    ("validation/mAP", AP.mean()),
                    ("validation/f1", f1.mean()),
                ]
                logger.list_of_scalars_summary(evaluation_metrics, epoch)

                # Print class APs and mAP
                ap_table = [["Index", "Class name", "AP"]]
                for i, c in enumerate(ap_class):
                    ap_table += [[c, class_names[c], "%.5f" % AP[i]]]
                print(AsciiTable(ap_table).table)
                print(f"---- mAP {AP.mean()}")
            else:
                print("---- mAP not measured (no detections found by model)")

        # Save current checkpoint (model) to drive
        if epoch % opt.checkpoint_interval == 0:
            torch.save(model.state_dict(), f"checkpoints/yolov3_ckpt_%d.pth" % epoch)
