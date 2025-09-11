from std_msgs.msg import Int32
from random import randint
import rclpy
from rclpy.node import Node


class TempNode(Node):
    def __init__(self):
        super().__init__("temp_node")
        self.publisher_node=self.create_publisher(Int32,'temp',10)
        self.create_timer(1,self.pub_callback)
    def pub_callback(self):
        msg=Int32()
        msg.data=randint(15,40)
        self.publisher_node.publish(msg)
def main():
    rclpy.init()
    node = TempNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
