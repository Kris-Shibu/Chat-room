import socket
import select
import sys
import time
import os
from colorama import Fore, init, Back
import random


init()


colors = [Fore.BLUE, Fore.CYAN, Fore.GREEN, Fore.LIGHTBLACK_EX, 
    Fore.LIGHTBLUE_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTGREEN_EX, 
    Fore.LIGHTMAGENTA_EX, Fore.LIGHTRED_EX, Fore.LIGHTWHITE_EX, 
    Fore.LIGHTYELLOW_EX, Fore.MAGENTA, Fore.RED, Fore.WHITE, Fore.YELLOW
]

def userKeyofWord(word):
	sum = 0
	flag = 0
	for i in word:
		if (i == '<'):
			flag = 1
		elif(i == '>'):
			flag = 0
		else:
			if(flag == 1):
				sum+= ord(i)
	sum = sum % 15
	return sum
		
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

IP_address = "127.0.0.1" # Setting the IP address of the client as local host
port = 12345 # Ports between 0-1024 are reserved, so choosing a port number outside the range

server.connect((IP_address, port))
print("Connected To server")
print("Welcome to the server, you can chat normally and if you wish to send a file type out <FILE> in the CLI and the client will go to file transfer mode")

user_id = input("Type user id: ") 
room_id = input("Type room id: ") #If a user wants to create/join any room he can enter it here

user_id = "<" + str(user_id) + ">"
client_color = colors[userKeyofWord(user_id)]

server.send(str.encode(user_id)) #Encodes the message into a string of format UTF-8
time.sleep(0.1)
server.send(str.encode(room_id))

while True:
    socket_list = [sys.stdin, server]#

    
    read_socket, write_socket, error_socket = select.select(socket_list, [], [])#select.select() unblocks a list when its being used

    for socks in read_socket:
        if socks == server:
            message = socks.recv(1024)#message is stored in the object message
            
          

            if str(message.decode()) == "FILE":#if the message recieves the word "FILE" the client gets ready to recieve the file
                file_name = socks.recv(1024).decode()
                lenOfFile = socks.recv(1024).decode()
                send_user = socks.recv(1024).decode()

                if os.path.exists(file_name):#deleting the duplicate
                    os.remove(file_name)

                #print("File name"+file_name+" Sent by"+end_user)
                print("File received")

                total = 0
                with open(file_name, 'wb') as file: #opens a new file
                    while str(total) != lenOfFile: 
                        data = socks.recv(1024) 
                        total = total + len(data)     
                        file.write(data) # data is written into the new file
                print("<" + str(send_user) + "> " + file_name + " sent")
                       
            else:
            	s_client_color = colors[userKeyofWord(message.decode())];	
            	print(s_client_color + message.decode())#prints the message on the console

        else:
            message = sys.stdin.readline() 

            if str(message) == "FILE\n": #if user enters "FILE",the client gets ready to send a file
                file_name = input("Enter the file name : ")
                server.send("FILE".encode())
                time.sleep(0.1)
                server.send(str("client_" + file_name).encode())#send file name
                time.sleep(0.1)
                server.send(str(os.path.getsize(file_name)).encode())#send file size
                time.sleep(0.1)

                file = open(file_name, "rb")
                data = file.read(1024)
                while data:
                    server.send(data)#send file data 1024 bytes at a time
                    data = file.read(1024)
                sys.stdout.write(client_color + "<You>")
                sys.stdout.write(client_color + "File sent successfully\n")
                sys.stdout.flush()

            else:
                server.send(message.encode())#sends text message 
                sys.stdout.write(client_color + "<You>")
                sys.stdout.write(client_color + message)
                sys.stdout.flush()#clears internal buffer of the file
server.close()


