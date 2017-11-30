import cmd as _cmd

class cmd(_cmd.Cmd):

    def __init__(self):

        prompt = 'CMD: '

        super.__init__(self)

    def send(self, args):
        if