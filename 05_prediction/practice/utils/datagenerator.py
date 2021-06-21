# Standard imports
import pickle
import os

# Thrid party imports
import torch
import numpy as np

repo_path = os.path.dirname(os.path.dirname(__file__))


# Dataset class for Indy
class OpenDDDataset(torch.utils.data.Dataset):
    def __init__(self, source_path):

        self.type_dict = {"Car": 1.0}

        if os.path.isdir(source_path):
            self.D = {}
            for root, _, files in os.walk(source_path):
                for file in files:
                    ff = os.path.join(root, file)
                    with open(ff, "rb") as fp:
                        temp_data = pickle.load(fp)
                        for key, values in temp_data.items():
                            if key not in self.D.keys():
                                self.D[key] = []
                            self.D[key] += values
            self.D["sampleID"] = list(
                range(len(self.D["sampleID"]))
            )  # concatenate all splitted data into one

        else:  # single file input
            with open(source_path, "rb") as fp:
                self.D = pickle.load(fp)

    def __len__(self):
        return len(self.D["hist"])

    def __getitem__(self, idx):

        # Get track history 'hist' = ndarray, and future track 'fut' = ndarray
        smpl_id = self.D["sampleID"][idx]
        hist = self.D["hist"][idx]
        fut = self.D["fut"][idx]
        lanes = self.D["lanes"][idx]
        classes = self.D["classes"][idx]
        ojbIDs = self.D["objID"][idx]

        return smpl_id, hist, fut, lanes, classes, ojbIDs

    # Collate function for dataloader
    def collate_fn(self, samples):

        len_in = len(samples[0][1])  # takes the length of hist of the first sample
        len_out = len(samples[0][2])  # takes the length of hist of the first sample
        num_lanes, len_lanes, _ = samples[0][3].shape

        # Initialize history, history lengths, future, output mask, lateral maneuver and longitudinal maneuver batches:
        hist_batch = torch.zeros(len_in, len(samples), 2)
        fut_batch = torch.zeros(len_out, len(samples), 2)
        lanes_batch = torch.zeros(num_lanes, len_lanes, len(samples), 2)
        class_batch = torch.zeros(1, len(samples), 1)
        objID_batch = torch.zeros(1, len(samples), 1)

        smpl_ids = []
        for dataID, (smpl_id, hist, fut, lanes, classes, objIDs) in enumerate(samples):

            # Set up history, future, lateral maneuver and longitudinalhsit maneuver batches:
            hist_batch[0 : len(hist), dataID, 0] = torch.from_numpy(hist[:, 0])
            hist_batch[0 : len(hist), dataID, 1] = torch.from_numpy(hist[:, 1])
            fut_batch[0 : len(fut), dataID, 0] = torch.from_numpy(fut[:, 0])
            fut_batch[0 : len(fut), dataID, 1] = torch.from_numpy(fut[:, 1])
            class_batch[0, dataID, 0] = self.type_dict.get(classes, 0.0)
            objID_batch[0, dataID, 0] = int(objIDs)
            for n in range(num_lanes):
                lanes_batch[n, 0:len_lanes, dataID, 0] = torch.from_numpy(
                    lanes[n, :, 0]
                )
                lanes_batch[n, 0:len_lanes, dataID, 1] = torch.from_numpy(
                    lanes[n, :, 1]
                )

            smpl_ids.append(smpl_id)

        return smpl_ids, hist_batch, fut_batch, lanes_batch, class_batch, objID_batch

    # Collate function for dataloader
    def collate(self, samples):

        len_in = len(samples[0][1])  # takes the length of hist of the first sample

        # Initialize history, history lengths, future, output mask, lateral maneuver and longitudinal maneuver batches:
        hist_batch = np.zeros([len_in, len(samples), 2])

        for dataID, (_, hist, _, _, _, _) in enumerate(samples):

            hist_batch[0 : len(hist), dataID, 1] = hist[:, 1]
            hist_batch[0 : len(hist), dataID, 0] = hist[:, 0]

        return hist_batch


# Collate function for dataloader
def collate_fn(samples):

    type_dict = {"Car": 1.0}

    len_in = len(samples[0][1])  # takes the length of hist of the first sample
    len_out = len(samples[0][2])  # takes the length of hist of the first sample
    num_lanes, len_lanes, _ = samples[0][3].shape

    # Initialize history, history lengths, future, output mask, lateral maneuver and longitudinal maneuver batches:
    hist_batch = torch.zeros(len_in, len(samples), 2)
    fut_batch = torch.zeros(len_out, len(samples), 2)
    lanes_batch = torch.zeros(num_lanes, len_lanes, len(samples), 2)
    class_batch = torch.zeros(1, len(samples), 1)
    objID_batch = torch.zeros(1, len(samples), 1)

    smpl_ids = []
    for dataID, (smpl_id, hist, fut, lanes, classes, objIDs) in enumerate(samples):

        # Set up history, future, lateral maneuver and longitudinalhsit maneuver batches:
        hist_batch[0 : len(hist), dataID, 0] = torch.from_numpy(hist[:, 0])
        hist_batch[0 : len(hist), dataID, 1] = torch.from_numpy(hist[:, 1])
        fut_batch[0 : len(fut), dataID, 0] = torch.from_numpy(fut[:, 0])
        fut_batch[0 : len(fut), dataID, 1] = torch.from_numpy(fut[:, 1])
        class_batch[0, dataID, 0] = type_dict.get(classes, 0.0)
        objID_batch[0, dataID, 0] = int(objIDs)
        for n in range(num_lanes):
            lanes_batch[n, 0:len_lanes, dataID, 0] = torch.from_numpy(lanes[n, :, 0])
            lanes_batch[n, 0:len_lanes, dataID, 1] = torch.from_numpy(lanes[n, :, 1])

        smpl_ids.append(smpl_id)

    return smpl_ids, hist_batch, fut_batch, lanes_batch, class_batch, objID_batch
