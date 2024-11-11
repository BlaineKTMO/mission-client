import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from rclpy.action.client import ClientGoalHandle

from std_msgs.msg import String
from mission_msgs.action import Mission
from action_msgs.msg import GoalStatusArray

import requests

class RN1(Node):
    def __init__(self):
        super().__init__('rn1')
        self.timer_period = 1
        self.timer = self.create_timer(self.timer_period, self.timer_callback)
        self._mission_client = ActionClient(self, Mission, 'mission')
        self.mission_client_status = 0

    def timer_callback(self):
        if self.mission_client_status == 0:
            response = requests.get('http://127.0.0.1:5000/api/mission').json()

            self.get_logger().info("Recieved json data")

            #msg = String()
            #msg.data = response["Waypoint"]

            goal_msg = Mission.Goal()
            goal_msg.waypoint = response['Waypoint']
            goal_msg.zone = response["Zone"]
            goal_msg.distance = response["Distance"]

            self._mission_client.wait_for_server()
            self._mission_client.send_goal_async(goal_msg, feedback_callback=self.goal_feedback_callback) \
                                                           .add_done_callback(self.goal_response_callback)

            self.get_logger().info("Sent goal")
            self.mission_client_status = 1
        else:
            self.get_logger().info("Currently running...")

    def goal_feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback

        response = requests.post("http://127.0.0.1:5000/api/mission_result", json={"result": False}) 

        self.get_logger().info(f"Distance to goal: {feedback.distance_to_goal}")

    def goal_response_callback(self, future):
        self.goal_handle_ : ClientGoalHandle = future.result()
 
        # Goal rejected
        if not self.goal_handle_.accepted:
            self.get_logger().info("Goal Rejected")
            return

        self.get_logger().info("Goal Accepted")

        self.goal_handle_.get_result_async().add_done_callback(self.goal_done_callback)

    def goal_done_callback(self, future):
        result = future.result().result
        self.mission_client_status = 0

        if result.finished:
            response = requests.post("http://127.0.0.1:5000/api/mission_result", json={"result": True}) 

        self.get_logger().info(f"Goal Reached: {result.finished}")


def main(args=None):
    rclpy.init(args=args)

    rn1 = RN1()
    rclpy.spin(rn1)

    # Upon ending
    rn1.destroy_node()
    rclpy.shutdown()


if __name__=='__main__':
    main()
