from launch import LaunchDescription
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.actions import Node
from launch.substitutions import Command
import os
from ament_index_python.packages import get_package_share_directory
from ament_index_python.packages import get_package_share_path

def generate_launch_description():

    urdf_path = os.path.join(get_package_share_path('go2_description'), 
                             'urdf', 'go2_nav2.urdf')
    rviz_config_path = os.path.join(get_package_share_path('go2_description'), 
                             'config', 'go2_urdf_config.rviz')
    
    robot_description = ParameterValue(Command(['xacro ', urdf_path]), value_type=str)

    robot_state_publisher_node = Node(
        package="robot_state_publisher", 
        executable="robot_state_publisher", 
        parameters=[{'robot_description': robot_description}]     
    )

    joint_state_publisher_gui_node = Node(
        package="joint_state_publisher_gui", 
        executable="joint_state_publisher_gui"
    )

    rviz2_node = Node(
        package="rviz2", 
        executable="rviz2", 
        arguments=['-d', rviz_config_path]
    )



    return LaunchDescription([

        Node(
            name='rplidar_composition',
            package='rplidar_ros',
            executable='rplidar_composition',
            output='screen',
            parameters=[{
                'serial_port': '/dev/ttyUSB0',
                'serial_baudrate': 115200,  # A1 / A2
                # 'serial_baudrate': 256000, # A3
                'frame_id': 'laser',
                'inverted': False,
                'angle_compensate': True,
            }],
        ),

        robot_state_publisher_node,
        joint_state_publisher_gui_node,
        rviz2_node
    ])