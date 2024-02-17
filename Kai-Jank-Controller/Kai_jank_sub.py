import socket 
import pickle
import os


#create a socket to run commands
def create_socket():
    port = 6969
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", port))
    s.listen(5)
    return s

#get command from controller
def get_command(s):
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established.")
    command = clientsocket.recv(6969)
    return command

#run command
def run_command(command):
    if command == "KILL":
        print("KILL")
        #os.system("cansend can0 000#")
    else:
        print("cansend can0 010#" + command)
        #os.system("cansend can0 010#" + command)

#main function
def main():
    s = create_socket()
    command = get_command(s)
    while True:
        run_command(command)
        command = get_command(s)

if __name__ == "__main__":
    main()