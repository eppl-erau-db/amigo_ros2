#include <algorithm>
#include <chrono>
#include <cmath>
#include <cctype>
#include <functional>
#include <iomanip>
#include <limits>
#include <memory>
#include <mutex>
#include <optional>
#include <sstream>
#include <string>

#include <geometry_msgs/msg/point_stamped.hpp>
#include <go2_interfaces/msg/robot_mode_state.hpp>
#include <image_transport/camera_subscriber.hpp>
#include <image_transport/image_transport.hpp>
#include <opencv2/imgproc.hpp>
#include <rclcpp/rclcpp.hpp>
#include <sensor_msgs/image_encodings.hpp>
#include <sensor_msgs/msg/camera_info.hpp>
#include <sensor_msgs/msg/image.hpp>
#include <std_msgs/msg/bool.hpp>
#include <std_msgs/msg/int32.hpp>
#include <std_msgs/msg/string.hpp>
#include <zed_msgs/msg/object.hpp>
#include <zed_msgs/msg/objects_stamped.hpp>

namespace
{
constexpr int8_t kTrackingStateOk = 1;
constexpr int8_t kTrackingStateSearching = 2;
}  // namespace

class PersonFollowVisionNode : public rclcpp::Node
{
public:
  PersonFollowVisionNode()
  : Node("person_follow_vision_node")
  {
    enabled_ = this->declare_parameter("enabled_on_start", false);
    image_topic_ = this->declare_parameter<std::string>(
      "image_topic", "/zed/zed_node/rgb/color/rect/image");
    objects_topic_ = this->declare_parameter<std::string>(
      "objects_topic", "/zed/zed_node/obj_det/objects");
    robot_mode_state_topic_ = this->declare_parameter<std::string>(
      "robot_mode_state_topic", "/robot_mode_state");
    image_transport_ = this->declare_parameter<std::string>(
      "image_transport", "raw");
    annotated_image_topic_ = this->declare_parameter<std::string>(
      "annotated_image_topic", "~/annotated_image");
    target_point_topic_ = this->declare_parameter<std::string>(
      "target_point_topic", "~/target_point");
    target_visible_topic_ = this->declare_parameter<std::string>(
      "target_visible_topic", "~/target_visible");
    target_id_topic_ = this->declare_parameter<std::string>(
      "target_id_topic", "~/target_id");
    status_topic_ = this->declare_parameter<std::string>(
      "status_topic", "~/status");
    target_label_ = normalizeToken(
      this->declare_parameter<std::string>("target_label", "person"));
    min_target_confidence_ = this->declare_parameter("min_target_confidence", 40.0);
    max_target_age_s_ = this->declare_parameter("max_target_age_s", 1.0);

    rclcpp::QoS camera_qos(rclcpp::KeepLast(10));
    camera_qos.reliable();
    camera_qos.durability_volatile();

    rclcpp::QoS sensor_qos(rclcpp::KeepLast(10));
    sensor_qos.best_effort();
    sensor_qos.durability_volatile();

    image_sub_ = image_transport::create_camera_subscription(
      this,
      image_topic_,
      std::bind(
        &PersonFollowVisionNode::imageCallback,
        this,
        std::placeholders::_1,
        std::placeholders::_2),
      image_transport_,
      camera_qos.get_rmw_qos_profile());
    objects_sub_ = this->create_subscription<zed_msgs::msg::ObjectsStamped>(
      objects_topic_, sensor_qos,
      std::bind(&PersonFollowVisionNode::objectsCallback, this, std::placeholders::_1));
    robot_mode_state_sub_ = this->create_subscription<go2_interfaces::msg::RobotModeState>(
      robot_mode_state_topic_, 10,
      std::bind(&PersonFollowVisionNode::robotModeStateCallback, this, std::placeholders::_1));

    annotated_image_pub_ = this->create_publisher<sensor_msgs::msg::Image>(
      annotated_image_topic_, 10);
    target_point_pub_ = this->create_publisher<geometry_msgs::msg::PointStamped>(
      target_point_topic_, 10);
    target_visible_pub_ = this->create_publisher<std_msgs::msg::Bool>(
      target_visible_topic_, 10);
    target_id_pub_ = this->create_publisher<std_msgs::msg::Int32>(
      target_id_topic_, 10);
    status_pub_ = this->create_publisher<std_msgs::msg::String>(
      status_topic_, 10);

    last_target_update_time_ = this->now();
    last_objects_received_time_ = this->now();

    stale_target_timer_ = this->create_wall_timer(
      std::chrono::milliseconds(200),
      std::bind(&PersonFollowVisionNode::staleTargetTimerCallback, this));

    publishTargetVisible(false);
    publishStatus(enabled_ ? "follow_enabled_waiting_for_target" : "follow_disabled");

    RCLCPP_INFO(
      this->get_logger(),
      "Person follow vision node ready. enabled=%s image_topic=%s objects_topic=%s robot_mode_state_topic=%s image_transport=%s",
      enabled_ ? "true" : "false",
      image_topic_.c_str(),
      objects_topic_.c_str(),
      robot_mode_state_topic_.c_str(),
      image_transport_.c_str());
  }

private:
  struct TargetCandidate
  {
    int id = -1;
    float confidence = 0.0F;
    int8_t tracking_state = 0;
    cv::Rect rect;
    geometry_msgs::msg::PointStamped point;
    std::string label;
    double distance_m = std::numeric_limits<double>::infinity();
  };

