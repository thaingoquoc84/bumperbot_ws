#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSDurabilityPolicy

class SimpleQoSPublisherNode(Node):
    def __init__(self):
        super().__init__("simple_qos_publisher")
        
        self.qos_profile_pub_ = QoSProfile(depth = 10)
        
        self.declare_parameter("reliability", "system_default")
        self.declare_parameter("durability", "system_default")
        
        reliability = self.get_parameter("reliability").get_parameter_value().string_value
        durability = self.get_parameter("durability").get_parameter_value().string_value
        
        if reliability == "best_effort":
            self.qos_profile_pub_.reliability = QoSReliabilityPolicy.BEST_EFFORT
            self.get_logger().info("[Reliability] : Best Effort")
            
        elif reliability == "reliable":
            self.qos_profile_pub_.reliability = QoSReliabilityPolicy.RELIABLE
            self.get_logger().info("[Reliability] : Reliable")
            
        elif reliability == "system_default":
            self.qos_profile_pub_.reliability = QoSReliabilityPolicy.SYSTEM_DEFAULT
            self.get_logger().info("[Reliability] : System Default")
            
        else:
            self.get_logger().error("Selected Reliability QoS: %s doesn't exists" % reliability)
            return
        
        if durability == "volatile":
            self.qos_profile_pub_.durability = QoSDurabilityPolicy.VOLATILE
            self.get_logger().info("[Durability] : Volatile")
            
        elif durability == "transient_local":
            self.qos_profile_pub_.durability = QoSDurabilityPolicy.TRANSIENT_LOCAL
            self.get_logger().info("[Durability] : Transient Local")
            
        elif durability == "system_default":
            self.qos_profile_pub_.durability = QoSDurabilityPolicy.SYSTEM_DEFAULT
            self.get_logger().info("[Durability] : System Default")
            
        else:
            self.get_logger().error("Selected Durability QoS: %s doesn't exists" % durability)
            return
        
        
        self.couter_ = 0
        self.frequency_ = 1.0
        self.pub_ = self.create_publisher(String, "chatter", self.qos_profile_pub_)
        self.timer_ = self.create_timer(self.frequency_, self.timer_Callback)
        
    def timer_Callback(self):
        msg = String()
        msg.data = "Hello ROS 2 - counter: %d " % self.couter_
        self.pub_.publish(msg)
        self.couter_ += 1 
def main(args=None):
    rclpy.init(args=args)
    node = SimpleQoSPublisherNode()
    rclpy.spin(node)
    rclpy.shutdown()
    
if __name__ == "__main__":
    main()