import socket
from threading import *
import cmd
from tkinter import *

ip = ''
port = 6000
buffer = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
online = False

def setup():
    global s
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((ip, port))
    s.listen(10)

class server(cmd.Cmd):

    def do_exit(self, line):
        global s
        s.close()
        return True

class main(cmd.Cmd):

    def do_server(self, line):
        serverCMD = server()
        serverCMD.prompt = self.prompt[:-2] + ':Server) '
        setup()
        serverCMD.cmdloop()

    def do_quit(self, line):
        exit(self)

Thread(None, main().cmdloop, None, ()).start()