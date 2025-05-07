#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool
from sensor_msgs.msg import Image
# Use zed_msgs.msg if your installation provides it, otherwise switch to zed_interfaces.msg
from zed_msgs.msg import ObjectsStamped  
import cv2
from cv_bridge import CvBridge, CvBridgeError
import threading
import smtplib
from email.message import EmailMessage

SENDER_EMAIL = "amigo_eppl@gmx.com"
RECEIVER_EMAIL_1 = "gabearod2@gmail.com"
RECEIVER_EMAIL_2 = "jcass358@gmail.com"
PASSWORD = "quaternion_kinematics" 

class PictureTaker(Node):
    def __init__(self):
        super().__init__('picture_taker')
        self.bridge = CvBridge()
        self.latest_image = None
        self.latest_objects = None  # Latest object detections
        self.display_lock = threading.Lock()
        self.take_picture_event = threading.Event()

        # Subscribe to the ZED camera's image topic.
        self.create_subscription(
            Image,
            "/zed/zed_node/rgb/image_rect_color",
            self.image_callback,
            10
        )

        # Subscribe to the object detection topic.
        self.create_subscription(
            ObjectsStamped,
            "/zed/zed_node/obj_det/objects",
            self.objects_callback,
            10
        )

        # Subscribe to the take_picture trigger.
        self.create_subscription(
            Bool,
            "take_picture",
            self.take_picture_callback,
            10
        )

        # Start the display loop in a separate thread.
        self.display_thread = threading.Thread(target=self.display_loop, daemon=True)
        self.display_thread.start()

        self.get_logger().info("PictureTaker node started")

    def image_callback(self, msg):
        with self.display_lock:
            self.latest_image = msg

    def objects_callback(self, msg):
        self.latest_objects = msg

    def take_picture_callback(self, msg):
        if msg.data:
            self.get_logger().info("Take picture trigger received.")
            self.take_picture_event.set()

    def display_loop(self):
        cv2.startWindowThread()
        while rclpy.ok():
            if self.take_picture_event.wait(timeout=0.1):
                with self.display_lock:
                    if self.latest_image is None:
                        self.get_logger().warn("No image received yet.")
                        self.take_picture_event.clear()
                        continue
                    try:
                        cv_image = self.bridge.imgmsg_to_cv2(self.latest_image, desired_encoding='bgr8')
                    except CvBridgeError as e:
                        self.get_logger().error(f"Image conversion error: {e}")
                        self.take_picture_event.clear()
                        continue

                human_detected = False
                # Process detected objects if available.
                if self.latest_objects is not None:
                    for obj in self.latest_objects.objects:
                        # Check if the detected object label is 'person'
                        if obj.label.lower() == "person":
                            human_detected = True
                            try:
                                # bounding_box_2d is a message with an array 'corners' containing 4 Keypoint2Di messages.
                                corners = obj.bounding_box_2d.corners
                                if len(corners) == 4:
                                    # Extract x and y from each corner's 'kp' field.
                                    xs = [corner.kp[0] for corner in corners]
                                    ys = [corner.kp[1] for corner in corners]
                                    x_min = int(min(xs))
                                    y_min = int(min(ys))
                                    x_max = int(max(xs))
                                    y_max = int(max(ys))
                                    # Draw the rectangle on the image.
                                    cv2.rectangle(cv_image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
                                else:
                                    self.get_logger().warn("Bounding box does not contain exactly 4 corners.")
                            except Exception as e:
                                self.get_logger().error(f"Error drawing bounding box: {e}")

                # Optionally display the image.
                cv2.imshow("Captured Image", cv_image)
                cv2.waitKey(1)
                self.get_logger().info("Picture displayed.")

                # Send email only if a human is detected.
                if human_detected:
                    self.send_email(cv_image, RECEIVER_EMAIL_1)
                    self.send_email(cv_image, RECEIVER_EMAIL_2)
                else:
                    self.get_logger().info("No human detected; email not sent.")

                self.take_picture_event.clear()
        cv2.destroyAllWindows()

    def send_email(self, cv_image, receiver_email):
        """Sends an email with an attached image."""
        msg = EmailMessage()
        msg["Subject"] = "AMIGO Diagnostic Report"
        msg["From"] = SENDER_EMAIL 
        msg["To"] = receiver_email
        msg.set_content("Hello! Here is an image captured by AMIGO Bot during autonomous operation.")

        ret, buffer = cv2.imencode('.jpg', cv_image)
        if not ret:
            self.get_logger().error("Failed to encode image")
            return
        image_bytes = buffer.tobytes()
        msg.add_attachment(image_bytes, maintype="image", subtype="jpeg", filename="captured_image.jpg")

        try:
            with smtplib.SMTP_SSL("mail.gmx.com", 465) as server:
                server.login(SENDER_EMAIL, PASSWORD)
                server.send_message(msg)
            self.get_logger().info("Email sent successfully!")
        except Exception as e:
            self.get_logger().error(f"Failed to send email: {e}")

def main(args=None):
    rclpy.init(args=args)
    node = PictureTaker()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Shutting down PictureTaker node.")
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
