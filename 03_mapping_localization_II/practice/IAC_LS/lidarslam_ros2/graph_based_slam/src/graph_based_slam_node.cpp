#include "graph_based_slam/graph_based_slam_component.h"
#include <rclcpp/rclcpp.hpp>

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::NodeOptions options;
  rclcpp::spin(std::make_shared<graphslam::GraphBasedSlamComponent>(options));
  rclcpp::shutdown();
  return 0;
}
