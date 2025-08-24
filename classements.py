import elo
import time


def text_to_tab(file):
    with open(file) as fichier:
        text = fichier.read()
    lines = text.split(sep="\n")
    tab = [i.split(sep=",") for i in lines]
    return tab[:-1]


def tab_to_file(tab, file):
    with open(file, "w") as fichier:
        for i in tab:
            print(*i, sep=",", end="\n", file=fichier)


def recup_joueur(nom, prenom):
    tab = text_to_tab("classements.csv")
    for i in range(len(tab)):
        if tab[i][0] == nom and tab[i][1] == prenom:
            joueur = {
                "ligne": int(i),
                "nom": nom,
                "prenom": prenom,
                "bullet": int(tab[i][2]),
                "nb_bullet": int(tab[i][3]),
                "blitz": int(tab[i][4]),
                "nb_blitz": int(tab[i][5]),
                "rapide": int(tab[i][6]),
                "nb_rapide": int(tab[i][7]),
            }
            return joueur
    return ""


def changer_n_ieme_colonne(ligne, n, nv_val):
    tab = text_to_tab("classements.csv")
    tab[ligne][n] = nv_val
    tab_to_file(tab, "classements.csv")


def calcul_coeff(joueur, format):
    if int(joueur[format]) <= 2400 and int(joueur[f"nb_{format}"]) < 30:
        return 30
    elif int(joueur[format]) <= 2400:
        return 20
    else:
        return 10


def fin_de_game(j1, j2, issue, format):
    j1_nom, j1_prenom = j1.split(" ")
    j2_nom, j2_prenom = j2.split(" ")
    j1_infos = recup_joueur(j1_nom, j1_prenom)
    j2_infos = recup_joueur(j2_nom, j2_prenom)
    if format != "rapide" and format != "blitz" and format != "bullet":
        print("veuillez indiquer un format valide")
        print(format)
        return 0
    elif j1_infos == "" or j2_infos == "":
        print("veuillez indiquer un utilisateur éxistant")
        return 0
    else:
        j1_elo = j1_infos[format]
        j2_elo = j2_infos[format]
        j1_nv = elo.nouvel_elo(
            j1_elo,
            elo.proba_de_gain(int(j1_elo) - int(j2_elo)),
            issue,
            coeff=calcul_coeff(j1_infos, format),
        )  # a voir pour le coeff
        j2_nv = elo.nouvel_elo(
            j2_elo,
            elo.proba_de_gain(int(j2_elo) - int(j1_elo)),
            issue * -1 + 1,
            coeff=calcul_coeff(j2_infos, format),
        )  # a voir pour le coeff
        if format == "bullet":
            changer_n_ieme_colonne(j1_infos["ligne"], 2, j1_nv)
            changer_n_ieme_colonne(j2_infos["ligne"], 2, j2_nv)
            changer_n_ieme_colonne(j1_infos["ligne"], 3, j1_infos["nb_bullet"] + 1)
            changer_n_ieme_colonne(j2_infos["ligne"], 3, j2_infos["nb_bullet"] + 1)
        elif format == "blitz":
            changer_n_ieme_colonne(j1_infos["ligne"], 4, j1_nv)
            changer_n_ieme_colonne(j2_infos["ligne"], 4, j2_nv)
            changer_n_ieme_colonne(j1_infos["ligne"], 5, j1_infos["nb_blitz"] + 1)
            changer_n_ieme_colonne(j2_infos["ligne"], 5, j2_infos["nb_blitz"] + 1)
        elif format == "rapide":
            changer_n_ieme_colonne(j1_infos["ligne"], 6, j1_nv)
            changer_n_ieme_colonne(j2_infos["ligne"], 6, j2_nv)
            changer_n_ieme_colonne(j1_infos["ligne"], 7, j1_infos["nb_rapide"] + 1)
            changer_n_ieme_colonne(j2_infos["ligne"], 7, j2_infos["nb_rapide"] + 1)
    with open("matchs.log", "a+") as log:
        log.write(f"{time.strftime('%Y-%m-%d %j')},{j1}-{j2},{issue},{format}\n")
