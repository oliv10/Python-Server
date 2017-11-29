###Made by Oliver Scotten###
###Simple Command Server###
###Version 1.3###

###Imports###
import socket
from threading import *

###Defined Variables###
ver = 1.3
buffer = 1024
ip = ''
port = 6000
userList = []
commandsFile = open("commands.txt","r").read()
online = True
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

###Defined Functions###

###
# Setup Local Server IP and Port
def setup(ip,port):
    global server
    server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    server.bind((ip,port))
    server.listen(10)

###
# Checks string for valid command
# When adding commands, add name and description to commands.txt
def commands(data):

    command = data[:-2]

    if command == "/help" or command == "/h":
        return 0
    if command == "/close":
        return 1
    if command == "/shutdown":
        return 2

###
# Creates Client Connection
def client(connection, address):

    for u in userList:
        if u == connection:
            continue
        else:
            u.send(("\n" + str(address) + " Connected\n").encode())

    while True:

        try:

            connection.send("\nCommand: ".encode())

            data = connection.recv(buffer)
            data = data.decode()
            print(str(address) + " Sent: " + data)

            if commands(data) == 0:
                connection.sendall((commandsFile + "\n").encode())
            elif commands(data) == 1:
                connection.send("Closing Connection".encode())
                break
            elif commands(data) == 2:
                for u in userList:
                    if u == connection:
                        continue
                    else:
                        u.send("\nShutting Down Server\n".encode())
                        u.close()
                connection.close()
                global online
                online = False
                global server
                server.close()
                break
            else:
                for u in userList:
                    if u == connection:
                        continue
                    else:
                        u.send(("\n" + str(address) + " Sent: " + data + "\nCommand: ").encode())
        except:
            print("Crashed Connection")
            break

    print(str(address) + " Disconnected")
    try:
        userList.remove(connection)
    except:
        connection.close()
    connection.close()

###
# Main Startup
def main():
    global online
    setup(ip,port)
    while online:
        print("Waiting Connection")
        conn, addr = server.accept()
        conn.send("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n".encode())
        conn.send("Welcome to Oliver's Text Chat Server, make sure to check out the help menu using /h or /help.".encode())
        userList.append(conn)
        Thread(None,client,None,(conn,addr)).start()
        print(str(addr) + " Connected")

    server.close()

###Start Program###
main()
