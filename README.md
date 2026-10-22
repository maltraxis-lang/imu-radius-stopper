# IMU-Based Radius Stopper

## Project Overview

A ROS 2 Humble project that controls a TurtleBot3 Burger
in Gazebo using IMU-based position estimation.

The robot moves forward at 0.2 m/s and automatically
publishes zero velocity when its IMU-estimated radial
displacement reaches 10 metres.

## ROS 2 Topics

- `/imu` — IMU sensor readings for position estimation
- `/cmd_vel` — Velocity commands to control the robot
- `/odom` — Used only to evaluate the final stopping error

## Algorithm

1. Subscribe to IMU data.
2. Extract yaw from the IMU orientation quaternion.
3. Transform horizontal acceleration into world coordinates.
4. Integrate acceleration to estimate velocity.
5. Integrate velocity to estimate x and y displacement.
6. Calculate radial displacement:

   r = sqrt(x² + y²)

7. Stop the robot when r >= 10 m.
8. Continue publishing zero velocity after stopping.

## Experimental Results

- Target distance: 10.00 m
- Final IMU estimate: 10.05 m
- Odometry-based displacement: 4.58323 m
- Distance short of target: 5.41677 m
- Error relative to target: 54.17%

## Limitations

Double integration of raw IMU acceleration accumulates
sensor bias and noise, causing position estimation drift.

The robot successfully stops based on the IMU threshold,
but the estimated distance differs substantially from
the odometry reference.


## Algorithm

1. Subscribe to the /imu topic.
2. Read acceleration and orientation from the IMU.
3. Calculate yaw from the orientation quaternion.
4. Transform acceleration into world coordinates.
5. Integrate acceleration to estimate velocity.
6. Integrate velocity to estimate x and y position.
7. Calculate radial displacement:

   r = sqrt(x^2 + y^2)

8. If r >= 10 metres, publish zero velocity.
9. Keep the robot stopped and print the final estimate.

## ROS 2 Topics

- /imu: Sensor data used for position estimation.
- /cmd_vel: Controls the robot's movement.
- /odom: Used only for evaluating stopping accuracy.


## Experimental Results

Target radial displacement: 10.00 m

Final IMU-estimated displacement: 10.05 m

Starting odometry position:
x = 0.00006219 m
y = -0.00000456 m

Final odometry position:
x = 4.58329265 m
y = -0.00008984 m

Odometry-based displacement: 4.58323 m

Distance short of target: 5.41677 m

Error relative to target: 54.17%

## Discussion

The robot successfully detected the 10 m threshold
using IMU-based position estimation and issued a
stop command.

However, the odometry reference showed that the
robot had travelled only approximately 4.58 m.

This large difference occurs because integrating
raw IMU acceleration twice accumulates sensor bias
and numerical errors over time.

The experiment demonstrates that IMU-only dead
reck

## Build Instructions

Requirements:
- Ubuntu 22.04
- ROS 2 Humble
- Gazebo 11
- TurtleBot3 Burger

Build the package:

```bash
cd ~/ros2_ws
source /opt/ros/humble/setup.bash
colcon build --packages-select radius_stopper
source ~/ros2_ws/install/setup.bash
```

## Run Instructions

Terminal 1 - Start Gazebo:

```bash
source /opt/ros/humble/setup.bash
gzserver --verbose -s libgazebo_ros_init.so -s libgazebo_ros_factory.so
```

Terminal 2 - Spawn the robot:

```bash
source /opt/ros/humble/setup.bash
export TURTLEBOT3_MODEL=burger
ros2 run gazebo_ros spawn_entity.py \
  -entity burger \
  -file /opt/ros/humble/share/turtlebot3_gazebo/models/turtlebot3_burger/model.sdf \
  -x 0.0 -y 0.0 -z 0.01
```

Terminal 3 - Run the controller:

```bash
source /opt/ros/humble/setup.bash
source ~/ros2_ws/install/setup.bash
ros2 run radius_stopper radius_stopper
```

The robot moves forward until the IMU-estimated
radial displacement reaches 10 metres, then stops.
