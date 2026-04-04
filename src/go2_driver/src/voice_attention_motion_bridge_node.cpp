#include <chrono>
#include <cctype>
#include <cstdint>
#include <cmath>
#include <functional>
#include <memory>
#include <stdexcept>
#include <string>

#include "geometry_msgs/msg/twist.hpp"
#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/bool.hpp"
#include <unitree/robot/channel/channel_factory.hpp>
#include <unitree/robot/go2/obstacles_avoid/obstacles_avoid_client.hpp>
#include <unitree/robot/go2/sport/sport_client.hpp>

namespace
{

enum class MotionBackend
{
    kSportFreeAvoid,
    kObstaclesAvoid,
};

std::string normalize_token(std::string value)
{
    for (char &ch : value) {
        if (ch == '-' || ch == ' ') {
            ch = '_';
            continue;
        }
        ch = static_cast<char>(std::tolower(static_cast<unsigned char>(ch)));
    }
    return value;
}

MotionBackend parse_backend(const std::string &backend_name)
{
    const std::string normalized = normalize_token(backend_name);
    if (
        normalized.empty() ||
        normalized == "legacy" ||
        normalized == "sport" ||
        normalized == "sport_free_avoid" ||
        normalized == "unitree_sport")
    {
        return MotionBackend::kSportFreeAvoid;
    }
    if (
        normalized == "obstacles" ||
        normalized == "obstacles_avoid" ||
        normalized == "unitree_obstacles_avoid")
    {
        return MotionBackend::kObstaclesAvoid;
    }

    throw std::runtime_error(
        "Unsupported backend \"" + backend_name +
        "\". Expected legacy, sport_free_avoid, or obstacles_avoid.");
}

std::string canonical_gait(const std::string &gait)
{
    const std::string normalized = normalize_token(gait);
    if (
        normalized.empty() ||
        normalized == "none" ||
        normalized == "off" ||
        normalized == "skip")
    {
        return "none";
    }
    if (normalized == "static" || normalized == "static_walk") {
        return "static_walk";
    }
    if (
        normalized == "economic" ||
        normalized == "economic_gait" ||
        normalized == "endurance")
    {
        return "economic_gait";
    }
    if (normalized == "classic" || normalized == "classic_walk") {
        return "classic_walk";
    }
    if (normalized == "free" || normalized == "free_walk") {
        return "free_walk";
    }
    if (normalized == "upright" || normalized == "walk_upright") {
        return "walk_upright";
    }
    if (normalized == "trot" || normalized == "trot_run") {
        return "trot_run";
    }
    return normalized;
}

int32_t send_gait_command(unitree::robot::go2::SportClient &sport_client, const std::string &gait)
{
    const std::string selected_gait = canonical_gait(gait);
    if (selected_gait == "static_walk") {
        return sport_client.StaticWalk();
    }
    if (selected_gait == "economic_gait") {
        return sport_client.EconomicGait();
    }
    if (selected_gait == "classic_walk") {
        return sport_client.ClassicWalk(true);
    }
    if (selected_gait == "free_walk") {
        return sport_client.FreeWalk();
    }
    if (selected_gait == "walk_upright") {
        return sport_client.WalkUpright(true);
    }
    if (selected_gait == "trot_run") {
        return sport_client.TrotRun();
    }

    throw std::runtime_error(
        "Unsupported gait \"" + gait +
        "\". Expected one of: none, static_walk, economic, classic_walk, free_walk, walk_upright, trot_run.");
}

bool is_zero_command(const geometry_msgs::msg::Twist &msg, double epsilon = 1.0e-4)
{
    return (
        std::fabs(static_cast<double>(msg.linear.x)) <= epsilon &&
        std::fabs(static_cast<double>(msg.linear.y)) <= epsilon &&
        std::fabs(static_cast<double>(msg.angular.z)) <= epsilon);
}

}  // namespace

