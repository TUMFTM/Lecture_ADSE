import os

import launch
import launch_ros.actions

from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    main_param_dir = launch.substitutions.LaunchConfiguration(
        'main_param_dir',
        default=os.path.join(
            get_package_share_directory('lidarslam'),
            'param',
            'lidarslam_tukuba.yaml'))

    mapping = launch_ros.actions.Node(
        package='scanmatcher',
        node_executable='scanmatcher_node',
        parameters=[main_param_dir],
        remappings=[('/input_cloud','/points_raw')],
        output='screen'
        )

    graphbasedslam = launch_ros.actions.Node(
        package='graph_based_slam',
        node_executable='graph_based_slam_node',
        parameters=[main_param_dir],
        output='screen'
        )


    return launch.LaunchDescription([
        launch.actions.DeclareLaunchArgument(
            'main_param_dir',
            default_value=main_param_dir,
            description='Full path to main parameter file to load'),
        mapping,
        graphbasedslam,
            ])
