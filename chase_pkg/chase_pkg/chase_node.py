import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import curses
import os
from turtlesim.msg import Pose
import random
from std_msgs.msg import Int32



class DualTeleop(Node):
    def __init__(self, stdscr):
        super().__init__('turtle_node')
        for i in range(1,4):

            x=random.uniform(0.0,11.0)
            y=random.uniform(0.0,11.0)

            os.system(f"ros2 service call /spawn turtlesim/srv/Spawn '{{x: {x}, y: {y}, theta: 0.0, name: \"enemy{i}\"}}'")

        self.pub1 = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.pub2 = self.create_publisher(Twist, '/enemy1/cmd_vel', 10)
        self.pub3 = self.create_publisher(Twist, '/enemy2/cmd_vel', 10)
        self.pub4 = self.create_publisher(Twist, '/enemy3/cmd_vel', 10)

        self.score_pub = self.create_publisher(Int32, '/score', 10)


        self.create_subscription(Pose,'/turtle1/pose',self.main_pose_callback,10)
        self.create_subscription(Pose,'/enemy1/pose',self.enemy1_pose_callback,10)
        self.create_subscription(Pose,'/enemy2/pose',self.enemy2_pose_callback,10)
        self.create_subscription(Pose,'/enemy3/pose',self.enemy3_pose_callback,10)

        self.score=0
        self.stdscr = stdscr
        curses.cbreak()
        self.stdscr.keypad(True)
        self.stdscr.nodelay(True) 
        self.get_logger().info("Controls: Arrow keys = Turtle1 | WASD = Turtle2 | q = quit")

        self.pos_main = None
        self.pos_enemy1 = None
        self.pos_enemy2 = None
        self.pos_enemy3 = None
        self.create_timer(0.05, self.key_loop)
    def main_pose_callback(self, msg): self.pos_main = msg
    def enemy1_pose_callback(self, msg): self.pos_enemy1 = msg
    def enemy2_pose_callback(self, msg): self.pos_enemy2 = msg
    def enemy3_pose_callback(self, msg): self.pos_enemy3 = msg

    def kill_respawn(self):
        positions=[self.pos_enemy1,self.pos_enemy2,self.pos_enemy3]
        for i,pos in enumerate(positions):
            if abs(self.pos_main.x-pos.x)<=0.5 and abs(self.pos_main.y-pos.y)<=0.5:
                self.score+=1
                msg = Int32()
                msg.data = self.score
                self.score_pub.publish(msg)

                print(f"Score: {self.score}", flush=True)

                
                x=random.uniform(0.0,11.0)
                y=random.uniform(0.0,11.0)

                os.system(f"ros2 service call /enemy{i+1}/teleport_absolute turtlesim/srv/TeleportAbsolute '{{x: {x}, y: {y}, theta: 0.0}}'")

    def key_loop(self):
        key = self.stdscr.getch()

        msg1 = Twist()

        if key == curses.KEY_UP:
            msg1.linear.x = 0.75
        elif key == curses.KEY_DOWN:
            msg1.linear.x = -0.75
        elif key == curses.KEY_LEFT:
            msg1.angular.z = 0.75
        elif key == curses.KEY_RIGHT:
            msg1.angular.z = -0.75

            
        elif key in [ord('q'), ord('Q')]:
            self.get_logger().info("Exiting teleop...")
            rclpy.shutdown()
            return

        if msg1.linear.x != 0.0 or msg1.angular.z != 0.0:
            self.pub1.publish(msg1)
            

        self.kill_respawn()


def main(stdscr):
    rclpy.init()
    node = DualTeleop(stdscr)
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()


def ros_main():
    curses.wrapper(main)

if __name__ == '__main__':
    ros_main()