  static std::string normalizeToken(const std::string & input)
  {
    std::string out;
    bool last_was_sep = true;

    for (char raw_ch : input) {
      const auto ch = static_cast<unsigned char>(raw_ch);
      if (std::isalnum(ch)) {
        out.push_back(static_cast<char>(std::tolower(ch)));
        last_was_sep = false;
      } else if (!last_was_sep) {
        out.push_back('_');
        last_was_sep = true;
      }
    }

    while (!out.empty() && out.back() == '_') {
      out.pop_back();
    }

    return out;
  }

  static cv::Rect boundingBoxRect(const zed_msgs::msg::Object & object)
  {
    int min_x = std::numeric_limits<int>::max();
    int min_y = std::numeric_limits<int>::max();
    int max_x = std::numeric_limits<int>::min();
    int max_y = std::numeric_limits<int>::min();

    for (const auto & corner : object.bounding_box_2d.corners) {
      min_x = std::min(min_x, static_cast<int>(corner.kp[0]));
      min_y = std::min(min_y, static_cast<int>(corner.kp[1]));
      max_x = std::max(max_x, static_cast<int>(corner.kp[0]));
      max_y = std::max(max_y, static_cast<int>(corner.kp[1]));
    }

    if (min_x >= max_x || min_y >= max_y) {
      return {};
    }

    return cv::Rect(min_x, min_y, max_x - min_x, max_y - min_y);
  }

  static double euclideanDistanceMeters(const zed_msgs::msg::Object & object)
  {
    const double x = static_cast<double>(object.position[0]);
    const double y = static_cast<double>(object.position[1]);
    const double z = static_cast<double>(object.position[2]);
    if (!std::isfinite(x) || !std::isfinite(y) || !std::isfinite(z)) {
      return std::numeric_limits<double>::infinity();
    }
    return std::sqrt((x * x) + (y * y) + (z * z));
  }

  static bool convertImageToBgr(
    const sensor_msgs::msg::Image & msg,
    cv::Mat & output,
    std::string & error)
  {
    if (msg.data.empty()) {
      error = "empty image buffer";
      return false;
    }

    if (msg.encoding == sensor_msgs::image_encodings::BGR8) {
      cv::Mat view(
        static_cast<int>(msg.height),
        static_cast<int>(msg.width),
        CV_8UC3,
        const_cast<unsigned char *>(msg.data.data()),
        static_cast<size_t>(msg.step));
      output = view.clone();
      return true;
    }

    if (msg.encoding == sensor_msgs::image_encodings::BGRA8) {
      cv::Mat view(
        static_cast<int>(msg.height),
        static_cast<int>(msg.width),
        CV_8UC4,
        const_cast<unsigned char *>(msg.data.data()),
        static_cast<size_t>(msg.step));
      cv::cvtColor(view, output, cv::COLOR_BGRA2BGR);
      return true;
    }

    if (msg.encoding == sensor_msgs::image_encodings::RGB8) {
      cv::Mat view(
        static_cast<int>(msg.height),
        static_cast<int>(msg.width),
        CV_8UC3,
        const_cast<unsigned char *>(msg.data.data()),
        static_cast<size_t>(msg.step));
      cv::cvtColor(view, output, cv::COLOR_RGB2BGR);
      return true;
    }

    if (msg.encoding == sensor_msgs::image_encodings::RGBA8) {
      cv::Mat view(
        static_cast<int>(msg.height),
        static_cast<int>(msg.width),
        CV_8UC4,
        const_cast<unsigned char *>(msg.data.data()),
        static_cast<size_t>(msg.step));
      cv::cvtColor(view, output, cv::COLOR_RGBA2BGR);
      return true;
    }

    error = "unsupported image encoding: " + msg.encoding;
    return false;
  }

