#include <chrono>
#include <cmath>
#include <functional>
#include <memory>
#include <stdexcept>
#include <string>

#include "geometry_msgs/msg/twist.hpp"
#include "go2_interfaces/msg/robot_mode_state.hpp"
#include "rclcpp/rclcpp.hpp"
#include <unitree/robot/channel/channel_factory.hpp>
#include <unitree/robot/go2/obstacles_avoid/obstacles_avoid_client.hpp>
#include <unitree/robot/go2/sport/sport_client.hpp>

#include "network_interface_utils.hpp"

namespace
{
enum class MotionBackend
{
    kSportFreeAvoid,
    kObstaclesAvoid,
};

MotionBackend parse_backend(const std::string &backend_name)
{
    if (
        backend_name == "sport" ||
        backend_name == "sport_free_avoid" ||
        backend_name == "unitree_sport"
    ) {
        return MotionBackend::kSportFreeAvoid;
    }
    if (
        backend_name == "obstacles" ||
        backend_name == "obstacles_avoid" ||
        backend_name == "unitree_obstacles_avoid"
    ) {
        return MotionBackend::kObstaclesAvoid;
    }

    throw std::runtime_error(
        "Unsupported backend \"" + backend_name +
        "\". Expected sport_free_avoid or obstacles_avoid.");
}

bool is_follow_motion_state(const go2_interfaces::msg::RobotModeState &state_msg)
{
    return (
        state_msg.task_mode == "FOLLOW" &&
        state_msg.posture_mode == "STANDING" &&
        state_msg.motion_enabled);
}

}  // namespace

class PersonFollowMotionBridgeNode : public rclcpp::Node
{
public:
    PersonFollowMotionBridgeNode()
    : Node("person_follow_motion_bridge_node"),
      backend_name_(this->declare_parameter<std::string>("backend", "sport_free_avoid")),
      backend_(parse_backend(backend_name_)),
      cmd_vel_topic_(this->declare_parameter<std::string>("cmd_vel_topic", "/person_follow/cmd_vel")),
      robot_mode_state_topic_(
          this->declare_parameter<std::string>(
              "robot_mode_state_topic",
              "/robot_mode_state")),
      network_interface_(this->declare_parameter<std::string>("network_interface", "")),
      command_timeout_s_(std::max(
          0.05,
          this->declare_parameter<double>("command_timeout_s", 0.5)))
    {
        initialize_unitree_sdk();

        cmd_vel_subscriber_ = this->create_subscription<geometry_msgs::msg::Twist>(
            cmd_vel_topic_,
            10,
            std::bind(&PersonFollowMotionBridgeNode::cmd_vel_callback, this, std::placeholders::_1));
        robot_mode_state_subscriber_ = this->create_subscription<go2_interfaces::msg::RobotModeState>(
            robot_mode_state_topic_,
            10,
            std::bind(&PersonFollowMotionBridgeNode::robot_mode_state_callback, this, std::placeholders::_1));
        watchdog_timer_ = this->create_wall_timer(
            std::chrono::milliseconds(100),
            std::bind(&PersonFollowMotionBridgeNode::watchdog_callback, this));

        RCLCPP_INFO(
            this->get_logger(),
            "Person follow motion bridge ready. backend=%s cmd_vel_topic=%s robot_mode_state_topic=%s requested_network_interface=%s resolved_network_interface=%s",
            backend_name_.c_str(),
            cmd_vel_topic_.c_str(),
            robot_mode_state_topic_.c_str(),
            network_interface_.empty() ? "<auto>" : network_interface_.c_str(),
            resolved_network_interface_.empty() ? "<auto>" : resolved_network_interface_.c_str());
    }

