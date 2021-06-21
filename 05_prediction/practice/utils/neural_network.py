import torch


def MSE(y_pred, y_gt):
    """MSE Loss for single outputs.

    Arguments:
        y_pred {[type]} -- [description]
        y_gt {[type]} -- [description]

    Returns:
        [type] -- [description]
    """

    # If GT has not enough timesteps, shrink y_pred
    if y_gt.shape[0] < y_pred.shape[0]:
        y_pred = y_pred[: y_gt.shape[0], :, :]

    muX = y_pred[:, :, 0]
    muY = y_pred[:, :, 1]
    x = y_gt[:, :, 0]
    y = y_gt[:, :, 1]
    mse_det = torch.pow(x - muX, 2) + torch.pow(y - muY, 2)
    count = torch.sum(torch.ones(mse_det.shape))
    mse = torch.sum(mse_det) / count
    return mse, mse_det
