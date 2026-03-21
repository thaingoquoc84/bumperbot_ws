#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
import time
from sensor_msgs.msg import Imu

class MyNode(Node):
    def __init__(self):
        super().__init__("imu_republisher_node")
        time.sleep(1)
        self.imu_pub_ = self.create_publisher(Imu, "imu_efk", 10)
        self.imu_sub_ = self.create_subscription(Imu, "imu", self.imuCallback, 10)
        
    def imuCallback(self, imu: Imu):
        imu.header.frame_id = "base_footprint_ekf"
        self.imu_pub_.publish(imu)
def main(args=None):
    rclpy.init(args=args)
    node = MyNode()
    rclpy.spin(node)
    rclpy.shutdown()
    
if __name__ == "__main__":
    main()