    ~PersonFollowMotionBridgeNode() override
    {
        if (sdk_initialized_) {
            send_motion_command(0.0F, 0.0F, 0.0F, false);
            disable_backend(false);
            unitree::robot::ChannelFactory::Instance()->Release();
        }
    }

private:
    void initialize_unitree_sdk()
    {
        RCLCPP_INFO(
            this->get_logger(),
            "Initializing Unitree SDK backend=%s network_interface=%s",
            backend_name_.c_str(),
            network_interface_.empty() ? "<auto>" : network_interface_.c_str());

        const auto network_interface = go2_driver::network_interface::resolve(network_interface_);
        resolved_network_interface_ = network_interface.selected;
        if (network_interface.changed) {
            const std::string available_suffix = network_interface.available_interfaces.empty()
                ? ""
                : " (available: " + network_interface.available_interfaces + ")";
            RCLCPP_WARN(
                this->get_logger(),
                "Requested Unitree network interface \"%s\" is not available%s. %s: %s.",
                network_interface.requested.c_str(),
                available_suffix.c_str(),
                network_interface.reason.c_str(),
                resolved_network_interface_.empty() ? "<auto>" : resolved_network_interface_.c_str());
        }

        if (resolved_network_interface_.empty()) {
            unitree::robot::ChannelFactory::Instance()->Init(0);
        } else {
            unitree::robot::ChannelFactory::Instance()->Init(0, resolved_network_interface_);
        }

        RCLCPP_INFO(
            this->get_logger(),
            "Unitree ChannelFactory initialized with network_interface=%s.",
            resolved_network_interface_.empty() ? "<auto>" : resolved_network_interface_.c_str());

        switch (backend_) {
        case MotionBackend::kSportFreeAvoid:
            sport_client_ = std::make_unique<unitree::robot::go2::SportClient>();
            sport_client_->SetTimeout(10.0F);
            sport_client_->Init();
            break;
        case MotionBackend::kObstaclesAvoid:
            obstacles_avoid_client_ =
                std::make_unique<unitree::robot::go2::ObstaclesAvoidClient>();
            obstacles_avoid_client_->SetTimeout(10.0F);
            obstacles_avoid_client_->Init();
            break;
        }

        sdk_initialized_ = true;
        RCLCPP_INFO(
            this->get_logger(),
            "Unitree SDK client initialized for backend %s.",
            backend_name_.c_str());
    }

    void robot_mode_state_callback(const go2_interfaces::msg::RobotModeState::SharedPtr msg)
    {
        const bool should_be_active = is_follow_motion_state(*msg);
        if (should_be_active == follow_motion_active_) {
            return;
        }

        follow_motion_active_ = should_be_active;
        if (follow_motion_active_) {
            stale_stop_sent_ = false;
            enable_backend();
            send_motion_command(0.0F, 0.0F, 0.0F, true);
            RCLCPP_INFO(
                this->get_logger(),
                "Follow motion became active. Enabled Unitree backend %s.",
                backend_name_.c_str());
            return;
        }

        send_motion_command(0.0F, 0.0F, 0.0F, true);
        disable_backend(true);
        RCLCPP_INFO(
            this->get_logger(),
            "Follow motion became idle. Disabled Unitree backend %s.",
            backend_name_.c_str());
    }

    void cmd_vel_callback(const geometry_msgs::msg::Twist::SharedPtr msg)
    {
        last_command_ = *msg;
        has_last_command_ = true;
        last_command_time_ = std::chrono::steady_clock::now();
        stale_stop_sent_ = false;

        if (!follow_motion_active_) {
            return;
        }

        if (!backend_enabled_ && !enable_backend()) {
            return;
        }

        send_motion_command(
            static_cast<float>(msg->linear.x),
            static_cast<float>(msg->linear.y),
            static_cast<float>(msg->angular.z),
            true);
    }

    void watchdog_callback()
    {
        if (!follow_motion_active_ || !backend_enabled_ || !has_last_command_) {
            return;
        }

        const double age_s = std::chrono::duration<double>(
            std::chrono::steady_clock::now() - last_command_time_).count();
        if (age_s <= command_timeout_s_ || stale_stop_sent_) {
            return;
        }

        send_motion_command(0.0F, 0.0F, 0.0F, true);
        stale_stop_sent_ = true;
        RCLCPP_WARN(
            this->get_logger(),
            "No follow motion command received for %.2fs. Sent a stop command to backend %s.",
            age_s,
            backend_name_.c_str());
    }

    bool enable_backend()
    {
        if (!sdk_initialized_) {
            return false;
        }
        if (backend_enabled_) {
            return true;
        }

        bool success = false;
        switch (backend_) {
        case MotionBackend::kSportFreeAvoid:
            success = (sport_client_ != nullptr && sport_client_->FreeAvoid(true) == 0);
            break;
        case MotionBackend::kObstaclesAvoid:
            success = (
                obstacles_avoid_client_ != nullptr &&
                obstacles_avoid_client_->UseRemoteCommandFromApi(true) == 0 &&
                obstacles_avoid_client_->SwitchSet(true) == 0);
            break;
        }

        if (!success) {
            RCLCPP_ERROR(
                this->get_logger(),
                "Failed to enable Unitree backend %s.",
                backend_name_.c_str());
            return false;
        }

        backend_enabled_ = true;
        return true;
    }

