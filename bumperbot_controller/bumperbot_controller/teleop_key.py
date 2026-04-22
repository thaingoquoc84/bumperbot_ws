#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, TwistStamped

class TwistRelayNode(Node):
    def __init__(self):
        super().__init__("twist_relay")
        self.controller_sub_ = self.create_subscription(
            Twist,
            "/cmd_vel",
            self.controller_twist_callback,
            10
        )
        self.controller_pub_ = self.create_publisher(
            TwistStamped,
            "/bumperbot_controller/cmd_vel",
            10
        )
    
    def controller_twist_callback(self, msg):
        twist_stamped = TwistStamped()
        twist_stamped.header.stamp = self.get_clock().now().to_msg()
        twist_stamped.twist = msg
        self.controller_pub_.publish(twist_stamped)
        
        
def main(args=None):
    rclpy.init(args=args)
    node = TwistRelayNode()
    rclpy.spin(node)
    rclpy.shutdown()
    
if __name__ == "__main__":
    main()