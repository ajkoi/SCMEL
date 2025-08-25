import math
import statistics
import classements

# min et max pour trouver les dates les plus récentes/anciennes


def min_dico(dico):
    dico_cle = tuple(dico.keys())
    min = dico[dico_cle[0]]
    for cle in dico_cle:
        if dico[cle] < min:
            min = dico[cle]
    return min


def max_dico(dico):
    dico_cle = tuple(dico.keys())
    max = dico[dico_cle[0]]
    for cle in dico_cle:
        if dico[cle] > max:
            max = dico[cle]
    return max


def f_gauss(x, s, mu):
    """gaussienne pour le matchmaking"""
    return (1 / (s * math.sqrt(2 * math.pi))) * math.e ** (-(1 / 2) * (x - mu) / s) ** 2


def recup_data_date_joueur(format):
    dico_date_j = {}
    tab_data = classements.text_to_tab("classements.csv")[
        1:
    ]  # recupère le classement entier pour avoir tt les joueurs

    for name in tab_data:
        dico_date_j[f"{name[0]} {name[1]}"] = "---"
        # crée un dico qui sera rempli petit à petit

    tab_matchs = classements.text_to_tab("matchs.log")
    for (
        date,
        joueurs,
        issues,
        format_match,
    ) in tab_matchs:  ### faudra faire gaffe si on rajoute le nb delo gagné
        print(format_match)
        if format == format_match:
            date_jeu = date[
                -3:
            ]  # coreespond à %j (c un nb entre 000 et 366) avec une petite correction quand on passera à  2026

            if date[:3] == 2026:
                date_jeu += 365

            j1, j2 = joueurs.split("-")
            print(j1, j2)
            if dico_date_j[j1] == "---":
                dico_date_j[j1] = (
                    date_jeu,
                    f"{j2}-{j1}",
                )  # date du dernier jeu + données du dernier adversaire, SI il n'en a pas eu
            if dico_date_j[j2] == "---":
                dico_date_j[j2] = date_jeu, f"{j2}-{j1}"

    return dico_date_j


def tab_date_normalise(format):
    dico_date_j = recup_data_date_joueur(
        format
    )  # reprend le dico d'avant, constitué de tuple de la date + du match
    min_date = min_dico(dico_date_j)
    max_date = max_dico(dico_date_j)

    dico_cle = dico_date_j.keys()  # joueurs
    for cle in dico_cle:
        if (
            dico_date_j[cle] == "---"
        ):  # si il n'a pas joué je lui donne la date la plus récente et ne lui attribue pas d'adversaire
            dico_date_j[cle] == max_date, 0
        print(max_date)
        dico_date_j[cle] = (
            int(math.fabs(int(dico_date_j[cle][0]) - int(max_date[0]))),
            dico_date_j[cle][1],
        )  # soustrait la date pour avoir en ensemble allant de O à max-min (tout est positif)

    return (
        dico_date_j  # dico tuple de "timedelta", du match avec comme cle le nom prenom
    )


def tab_date_coef(format):
    dico_date_j = tab_date_normalise(format)  # reprend le dico d'avant
    dico_cle = dico_date_j.keys()

    dico_coef_j = {}

    for cle in dico_cle:
        dico_coef_j[cle] = (
            f_gauss(
                x=dico_date_j[cle][0],
                s=1,
                mu=statistics.median([i[0] for i in dico_date_j.values()]),
            ),
            dico_date_j[cle][1],
        )

    return dico_coef_j  # dico (cle: nom prenom) coef determiné par f_gauss et le "timedelta" et le dernier match


############################    Choix des 2 joueurs   ###############################


# Calcul de la différence entre les elo ET renseignement de celui a l'elo le plus élevé


def diff_elo_joueur(j1: tuple, j2: tuple, format):  # format (nom, prenom)
    """
    j1,j2:tuples(nom, prénom)
    """
    elo_j1 = classements.recup_joueur(j1[0], j1[1])[format]
    elo_j2 = classements.recup_joueur(j2[0], j2[1])[format]

    if elo_j1 > elo_j2:
        max_elo = elo_j1
    else:
        max_elo = elo_j2

    return math.fabs(elo_j1 - elo_j2), max_elo


def min_sousmin(tab):
    """trouve les 2 minimums (regarde la seconde valeure)"""
    print(tab)
    min = tab[0][1]
    j_min = tab[0][0]
    sousmin = tab[0][1] if tab[1][1] < tab[0][1] else tab[1][1]
    j_sousmin = tab[0][0] if tab[1][1] < tab[0][1] else tab[1][0]

    for ind in range(len(tab)):
        if tab[ind][1] < min:
            sousmin = min
            j_sousmin = j_min
            min = tab[ind][1]
            j_min = tab[ind][0]
        if tab[ind][1] < sousmin and tab[ind][1] > min:
            sousmin = tab[ind][1]
            j_sousmin = tab[ind][0]
    return (j_min, min), (j_sousmin, sousmin)  # 2 tuples du joueur [0] avec son elo [1]


