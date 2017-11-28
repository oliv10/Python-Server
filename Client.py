import cmd
import socket
from threading import *

s = None
buffer = 1024

class server(cmd.Cmd):

    # Closes connection to server
    def do_close(self, line):
        global s
        s.send("/close  ".encode())
        s.close()
        return True

    # Sends data to server
    def do_send(self, line):
        global s
        s.send(line.encode())

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

    # Quits the program
    def do_quit(self, line):
        exit(self)


Thread(None, client().cmdloop, None, ()).start()