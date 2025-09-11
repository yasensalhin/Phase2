from std_msgs.msg import Int32
from random import randint
import rclpy
from rclpy.node import Node

class PressureNode(Node):
    def __init__(self):
        super().__init__("Pressure_node")
        self.publisher_node=self.create_publisher(Int32,'Pressure',10)
        self.create_timer(3,self.pub_callback)
    def pub_callback(self):
        msg=Int32()
        msg.data=randint(20,100)
        self.publisher_node.publish(msg)
def main():
    rclpy.init()
    node = PressureNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()