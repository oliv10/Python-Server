###Made by Oliver Scotten###
###Simple Command Server###
###Version 1.5###

###Imports***
import cmd
import socket
from threading import *

###Defined Variables###
ver = '1.5.2'
buffer = 1024
ip = ''
port = 6000
userList = []
connectionList = []
socket_server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

###Defined Functions and Classes###

###
# Starts at the beginning to listen for incoming client connections
class listening(Thread):

    def run(self):
        global userList, connectionList, socket_server
        while True:
            conn, addr = socket_server.accept()
            userList.append(str(addr))
            connectionList.append(conn)
            client(conn,addr).start()

###
# Created when a client connects to the server and waits for that connections input
class client(Thread):

    def __init__(self, connection, address):
        Thread.__init__(self)
        self.connection = connection
        self.address = address
        self.setDaemon(True)

    def run(self):
        global userList, connectionList
        while True:
            try:
                data = self.connection.recv(buffer)
                data = data.decode()
                if data == "/close  ":
                    break
                msg = str(self.address) + ": " + str(data)
                server.send(server(), str(msg))
            except:
                server.send(server(), "Crashed Connection")
                break
        try:
            userList.remove(str(self.address))
            connectionList.remove(self.connection)
        except:
            self.connection.close()
        self.connection.close()

###
# The main user interface for the server
class server(cmd.Cmd):

    prompt = '(CMD:Server) '
    intro = 'Message Server: Version ' + str(ver)

    def send(cls, args):
        print('\nReceived: ' + str(args) + '\n' + cls.prompt)

    def preloop(self):
        global socket_server, ip, port
        socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        socket_server.bind((ip, port))
        socket_server.listen(10)
        w = listening()
        w.setDaemon(True)
        w.start()

    def postloop(self):
        global socket_server
        socket_server.close()

    def do_quit(self, args):
        raise SystemExit

    def help_quit(self):
        self.stdout.write("Quits the program and shuts down the server.\n")

    def do_userlist(self, args):
        global userList
        self.stdout.write("List of Connected Users:\n")
        self.stdout.write("========================\n")
        self.columnize(userList,80)

    def help_userlist(self):
        self.stdout.write("Prints a list of the connected users.\n")

    def do_message(self, args):
        try:
            pos = args[:1]
            msg = args[2:]
            conn = connectionList[int(pos)]
            conn.send(str(msg).encode())
        except:
            self.stdout.write("*** User does not exist.\n")

    def help_message(self):
        self.stdout.write("Send message to user in list.\n")

    def do_version(self, args):
        global ver
        self.stdout.write("Server Version " + str(ver) + '\n')

    def help_version(self):
        self.stdout.write("Version of Server.\n")