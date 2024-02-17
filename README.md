# Controller

This code aims to control club robots through teleop

## Dependencies

This packages relies on a few other packages 

    - ROS2 joy_node
    - Mechatronics CAN Driver written by Connor Larmer
    - scion_types package with ROS2 types

## Running

To run the controller, there are three separate programs. The two dependencies binaries are included here in the package and can be run.
For the CAN Driver to find the scion_types dynamic library, you have to source the ROS2 shell script located at scion_types/install/setup.bash
This is assuming scion_types is built
