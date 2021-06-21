import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
import sys

from matplotlib.patches import Ellipse
import matplotlib.transforms as transforms


def v2(
    prediction,
    hist,
    fut,
    lanes_vis,
    ax,
    class_label=None,
    objID=None,
    show=True,
    save=False,
    rmse=None,
    ax_no=None,
    jupy=False,
):

    ax.cla()

    if ax_no is not None:
        lanes = lanes_vis[:, :, ax_no, :].detach().numpy()
    else:
        lanes = lanes_vis[:, :, 0, :].detach().numpy()

    if len(fut.shape) > 2:
        fut = fut[:, 0, :].detach().numpy()

    if rmse:
        ax.text(0, -30, "$RMSE$: " + str(np.round(rmse, 2)) + "m", fontsize=11)

    hist = hist[:, 0, :].detach().numpy()

    if type(prediction) is not np.ndarray:
        prediction = prediction.detach().numpy()

    fut_pos_list = prediction[:, 0, :2]
    sigma_x = 1 / (prediction[:, 0, 2] + sys.float_info.epsilon)
    sigma_y = 1 / (prediction[:, 0, 3] + sys.float_info.epsilon)
    rho = prediction[:, 0, 4]

    sigma_cov = np.array(
        [
            [sigma_x ** 2, rho * sigma_x * sigma_y],
            [rho * sigma_x * sigma_y, sigma_y ** 2],
        ]
    )

    # Swap axes to shape (50,2,2)
    sigma_cov = sigma_cov.swapaxes(0, 2)
    sigma_cov = sigma_cov.swapaxes(1, 2)

    draw_with_uncertainty([fut_pos_list], [sigma_cov], ax)

    ax.plot(fut_pos_list[:, 0], fut_pos_list[:, 1], "g-")
    if class_label is None:
        class_label = "Unkown"
    if objID is not None:
        class_label += ", objID: {:d}".format(int(objID))
    ax.plot(
        hist[:, 0],
        hist[:, 1],
        "r--",
        label="Input - Past coordinates, Type: {}".format(class_label),
    )
    ax.plot(fut[:, 0], fut[:, 1], "b--", label="Output - Ground Truth")

    for j in range(lanes.shape[0]):
        kmax = 20
        if np.any(lanes[j, :, 0] == 0.0):
            kmax = np.argmin(lanes[j, :, 0] != 0.0)
            if kmax < 2:
                continue
        kmax = np.min([kmax, 20])

        lane_trajectory = lanes[j, :kmax]

        ax.arrow(
            lane_trajectory[-2, 0],
            lane_trajectory[-2, 1],
            (lane_trajectory[-1, 0] - lane_trajectory[-2, 0]),
            (lane_trajectory[-1, 1] - lane_trajectory[-2, 1]),
            head_width=1.5,
            width=0.5,
            ec="red",
        )
        ax.arrow(
            lane_trajectory[0, 0],
            lane_trajectory[0, 1],
            (lane_trajectory[1, 0] - lane_trajectory[0, 0]),
            (lane_trajectory[1, 1] - lane_trajectory[0, 1]),
            head_width=1.5,
            width=0.5,
            ec="black",
        )

        if j == lanes.shape[1] - 1:
            ax.plot(
                lane_trajectory[:, 0],
                lane_trajectory[:, 1],
                "k-",
                label="Input - Lanes",
            )
        else:
            ax.plot(lane_trajectory[:, 0], lane_trajectory[:, 1], "k-")

    ax.axis("equal")
    ax.set_xlabel("x in m", fontsize=16)
    ax.set_ylabel("y in m", fontsize=16)
    ax.legend(loc="upper left")

    if jupy:
        plt.show()
    elif show:
        plt.pause(1e-3)


def visualize_multi(prediction, hist, fut, lanes_vis, axes, ax_no):
    """Allows to visualize multiple predictions in subplots.

    Args:
        prediction ([type]): [description]
        hist ([type]): [description]
        fut ([type]): [description]
        lanes_vis ([type]): [description]
        axes ([type]): [description]
        ax_no ([type]): [description]
    """

    if ax_no < len(axes):
        axes[ax_no].cla()

        visualize(prediction, hist, fut, lanes_vis, axes[ax_no], ax_no=ax_no)


def confidence_ellipse(mu, cov, ax, n_std=3.0, facecolor="red", **kwargs):
    """
    Create a plot of the covariance confidence ellipse of *x* and *y*.

    Parameters
    ----------
    x, y : array-like, shape (n, )
        Input data.

    ax : matplotlib.axes.Axes
        The axes object to draw the ellipse into.

    n_std : float
        The number of standard deviations to determine the ellipse's radiuses.

    **kwargs
        Forwarded to `~matplotlib.patches.Ellipse`

    Returns
    -------
    matplotlib.patches.Ellipse
    """

    mu_x = mu[0]
    mu_y = mu[1]

    pearson = cov[0, 1] / (np.sqrt(cov[0, 0] * cov[1, 1]) + sys.float_info.epsilon)
    # Using a special case to obtain the eigenvalues of this
    # two-dimensionl dataset.
    ell_radius_x = np.sqrt(1 + pearson)
    ell_radius_y = np.sqrt(1 - pearson)
    ellipse = Ellipse(
        (0, 0),
        width=ell_radius_x * 2,
        height=ell_radius_y * 2,
        facecolor=facecolor,
        alpha=0.5,
        **kwargs
    )

    # Calculating the stdandard deviation of x from
    # the squareroot of the variance and multiplying
    # with the given number of standard deviations.
    scale_x = np.sqrt(cov[0, 0]) * n_std

    # calculating the stdandard deviation of y ...
    scale_y = np.sqrt(cov[1, 1]) * n_std

    transf = (
        transforms.Affine2D()
        .rotate_deg(45)
        .scale(scale_x, scale_y)
        .translate(mu_x, mu_y)
    )

    ellipse.set_transform(transf + ax.transData)
    return ax.add_patch(ellipse)


