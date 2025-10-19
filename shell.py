import cmd
import classements


class MyShell(cmd.Cmd):
    intro = "Bienvenue dans le shell du SCMEL"
    prompt = "(SCMEL)"

    def do_nouveau_joueur(self, line):
        """Args: nom, prénom, crée un nouveau joueur"""
        args = line.split(" ")
        if len(args) != 2:
            print("Seulement le nom et le prénom")
        else:
            if classements.recup_joueur(*args):
                print("Ce joueur existe déjà.")
            else:
                classements.nouveau_joueur(*args)
                print(f"{args[0]} {args[1]} à été rajouté aux joueurs.")
        pass

    def do_fin_de_partie(self, line):
        """
        Arguments : nom1, prenom1, nom2, prénom2, issue, format
        issue : 1 ou 0.5 ou 0, du point de vue du joueur 1 (1 est une victoire, 0.5 est un match nul et 0 est une défaite).
        format: bullet ou rapide ou blitz.
        """
        args = line.split(" ")
        if len(args) != 6:
            print("Mauvais nombre d'arguments")
        elif args[4] not in ["1", "0.5", "0"]:
            print("Mauvais argument pour l'issue du match")
        elif args[5] not in ["bullet", "blitz", "rapide"]:
            print("Mauvais argument pour le format du match")
        else:
            args[4] = int(
                args[4]
            )  # avoir un int, on vérifie maintenant car on est sur que c'est un integer
            joueur1 = classements.recup_joueur(*args[0:2])
            joueur2 = classements.recup_joueur(*args[2:4])
            if joueur1 == "":
                print("Le premier joueur n'est pas enregistré")
                return 0
            if joueur2 == "":
                print("Le deuxième joueur n'est pas enregistré.")
                return 0

            classements.fin_de_game(joueur1, joueur2, *args[4:])
            print("La fin de match à été enregistré.")
            print(
                f"Nouvel elo de {args[0]} {args[1]} : {classements.recup_joueur(*args[0:2])[args[5]]}."
            )
            print(
                f"Nouvel elo de {args[2]} {args[3]} : {classements.recup_joueur(*args[2:4])[args[5]]}."
            )

    def do_classement(self, line):
        tab = classements.text_to_tab("classements.csv")
        largeur = [0 for i in range(len(tab[0]))]
        for i in range(len(tab)):
            for j in range(len(tab[0])):
                if largeur[j] < len(str(tab[i][j])):
                    largeur[j] = len(str(tab[i][j]))
        for i in range(len(tab[0])):
            print(f"{tab[0][i]:{largeur[i] + 1}}", end="|")
        print()
        for i in range(len(tab[0])):
            print("".join(["-" for _ in range(largeur[i] + 1)]), end="|")
        for i in range(1, len(tab)):
            print()
            for j in range(len(tab[0])):
                print(f"{tab[i][j]:{largeur[j] + 1}}", end="|")
        print()

    def do_exit(self, line):
        """
        Sortir du shell.
        """
        print("Au revoir.")
        return True


if __name__ == "__main__":
    MyShell().cmdloop()
