import elo


def n_ieme_colonne(n, ligne):
    """
    Avoir l'information se situant dans la n ieme colonne d'une ligne
    """
    colonne = 0
    output = ""
    for i in range(len(ligne)):
        if ligne[i] == ",":
            colonne += 1
        elif colonne == n:
            output += ligne[i]
        else:
            continue
    return output


def recup_joueur(nom, prenom):
    with open("classements.csv") as classement:
        for i in classement:
            if n_ieme_colonne(0, i) == nom and n_ieme_colonne(1, i) == prenom:
                joueur = {
                    "nom": nom,
                    "prenom": prenom,
                    "bullet": n_ieme_colonne(2, i),
                    "nb_bullet": n_ieme_colonne(3, i),
                    "blitz": n_ieme_colonne(4, i),
                    "nb_blitz": n_ieme_colonne(5, i),
                    "rapide": n_ieme_colonne(6, i),
                    "nb_rapide": n_ieme_colonne(7, i),
                }
                return joueur
    return ""


# TODO : faire la fonction pour modifier une colonne et faire la fn pour modifier après une partie
#


def changer_n_ieme_colonne(ligne, n, nv_val):
    with open("classement.csv", mode="r") as classements:
        j = 0
        for i in classements:
            if j == ligne:
                
            j += 1
    pass


def fin_de_game(j1, j2, issue):
    pass
