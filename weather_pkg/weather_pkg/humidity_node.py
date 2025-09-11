from std_msgs.msg import Int32
from random import randint
import rclpy
from rclpy.node import Node

class HumidityNode(Node):
    def __init__(self):
        super().__init__("Humidity_node")
        self.publisher_node=self.create_publisher(Int32,'Humidity',10)
        self.create_timer(2,self.pub_callback)
    def pub_callback(self):
        msg=Int32()
        msg.data=randint(20,100)
        self.publisher_node.publish(msg)


def main():
    rclpy.init()
    node = HumidityNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()