class VoiceAttentionMotionBridgeNode : public rclcpp::Node
{
public:
    VoiceAttentionMotionBridgeNode()
    : Node("voice_attention_motion_bridge_node"),
      backend_name_(this->declare_parameter<std::string>("backend", "sport_free_avoid")),
      backend_(parse_backend(backend_name_)),
      cmd_vel_topic_(this->declare_parameter<std::string>("cmd_vel_topic", "/voice/attention/cmd_vel")),
      reassert_gait_topic_(
          this->declare_parameter<std::string>(
              "reassert_gait_topic",
              "/voice/attention/reassert_gait")),
      network_interface_(this->declare_parameter<std::string>("network_interface", "")),
      desired_gait_(this->declare_parameter<std::string>("desired_gait", "static_walk")),
      command_timeout_s_(std::max(
          0.05,
          this->declare_parameter<double>("command_timeout_s", 0.35))),
      gait_reassert_period_s_(std::max(
          0.0,
          this->declare_parameter<double>("gait_reassert_period_s", 0.5))),
      debug_(this->declare_parameter<bool>("debug", false))
    {
        initialize_unitree_sdk();

        cmd_vel_subscriber_ = this->create_subscription<geometry_msgs::msg::Twist>(
            cmd_vel_topic_,
            10,
            std::bind(&VoiceAttentionMotionBridgeNode::cmd_vel_callback, this, std::placeholders::_1));
        reassert_gait_subscriber_ = this->create_subscription<std_msgs::msg::Bool>(
            reassert_gait_topic_,
            10,
            std::bind(
                &VoiceAttentionMotionBridgeNode::reassert_gait_callback,
                this,
                std::placeholders::_1));
        watchdog_timer_ = this->create_wall_timer(
            std::chrono::milliseconds(100),
            std::bind(&VoiceAttentionMotionBridgeNode::watchdog_callback, this));

        RCLCPP_INFO(
            this->get_logger(),
            "Voice attention motion bridge ready. backend=%s cmd_vel_topic=%s reassert_gait_topic=%s desired_gait=%s network_interface=%s",
            backend_name_.c_str(),
            cmd_vel_topic_.c_str(),
            reassert_gait_topic_.c_str(),
            desired_gait_.c_str(),
            network_interface_.empty() ? "<auto>" : network_interface_.c_str());
    }

    ~VoiceAttentionMotionBridgeNode() override
    {
        if (!sdk_initialized_) {
            return;
        }

        send_motion_command(0.0F, 0.0F, 0.0F, false);
        disable_backend(false);
        unitree::robot::ChannelFactory::Instance()->Release();
    }

private:
    void initialize_unitree_sdk()
    {
        RCLCPP_INFO(
            this->get_logger(),
            "Initializing Unitree SDK backend=%s network_interface=%s desired_gait=%s",
            backend_name_.c_str(),
            network_interface_.empty() ? "<auto>" : network_interface_.c_str(),
            desired_gait_.c_str());

        if (network_interface_.empty()) {
            unitree::robot::ChannelFactory::Instance()->Init(0);
        } else {
            unitree::robot::ChannelFactory::Instance()->Init(0, network_interface_);
        }

        sport_client_ = std::make_unique<unitree::robot::go2::SportClient>();
        sport_client_->SetTimeout(10.0F);
        sport_client_->Init();

        if (backend_ == MotionBackend::kObstaclesAvoid) {
            obstacles_avoid_client_ =
                std::make_unique<unitree::robot::go2::ObstaclesAvoidClient>();
            obstacles_avoid_client_->SetTimeout(10.0F);
            obstacles_avoid_client_->Init();
        }

        sdk_initialized_ = true;
        const std::string selected_gait = canonical_gait(desired_gait_);
        if (selected_gait == "none") {
            RCLCPP_INFO(this->get_logger(), "Attention motion bridge will not reassert gait.");
        } else {
            apply_gait(selected_gait, false, "startup");
        }
    }

    void cmd_vel_callback(const geometry_msgs::msg::Twist::SharedPtr msg)
    {
        if (!sdk_initialized_) {
            return;
        }

        last_command_time_ = std::chrono::steady_clock::now();

        if (is_zero_command(*msg)) {
            if (backend_enabled_) {
                send_motion_command(0.0F, 0.0F, 0.0F, true);
            }
            active_motion_ = false;
            stale_stop_sent_ = true;
            return;
        }

        active_motion_ = true;
        stale_stop_sent_ = false;

        if (!ensure_motion_ready()) {
            return;
        }

        maybe_reassert_gait("periodic");
        send_motion_command(
            static_cast<float>(msg->linear.x),
            static_cast<float>(msg->linear.y),
            static_cast<float>(msg->angular.z),
            true);
    }

    void reassert_gait_callback(const std_msgs::msg::Bool::SharedPtr msg)
    {
        if (!msg->data) {
            return;
        }

        const std::string selected_gait = canonical_gait(desired_gait_);
        if (selected_gait == "none") {
            return;
        }

        apply_gait(selected_gait, true, "explicit_request");
    }

    void watchdog_callback()
    {
        if (!sdk_initialized_ || !backend_enabled_ || stale_stop_sent_) {
            return;
        }

        const double age_s = std::chrono::duration<double>(
            std::chrono::steady_clock::now() - last_command_time_).count();
        if (age_s <= command_timeout_s_) {
            return;
        }

        send_motion_command(0.0F, 0.0F, 0.0F, true);
        disable_backend(true);
        reassert_desired_gait("watchdog_stop");
        active_motion_ = false;
        stale_stop_sent_ = true;

        RCLCPP_INFO(
            this->get_logger(),
            "Attention motion command timed out after %.2fs. Sent stop and restored gait %s.",
            age_s,
            canonical_gait(desired_gait_).c_str());
    }

    bool ensure_motion_ready()
    {
        reassert_desired_gait("pre_enable");

        if (!backend_enabled_ && !enable_backend()) {
            return false;
        }

        reassert_desired_gait("post_enable");
        return true;
    }