    void disable_backend(bool log_failures)
    {
        if (!backend_enabled_ || !sdk_initialized_) {
            return;
        }

        bool success = false;
        std::string failure_detail;
        switch (backend_) {
        case MotionBackend::kSportFreeAvoid:
            if (sport_client_ == nullptr) {
                failure_detail = "sport client unavailable";
                break;
            }
            {
                const int32_t stop_move_result = sport_client_->StopMove();
                const int32_t free_avoid_result = sport_client_->FreeAvoid(false);
                success = (free_avoid_result == 0);
                if (!success) {
                    failure_detail =
                        "StopMove=" + std::to_string(stop_move_result) +
                        " FreeAvoid(false)=" + std::to_string(free_avoid_result);
                } else if (stop_move_result != 0 && log_failures) {
                    RCLCPP_WARN(
                        this->get_logger(),
                        "StopMove() returned %d while disabling backend %s, but FreeAvoid(false) succeeded.",
                        stop_move_result,
                        backend_name_.c_str());
                }
            }
            break;
        case MotionBackend::kObstaclesAvoid:
            if (obstacles_avoid_client_ == nullptr) {
                failure_detail = "obstacles avoid client unavailable";
                break;
            }
            {
                const int32_t move_result =
                    obstacles_avoid_client_->Move(0.0F, 0.0F, 0.0F);
                const int32_t switch_result = obstacles_avoid_client_->SwitchSet(false);
                const int32_t remote_result =
                    obstacles_avoid_client_->UseRemoteCommandFromApi(false);
                success = (switch_result == 0 && remote_result == 0);
                if (!success) {
                    failure_detail =
                        "Move(0,0,0)=" + std::to_string(move_result) +
                        " SwitchSet(false)=" + std::to_string(switch_result) +
                        " UseRemoteCommandFromApi(false)=" + std::to_string(remote_result);
                }
            }
            break;
        }

        if (!success) {
            if (log_failures) {
                RCLCPP_ERROR(
                    this->get_logger(),
                    "Failed to disable Unitree backend %s cleanly. %s",
                    backend_name_.c_str(),
                    failure_detail.empty() ? "" : failure_detail.c_str());
            }
            return;
        }

        backend_enabled_ = false;
    }

    void send_motion_command(float vx, float vy, float wz, bool log_failures)
    {
        if (!sdk_initialized_ || !backend_enabled_) {
            return;
        }

        const int32_t result = [this, vx, vy, wz]() {
            switch (backend_) {
            case MotionBackend::kSportFreeAvoid:
                if (sport_client_ == nullptr) {
                    return -1;
                }
                return sport_client_->Move(vx, vy, wz);
            case MotionBackend::kObstaclesAvoid:
                if (obstacles_avoid_client_ == nullptr) {
                    return -1;
                }
                return obstacles_avoid_client_->Move(vx, vy, wz);
            }
            return -1;
        }();

        if (result != 0 && log_failures) {
            RCLCPP_ERROR(
                this->get_logger(),
                "Failed to send motion command to backend %s (vx=%.3f vy=%.3f wz=%.3f, result=%d).",
                backend_name_.c_str(),
                vx,
                vy,
                wz,
                result);
        }

        if (result == 0 && vx == 0.0F && vy == 0.0F && wz == 0.0F) {
            last_command_ = geometry_msgs::msg::Twist();
            has_last_command_ = true;
            last_command_time_ = std::chrono::steady_clock::now();
            stale_stop_sent_ = true;
        }
    }

    std::string backend_name_;
    MotionBackend backend_;
    std::string cmd_vel_topic_;
    std::string robot_mode_state_topic_;
    std::string network_interface_;
    std::string resolved_network_interface_;
    double command_timeout_s_;

    bool sdk_initialized_ = false;
    bool follow_motion_active_ = false;
    bool backend_enabled_ = false;
    bool has_last_command_ = false;
    bool stale_stop_sent_ = false;
    geometry_msgs::msg::Twist last_command_;
    std::chrono::steady_clock::time_point last_command_time_{std::chrono::steady_clock::now()};

    std::unique_ptr<unitree::robot::go2::SportClient> sport_client_;
    std::unique_ptr<unitree::robot::go2::ObstaclesAvoidClient> obstacles_avoid_client_;

    rclcpp::Subscription<geometry_msgs::msg::Twist>::SharedPtr cmd_vel_subscriber_;
    rclcpp::Subscription<go2_interfaces::msg::RobotModeState>::SharedPtr robot_mode_state_subscriber_;
    rclcpp::TimerBase::SharedPtr watchdog_timer_;
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<PersonFollowMotionBridgeNode>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}
