import client
from threading import *

if __name__ == '__main__':
    Thread(None, client.client().cmdloop, None, ()).start()