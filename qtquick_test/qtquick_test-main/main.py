import sys
import subprocess
import threading
import rclpy
import math
import json
from rclpy.node import Node
from PySide6.QtCore import (
    QAbstractListModel,
    QModelIndex,
    Qt,
    QTimer,
    Slot,
    QObject,
    Signal,
    Property,
)
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from std_msgs.msg import String
from sensor_msgs.msg import NavSatFix
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Odometry


# Topic alias mapping
TOPIC_ALIASES = {
    "/fix": "GPS Location",
    "/fix_velocity": "GPS Velocity",
    "/odom": "Dead Reckoning",
    "/imu/data_raw": "IMU Data",
    "/cmd_vel": "Velocity Command",
    "/scan": "Lidar Scan",
    "/camera/image": "Camera Feed",
    "/battery": "Battery Status",
}


class TopicModel(QAbstractListModel):
    """Model that tracks ROS2 topics with aliases and activity status."""
    
    AliasRole = Qt.UserRole + 1
    TopicRole = Qt.UserRole + 2
    StatusRole = Qt.UserRole + 3

    def __init__(self, node, monitored_topics):
        super().__init__()
        self._node = node
        self._monitored_topics = monitored_topics
        self._topic_data = []
        self._subscriptions = {}
        self._last_received = {}
        
        # Create subscriptions for each monitored topic
        self._setup_subscriptions()

    def _setup_subscriptions(self):
        """Create subscribers for all monitored topics."""
        for topic in self._monitored_topics:
            # Create a generic subscriber - you may need to adjust message types
            # based on your actual topics
            try:
                # Try to get topic type
                topic_list = self._node.get_topic_names_and_types()
                topic_type = None
                
                for name, types in topic_list:
                    if name == topic:
                        topic_type = types[0] if types else None
                        break
                
                # Create callback that updates last received time
                def make_callback(topic_name):
                    def callback(msg):
                        self._last_received[topic_name] = self._node.get_clock().now()
                    return callback
                
                # For now, use a generic subscription approach
                # You'll need to import the correct message types for your topics
                self._last_received[topic] = None
                
            except Exception as e:
                self._node.get_logger().warn(f"Could not subscribe to {topic}: {e}")

    def data(self, index, role):
        if not index.isValid() or index.row() >= len(self._topic_data):
            return None
        
        topic_info = self._topic_data[index.row()]
        
        if role == self.AliasRole:
            return topic_info["alias"]
        elif role == self.TopicRole:
            return topic_info["topic"]
        elif role == self.StatusRole:
            return topic_info["status"]
        
        return None

    def rowCount(self, parent=QModelIndex()):
        return len(self._topic_data)

    def roleNames(self):
        return {
            self.AliasRole: b"alias",
            self.TopicRole: b"topic",
            self.StatusRole: b"status",
        }

    @Slot()
    def updateTopics(self):
        """Check which topics are active and update the model."""
        active_topics = [name for name, _ in self._node.get_topic_names_and_types()]
        current_time = self._node.get_clock().now()
        
        self.beginResetModel()
        self._topic_data = []
        
        for topic in self._monitored_topics:
            alias = TOPIC_ALIASES.get(topic, topic)
            
            # Check if topic exists and has recent data
            if topic in active_topics:
                last_msg_time = self._last_received.get(topic)
                
                # Consider "receiving" if we got data in last 5 seconds
                if last_msg_time and (current_time - last_msg_time).nanoseconds / 1e9 < 5.0:
                    status = "Receiving"
                else:
                    # Topic exists but no recent messages
                    status = "No Data"
            else:
                status = "Offline"
            
            self._topic_data.append({
                "alias": alias,
                "topic": topic,
                "status": status
            })
        
        self.endResetModel()


class Ros2Node(Node):
    """ROS 2 node to monitor topic graph and subscribe to topics."""

    def __init__(self):
        super().__init__("qml_topic_viewer")


