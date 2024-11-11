import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer

from mission_msgs.action import Mission

class RN2(Node):
    def __init__(self):
        super().__init__('rn2')

        self._mission_action_server = ActionServer(
                self,
                Mission,
                'mission',
                self.execute_callback
                )

    def execute_callback(self, goal_handle):
        self.get_logger().info("Recieved Goal")
        self.get_logger().info(f"Waypoint: {goal_handle.request.waypoint}")

        goal_handle.succeed()

        result = Mission.Result()
        result.finished = True

        return result

def main(args=None):
    rclpy.init(args=args)

    rn2 = RN2()
    rclpy.spin(rn2)

    # On end
    rn2.destroy_node()
    rclpy.shutdown()
