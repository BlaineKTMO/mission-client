import rclpy
from rclpy.node import Node


class RN2(Node):
    def __init__(self):
        super().__init__('rn2')


def main(args=None):
    rclpy.init(args=args)

    rn2 = RN2()
    rclpy.spin(rn2)

    # On end
    rn2.destroy_node()
    rclpy.shutdown()
