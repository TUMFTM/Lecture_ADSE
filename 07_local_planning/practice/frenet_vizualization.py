import numpy as np
from matplotlib import pyplot as plt
from matplotlib import patches as mpatches
from matplotlib.lines import Line2D
from reference_path import ReferencePath


def visualize(
    trajectories_over_time: dict, reference_path: ReferencePath, params: dict
):
    """Visualization of trajectory planning

    :param trajectories_over_time: dictionary containing all possible trajectories of every time step
    :type: dict
    :param reference_path: reference path
    :type: ReferencePath
    :param params: dictionary containing all parameters
    :type: dict"""

    # global trajectory (trajectory, that is ultimately driven by the car)
    global_trajectory = []

    # create new figure and set its size
    fig, ax = plt.subplots()
    fig.set_size_inches(10, 6.5)

    # create colorbar
    colorbar = fig.colorbar(
        mappable=plt.cm.ScalarMappable(cmap=plt.cm.RdYlGn_r),
        label="cost of valid trajectories",
        extend="both",
    )
    colorbar.minorticks_on()

    # iterate through steps
    for step_counter in trajectories_over_time.keys():

        # extract valid trajectories of the current step
        valid_trajectories = trajectories_over_time[step_counter]["valid"]

        # extract invalid trajectories of the current step
        invalid_trajectories = trajectories_over_time[step_counter]["invalid"]

        # cost of cheapest valid trajectory
        cost_min = valid_trajectories[0].cost

        # cost of most expensive valid trajectory
        cost_max = valid_trajectories[-1].cost

        # set tick labels of color bar
        colorbar.set_ticks(ticks=np.linspace(start=0, stop=1, num=6))
        colorbar.set_ticklabels(
            ticklabels=np.linspace(
                start=np.floor(cost_min), stop=np.ceil(cost_max), num=6
            ).astype(int)
        )

        # clear axis
        ax.cla()

        # plot reference path
        ax.plot(
            reference_path.xy_rp[:, 0],
            reference_path.xy_rp[:, 1],
            "b--",
            label="reference path",
        )

        # iterate through invalid trajectories
        for invalid_trajectory in invalid_trajectories:

            # plot invalid trajectories
            ax.plot(
                invalid_trajectory.xy[:, 0], invalid_trajectory.xy[:, 1], color="gray"
            )

        # iterate through valid trajectories
        for valid_trajectory in valid_trajectories:

            # check whether there is only one valid trajectory
            if len(valid_trajectories) == 1:

                # assign color value
                color_value = 1

            else:

                # calculate color value
                color_value = (valid_trajectory.cost - cost_min) / (cost_max - cost_min)

            # plot valid trajectories
            ax.plot(
                valid_trajectory.xy[:, 0],
                valid_trajectory.xy[:, 1],
                color=plt.cm.RdYlGn_r(color_value),
            )

        # plot global trajectory
        global_trajectory.append(
            [valid_trajectories[0].xy[0, 0], valid_trajectories[0].xy[0, 1]]
        )
        ax.plot(
            np.array(global_trajectory)[:, 0],
            np.array(global_trajectory)[:, 1],
            "k--",
            label="driven trajectory",
        )

        # plot optimal trajectory
        ax.plot(
            valid_trajectories[0].xy[:, 0],
            valid_trajectories[0].xy[:, 1],
            "k",
            label="optimal trajectory",
        )

        # plot car at current position
        xy_rectangle = (
            valid_trajectories[0].xy[0, 0]
            - params["discretization"]["car_length"]
            / 2
            * np.cos(valid_trajectories[0].theta[0])
            + params["discretization"]["car_width"]
            / 2
            * np.sin(valid_trajectories[0].theta[0]),
            valid_trajectories[0].xy[0, 1]
            - params["discretization"]["car_length"]
            / 2
            * np.sin(valid_trajectories[0].theta[0])
            - params["discretization"]["car_width"]
            / 2
            * np.cos(valid_trajectories[0].theta[0]),
        )
        rectangle = plt.Rectangle(
            xy=xy_rectangle,
            width=params["discretization"]["car_length"],
            height=params["discretization"]["car_width"],
            angle=np.rad2deg(valid_trajectories[0].theta[0]),
            edgecolor="b",
            fill=True,
        )
        ax.add_patch(p=rectangle)

        # plot circle at current position
        circle = plt.Circle(
            xy=(valid_trajectories[0].xy[0, 0], valid_trajectories[0].xy[0, 1]),
            radius=np.sqrt(
                (params["discretization"]["car_length"] / 2) ** 2
                + (params["discretization"]["car_width"] / 2) ** 2
            ),
            edgecolor="b",
            fill=False,
            linestyle="--",
        )
        ax.add_patch(p=circle)

        # plot obstacles
        ax.plot(
            params["xy_obstacles"][:, 0],
            params["xy_obstacles"][:, 1],
            "rx",
            label="obstacles",
        )

        # add legend to plot
        handles, labels = ax.get_legend_handles_labels()
        invalid_trajectories_handle = Line2D(
            xdata=[0], ydata=[0], color="gray", label="invalid trajectories"
        )
        handles.insert(-1, invalid_trajectories_handle)
        rectangle_handle = mpatches.Patch(edgecolor="b", fill=True, label="car")
        handles.insert(-1, rectangle_handle)
        circle_handle = mpatches.Patch(
            edgecolor="b", fill=False, linestyle="--", label="over-approximation of car"
        )
        handles.insert(-1, circle_handle)
        ax.legend(handles=handles, ncol=2)

        # plot settings
        ax.axis("equal")
        ax.set_xlim(
            left=valid_trajectories[0].xy[0, 0] - params["limits"]["v_max"],
            right=valid_trajectories[0].xy[0, 0]
            + params["discretization"]["t_max"] * params["limits"]["v_max"],
        )
        ax.set_title(
            label=r"$t = %3.2f\/s\/\/\/,\/\/\/v = %2.2f\/\frac{m}{s}\/\/\/$"
            % (
                step_counter * params["discretization"]["fixed_calc_time"],
                valid_trajectories[0].v[0],
            )
        )
        ax.set_xlabel(xlabel=r"$x$ in $m$")
        ax.set_ylabel(ylabel=r"$y$ in $m$")
        ax.grid(b=True)

        plt.pause(interval=params["discretization"]["fixed_calc_time"] * 0.5)

    plt.show()
