###Made by Oliver Scotten###
###Simple Command Server###
###Version 1.4###

###Imports###
import socket
from threading import *

###Defined Variables###
ver = 1.4
buffer = 1024
ip = ''
port = 6000
userList = []
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

###Defined Functions###

###
# Setup Local Server IP and Port
def setup(ip,port):
    global server
    server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    server.bind((ip,port))
    server.listen(10)

def client(connection, address):

    while True:

        try:

            data = connection.recv(buffer)
            data = data.decode()

            if data == "/close  ":
                break

            print(str(address) + " Sent: " + data)

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
    setup(ip,port)
    print("Waiting for Initial Connection...")
    while True:
        conn, addr = server.accept()
        userList.append(conn)
        Thread(None,client,None,(conn,addr)).start()
        print(str(addr) + " Connected")

###Start Program###
main()
