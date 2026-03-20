#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from bumperbot_msgs.srv import AddTwoInts

class MyNode(Node):
    def __init__(self):
        super().__init__("simple_service_server")
        
        self.server_ = self.create_service(AddTwoInts, "add_two_ints", self.serviceCallback)
        
    def serviceCallback(self, req, res):
        res.sum = req.a + req.b
        
        self.get_logger().info("Sum %d" % res.sum)
        
        return res
        
        
        
def main(args=None):
    rclpy.init(args=args)
    node = MyNode()
    rclpy.spin(node)
    rclpy.shutdown()
    
if __name__ == "__main__":
    main()