import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class StatusListener(Node):

    def __init__(self):
        super().__init__("status_listener")

        self.subscription = self.create_subscription(
            String,
            "/camera/status",
            self.status_callback,
            10
        )

        self.get_logger().info(
            "Status listener started!"
        )

    def status_callback(self, msg):

        self.get_logger().info(
            f"Received: {msg.data}"
        )

def main(args = None):

    rclpy.init(args=args)
    node = StatusListener()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()