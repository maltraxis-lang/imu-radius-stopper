import math
import rclpy

from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import Imu
from geometry_msgs.msg import Twist


class RadiusStopper(Node):

    def __init__(self):
        super().__init__('radius_stopper')

        self.declare_parameter('stop_radius', 10.0)
        self.stop_radius = self.get_parameter('stop_radius').value

        self.imu_sub = self.create_subscription(
            Imu,
            '/imu',
            self.imu_callback,
            qos_profile_sensor_data
        )

        self.cmd_pub = self.create_publisher(
            Twist,
            '/cmd_vel',
            10
        )

        self.timer = self.create_timer(
            0.1,
            self.control_loop
        )

        self.vx = self.vy = 0.0
        self.x = self.y = 0.0

        self.last_time = None
        self.stopped = False

    def imu_callback(self, msg: Imu):
        if self.stopped:
            return
        # TODO 1:
        # Compute dt from IMU timestamps.
        # Skip the first message.
        current_time = msg.header.stamp.sec + msg.header.stamp.nanosec / 1000000000
        if self.last_time is None:
            self.last_time = current_time 
            return
        dt = current_time - self.last_time  
        self.last_time = current_time
        if dt <= 0:
            return




        # TODO 2:
        # (Optional) Extract yaw from orientation
        # and rotate acceleration into world coordinates.
        qx = msg.orientation.x
        qy = msg.orientation.y
        qz = msg.orientation.z
        qw = msg.orientation.w

        numerator = 2*(qx*qy + qw*qz) 
        denominator = 1 - 2*(qy**2 + qz**2)

        yaw = math.atan2(numerator,denominator)

        ax = msg.linear_acceleration.x
        ay = msg.linear_acceleration.y
        az = msg.linear_acceleration.z

        ax_world = ax*math.cos(yaw) - ay*math.sin(yaw)
        ay_world = ax*math.sin(yaw) + ay*math.cos(yaw) 





        # TODO 3:
        # Integrate acceleration -> velocity -> position.
        self.vx = self.vx + ax_world*dt
        self.vy = self.vy + ay_world*dt
        self.x = self.x + self.vx*dt
        self.y = self.y + self.vy*dt


        

    def control_loop(self):

        cmd = Twist()

        r = math.hypot(self.x, self.y)

        if r >= self.stop_radius:
            self.stopped = True

        if self.stopped:
            cmd.linear.x = 0.0
        else:
            cmd.linear.x = 0.2

        self.cmd_pub.publish(cmd)

        self.get_logger().info(
            f'estimated r = {r:.2f} m'
        )


def main(args=None):

    rclpy.init(args=args)

    node = RadiusStopper()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()