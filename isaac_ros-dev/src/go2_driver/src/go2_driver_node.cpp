#include <cmath>
#include <iostream>
#include <memory>
#include <string>
#include <vector>

#include "rclcpp/rclcpp.hpp"
#include "geometry_msgs/msg/twist.hpp"
#include "unitree_api/msg/request.hpp"
#include "unitree_go/msg/sport_mode_state.hpp"
#include "common/ros2_sport_client.h"

using std::placeholders::_1;

class Go2DriverNode : public rclcpp::Node
{
public:
    Go2DriverNode() : Node("go2_driver")
    {
        // Publisher for sending commands to the robot
        command_publisher_ = this->create_publisher<unitree_api::msg::Request>("/api/sport/request", 10);
        
        // Subscriber for receiving velocity commands
        velocity_subscriber_ = this->create_subscription<geometry_msgs::msg::Twist>(
            "cmd_vel", 10, std::bind(&Go2DriverNode::velocity_callback, this, _1));

        // Sport client used for sending movement commands
        sport_client_ = std::make_shared<SportClient>();
    }

private:
    void velocity_callback(const geometry_msgs::msg::Twist::SharedPtr msg)
    {
        // Extract linear and angular velocities
        float vx = msg->linear.x;
        float vy = msg->linear.y;
        float vyaw = msg->angular.z;

        // Log received command
        RCLCPP_INFO(this->get_logger(), "Received velocity command: vx = %.2f, vy = %.2f, vyaw = %.2f", vx, vy, vyaw);

        // Prepare the request message
        unitree_api::msg::Request request_msg;
        sport_client_->Move(request_msg, vx, vy, vyaw);

        // Publish the request
        command_publisher_->publish(request_msg);
        RCLCPP_INFO(this->get_logger(), "Published movement command to Go2");
    }

    rclcpp::Publisher<unitree_api::msg::Request>::SharedPtr command_publisher_;
    rclcpp::Subscription<geometry_msgs::msg::Twist>::SharedPtr velocity_subscriber_;
    std::shared_ptr<SportClient> sport_client_;
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<Go2DriverNode>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}
