import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import curses

class DualTeleop(Node):
    def __init__(self, stdscr):
        super().__init__('dual_teleop')

        
        self.pub1 = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.pub2 = self.create_publisher(Twist, '/turtle2/cmd_vel', 10)

        
        self.stdscr = stdscr
        curses.cbreak()
        self.stdscr.keypad(True)
        self.stdscr.nodelay(True)

        self.get_logger().info(
            "Controls: Arrow keys = Turtle1 | WASD = Turtle2 | Q = quit"
        )

        
        self.create_timer(0.1, self.key_loop)

    def key_loop(self):
        key = self.stdscr.getch()
        msg1 = Twist()
        msg2 = Twist()

        
        if key == curses.KEY_UP:
            msg1.linear.x = 2.0
        elif key == curses.KEY_DOWN:
            msg1.linear.x = -2.0
        elif key == curses.KEY_LEFT:
            msg1.angular.z = 2.0
        elif key == curses.KEY_RIGHT:
            msg1.angular.z = -2.0

        
        elif key in (ord('w'), ord('W')):
            msg2.linear.x = 2.0
        elif key in (ord('s'), ord('S')):
            msg2.linear.x = -2.0
        elif key in (ord('a'), ord('A')):
            msg2.angular.z = 2.0
        elif key in (ord('d'), ord('D')):
            msg2.angular.z = -2.0

        
        elif key in (ord('q'), ord('Q')):
            self.get_logger().info("Exiting teleop...")
            rclpy.shutdown()
            return

        if msg1.linear.x or msg1.angular.z:
            self.pub1.publish(msg1)
        if msg2.linear.x or msg2.angular.z:
            self.pub2.publish(msg2)


def main():
    import curses

    def run(stdscr):
        rclpy.init()
        node = DualTeleop(stdscr)
        try:
            rclpy.spin(node)
        except KeyboardInterrupt:
            pass
        finally:
            node.destroy_node()
            rclpy.shutdown()

    curses.wrapper(run)


if __name__ == "__main__":
    curses.wrapper(main)
