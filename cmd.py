import cmd
import classements


class MyShell(cmd.cmd):
    intro = "Welcome to the SCMEL shell"
    prompt = "$"

    def hello(self, arg):
        name = arg.strip() or "stranger"
        print(name)
