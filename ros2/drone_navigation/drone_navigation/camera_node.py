import cv2
import rclpy

from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from std_msgs.msg import String

class CameraNode(Node):
    def __init__(self):
        super().__init__("camera_node")

        self.publisher = self.create_publisher(
            Image,
            "/camera/image",
            10
        )

        self.bridge = CvBridge()

        self.camera = cv2.VideoCapture(0)

        if not self.camera.isOpened():
            self.get_logger().error(
                "Could not open camera."
            )

        self.timer = self.create_timer(
            0.033,
            self.publish_image
        )

        self.get_logger().info(
            "Camera node started!"
        )

    def publish_image(self):

        ret, frame = self.camera.read()

        if not ret:
            self.get_logger().warning(
                "Could not read camera frame."
            )
            return 
        
        image_msg = self.bridge.cv2_to_imgmsg(
            frame,
            encoding="bgr8"
        )

        self.publisher.publish(image_msg)

def main(args=None):
    rclpy.init(args=args)
    node = CameraNode()
    rclpy.spin(node)
    node.camera.release()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()