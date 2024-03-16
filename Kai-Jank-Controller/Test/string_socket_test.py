#connect to socket and send string command
import socket
import time

class StringTest:
    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 6969
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    def connect_to_socket(self):
        self.s.connect((self.host, self.port))
        return self.s
    
    def send_command(self, s, command):
        s.send(command.encode())
        return s
    
    def main(self):
        s = self.connect_to_socket()
        command = "0000000000000000"
        while True:
            time.sleep(.05)
            # self.connect_to_socket()
            print("sending command")
            s = self.send_command(s, command)
        s.close()
        return s
 
        
if __name__ == "__main__":
    test = StringTest()
    test.main()
