#include <rclcpp/rclcpp.hpp>
#include <sensor_msgs/msg/point_cloud2.hpp>
#include <tf2_ros/buffer.h>
#include <tf2_ros/transform_listener.h>
#include <tf2_eigen/tf2_eigen.hpp>
#include <Eigen/Geometry>
#include <cstring>
#include <string>

class ZBandFilterNode : public rclcpp::Node {
public:
  ZBandFilterNode()
  : Node("z_band_filter_node"),
    tf_buffer_(this->get_clock()),
    tf_listener_(tf_buffer_) {
    // Params
    input_topic_   = declare_parameter<std::string>("input", "/velodyne_points");
    output_topic_  = declare_parameter<std::string>("output", "/velodyne_points_global_band");
    target_frame_  = declare_parameter<std::string>("target_frame", "odom");
    min_z_         = declare_parameter<double>("min_z", 1.0);
    max_z_         = declare_parameter<double>("max_z", 1.5);
    tf_timeout_s_  = declare_parameter<double>("tf_timeout", 0.05);
    use_latest_tf_ = declare_parameter<bool>("use_latest_tf", true);

    // Sub: match typical LiDAR (best-effort, small queue)
    sub_ = create_subscription<sensor_msgs::msg::PointCloud2>(
      input_topic_, rclcpp::SensorDataQoS(),
      std::bind(&ZBandFilterNode::onCloud, this, std::placeholders::_1));

    // Pub: RELIABLE so it is compatible with RTAB-Map's default subscription
    rclcpp::QoS pub_qos(rclcpp::KeepLast(10));
    pub_qos.reliable();           // <-- key fix
    pub_qos.durability_volatile();
    pub_ = create_publisher<sensor_msgs::msg::PointCloud2>(output_topic_, pub_qos);
  }

private:
  struct Offsets { int32_t x=-1, y=-1, z=-1; } off_;

  bool computeOffsets_(const sensor_msgs::msg::PointCloud2& msg) {
    off_ = {};
    for (const auto& f : msg.fields) {
      if      (f.name == "x") off_.x = f.offset;
      else if (f.name == "y") off_.y = f.offset;
      else if (f.name == "z") off_.z = f.offset;
    }
    if (off_.x < 0 || off_.y < 0 || off_.z < 0) {
      RCLCPP_WARN(get_logger(), "PointCloud2 missing x/y/z fields.");
      return false;
    }
    return true;
  }

  static inline float readFloat_(const uint8_t* p) {
    float v; std::memcpy(&v, p, sizeof(float)); return v;
  }

  void onCloud(const sensor_msgs::msg::PointCloud2::SharedPtr msg) {
    if (msg->fields.empty() || msg->point_step == 0) return;
    if (off_.x < 0 && !computeOffsets_(*msg)) return;

    // Lookup transform velodyne->target_frame (typically odom)
    geometry_msgs::msg::TransformStamped T;
    try {
      if (use_latest_tf_) {
        T = tf_buffer_.lookupTransform(target_frame_, msg->header.frame_id,
                                       tf2::TimePointZero);
      } else {
        T = tf_buffer_.lookupTransform(target_frame_, msg->header.frame_id,
                                       msg->header.stamp,
                                       tf2::durationFromSec(tf_timeout_s_));
      }
    } catch (const std::exception& e) {
      RCLCPP_WARN_THROTTLE(get_logger(), *get_clock(), 2000,
                           "TF %s->%s failed: %s",
                           msg->header.frame_id.c_str(), target_frame_.c_str(), e.what());
      return;
    }

    Eigen::Isometry3d Iso = tf2::transformToEigen(T.transform);
    const Eigen::Matrix3d& R = Iso.linear();
    const Eigen::Vector3d& t = Iso.translation();

    // Build filtered cloud (unorganized). Preserve fields & encoding.
    sensor_msgs::msg::PointCloud2 out;
    out.header       = msg->header;           // keep original frame & time
    out.fields       = msg->fields;
    out.is_bigendian = msg->is_bigendian;
    out.point_step   = msg->point_step;
    out.is_dense     = msg->is_dense;
    out.height = 1;
    out.width  = 0;
    out.data.reserve(msg->data.size());

    const size_t npts = static_cast<size_t>(msg->height) * static_cast<size_t>(msg->width);
    const uint8_t* base = msg->data.data();
    const size_t ps = msg->point_step;

    size_t kept = 0;
    for (size_t i = 0; i < npts; ++i) {
      const uint8_t* p = base + i * ps;
      const float x = readFloat_(p + off_.x);
      const float y = readFloat_(p + off_.y);
      const float z = readFloat_(p + off_.z);

      // world z: zw = R(2,:)*[x y z]^T + t.z()
      const double zw = R(2,0)*x + R(2,1)*y + R(2,2)*z + t.z();
      if (zw >= min_z_ && zw <= max_z_) {
        out.data.insert(out.data.end(), p, p + ps);
        ++kept;
      }
    }
    out.width   = static_cast<uint32_t>(kept);
    out.row_step = out.point_step * out.width;

    pub_->publish(out);
  }

  // Params
  std::string input_topic_, output_topic_, target_frame_;
  double min_z_, max_z_, tf_timeout_s_;
  bool use_latest_tf_;

  // ROS
  rclcpp::Subscription<sensor_msgs::msg::PointCloud2>::SharedPtr sub_;
  rclcpp::Publisher<sensor_msgs::msg::PointCloud2>::SharedPtr pub_;
  tf2_ros::Buffer tf_buffer_;
  tf2_ros::TransformListener tf_listener_;
};

int main(int argc, char** argv) {
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<ZBandFilterNode>());
  rclcpp::shutdown();
  return 0;
}
