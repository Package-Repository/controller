from inputs import get_gamepad
from inputs import devices
import inputs
import math
import threading
import numpy as np
import socket
import time

class Controller(object):
    print(inputs.devices.all_devices)
    MAX_TRIG_VAL = math.pow(2, 8)
    MAX_JOY_VAL = math.pow(2, 15)
    
    #ip configuration, matches sub
    PORT = 6969
    ADDRESS = "192.168.194.2"
    
    #do not change, thanks
    MAX_MOTOR_VAL = 100
    
    #set ~10 for in air, ~30 in water---------------------------------------------------------------
    REASONABLE_MOTOR_MAX = 10
    #-------------------------------------------------------------------------------------------------
    def __init__(self):

        self.motors = [
#	     LjoyX   LjoyY   RjoyX   RjoyY  Rtrig   Ltrig   Lbump   Rbump
            [ 0,      -1,     -1,  	0,     -1,  	1,	1,     -1], # motor 0 (top front left)
            [ 1,  	0,  	0,     -1,  	0,  	0,	0,	0], # motor 1 (bottom front left)
            [ 0,  	1,     -1,  	0,     -1,  	1,	1,     -1], # motor 2 (top back left)
            [ 1,  	0,  	0,     -1,   	0,  	0,	0,	0], # motor 3 (bottom back left)
            [ 0,  	1,  	1,  	0,     -1,  	1,     -1,	1], # motor 4 (top back right)
            [-1,  	0,  	0,     -1,  	0,  	0,	0,	0], # motor 5 (bottom back right)
            [ 0,      -1,  	1,  	0,     -1,  	1,     -1,	1], # motor 6 (top front right)
            [-1,  	0,  	0,     -1,     0,  	0,	0,	0]  # motor 7 (bottom front right)
        ]

        self.LeftJoystickY = 0
        self.LeftJoystickX = 0
        self.RightJoystickY = 0
        self.RightJoystickX = 0
        self.LeftTrigger = 0
        self.RightTrigger = 0
        self.LeftBumper = 0
        self.RightBumper = 0
        self.A = 0
        self.X = 0
        self.Y = 0
        self.B = 0
        self.LeftThumb = 0
        self.RightThumb = 0
        self.Back = 0
        self.Start = 0
        self.LeftDPad = 0
        self.RightDPad = 0
        self.UpDPad = 0
        self.DownDPad = 0
        self.input_list = []

        self._monitor_thread = threading.Thread(target=self._monitor_controller, args=())
        self._monitor_thread.daemon = True
        self._monitor_thread.start()

    def connect_to_socket(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.ADDRESS, self.PORT))
    
    def send_command(self, command):
        self.s.send(command.encode())

    def twosComplement(self, value, bitLength):
        if (value < 0):
            value = 255 - abs(value)
        return value

    def read(self): # return the buttons/triggers that you care about in this method
        # FIXME: make the triggers in L,R order, update motor values above 
        self.input_list = [self.LeftJoystickX, self.LeftJoystickY, self.RightJoystickX, self.RightJoystickY, self.RightTrigger, self.LeftTrigger, self.LeftBumper, self.RightBumper]
        thrust_list = []
        for motor in self.motors:
            thrust_list.append(int(Controller.REASONABLE_MOTOR_MAX * np.dot(motor, self.input_list)))

        command = ""
        for motor_value in thrust_list:
            motor_value = self.twosComplement(int(motor_value), 2)
            command += '{:02X}'.format(motor_value)
        
        time.sleep(.1)
        self.send_command(command)
        print(command)
        #send command to socket
        return command

    def _monitor_controller(self):
        while True:
            events = get_gamepad()
            for event in events:
                if event.code == 'ABS_Y':
                    self.LeftJoystickY = round(event.state / Controller.MAX_JOY_VAL, 2) # normalize between -1 and 1
                elif event.code == 'ABS_X':
                    self.LeftJoystickX = round(event.state / Controller.MAX_JOY_VAL, 2) # normalize between -1 and 1
                elif event.code == 'ABS_RY':
                    self.RightJoystickY = round(event.state / Controller.MAX_JOY_VAL, 2) # normalize between -1 and 1
                elif event.code == 'ABS_RX':
                    self.RightJoystickX = round(event.state / Controller.MAX_JOY_VAL, 2 ) # normalize between -1 and 1
                elif event.code == 'ABS_Z':
                    self.LeftTrigger = round(event.state / Controller.MAX_TRIG_VAL / 4, 2) # normalize between 0 and 1
                elif event.code == 'ABS_RZ':
                    self.RightTrigger = round(event.state / Controller.MAX_TRIG_VAL / 4, 2) # normalize between 0 and 1
                elif event.code == 'BTN_TL': #FIXME: not working (doesn't hold down)
                    print("Left Bumper")
                    self.LeftBumper = round(event.state / Controller.MAX_JOY_VAL, 2) # normalize between -1 and 1
                elif event.code == 'BTN_TR': #FIXME: not working (doesn't hold down)
                    print("Right Bumper")
                    self.RightBumper = round(event.state / Controller.MAX_JOY_VAL, 2) # normalize between -1 and 1
                elif event.code == 'BTN_SOUTH':
                    self.A = event.state
                elif event.code == 'BTN_NORTH':
                    self.Y = event.state #previously switched with X
                elif event.code == 'BTN_WEST':
                    self.X = event.state #previously switched with Y
                elif event.code == 'BTN_EAST':
                    self.B = event.state
                # elif event.code == 'BTN_THUMBL':
                #     self.LeftThumb = event.state
                # elif event.code == 'BTN_THUMBR':
                #     self.RightThumb = event.state
                # elif event.code == 'BTN_SELECT':
                #     self.Back = event.state
                # elif event.code == 'BTN_START':
                #     self.Start = event.state
                # elif event.code == 'BTN_TRIGGER_HAPPY1':
                #     self.LeftDPad = event.state
                # elif event.code == 'BTN_TRIGGER_HAPPY2':
                #     self.RightDPad = event.state
                # elif event.code == 'BTN_TRIGGER_HAPPY3':
                #     self.UpDPad = event.state
                # elif event.code == 'BTN_TRIGGER_HAPPY4':
                #     self.DownDPad = event.state




if __name__ == '__main__':
    joy = Controller()
    joy.connect_to_socket()
    while True:
        joy.read()
