#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String , Int16
import random

class MinimalPublisher(Node):
    def __init__(self):
        super().__init__('publisher_node')
        self.counter=10
        self.timer_ = self.create_timer(1.0, self.timer_callback) 
    def timer_callback(self):
        if self.counter==0:
            self.get_logger().info("Timer is Up!")
            return
        self.get_logger().info(str(self.counter))
        self.counter-=1



def main(args=None):
    rclpy.init(args=args)
    node = MinimalPublisher()
    rclpy.spin(node)
    rclpy.shutdown()
    node.destroy_node()

if __name__ == '__main__':
    main()
    