import cmd
import socket
from threading import *

ver = 1.4
buffer = 1024
connected = False
s = None
response = ""
prev_response = None

class listening():

    def listen(self):
        global s, response
        while connected:
            try:
                text = s.recv(buffer)
                print("\nServer Sent: " + text.decode() + "\n" + client.prompt)
            except:
                pass
        if not connected:
            quit(0)

class client(cmd.Cmd):

    prompt = '(Cmd:Client) '

    def do_connect(self, args):
        global connected
        global s
        try:
            try:
                ip, port = [str(x) for x in args.split()]
            except SyntaxError as ERROR:
                self.stdout.write(ERROR)
            port = int(port)

            try:
                s = socket.socket()
                s.connect((ip,port))
                connected = True
                Thread(None, listening().listen, None, ()).start()
            except ConnectionRefusedError as ERROR:
                self.stdout.write(ERROR)
        except:
            self.stdout.write("Connection Error\n")

    def do_send(self, args):
        global s
        if connected:
            s.send(args.encode())
        else:
            pass

    def do_close(self, args):
        global s, connected
        if connected:
            s.send("/close  ".encode())
            s.close()
            connected = False
        else:
            pass

    def do_quit(self, args):
        quit(0)