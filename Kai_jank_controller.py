from inputs import get_gamepad
import math
import threading
import numpy as np
import os

class Controller(object):
    MAX_TRIG_VAL = math.pow(2, 8)
    MAX_JOY_VAL = math.pow(2, 15)

    MAX_MOTOR_VAL = 100
    REASONABLE_MOTOR_MAX = 30
    def __init__(self):

        self.motors = [
            [ 0, -1, -1,  0,  0,  1],
            [ 1,  0,  0,  1,  1,  0],
            [ 0,  1, -1,  0,  0,  1],
            [ 1,  0,  0,  1, -1,  0],
            [ 0,  1,  1,  0,  0,  1],
            [-1,  0,  0,  1,  1,  0],
            [ 0, -1,  1,  0,  0,  1],
            [-1,  0,  0,  1, -1,  0]
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


    def read(self): # return the buttons/triggers that you care about in this methode
        
        self.input_list = [self.LeftJoystickX, self.LeftJoystickY, self.RightJoystickX, self.RightJoystickY, self.RightTrigger, self.LeftTrigger]
        thrust_list = []
        for motor in self.motors:
            thrust_list.append(int(Controller.REASONABLE_MOTOR_MAX * np.dot(motor, self.input_list)))


        command = "cansend can0 010#"
        for motor_value in thrust_list:
            command += '{:02X}'.format(abs(motor_value))
        
        os.system(command)
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
                elif event.code == 'BTN_TL':
                    self.LeftBumper = event.state
                elif event.code == 'BTN_TR':
                    self.RightBumper = event.state
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
    while True:
        print(joy.read())