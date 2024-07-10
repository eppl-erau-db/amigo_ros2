// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from unitree_go:msg/LidarState.idl
// generated code does not contain a copyright notice

#ifndef UNITREE_GO__MSG__DETAIL__LIDAR_STATE__TRAITS_HPP_
#define UNITREE_GO__MSG__DETAIL__LIDAR_STATE__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "unitree_go/msg/detail/lidar_state__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace unitree_go
{

namespace msg
{

inline void to_flow_style_yaml(
  const LidarState & msg,
  std::ostream & out)
{
  out << "{";
  // member: stamp
  {
    out << "stamp: ";
    rosidl_generator_traits::value_to_yaml(msg.stamp, out);
    out << ", ";
  }

  // member: firmware_version
  {
    out << "firmware_version: ";
    rosidl_generator_traits::value_to_yaml(msg.firmware_version, out);
    out << ", ";
  }

  // member: software_version
  {
    out << "software_version: ";
    rosidl_generator_traits::value_to_yaml(msg.software_version, out);
    out << ", ";
  }

  // member: sdk_version
  {
    out << "sdk_version: ";
    rosidl_generator_traits::value_to_yaml(msg.sdk_version, out);
    out << ", ";
  }

  // member: sys_rotation_speed
  {
    out << "sys_rotation_speed: ";
    rosidl_generator_traits::value_to_yaml(msg.sys_rotation_speed, out);
    out << ", ";
  }

  // member: com_rotation_speed
  {
    out << "com_rotation_speed: ";
    rosidl_generator_traits::value_to_yaml(msg.com_rotation_speed, out);
    out << ", ";
  }

  // member: error_state
  {
    out << "error_state: ";
    rosidl_generator_traits::value_to_yaml(msg.error_state, out);
    out << ", ";
  }

  // member: cloud_frequency
  {
    out << "cloud_frequency: ";
    rosidl_generator_traits::value_to_yaml(msg.cloud_frequency, out);
    out << ", ";
  }

  // member: cloud_packet_loss_rate
  {
    out << "cloud_packet_loss_rate: ";
    rosidl_generator_traits::value_to_yaml(msg.cloud_packet_loss_rate, out);
    out << ", ";
  }

  // member: cloud_size
  {
    out << "cloud_size: ";
    rosidl_generator_traits::value_to_yaml(msg.cloud_size, out);
    out << ", ";
  }

  // member: cloud_scan_num
  {
    out << "cloud_scan_num: ";
    rosidl_generator_traits::value_to_yaml(msg.cloud_scan_num, out);
    out << ", ";
  }

  // member: imu_frequency
  {
    out << "imu_frequency: ";
    rosidl_generator_traits::value_to_yaml(msg.imu_frequency, out);
    out << ", ";
  }

  // member: imu_packet_loss_rate
  {
    out << "imu_packet_loss_rate: ";
    rosidl_generator_traits::value_to_yaml(msg.imu_packet_loss_rate, out);
    out << ", ";
  }

  // member: imu_rpy
  {
    if (msg.imu_rpy.size() == 0) {
      out << "imu_rpy: []";
    } else {
      out << "imu_rpy: [";
      size_t pending_items = msg.imu_rpy.size();
      for (auto item : msg.imu_rpy) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: serial_recv_stamp
  {
    out << "serial_recv_stamp: ";
    rosidl_generator_traits::value_to_yaml(msg.serial_recv_stamp, out);
    out << ", ";
  }

  // member: serial_buffer_size
  {
    out << "serial_buffer_size: ";
    rosidl_generator_traits::value_to_yaml(msg.serial_buffer_size, out);
    out << ", ";
  }

  // member: serial_buffer_read
  {
    out << "serial_buffer_read: ";
    rosidl_generator_traits::value_to_yaml(msg.serial_buffer_read, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const LidarState & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: stamp
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "stamp: ";
    rosidl_generator_traits::value_to_yaml(msg.stamp, out);
    out << "\n";
  }

  // member: firmware_version
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "firmware_version: ";
    rosidl_generator_traits::value_to_yaml(msg.firmware_version, out);
    out << "\n";
  }

  // member: software_version
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "software_version: ";
    rosidl_generator_traits::value_to_yaml(msg.software_version, out);
    out << "\n";
  }

  // member: sdk_version
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "sdk_version: ";
    rosidl_generator_traits::value_to_yaml(msg.sdk_version, out);
    out << "\n";
  }

  // member: sys_rotation_speed
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "sys_rotation_speed: ";
    rosidl_generator_traits::value_to_yaml(msg.sys_rotation_speed, out);
    out << "\n";
  }

  // member: com_rotation_speed
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "com_rotation_speed: ";
    rosidl_generator_traits::value_to_yaml(msg.com_rotation_speed, out);
    out << "\n";
  }

  // member: error_state
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "error_state: ";
    rosidl_generator_traits::value_to_yaml(msg.error_state, out);
    out << "\n";
  }

  // member: cloud_frequency
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "cloud_frequency: ";
    rosidl_generator_traits::value_to_yaml(msg.cloud_frequency, out);
    out << "\n";
  }

  // member: cloud_packet_loss_rate
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "cloud_packet_loss_rate: ";
    rosidl_generator_traits::value_to_yaml(msg.cloud_packet_loss_rate, out);
    out << "\n";
  }

  // member: cloud_size
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "cloud_size: ";
    rosidl_generator_traits::value_to_yaml(msg.cloud_size, out);
    out << "\n";
  }

  // member: cloud_scan_num
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "cloud_scan_num: ";
    rosidl_generator_traits::value_to_yaml(msg.cloud_scan_num, out);
    out << "\n";
  }

  // member: imu_frequency
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "imu_frequency: ";
    rosidl_generator_traits::value_to_yaml(msg.imu_frequency, out);
    out << "\n";
  }

  // member: imu_packet_loss_rate
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "imu_packet_loss_rate: ";
    rosidl_generator_traits::value_to_yaml(msg.imu_packet_loss_rate, out);
    out << "\n";
  }

  // member: imu_rpy
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.imu_rpy.size() == 0) {
      out << "imu_rpy: []\n";
    } else {
      out << "imu_rpy:\n";
      for (auto item : msg.imu_rpy) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: serial_recv_stamp
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "serial_recv_stamp: ";
    rosidl_generator_traits::value_to_yaml(msg.serial_recv_stamp, out);
    out << "\n";
  }

  // member: serial_buffer_size
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "serial_buffer_size: ";
    rosidl_generator_traits::value_to_yaml(msg.serial_buffer_size, out);
    out << "\n";
  }

  // member: serial_buffer_read
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "serial_buffer_read: ";
    rosidl_generator_traits::value_to_yaml(msg.serial_buffer_read, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const LidarState & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace unitree_go

namespace rosidl_generator_traits
{

[[deprecated("use unitree_go::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const unitree_go::msg::LidarState & msg,
  std::ostream & out, size_t indentation = 0)
{
  unitree_go::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use unitree_go::msg::to_yaml() instead")]]
inline std::string to_yaml(const unitree_go::msg::LidarState & msg)
{
  return unitree_go::msg::to_yaml(msg);
}

template<>
inline const char * data_type<unitree_go::msg::LidarState>()
{
  return "unitree_go::msg::LidarState";
}

template<>
inline const char * name<unitree_go::msg::LidarState>()
{
  return "unitree_go/msg/LidarState";
}

template<>
struct has_fixed_size<unitree_go::msg::LidarState>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<unitree_go::msg::LidarState>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<unitree_go::msg::LidarState>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // UNITREE_GO__MSG__DETAIL__LIDAR_STATE__TRAITS_HPP_