class LocationBridge(QObject):
    """Bridge to expose GPS location and waypoint to QML."""
    
    gpsLocationChanged = Signal()
    waypointChanged = Signal()
    odomChanged = Signal()
    
    def __init__(self, node):
        super().__init__()
        self._node = node
        self._gps_lat = 0
        self._gps_lon = 0
        self._waypoint_lat = 29.1920
        self._waypoint_lon = -81.0490
        self._odom_heading_deg = 0.0
        
        # Subscribe to /fix for GPS location
        self._fix_sub = self._node.create_subscription(
            NavSatFix,
            '/fix',
            self._fix_callback,
            10
        )
        
        # Subscribe to waypoint topic (adjust topic name as needed)
        # Assuming waypoint comes as PoseStamped with latitude/longitude
        # You may need to adjust this based on your actual waypoint message type
        self._waypoint_sub = self._node.create_subscription(
            PoseStamped,
            '/waypoint',
            self._waypoint_callback,
            10
        )

        # Subscribe to odometry to get global heading (yaw)
        try:
            self._odom_sub = self._node.create_subscription(
                Odometry,
                '/odom',
                self._odom_callback,
                10
            )
        except Exception:
            # If Odometry isn't available or topic differs, ignore for now
            self._node.get_logger().warn("LocationBridge: could not subscribe to /odom (Odometry)")
    
    def _fix_callback(self, msg):
        """Update GPS location from /fix topic.

        This handles the normal sensor_msgs/NavSatFix case and does
        a defensive conversion to floats and NaN checks.
        """
        try:
            # Log incoming message type for diagnostics
            self._node.get_logger().debug(f"/fix msg type={type(msg)}")

            # Preferred path: NavSatFix has latitude/longitude attributes
            if hasattr(msg, "latitude") and hasattr(msg, "longitude"):
                lat = float(msg.latitude)
                lon = float(msg.longitude)
            else:
                # Fallback: maybe a std_msgs/String with JSON payload
                lat = None
                lon = None
                if hasattr(msg, "data"):
                    try:
                        payload = json.loads(msg.data)
                        lat = float(payload.get("latitude") or payload.get("lat") or payload.get("y"))
                        lon = float(payload.get("longitude") or payload.get("lon") or payload.get("x"))
                    except Exception:
                        pass

            # Validate
            if math.isnan(lat) or math.isnan(lon):
                self._node.get_logger().warn("GPS: Received NaN latitude/longitude (no fix)")
                return

            # Update and notify
            self._gps_lat = lat
            self._gps_lon = lon
            self.gpsLocationChanged.emit()

        except Exception as e:
            self._node.get_logger().error(f"_fix_callback error parsing /fix: {e}")
    
    def _waypoint_callback(self, msg):
        """Update waypoint from waypoint topic."""
        # Assuming the waypoint contains lat/lon in the pose
        # You may need to adjust this based on your actual message structure
        # This is a simplified example
        self._waypoint_lat = msg.pose.position.x  # Adjust as needed
        self._waypoint_lon = msg.pose.position.y  # Adjust as needed
        self.waypointChanged.emit()

    def _odom_callback(self, msg):
        """Extract yaw (heading) from Odometry quaternion and expose degrees to QML.

        Uses the standard conversion from quaternion to yaw (Z axis rotation).
        """
        try:
            q = msg.pose.pose.orientation
            x = q.x
            y = q.y
            z = q.z
            w = q.w

            # yaw (rotation about Z axis)
            yaw = math.atan2(2.0 * (w * z + x * y), 1.0 - 2.0 * (y * y + z * z))
            yaw_deg = math.degrees(yaw)

            # Normalize to [0,360) if you prefer, but QML rotation works with negative values too
            # yaw_deg = (yaw_deg + 360.0) % 360.0

            self._odom_heading_deg = yaw_deg
            self.odomChanged.emit()
        except Exception as e:
            self._node.get_logger().error(f"_odom_callback error: {e}")
    
    @Property(float, notify=gpsLocationChanged)
    def gpsLatitude(self):
        return self._gps_lat
    
    @Property(float, notify=gpsLocationChanged)
    def gpsLongitude(self):
        return self._gps_lon
    
    @Property(float, notify=waypointChanged)
    def waypointLatitude(self):
        return self._waypoint_lat
    
    @Property(float, notify=waypointChanged)
    def waypointLongitude(self):
        return self._waypoint_lon

    @Property(float, notify=odomChanged)
    def odomHeading(self):
        """Heading in degrees extracted from global odometry (yaw)."""
        return self._odom_heading_deg