def draw_with_uncertainty(fut_pos_list, fut_cov_list, ax):

    for i, fut_pos in enumerate(fut_pos_list):
        ax.plot(
            fut_pos[:, 0],
            fut_pos[:, 1],
            "*c",
            markersize=2,
            alpha=0.8,
            zorder=15,
            label="Output - Prediction",
        )
        for j, pos in enumerate(fut_pos):
            confidence_ellipse(
                pos, fut_cov_list[i][j], ax, n_std=3.0, facecolor="yellow"
            )
            if fut_cov_list[i][j][0][0] > 10:
                break
        for j, pos in enumerate(fut_pos):
            confidence_ellipse(
                pos, fut_cov_list[i][j], ax, n_std=2.0, facecolor="orange"
            )
            if fut_cov_list[i][j][0][0] > 10:
                break
        for j, pos in enumerate(fut_pos):
            confidence_ellipse(pos, fut_cov_list[i][j], ax, n_std=1.0, facecolor="red")
            if fut_cov_list[i][j][0][0] > 10:
                break


def visualize(
    ax,
    hist,
    fut,
    bound_list,
    class_label=None,
    objID=None,
    allbounds=None,
    neigh_zip=None,
    n_visz=100,
):

    k = 0
    ax.cla()
    xmin = -25
    xmax = 55
    ymin = -20
    ymax = 30
    hist = np.array(hist)
    ax.plot(
        hist[:, 0],
        hist[:, 1],
        "r.",
        label="Past Positions ({}, ID: {})".format(
            "" if class_label is None else class_label, "0" if objID is None else objID
        ),
    )

    if k == n_visz:
        ax.set_xlabel("x in m")
        ax.set_ylabel("y in m")
        ax.legend()
        ax.grid()
        ax.set_xlim((xmin, xmax))
        ax.set_ylim((ymin, ymax))
        print("\n\n\n Plot object past positions ..")
        plt.show()
        return ax
    k += 1

    fut = np.array(fut)
    ax.plot(
        fut[:, 0],
        fut[:, 1],
        "b.",
        label="Future Positions ({}, ID: {})".format(
            "" if class_label is None else class_label, "0" if objID is None else objID
        ),
    )

    if k == n_visz:
        ax.set_xlabel("x in m")
        ax.set_ylabel("y in m")
        ax.legend()
        ax.grid()
        ax.set_xlim((xmin, xmax))
        ax.set_ylim((ymin, ymax))
        print("\n\n\n Adding object future positions ..")
        plt.show()
        return ax
    k += 1

    valid_bounds = sum([np.linalg.norm(b) > 0 for b in bound_list])
    for j, bound in enumerate(bound_list):
        if isinstance(bound, list):
            bound = np.array(bound)
        bound = bound[np.linalg.norm(bound, axis=1) != 0]
        if len(bound) == 0:
            continue
        mean_pos = bound[int(len(bound) * 0.4), :]
        mean_pos[0] = min(mean_pos[0], 35)
        if j == valid_bounds - 1:
            plt.plot(
                bound[:, 0],
                bound[:, 1],
                "k--",
                label="Lane Centers (total: {})".format(j + 1),
            )
        else:
            plt.plot(bound[:, 0], bound[:, 1], "k--")
        plt.text(mean_pos[0] + 1, mean_pos[1] + 1, "{}".format(j))

    if k == n_visz:
        ax.set_xlabel("x in m")
        ax.set_ylabel("y in m")
        ax.legend()
        ax.set_xlim((xmin, xmax))
        ax.set_ylim((ymin, ymax))
        ax.grid()
        print("\n\n\n Adding centerlanes from breath first search ..")
        plt.show()
        return ax
    k += 1

    if allbounds is not None:
        for j, bd in enumerate(allbounds):
            if j == len(allbounds) - 1:
                ax.plot(bd[:, 0], bd[:, 1], color="silver", label="Lane Boundaries")
            else:
                ax.plot(bd[:, 0], bd[:, 1], color="silver")

    if k == n_visz:
        ax.set_xlabel("x in m")
        ax.set_ylabel("y in m")
        ax.legend()
        ax.grid()
        ax.set_xlim((xmin, xmax))
        ax.set_ylim((ymin, ymax))
        print(
            "\n\n\n Adding lane boundaries (only for visualization, no features in data set) .."
        )
        plt.show()
        return ax
    k += 1

    if k == n_visz:
        return

    ax.set_xlabel("x in m")
    ax.set_ylabel("y in m")
    ax.set_xlim((xmin, xmax))
    ax.set_ylim((ymin, ymax))
    ax.legend()
    plt.pause(1e-3)
