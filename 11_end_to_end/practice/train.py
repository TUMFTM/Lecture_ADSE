import numpy as np
import torch
import gym.wrappers
from nets.imitator import Policy
from dataset import MarkovProcess
from early_stopping import EarlyStopping
from utils import make_Dirs, save_Result, get_EnvInfo


######################################################
# hyperparameters
######################################################
DATA_NAME = "./expert/summary.csv"

BATCH_SIZE = 128
TRAIN_VALID = 0.95
EARLY_LENGTH = 5
N_EPOCH = 50
METHOD = "PracticeSession_BC"

SAVE_DIR = "./result/" + METHOD + "/"

######################################################
# one epoch for updating policy
######################################################
def epoch_policy(dataset, policy, n_epoch, mode):
    loss_sum = 0.0
    loss_num = 0
    if "train" in mode:
        policy.train()
    else:
        policy.eval()
    for batch_idx, (so, a_) in enumerate(dataset):
        output = policy(so)
        loss = policy.criterion(output, a_).mean()
        if policy.training:
            policy.optimizer.zero_grad()
            loss.backward()
            policy.optimizer.step()
        loss_sum += loss.data.item()
        loss_num += 1
    loss_sum /= loss_num
    print(
        "{}-th epoch {} of policy was end: \n\tloss = {}".format(
            n_epoch, mode, loss_sum
        )
    )
    return loss_sum


######################################################
# prepare environment and agent (imitator)
env = gym.make("CarRacing-v0")
s_dim, a_dim, transform = get_EnvInfo(env)

# prepare save directories
sdir = SAVE_DIR + "/"
make_Dirs(sdir)
# specify the random seeds
torch.manual_seed(0)
np.random.seed(0)
env.seed(0)
# set expert dataset
dataset = MarkovProcess(DATA_NAME, transform=transform)
len_train = int(TRAIN_VALID * len(dataset))
train_loader, valid_loader = torch.utils.data.random_split(
    dataset, [len_train, len(dataset) - len_train]
)
train_loader = torch.utils.data.DataLoader(
    train_loader, batch_size=BATCH_SIZE, shuffle=True
)
valid_loader = torch.utils.data.DataLoader(
    valid_loader, batch_size=BATCH_SIZE, shuffle=True
)
# initialize policy network
policy = Policy(s_dim, a_dim)
stopper = EarlyStopping(length=EARLY_LENGTH)

# prepare buffers to store results
train_loss_policy = []
valid_loss_policy = []

# optimize policy by the expert dataset
print("Start learning policy!")
for n_epoch in range(1, N_EPOCH + 1):
    train_loss_policy.append(epoch_policy(train_loader, policy, n_epoch, "train"))
    valid_loss_policy.append(epoch_policy(valid_loader, policy, n_epoch, "valid"))
    # early stopping
    if stopper(valid_loss_policy[-1]):
        print("Early Stopping to avoid overfitting!")
        break

# save trained model
policy.release(sdir)

# csv and plot
save_Result(
    sdir, "loss_policy", {"train": train_loss_policy, "valid": valid_loss_policy}
)

# close everything
env.close()