def Deux_choix_joueur(joueur: tuple, format):
    # elo_J = classements.recup_joueur(joueur[0], joueur[1])[format]

    tab_joueurs = classements.text_to_tab("classements.csv")[1:]

    tab_elo = []
    for info_joueur in (
        tab_joueurs
    ):  # tableau de tuple comprenant "nom prenom" et diff elo avec le joueur
        tab_elo += [
            (
                f"{info_joueur[0]} {info_joueur[1]}",
                diff_elo_joueur(
                    (info_joueur[0], info_joueur[1]),
                    (joueur[0], joueur[1]),
                    format,
                )[0],
            )
        ]

    J_min, J_sousmin = min_sousmin(tab_elo)

    return (
        f"{joueur}-{J_min[0]}",
        f"{joueur}-{J_sousmin[0]}",
    )  # 2match du joueur avec le format de base "j1-j2"


############################    Corélation entre Match/Coef/Double   ###############################


def pas_de_doublon(tab_match):
    tab_nv_match = []

    for match in tab_match:
        j1, j2 = match.split(
            "-"
        )  # separe le match avec les 2 joueurs pour reperer j1-j2 comme j2-j1
        for ind_match in range(len(tab_match)):
            if f"{j1}-{j2}" not in tab_nv_match and f"{j2}-{j1}" not in tab_nv_match:
                tab_nv_match += [
                    match
                ]  # si le match n'est pas ds ce nv tab alors il est inscrit
    return tab_nv_match


def verif_match(tab_match, tab_interdit):  # fonctionnement semblable a pas-de-doublon()
    tab_nv_match = []

    for match_interdit in tab_interdit:
        j1, j2 = match_interdit.split("-")
        for ind_match in range(len(tab_match)):  # 2 possibilités(qui sont les mêmes)
            if (
                f"{j1}-{j2}" != tab_match[ind_match]
                and f"{j2}-{j1}" != tab_match[ind_match]
            ):
                tab_nv_match += [tab_match[ind_match]]
    return tab_nv_match


def tout_match(format):
    tab_joueurs = classements.text_to_tab()[1:]  # tab des joueurs
    match = []
    dico_coef_J = tab_date_coef(format)  # dico joueur to coef, match interdit
    match_interdit = []

    for info_joueur in tab_joueurs:
        match1, match2 = Deux_choix_joueur(
            (info_joueur[1], info_joueur[2]), format
        )  # 2 options de match par joueur
        match += [match1, match2]  # rajouté à la liste

        match_interdit += [
            dico_coef_J[f"{info_joueur[1]} {info_joueur[2]}"][1]
        ]  # ajout du match interdit

    tab_match_valable = verif_match(match, match_interdit)
    tab_match_propre = pas_de_doublon(
        tab_match_valable
    )  # creation du tableau des matchs propre

    return tab_match_propre


def attribution_coef(tab_match, format):
    dico_coef_J = tab_date_coef(format)  # accès au tbleau des coefficients
    tab_tuple_coef_match = []

    for match in tab_match:
        j1, j2 = match.split("-")
        tab_tuple_coef_match += (
            match,
            dico_coef_J[j1][0] * dico_coef_J[j2][0],
        )  # tuple du match avec son coeff  /!\ ptet qu'on mettra une addition plutôt qu'une multiplication

    return tab_tuple_coef_match


def max_tab_ind1(tab):  # fonction de max pour trier les matchs
    max = tab[0][1]  # ca tri le [1] vu que le [0] c le match
    ind_max = 0
    for ind in range(len(tab)):
        if tab[ind][1] > max:
            max = tab[ind][1]
            ind_max = ind
    return ind_max  # ca renvoie l'indice


def classement_match(format):
    tab_tuple_coef_match = attribution_coef(tout_match(format), format)  # tab avec coef
    tab_match_copy = tab_tuple_coef_match.copy()
    classemt_match = []  # tab qui acceuillera les match classés/triés

    for i in range(
        len(tab_tuple_coef_match)
    ):  # c la boucle qui regarde le max ds le tab copié puis le supprim, etc
        ind_max = max_tab_ind1(tab_match_copy)
        classemt_match += tab_match_copy[ind_max]
        del tab_match_copy[ind_max]
        # faut faire attention je pense que ca fonctionne mais ptet que j'ai fais un mauvais calcul et donc ce n'est pas "tab_match_copy[ind_max]" mais  "tab_match_copy[ind_max-i]" qui faut del

    return classemt_match


def affich_classement(
    format,
):  # cette fonct est simple mais ca suffit pour l'instant si on veut faire un truc mieux on pourra le faire après
    print(classement_match(format))
