import os
import rclpy
from ament_index_python.packages import get_package_share_directory
import lewansoul_xarm


def shutdown():
    print('\nshutting down xArm...')


def ros_main(args=None):
    rclpy.init(args=args)
    #rclpy.init(args=sys.argv)


    # connect to xArm
    global controller # so we can shutdown
    controller = lewansoul_xarm.controller()

    pkg_path = get_package_share_directory('lewansoul_xarm')
    
    urdf_file = pkg_path + '/urdf/xArm.urdf'
    if not os.path.isfile(urdf_file):
        print('couldn\'t find file: ' + urdf_file + '. cartesian moves will be disabled')
        urdf_file = ''
    config_file = pkg_path + '/config/xArm-49770F673737-arm.json'
    arm = controller.add_arm("arm", config_file, urdf_file)
    arm.enable()
    arm.home()
    config_file = pkg_path + '/config/xArm-49770F673737-gripper.json'
    gripper = controller.add_arm("gripper", config_file)
    gripper.enable()
    gripper.home()


    controller_ros = lewansoul_xarm.controller_ros(controller)

    prev = controller_ros.get_clock().now()
    while rclpy.ok():
        try:
            rclpy.spin_once(controller_ros, timeout_sec=0.1)
            controller_ros.tick(prev)
            prev = controller_ros.get_clock().now()
        except KeyboardInterrupt:
            break

    controller_ros.destroy_node()
    controller.shutdown()
    rclpy.shutdown()

if __name__ == '__main__':
    ros_main()