class CommandBridge(QObject):
    """Bridge to handle ROS2 command execution from QML."""
    
    commandStarted = Signal(str)  # Emits command description when started
    commandCompleted = Signal(str)  # Emits result when completed
    commandError = Signal(str)  # Emits error message if failed
    
    def __init__(self, node):
        super().__init__()
        self._node = node
        self._processes = {}  # Store running processes
        
    def _run_command_async(self, cmd_name, command, log_file=None):
        """Run a command asynchronously in a separate thread."""
        def run():
            try:
                self.commandStarted.emit(f"Starting: {cmd_name}")
                self._node.get_logger().info(f"Executing: {command}")
                
                if log_file:
                    # Run command with output redirected to log file
                    with open(log_file, 'w') as f:
                        process = subprocess.Popen(
                            command,
                            shell=True,
                            stdout=f,
                            stderr=subprocess.STDOUT
                        )
                        self._processes[cmd_name] = process
                        process.wait()
                else:
                    # Run command normally
                    process = subprocess.Popen(
                        command,
                        shell=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE
                    )
                    self._processes[cmd_name] = process
                    stdout, stderr = process.communicate()
                    
                    if process.returncode == 0:
                        self.commandCompleted.emit(f"{cmd_name} completed successfully")
                        self._node.get_logger().info(f"{cmd_name} completed")
                    else:
                        error_msg = stderr.decode() if stderr else "Unknown error"
                        self.commandError.emit(f"{cmd_name} failed: {error_msg}")
                        self._node.get_logger().error(f"{cmd_name} failed: {error_msg}")
                        
            except Exception as e:
                error_msg = f"Error executing {cmd_name}: {str(e)}"
                self.commandError.emit(error_msg)
                self._node.get_logger().error(error_msg)
                
        # Start command in separate thread
        thread = threading.Thread(target=run, daemon=True)
        thread.start()
    
    @Slot()
    def startMapping(self):
        """Launch the mapping process."""
        command = "ros2 launch go2_bringup mapping.launch.py"
        self._run_command_async("Mapping", command, "mappingOutput.log")
    
    @Slot()
    def logNormalPose(self):
        """Send action to log normal pose."""
        command = "ros2 action send_goal /log_pose go2_interfaces/action/LogPose \"{task_type: 'normal'}\""
        self._run_command_async("Log Normal Pose", command)
    
    @Slot()
    def logTaskPose(self):
        """Send action to log task pose."""
        command = "ros2 action send_goal /log_pose go2_interfaces/action/LogPose \"{task_type: 'task'}\""
        self._run_command_async("Log Task Pose", command)
    
    @Slot(str)
    def saveMap(self, map_name):
        """Save the current map with the given name."""
        if not map_name:
            self.commandError.emit("Map name cannot be empty")
            return
            
        command = f"ros2 run nav2_map_server map_saver_cli -f src/go2_description/maps/{map_name} --free 0.25 --occ 0.65 --fmt png"
        self._run_command_async("Save Map", command)
    
    @Slot(str)
    def deployNav(self, map_name):
        """Deploy navigation with the specified map."""
        if not map_name:
            self.commandError.emit("Map name cannot be empty")
            return
            
        command = f"ros2 launch go2_bringup go2_deploy.launch.py map_file:=src/go2_description/maps/{map_name}.yaml rviz:=true visualization:=false initial_pose:=false"
        self._run_command_async("Deploy Navigation", command, "navOutput.log")
    
    @Slot(str)
    def stopCommand(self, cmd_name):
        """Stop a running command by name."""
        if cmd_name in self._processes:
            process = self._processes[cmd_name]
            if process.poll() is None:  # Process is still running
                process.terminate()
                self.commandCompleted.emit(f"{cmd_name} stopped")
                self._node.get_logger().info(f"{cmd_name} stopped by user")


def main():
    # Initialize ROS 2
    rclpy.init()
    node = Ros2Node()

    # Define which topics you want to monitor
    monitored_topics = [
        "/fix",
        "/fix_velocity",
        "/odom",
        "/imu/data_raw",
        "/cmd_vel",
        "/scan",
    ]

    # Create Qt application
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    # Create and expose the topic model to QML
    model = TopicModel(node, monitored_topics)
    engine.rootContext().setContextProperty("topicModel", model)
    
    # Create and expose location bridge to QML
    location_bridge = LocationBridge(node)
    engine.rootContext().setContextProperty("locationBridge", location_bridge)
    
    # Create and expose command bridge to QML
    command_bridge = CommandBridge(node)
    engine.rootContext().setContextProperty("commandBridge", command_bridge)

    # Periodically refresh topics
    timer = QTimer()
    timer.timeout.connect(model.updateTopics)
    timer.start(1000)  # Update every 1 second
    model.updateTopics()

    # Spin ROS2 node in background
    ros_timer = QTimer()
    ros_timer.timeout.connect(lambda: rclpy.spin_once(node, timeout_sec=0))
    ros_timer.start(10)  # Spin every 10ms

    # Load QML UI
    engine.load("main.qml")
    if not engine.rootObjects():
        sys.exit(-1)

    # Run Qt event loop
    app.exec()

    # Cleanup
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()