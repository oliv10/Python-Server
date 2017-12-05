###Made by Oliver Scotten###
###Simple Command Server###
###Version 1.1###

###Imports###
import cmd
import socket
from threading import *

###Defined Variables###
ver = 1.1
s = None
buffer = 1024

###Defined Classes and Functions###
class server(cmd.Cmd):

    def default(self, line):
        """OVERRIDE"""
        self.stdout.write('*** Unknown command: %s\n' % line)

    # Closes connection to server
    def do_close(self, line):
        global s
        s.send("/close  ".encode())
        s.close()
        return True

    # Help with close command
    def help_close(self):
        self.stdout.write("Closes connection to server.\n")

    # Sends data to server
    def do_send(self, line):
        global s
        s.send(line.encode())

    # Help with send command
    def help_send(self):
        self.stdout.write("Send message to server.\n")

class client(cmd.Cmd):

    def default(self, line):
        """OVERRIDE"""
        self.stdout.write('*** Unknown command: %s\n' % line)

    # Connects to a server with given IP and PORT
    def do_connect(self, line):
        global s
        try:
            try:
                ip, port = [str(x) for x in line.split()]
            except:
                self.stdout.write("Syntax Error\n")

            port = int(port)

            try:
                s = socket.socket()
                s.connect((ip,port))
                serverCMD = server()
                serverCMD.prompt = self.prompt[:-2] + ':Server) '
                serverCMD.cmdloop()
            except:
                self.stdout.write("Connection Refused\n")
        except:
            self.stdout.write("")

    # Help for connect command
    def help_connect(self):
        self.stdout.write("Connect to given IP and PORT.\n")

    # Prints the version of the program
    def do_version(self, line):
        self.stdout.write("Client Version " + str(ver) + "\n")

    # Help for version command
    def help_version(self):
        self.stdout.write("Version of program.\n")

    # Quits the program
    def do_quit(self, line):
        exit(self)

    # Help for quit command
    def help_quit(self):
        self.stdout.write("Quits program.\n")

###Start Program###
Thread(None, client().cmdloop, None, ()).start()
