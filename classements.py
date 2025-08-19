import elo


def text_to_tab(file):
    with open(file) as fichier:
        text = fichier.read()
    lines = text.split(sep="\n")
    tab = [i.split(sep=",") for i in lines]
    return tab


def tab_to_file(tab, file):
    with open(file, "w") as fichier:
        for i in tab:
            print(i, sep=",", end="\n", file=fichier)


def recup_joueur(nom, prenom):
    tab = text_to_tab("classements.csv")
    for i in range(len(tab)):
        if tab[i][0] == nom and tab[i][1] == prenom:
            joueur = {
                "ligne": i,
                "nom": nom,
                "prenom": prenom,
                "bullet": tab[i][2],
                "nb_bullet": tab[i][3],
                "blitz": tab[i][4],
                "nb_blitz": tab[i][5],
                "rapide": tab[i][6],
                "nb_rapide": tab[i][7],
            }
            return joueur
    return ""


# TODO : faire la fonction pour modifier une colonne et faire la fn pour modifier après une partie
#


def changer_n_ieme_colonne(ligne, n, nv_val):
    tab = text_to_tab("classements.csv")
    tab[ligne][n] = nv_val
    tab_to_file(tab, "classements.csv")


def fin_de_game(j1, j2, issue, format):
    j1_nom, j1_prenom = j1.split(" ")
    j2_nom, j2_prenom = j2.split(" ")
    j1_infos = recup_joueur(j1_nom, j1_prenom)
    j2_infos = recup_joueur(j2_nom, j2_prenom)