  bool isTrackUsable(const zed_msgs::msg::Object & object) const
  {
    if (normalizeToken(object.label) != target_label_) {
      return false;
    }

    if (static_cast<double>(object.confidence) < min_target_confidence_) {
      return false;
    }

    if (object.tracking_available &&
      object.tracking_state != kTrackingStateOk &&
      object.tracking_state != kTrackingStateSearching)
    {
      return false;
    }

    return boundingBoxRect(object).area() > 0;
  }

  std::optional<TargetCandidate> chooseTarget(
    const zed_msgs::msg::ObjectsStamped & msg,
    int current_target_id,
    int image_width,
    int image_height) const
  {
    std::optional<TargetCandidate> best_candidate;
    double best_score = -std::numeric_limits<double>::infinity();

    for (const auto & object : msg.objects) {
      if (!isTrackUsable(object)) {
        continue;
      }

      TargetCandidate candidate;
      candidate.id = static_cast<int>(object.label_id);
      candidate.confidence = object.confidence;
      candidate.tracking_state = object.tracking_state;
      candidate.rect = boundingBoxRect(object);
      candidate.label = object.label;
      candidate.distance_m = euclideanDistanceMeters(object);
      candidate.point.header = msg.header;
      candidate.point.point.x = static_cast<double>(object.position[0]);
      candidate.point.point.y = static_cast<double>(object.position[1]);
      candidate.point.point.z = static_cast<double>(object.position[2]);

      if (candidate.id == current_target_id) {
        return candidate;
      }

      double score = static_cast<double>(candidate.confidence) / 100.0;

      if (image_width > 0 && image_height > 0) {
        const double center_x = static_cast<double>(candidate.rect.x) +
          (static_cast<double>(candidate.rect.width) * 0.5);
        const double center_y = static_cast<double>(candidate.rect.y) +
          (static_cast<double>(candidate.rect.height) * 0.5);
        const double dx = center_x - (static_cast<double>(image_width) * 0.5);
        const double dy = center_y - (static_cast<double>(image_height) * 0.5);
        const double max_dist = std::hypot(
          static_cast<double>(image_width) * 0.5,
          static_cast<double>(image_height) * 0.5);
        const double center_score = 1.0 - std::min(1.0, std::hypot(dx, dy) / std::max(1.0, max_dist));
        const double area_score = static_cast<double>(candidate.rect.area()) /
          std::max(1.0, static_cast<double>(image_width * image_height));
        score += (0.75 * center_score) + (3.0 * area_score);
      }

      if (std::isfinite(candidate.distance_m)) {
        score += std::max(0.0, 1.0 - (candidate.distance_m / 10.0));
      }

      if (!best_candidate.has_value() || score > best_score) {
        best_candidate = candidate;
        best_score = score;
      }
    }

    return best_candidate;
  }

  void publishTargetVisible(bool visible)
  {
    if (visible == last_target_visible_) {
      return;
    }

    std_msgs::msg::Bool msg;
    msg.data = visible;
    target_visible_pub_->publish(msg);
    last_target_visible_ = visible;
  }

  void publishTargetId(int id)
  {
    if (id == last_published_target_id_) {
      return;
    }

    std_msgs::msg::Int32 msg;
    msg.data = id;
    target_id_pub_->publish(msg);
    last_published_target_id_ = id;
  }

  void publishStatus(const std::string & status)
  {
    if (status == last_status_) {
      return;
    }

    std_msgs::msg::String msg;
    msg.data = status;
    status_pub_->publish(msg);
    last_status_ = status;
  }

  void clearTarget(const std::string & reason)
  {
    active_target_id_ = -1;
    publishTargetVisible(false);
    publishTargetId(-1);
    publishStatus(reason);
  }

