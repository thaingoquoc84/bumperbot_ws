#!/usr/bin/env python3
import time
import math
from enum import Enum

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Bool
from twist_mux_msgs.action import JoyTurbo
from rclpy.action import ActionClient
from visualization_msgs.msg import Marker, MarkerArray

class State(Enum):
    FREE = 0
    WARNING = 1
    DANGER = 2
    
class SafetyStopNode(Node):
    def __init__(self):
        super().__init__("safety_stop_node")
        self.declare_parameter("danger_distance", 0.2)
        self.declare_parameter("warning_distance", 0.6)
        self.declare_parameter("scan_topic", "scan")
        self.declare_parameter("safety_stop_topic", "safety_stop")
        
        self.danger_distance = self.get_parameter("danger_distance").get_parameter_value().double_value
        self.scan_topic = self.get_parameter("scan_topic").get_parameter_value().string_value
        self.safety_stop_topic = self.get_parameter("safety_stop_topic").get_parameter_value().string_value
        self.warning_distance = self.get_parameter("warning_distance").get_parameter_value().double_value
        
        self.laser_sub_ = self.create_subscription(LaserScan, self.scan_topic, self.laser_callback, 10)
        self.safety_stop_pub_ = self.create_publisher(Bool, self.safety_stop_topic, 10)
        
        self.decrease_speed_client_ = ActionClient(self, JoyTurbo, "joy_turbo_decrease")
        self.increase_speed_client_ = ActionClient(self, JoyTurbo, "joy_turbo_increase")
        self.zones_pub_ = self.create_publisher(MarkerArray, "zones", 10)
        
        self.state = State.FREE
        self.is_first_msg = True
        self.prev_state = State.FREE
        
        # while not self.decrease_speed_client_.wait_for_server(1.0) and rclpy.ok:
        #     self.get_logger().warn("Action /joy_turbo_decrease not available! Waiting..")
        #     time.sleep(2.0)
            
        # while not self.increase_speed_client_.wait_for_server(1.0) and rclpy.ok:
        #     self.get_logger().warn("Action /joy_turbo_increase not available! Waiting..")
        #     time.sleep(2.0)
            
        self.zones = MarkerArray()
        waring_zone = Marker()
        waring_zone.id = 0
        waring_zone.type = Marker.CYLINDER
        waring_zone.action = Marker.ADD
        waring_zone.scale.z = 0.01
        waring_zone.scale.x = self.warning_distance * 2
        waring_zone.scale.y = self.warning_distance * 2
        waring_zone.color.r = 1.0
        waring_zone.color.g = 0.984
        waring_zone.color.b = 0.0
        waring_zone.color.a = 0.5
        
        danger_zone = Marker()
        danger_zone.id = 1
        danger_zone.type = Marker.CYLINDER
        danger_zone.action = Marker.ADD
        danger_zone.scale.z = 0.01
        danger_zone.scale.x = self.danger_distance * 2
        danger_zone.scale.y = self.danger_distance * 2
        danger_zone.color.r = 1.0
        danger_zone.color.g = 0.0
        danger_zone.color.b = 0.0
        danger_zone.color.a = 0.5
        danger_zone.pose.position.z = 0.01
        
        self.zones.markers = [waring_zone, danger_zone]
        
        
    def laser_callback(self, msg: LaserScan):
        self.state = State.FREE
        
        for range_value in msg.ranges:
            if not math.isinf(range_value) and range_value <= self.danger_distance:
                self.state = State.DANGER
                break
            
        if self.state != self.prev_state:
            is_safety_stop = Bool()
            
            if self.state == State.WARNING:
                is_safety_stop.data = False
                self.decrease_speed_client_.send_goal_async(JoyTurbo.Goal())
                self.zones.markers[0].color.a = 1.0
                self.zones.markers[1].color.a = 0.5
            
            elif self.state == State.DANGER:
                is_safety_stop.data = True
                self.zones.markers[0].color.a = 1.0
                self.zones.markers[1].color.a = 1.0
            
            elif self.state == State.FREE:
                is_safety_stop.data = False
                self.increase_speed_client_.send_goal_async(JoyTurbo.Goal())
                self.zones.markers[0].color.a = 0.5
                self.zones.markers[1].color.a = 0.5
            
            self.prev_state = self.state
            self.safety_stop_pub_.publish(is_safety_stop)
            
        if self.is_first_msg:
            for zone in self.zones.markers:
                zone.header.frame_id = msg.header.frame_id
                
            self.is_first_msg = False
            
        self.zones_pub_.publish(self.zones)
        
        
def main(args=None):
    rclpy.init(args=args)
    node = SafetyStopNode()
    rclpy.spin(node)
    rclpy.shutdown()
    
if __name__ == "__main__":
    main()