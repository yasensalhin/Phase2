from std_msgs.msg import Int32
import rclpy
from rclpy.node import Node
from pathlib import Path

class Monitornode(Node):
    def __init__(self):
        super().__init__("Monitor")
        self.temp = 0
        self.hum = 0
        self.press = 0
        self.subscriber=self.create_subscription(Int32,'temp',self.call_temp_back,10)
        self.subscriber=self.create_subscription(Int32,'Humidity',self.call_hum_back,10)
        self.subscriber=self.create_subscription(Int32,'Pressure',self.call_press_back,10)
        self.create_timer(1 ,self.timer_callback)
        self.file_path =Path('output.txt')
    def call_temp_back(self,msg):
        self.temp=msg.data
    def call_hum_back(self,msg):
        self.hum=msg.data
    def call_press_back(self,msg):
        self.press=msg.data
    def timer_callback(self):
        msg = f"Temp = {self.temp}°C, Humidity = {self.hum}%, Pressure = {self.press} hPa\n"
        self.get_logger().info(msg)
        with self.file_path.open('a') as file:
            file.write(msg)
def main():
    rclpy.init()
    node = Monitornode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()