  void robotModeStateCallback(const go2_interfaces::msg::RobotModeState::SharedPtr msg)
  {
    const bool should_enable =
      msg->task_mode == "FOLLOW" &&
      msg->posture_mode == "STANDING" &&
      msg->motion_enabled;
    std::lock_guard<std::mutex> lock(state_mutex_);

    if (should_enable == enabled_) {
      return;
    }

    enabled_ = should_enable;
    active_target_id_ = -1;
    last_target_update_time_ = this->now();
    publishTargetVisible(false);
    publishTargetId(-1);
    publishStatus(enabled_ ? "follow_enabled_waiting_for_target" : "follow_disabled");

    RCLCPP_INFO(
      this->get_logger(),
      "Mission supervisor %s person follow perception.",
      enabled_ ? "enabled" : "disabled");
  }

  void objectsCallback(const zed_msgs::msg::ObjectsStamped::SharedPtr msg)
  {
    bool enabled_snapshot = false;
    int current_target_id = -1;
    int image_width = 0;
    int image_height = 0;

    {
      std::lock_guard<std::mutex> lock(state_mutex_);
      latest_objects_ = msg;
      last_objects_received_time_ = this->now();
      enabled_snapshot = enabled_;
      current_target_id = active_target_id_;
      image_width = latest_image_width_;
      image_height = latest_image_height_;
    }

    if (!enabled_snapshot) {
      return;
    }

    const auto target = chooseTarget(*msg, current_target_id, image_width, image_height);
    if (!target.has_value()) {
      return;
    }

    {
      std::lock_guard<std::mutex> lock(state_mutex_);
      active_target_id_ = target->id;
      last_target_update_time_ = this->now();
    }

    target_point_pub_->publish(target->point);
    publishTargetVisible(true);
    publishTargetId(target->id);

    std::ostringstream status;
    status << "follow_tracking"
           << " id=" << target->id
           << " label=" << target->label
           << " confidence=" << target->confidence
           << " distance_m=" << target->distance_m
           << " tracking_state=" << static_cast<int>(target->tracking_state);
    publishStatus(status.str());
  }

  void imageCallback(
    const sensor_msgs::msg::Image::ConstSharedPtr & msg,
    const sensor_msgs::msg::CameraInfo::ConstSharedPtr &)
  {
    zed_msgs::msg::ObjectsStamped::SharedPtr objects_snapshot;
    bool enabled_snapshot = false;
    int active_target_id_snapshot = -1;
    rclcpp::Time last_objects_time = this->now();

    {
      std::lock_guard<std::mutex> lock(state_mutex_);
      latest_image_width_ = static_cast<int>(msg->width);
      latest_image_height_ = static_cast<int>(msg->height);
      enabled_snapshot = enabled_;
      active_target_id_snapshot = active_target_id_;
      objects_snapshot = latest_objects_;
      last_objects_time = last_objects_received_time_;
    }

    if (!logged_first_image_) {
      logged_first_image_ = true;
      RCLCPP_INFO(
        this->get_logger(),
        "Received first image frame on %s (%ux%u, encoding=%s)",
        image_topic_.c_str(),
        msg->width,
        msg->height,
        msg->encoding.c_str());
    }

    if (!enabled_snapshot || !objects_snapshot) {
      return;
    }

    if ((this->now() - last_objects_time).seconds() > max_target_age_s_) {
      return;
    }

    cv::Mat annotated_image;
    std::string conversion_error;
    if (!convertImageToBgr(*msg, annotated_image, conversion_error)) {
      RCLCPP_WARN(
        this->get_logger(),
        "Failed to convert image for annotation: %s",
        conversion_error.c_str());
      return;
    }

    bool drew_target = false;
    for (const auto & object : objects_snapshot->objects) {
      if (!isTrackUsable(object)) {
        continue;
      }

      const cv::Rect rect = boundingBoxRect(object);
      if (rect.area() <= 0) {
        continue;
      }

      const bool is_active_target =
        static_cast<int>(object.label_id) == active_target_id_snapshot;
      const cv::Scalar color = is_active_target ? cv::Scalar(0, 220, 0) : cv::Scalar(0, 200, 255);
      const int thickness = is_active_target ? 3 : 2;

      cv::rectangle(annotated_image, rect, color, thickness);

      const double distance_m = euclideanDistanceMeters(object);
      std::ostringstream label;
      label << object.label
            << " id=" << static_cast<int>(object.label_id)
            << " conf=" << object.confidence;
      if (std::isfinite(distance_m)) {
        label << " dist=" << std::fixed << std::setprecision(2) << distance_m << "m";
      }

      const int text_y = std::max(20, rect.y - 8);
      cv::putText(
        annotated_image,
        label.str(),
        cv::Point(rect.x, text_y),
        cv::FONT_HERSHEY_SIMPLEX,
        0.55,
        color,
        2);

      if (is_active_target) {
        drew_target = true;
      }
    }

    const cv::Scalar banner_color = drew_target ? cv::Scalar(0, 220, 0) : cv::Scalar(0, 200, 255);
    const std::string banner_text = drew_target ?
      "FOLLOW TARGET LOCKED" :
      "FOLLOW ENABLED - WAITING FOR PERSON";
    cv::putText(
      annotated_image,
      banner_text,
      cv::Point(20, 32),
      cv::FONT_HERSHEY_SIMPLEX,
      0.8,
      banner_color,
      2);

    sensor_msgs::msg::Image annotated_msg;
    annotated_msg.header = msg->header;
    annotated_msg.height = static_cast<uint32_t>(annotated_image.rows);
    annotated_msg.width = static_cast<uint32_t>(annotated_image.cols);
    annotated_msg.encoding = sensor_msgs::image_encodings::BGR8;
    annotated_msg.is_bigendian = msg->is_bigendian;
    annotated_msg.step = static_cast<sensor_msgs::msg::Image::_step_type>(annotated_image.step);
    const auto * data_begin = annotated_image.data;
    const auto * data_end = data_begin + (annotated_image.step * annotated_image.rows);
    annotated_msg.data.assign(data_begin, data_end);

    annotated_image_pub_->publish(annotated_msg);
    if (!logged_first_annotated_image_) {
      logged_first_annotated_image_ = true;
      RCLCPP_INFO(
        this->get_logger(),
        "Published first annotated image frame to %s",
        annotated_image_topic_.c_str());
    }
  }

