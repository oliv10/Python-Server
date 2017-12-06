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

class connected(cmd.Cmd):

    def do_close(self, line):
        global s
        s.send("/close  ".encode())
        s.close()
        return True

    def help_close(self):
        self.stdout.write("Closes connection to server.\n")

    def do_send(self, line):
        global s
        s.send(line.encode())

    def help_send(self):
        self.stdout.write("Send message to server.\n")

###
# Main user interface for the Client
class client(cmd.Cmd):

    def do_quit(self, args):
        raise SystemExit

    def help_quit(self):
        print("Quits program.\n")

    def do_version(self, args):
        print("Client Version: " + str(ver) + "\n")

    def help_version(self):
        self.stdout.write("Version of client.\n")

    def do_connect(self, args):
        global s
        try:
            try:
                ip, port = [str(x) for x in args.split()]
            except:
                self.stdout.write("Syntax Error\n")

            port = int(port)

            try:
                s = socket.socket()
                s.connect((ip, port))
                serverCMD = connected()
                serverCMD.prompt = self.prompt[:-2] + ':Server) '
                serverCMD.cmdloop()
            except:
                self.stdout.write("Connection Refused\n")
        except:
            self.stdout.write("")