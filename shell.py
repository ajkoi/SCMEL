import cmd
import classements


class MyShell(cmd.Cmd):
    intro = "Bienvenue dans le shell du SCMEL"
    prompt = "(SCMEL)"

    def do_nouveau_joueur(self, line):
        """Args: nom, prénom, crée un nouveau joueur"""
        args = line.split(" ")
        if len(args) > 2:
            print("Seulement le nom et le prénom")
        else:
            if classements.recup_joueur(*args):
                print("Ce joueur existe déjà.")
            else:
                classements.nouveau_joueur(*args)
                print(f"{*args} à été rajouté aux joueurs.")
        pass

    def do_exit(self, line):
        """
        Sortir du shell.
        """
        print("Au revoir")
        return True


if __name__ == "__main__":
    MyShell().cmdloop()
