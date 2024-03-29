#!/usr/bin/env python3

import os
import rclpy
import fork_processes
import json
import numpy as np
from rclpy.node import Node
from sensor_msgs.msg import Joy
from can_client import Can_Client
from math_operations import normalize_ctrl_vals

#######################################################
""" 
    NODE CONTEXT
"""

CONTROLLER_NODE_NAME                    = "controller"
JOY_NODE_TOPIC_NAME                     = "/joy"
JOY_BINARY_NAME                         = "joy"
CONFIG_FILE_NAME                        = "config.json"
CAN_BINARY_NAME                         = "can_driver"
CAN_DRIVER_ARGS                         = [CAN_BINARY_NAME, "--ros-args", "-p", "can_bus_interface:='can0'", "-p", "do_module_polling:=false", "-p", "module_bitfield:=255"]
CONFIG_PATH                             = os.curdir + "/" + CONFIG_FILE_NAME
JOY_PATH                                = os.curdir + "/" + JOY_BINARY_NAME
CAN_PATH                                = os.curdir + "/" + CAN_BINARY_NAME
JOY_NODE_QUEUE_SIZE                     = 10
MAX_POWER                               = 30

""" 
    STICK_CONSTANTS
"""
INVERT                                  = -1
DEFAULT_1_OF_TRIGGER_BUTTONS            = 1
LEFT_STICK_HORIZONTAL_JOY_TOPIC_INDEX   = 0
LEFT_STICK_VERTICAL_JOY_TOPIC_INDEX     = 1
RIGHT_STICK_HORIZONTAL_JOY_TOPIC_INDEX  = 4
RIGHT_STICK_VERTICAL_JOY_TOPIC_INDEX    = 3
RIGHT_TRIGGER_JOY_TOPIC_INDEX           = 5
LEFT_TRIGGER_JOY_TOPIC_INDEX            = 2

""" 
    BUTTON CONSTANTS
"""
X_BUTTON                                = 0
O_BUTTON                                = 1
TRI_BUTTON                              = 2
SQUARE_BUTTON                           = 3
BUTTON_PRESSED                          = 1
BUTTON_RELEASED                         = 0
#######################################################


class Controller(Node):
    def __init__(self, thrust_mapper):
        super().__init__(CONTROLLER_NODE_NAME)
        self.thrust_mapper = thrust_mapper
        self.controller_subscription = self.create_subscription(
            Joy, 
            JOY_NODE_TOPIC_NAME, 
            self.controller_subscription_callback, 
            JOY_NODE_QUEUE_SIZE
        )
        self.buttons = [
            BUTTON_RELEASED,
            BUTTON_RELEASED,
            BUTTON_RELEASED,
            BUTTON_RELEASED
        ]
        self.button_functions = [
            Can_Client.kill_robot,
            Can_Client.all_clear,
            Can_Client.turn_on_light,
            Can_Client.turn_off_light
        ]
        self.can_client = Can_Client()
        self.can_client.set_bot_in_safe_mode()
        self.can_client.all_clear()

    def controller_subscription_callback(self, msg):
        yaw =   INVERT * msg.axes[LEFT_STICK_HORIZONTAL_JOY_TOPIC_INDEX]
        pitch =          msg.axes[RIGHT_TRIGGER_JOY_TOPIC_INDEX] - DEFAULT_1_OF_TRIGGER_BUTTONS
        roll =           msg.axes[LEFT_TRIGGER_JOY_TOPIC_INDEX] - DEFAULT_1_OF_TRIGGER_BUTTONS
        x =              msg.axes[RIGHT_STICK_HORIZONTAL_JOY_TOPIC_INDEX]
        y =     INVERT * msg.axes[RIGHT_STICK_VERTICAL_JOY_TOPIC_INDEX]
        z =     INVERT * msg.axes[LEFT_STICK_VERTICAL_JOY_TOPIC_INDEX]

        self.process_stick_inputs([yaw, pitch, roll, x, y, z])
        # self.process_button_inputs(msg.buttons[X_BUTTON], msg.buttons[O_BUTTON], msg.buttons[TRI_BUTTON], msg.buttons[SQUARE_BUTTON])

    def process_stick_inputs(self, ctrl_vals):
        thrusts = np.dot(self.thrust_mapper, normalize_ctrl_vals(ctrl_vals)) 
        motor_request = []
        for thrust in thrusts:
            motor_request.append(int(MAX_POWER*thrust))
        print(motor_request)
        self.can_client.make_motor_request(motor_request)
        
    def process_button_inputs(self, button_inputs):
        for i in range(len(button_inputs)):
            
            button_currently_pressed = button_inputs[i]
            button_recorded_as_pressed = self.buttons[i]

            if button_currently_pressed and not button_recorded_as_pressed:
                self.buttons[i] = BUTTON_PRESSED
                self.button_functions[i]()
            if not button_currently_pressed and button_recorded_as_pressed:
                self.buttons[i] = BUTTON_RELEASED


def determine_matrix():
    """ 
        Read Config file for correct Matrix
    """
    MATRIX_KEY = "matrix"
    READ_MODE  = 'r'
    with open(CONFIG_PATH, READ_MODE) as json_File :
        sample_load_file=json.load(json_File)
    return sample_load_file[sample_load_file[MATRIX_KEY]]


def main(args=None):
    """ 
        Fork Joy Node and Spin Controller Node
    """
    children = []
    fork_processes.create_child_program(child_pids=children, program=JOY_PATH, args=[JOY_BINARY_NAME]) # This needs to run on laptop for underwater vehicles
    fork_processes.create_child_program(child_pids=children, program=CAN_PATH, args=CAN_DRIVER_ARGS)
    rclpy.init(args=args)
    controller = Controller(thrust_mapper=determine_matrix())
    rclpy.spin(controller)
    controller.destroy_node()
    rclpy.shutdown()
    fork_processes.kill_processes(children_processes=children)

if __name__ == '__main__':
    main()
