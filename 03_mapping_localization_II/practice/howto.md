## Practice ADSE: Localization & Mapping II

# Show data: 

cd ~/Repos/ADSE/03-MapLoc2/ros1_ws

source /opt/ros/melodic/setup.zsh
source devel/setup.zsh

roscore (extra terminal)
rviz (extra terminal)

rosbag play /media/florian/SwapSpace/kitti/rosbag/kitti_scene07_complete.bag


# Cartographer:

roslaunch cartographer_kitti_config demo_kitti_3d.launch bag_filename:=/media/florian/SwapSpace/kitti/rosbag/kitti_scene07.bag


# openVSLAM:

cd ~/Repos/ADSE/03-MapLoc2/IAC_LS/vSLAM/openvslam/build

./run_kitti_slam -v ../orb_vocab/orb_vocab.dbow2 -d /media/florian/SwapSpace/kitti/data_odometry_gray/dataset/sequences/07 -c ../example/kitti/KITTI_mono_04-12.yaml

