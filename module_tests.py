import subprocess
import socket

#line = 'ping -c 4 python.org'
#command = line.split(' ')


#process = subprocess.Popen(command, stdout=subprocess.PIPE, universal_newlines=True)

#while True:
#    output = process.stdout.readline()
#    print(output.strip())
#    # Do something else
#    return_code = process.poll()
#    if return_code is not None:
#        print('RETURN CODE', return_code)
#        # Process has finished, read rest of the output 
#        for output in process.stdout.readlines():
#            print(output.strip())
#        break
#input()

#subprocess.call("notepad.exe")
#victims = {}
#ip_server = "192.168.43.187"
#port_server = 1234
#i = 0

#sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#sock.bind((ip_server, port_server))
#sock.listen(10)
#while i<1:
#    victim, address_victim = sock.accept()
#    victims[address_victim] = victim
#    print(victims)
#    i +=1

#print(victims[address_victim])

#for b in victims:
#    print(b)

comm = subprocess.Popen(str("ipconfig"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
STDOUT, STDERR = comm.communicate()

#print(STDERR)

print(STDOUT)