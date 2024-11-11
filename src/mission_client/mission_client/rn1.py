import rclpy
from rclpy.node import Node

from std_msgs.msg import String

import requests


class RN1(Node):
    def __init__(self):
        super().__init__('rn1')
        self.string_pub = self.create_publisher(String, 'mission', 10)
        self.timer_period = 1
        self.timer = self.create_timer(self.timer_period, self.timer_callback)

    def timer_callback(self):
        response = requests.get('http://127.0.0.1:5000/api/mission').json()

        self.get_logger().info("Recieved json data")

        msg = String()
        msg.data = response["Waypoint"]


def main(args=None):
    rclpy.init(args=args)

    rn1 = RN1()
    rclpy.spin(rn1)

    # Upon ending
    rn1.destroy_node()
    rclpy.shutdown()


if __name__=='__main__':
    main()
