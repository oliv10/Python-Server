###Made by Oliver Scotten###
###Simple Server Client###
###Version 1.3###

###Imports###
import cmd
import socket
from threading import *

###Defined Variables###
ver = 1.3
buffer = 1024
s = None

###Defined Functions and Classes###

###
# Started when the client successfully connects to server, listens for incoming messages
class listening(Thread):

    def run(self):
        global s
        while True:
            try:
                data = s.recv(buffer)
                data = data.decode()
                connected.send(connected(),str(data))
            except:
                pass

###
# CMD Loop changes to this when client has connected to a server successfully
class connected(cmd.Cmd):

    prompt = "(CMD:Server) "

    def preloop(self):
        l = listening()
        l.setDaemon(True)
        l.start()

    def send(cls, args):
        print("\nReceived: " + str(args) + "\n" + connected.prompt)

    def do_close(self, args):
        global s, connect
        s.send("/close  ".encode())
        s.close()
        return True

    def help_close(self):
        self.stdout.write("Closes connection to server.\n")

    def do_send(self, args):
        global s
        s.send(args.encode())

    def help_send(self):
        self.stdout.write("Send message to server.\n")

###
# Main user interface for the Client
class client(cmd.Cmd):

    intro = "Message Client: Version " + str(ver)
    prompt = "(CMD:Client) "

    def do_quit(self, args):
        raise SystemExit

    def help_quit(self):
        print("Quits program.\n")

    def do_version(self, args):
        global ver
        print("Client Version " + str(ver) + "\n")

    def help_version(self):
        self.stdout.write("Version of client.\n")

    def do_connect(self, args):
        global s
        ip = None
        port = None
        try:
            try:
                ip, port = [str(x) for x in args.split()]
            except:
                self.stdout.write("*** Syntax Error\n")

            port = int(port)

            try:
                s = socket.socket()
                s.connect((ip, port))
                serverCMD = connected()
                serverCMD.prompt = self.prompt[:-8] + "Server) "
                serverCMD.cmdloop()
            except:
                self.stdout.write("*** Connection Refused\n")
        except:
            self.stdout.write("")

    def help_connect(self):
        self.stdout.write("Connect to given IP and PORT.\n")