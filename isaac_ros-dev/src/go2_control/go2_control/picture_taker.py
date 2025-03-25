#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge, CvBridgeError
import threading
import smtplib
from email.message import EmailMessage

SENDER_EMAIL = "amigo_bot@gmx.com"
RECEIVER_EMAIL_1 = "gabearod2@gmail.com"
RECEIVER_EMAIL_2 = "rodrig43@my.erau.edu"
PASSWORD = "quaternion_kinematics" 

class PictureTaker(Node):
    def __init__(self):
        super().__init__('picture_taker')
        self.bridge = CvBridge()
        self.latest_image = None
        self.display_lock = threading.Lock()
        # Event used to trigger image display only when take_picture is True.
        self.take_picture_event = threading.Event()

        # Subscribe to the image topic from the ZED camera
        self.create_subscription(
            Image,
            "/zed/zed_node/rgb/image_rect_color",
            self.image_callback,
            10
        )

        # Subscribe to the take_picture topic
        self.create_subscription(
            Bool,
            "take_picture",
            self.take_picture_callback,
            10
        )

        # Start a separate thread for the OpenCV display loop
        self.display_thread = threading.Thread(target=self.display_loop, daemon=True)
        self.display_thread.start()

        self.get_logger().info("PictureTaker node started")

    def image_callback(self, msg):
        with self.display_lock:
            self.latest_image = msg

    def take_picture_callback(self, msg):
        if msg.data:
            self.get_logger().info("Take picture trigger received.")
            self.take_picture_event.set()

    def display_loop(self):
        # Optionally, start the window thread
        cv2.startWindowThread()
        while rclpy.ok():
            # Wait until the take_picture_event is set
            if self.take_picture_event.wait(timeout=0.1):
                with self.display_lock:
                    if self.latest_image is None:
                        self.get_logger().warn("No image received yet.")
                        self.take_picture_event.clear()
                        continue
                    try:
                        # Convert ROS Image to OpenCV image (BGR8 encoding)
                        cv_image = self.bridge.imgmsg_to_cv2(self.latest_image, desired_encoding='bgr8')
                    except CvBridgeError as e:
                        self.get_logger().error(f"Image conversion error: {e}")
                        self.take_picture_event.clear()
                        continue
                # Display the image once
                cv2.imshow("Captured Image", cv_image)
                self.send_email(cv_image, RECEIVER_EMAIL_1)
                self.send_email(cv_image, RECEIVER_EMAIL_2)
                # Wait a short moment to ensure the window updates
                cv2.waitKey(1)
                self.get_logger().info("Picture displayed.")
                # Clear the event so that we don't keep displaying continuously
                self.take_picture_event.clear()
        cv2.destroyAllWindows()

    def send_email(self, cv_image, receiver_email):
        """ Sends an email with an attached image. """

        # Initializing the email message
        msg = EmailMessage()
        msg["Subject"] = "AMIGO Diagnostic Report"
        msg["From"] = SENDER_EMAIL 
        msg["To"] = receiver_email
        msg.set_content("Hello! Here is an image captured by AMIGO Bot during autonomous operation.")

        # Encoding the image to a jpeg
        ret, buffer = cv2.imencode('.jpg', cv_image)
        if not ret:
            self.get_logger().error("Failed to encode image")
            return
        image_bytes = buffer.tobytes()
        msg.add_attachment(image_bytes, maintype="image", subtype="jpeg", filename="captured_image.jpg")

        # Try sendin the email
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