  void staleTargetTimerCallback()
  {
    std::lock_guard<std::mutex> lock(state_mutex_);

    if (!enabled_) {
      return;
    }

    if (active_target_id_ < 0) {
      return;
    }

    if ((this->now() - last_target_update_time_).seconds() <= max_target_age_s_) {
      return;
    }

    clearTarget("follow_enabled_target_lost");
  }

  std::mutex state_mutex_;

  bool enabled_ = false;
  bool last_target_visible_ = false;
  int active_target_id_ = -1;
  int last_published_target_id_ = -1;
  int latest_image_width_ = 0;
  int latest_image_height_ = 0;
  double min_target_confidence_ = 40.0;
  double max_target_age_s_ = 1.0;

  std::string image_topic_;
  std::string objects_topic_;
  std::string robot_mode_state_topic_;
  std::string image_transport_;
  std::string annotated_image_topic_;
  std::string target_point_topic_;
  std::string target_visible_topic_;
  std::string target_id_topic_;
  std::string status_topic_;
  std::string target_label_;
  std::string last_status_;

  rclcpp::Time last_target_update_time_{0, 0, RCL_ROS_TIME};
  rclcpp::Time last_objects_received_time_{0, 0, RCL_ROS_TIME};

  zed_msgs::msg::ObjectsStamped::SharedPtr latest_objects_;

  bool logged_first_image_ = false;
  bool logged_first_annotated_image_ = false;

  image_transport::CameraSubscriber image_sub_;
  rclcpp::Subscription<zed_msgs::msg::ObjectsStamped>::SharedPtr objects_sub_;
  rclcpp::Subscription<go2_interfaces::msg::RobotModeState>::SharedPtr robot_mode_state_sub_;

  rclcpp::Publisher<sensor_msgs::msg::Image>::SharedPtr annotated_image_pub_;
  rclcpp::Publisher<geometry_msgs::msg::PointStamped>::SharedPtr target_point_pub_;
  rclcpp::Publisher<std_msgs::msg::Bool>::SharedPtr target_visible_pub_;
  rclcpp::Publisher<std_msgs::msg::Int32>::SharedPtr target_id_pub_;
  rclcpp::Publisher<std_msgs::msg::String>::SharedPtr status_pub_;

  rclcpp::TimerBase::SharedPtr stale_target_timer_;
};

int main(int argc, char ** argv)
{
  rclcpp::init(argc, argv);
  auto node = std::make_shared<PersonFollowVisionNode>();
  rclcpp::spin(node);
  rclcpp::shutdown();
  return 0;
}