    bool enable_backend()
    {
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
                "Failed to enable Unitree backend %s for attention motion.",
                backend_name_.c_str());
            return false;
        }

        backend_enabled_ = true;
        if (debug_) {
            RCLCPP_INFO(
                this->get_logger(),
                "Enabled Unitree backend %s for attention motion.",
                backend_name_.c_str());
        }
        return true;
    }

    void disable_backend(bool log_failures)
    {
        if (!backend_enabled_) {
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
                const int32_t stop_result = sport_client_->StopMove();
                const int32_t free_avoid_result = sport_client_->FreeAvoid(false);
                success = (free_avoid_result == 0);
                if (!success) {
                    failure_detail =
                        "StopMove=" + std::to_string(stop_result) +
                        " FreeAvoid(false)=" + std::to_string(free_avoid_result);
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
        if (debug_) {
            RCLCPP_INFO(
                this->get_logger(),
                "Disabled Unitree backend %s for attention motion.",
                backend_name_.c_str());
        }
    }

    void send_motion_command(float vx, float vy, float wz, bool log_failures)
    {
        if (!backend_enabled_) {
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
                "Failed to send attention motion command to backend %s (vx=%.3f vy=%.3f wz=%.3f, result=%d).",
                backend_name_.c_str(),
                vx,
                vy,
                wz,
                result);
            return;
        }

        if (
            debug_ &&
            (std::fabs(vx) > 1.0e-4F || std::fabs(vy) > 1.0e-4F || std::fabs(wz) > 1.0e-4F))
        {
            RCLCPP_INFO(
                this->get_logger(),
                "Attention motion command sent via backend %s (vx=%.3f vy=%.3f wz=%.3f).",
                backend_name_.c_str(),
                vx,
                vy,
                wz);
        }
    }

    void maybe_reassert_gait(const char *context)
    {
        if (gait_reassert_period_s_ <= 0.0) {
            return;
        }

        const auto now = std::chrono::steady_clock::now();
        const double age_s = std::chrono::duration<double>(now - last_gait_command_time_).count();
        if (age_s < gait_reassert_period_s_) {
            return;
        }

        reassert_desired_gait(context);
    }

    void reassert_desired_gait(const char *context)
    {
        const std::string selected_gait = canonical_gait(desired_gait_);
        if (selected_gait == "none") {
            return;
        }

        apply_gait(selected_gait, true, context);
    }

    bool apply_gait(const std::string &selected_gait, bool log_failures, const char *context)
    {
        if (selected_gait == "none") {
            return true;
        }
        if (sport_client_ == nullptr) {
            if (log_failures) {
                RCLCPP_ERROR(
                    this->get_logger(),
                    "Cannot apply attention gait %s because the sport client is unavailable.",
                    selected_gait.c_str());
            }
            return false;
        }

        int32_t result = 0;
        try {
            result = send_gait_command(*sport_client_, selected_gait);
        } catch (const std::exception &exc) {
            if (log_failures) {
                RCLCPP_ERROR(
                    this->get_logger(),
                    "Failed to apply attention gait %s during %s: %s",
                    selected_gait.c_str(),
                    context,
                    exc.what());
            }
            return false;
        }

        if (result != 0) {
            if (log_failures) {
                RCLCPP_ERROR(
                    this->get_logger(),
                    "Attention gait command %s during %s returned %d.",
                    selected_gait.c_str(),
                    context,
                    result);
            }
            return false;
        }

        last_gait_command_time_ = std::chrono::steady_clock::now();
        if (debug_) {
            RCLCPP_INFO(
                this->get_logger(),
                "Applied attention gait %s during %s.",
                selected_gait.c_str(),
                context);
        }
        return true;
    }

    std::string backend_name_;
    MotionBackend backend_;
    std::string cmd_vel_topic_;
    std::string reassert_gait_topic_;
    std::string network_interface_;
    std::string desired_gait_;
    double command_timeout_s_;
    double gait_reassert_period_s_;
    bool debug_ = false;

    bool sdk_initialized_ = false;
    bool backend_enabled_ = false;
    bool active_motion_ = false;
    bool stale_stop_sent_ = true;

    std::chrono::steady_clock::time_point last_command_time_{std::chrono::steady_clock::now()};
    std::chrono::steady_clock::time_point last_gait_command_time_{std::chrono::steady_clock::time_point::min()};

    std::unique_ptr<unitree::robot::go2::SportClient> sport_client_;
    std::unique_ptr<unitree::robot::go2::ObstaclesAvoidClient> obstacles_avoid_client_;

    rclcpp::Subscription<geometry_msgs::msg::Twist>::SharedPtr cmd_vel_subscriber_;
    rclcpp::Subscription<std_msgs::msg::Bool>::SharedPtr reassert_gait_subscriber_;
    rclcpp::TimerBase::SharedPtr watchdog_timer_;
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<VoiceAttentionMotionBridgeNode>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}
