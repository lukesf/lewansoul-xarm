#  Author(s):  Anton Deguet
#  Created on: 2020-04

# (C) Copyright 2020 Johns Hopkins University (JHU), All Rights Reserved.

# --- begin cisst license - do not edit ---

# This software is provided "as is" under an open source license, with
# no warranty.  The complete license can be found in license.txt and
# http://www.cisst.org/cisst/license.txt.

# --- end cisst license ---
import rclpy
import lewansoul_xarm

from rclpy.node import Node, ParameterDescriptor


class controller_ros(Node):
    """Simple arm API wrapping around ROS messages
    """

    # initialize the controller
    def __init__(self, controller):
        super(controller_ros, self).__init__('xarm_controller')

        self._controller = controller
        self._arms = []
        for arm in self._controller._arms:
            self._arms.append(lewansoul_xarm.arm_ros(arm,self))

        self.get_logger().info('Created node')



    def loop(self, rate):
        ros_rate = rclpy.Rate(rate)
        while not rclpy.is_shutdown():
            for arm in self._arms:
                arm.publish()
            ros_rate.sleep()

    def tick(self, previous_time):
        now = self.get_clock().now()
        dt = now - previous_time
        dt_secs = dt.nanoseconds / 1000000000

        self.get_logger().debug('tick')

        for arm in self._arms:
            arm.publish(now)

