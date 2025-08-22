import math
import statistics
import classements

def min_dico(dico):
    dico_cle = dico.keys()
    min = dico[dico_cle[0]]
    for cle in dico_cle:
        if dico[cle]<min:
            min = dico[cle]
    return min

def max_dico(dico):
    dico_cle = dico.keys()
    max = dico[dico_cle[0]]
    for cle in dico_cle:
        if dico[cle]>max:
            max = dico[cle]
    return max


def f_gauss(x, s, µ):
    return (1/(s*math.sqrt(2*math.pi)))*math.e^(-(1/2)*((x-µ)/s)**2)


def recup_data_date_joueur(format):
    dico_date_j = {}
    tab_data = classements.text_to_tab("classements.csv")[1:]

    nb_joueur = len(tab_data)
    for name in tab_data:
        dico_date_j += {f"{name[1]} {name[2]}":"---"}
    
    tab_matchs = classements.text_to_tab("matchs.log")
    for date, joueurs,issues, format_match in tab_matchs:   ### faudra faire gaffe si on rajoute le nb delo gagné
        if format == format_match:

            date_jeu = date[-3:-1]
            if date[:3] == 2026:
                date_jeu += 365

            j1,j2 = joueurs.split('-')
            if dico_date_j[j1] == "---":
                dico_date_j[j1] = date_jeu, f"{j2}-{j1}"
            if dico_date_j[j2] == "---":
                dico_date_j[j2] = date_jeu, f"{j2}-{j1}"

    return dico_date_j




def tab_date_normalise(format):
    dico_date_j = recup_data_date_joueur(format)
    min_date = min_dico(dico_date_j)
    max_date = max_dico(dico_date_j)

    dico_cle = dico_date_j.keys()
    for cle in dico_cle:
        if dico_date_j[cle] == "---":
            dico_date_j[cle] == min_date, 0
        dico_date_j[cle] = int(math.fabs(dico_date_j[cle][0]-max_date)), dico_date_j[cle][1]
    
    return dico_date_j


def tab_date_coef(format):
    dico_date_j = tab_date_normalise(format)
    dico_cle = dico_date_j.keys()

    dico_coef_j = {}

    for cle in dico_cle:
        dico_coef_j[cle] = f_gauss(x = dico_date_j[cle][0],
                                    s = 1,
                                    µ = statistics.median(dico_date_j.values())), dico_date_j[cle][1]
        
    return dico_coef_j


############################    Choix des 2 joueurs   ###############################



def diff_elo_joueur(j1:tuple, j2:tuple, format):    #format (nom, prenom)
    elo_j1 = classements.recup_joueur(j1[0], j1[1])[format]
    elo_j2 = classements.recup_joueur(j2[0], j2[1])[format]

    if elo_j1>elo_j2:
        max_elo = elo_j1
    else:
        max_elo = elo_j2

    return math.fabs(elo_j1-elo_j2), max_elo


def min_sousmin(tab):
    min = tab[0][1]
    j_min = tab[0][0]
    sousmin = tab[0][1] if tab[1][1]<tab[0][1] else tab[1][1]
    j_sousmin = tab[0][0] if tab[1][1]<tab[0][1] else tab[1][0]

    for ind in range(len(tab)):
        if tab[ind][1]<min:
            sousmin = min
            j_sousmin = j_min
            min = tab[ind][1]
            j_min = tab[ind][0]
        if tab[ind][1]<sousmin and tab[ind][1]>min:
            sousmin = tab[ind][1]
            j_sousmin = tab[ind][0]
    return (j_min, min), (j_sousmin, sousmin)


def Deux_choix_joueur(joueur:tuple, format):
    # elo_J = classements.recup_joueur(joueur[0], joueur[1])[format]

    tab_joueurs = classements.text_to_tab()

    for info_joueur in tab_joueurs:
        tab_elo += ((info_joueur[0], info_joueur[1]), diff_elo_joueur((info_joueur[0], info_joueur[1]), joueur, format)[0])

    J_min, J_sousmin = min_sousmin(tab_elo)

    return f"{joueur}-{J_min[0]}", f"{joueur}-{J_sousmin[0]}"



############################    Corélation entre Match/Coef/Double   ###############################

def pas_de_doublon(tab_match):
    tab_nv_match = []

    for match in tab_match:
        j1, j2 = match.split('-')
        for ind_match in range(len(tab_match)):
            if f"{j1}-{j2}" not in tab_nv_match and f"{j2}-{j1}" not in tab_nv_match:
                tab_nv_match += [match]
    return tab_nv_match


def verif_match(tab_match, tab_interdit):
    tab_nv_match = []

    for match_interdit in tab_interdit:
        j1, j2 = match_interdit.split('-')
        for ind_match in range(len(tab_match)):
            if f"{j1}-{j2}" != tab_match[ind_match] and f"{j2}-{j1}" != tab_match[ind_match]:
                tab_nv_match += [tab_match[ind_match]]
    return tab_nv_match



def tout_match(format):
    tab_joueurs = classements.text_to_tab()
    match = []
    dico_coef_J = tab_date_coef(format)
    match_interdit = []

    for info_joueur in tab_joueurs:
        match1, match2 = Deux_choix_joueur((info_joueur[1], info_joueur[2]), format)
        match += [match1,match2]

        match_interdit += [dico_coef_J[f"{info_joueur[1]} {info_joueur[2]}"][1]]
    
    tab_match_valable = verif_match(match, match_interdit)
    tab_match_propre = pas_de_doublon(tab_match_valable)

    return tab_match_propre

def attribution_coef(tab_match, format):
    dico_coef_J = tab_date_coef(format)
    tab_joueurs = classements.text_to_tab()
    tab_tuple_coef_match = []

    for match in tab_match:
        j1, j2 = match.split('-')
        tab_tuple_coef_match += (match, dico_coef_J[j1][0] * dico_coef_J[j2][0])
    
    return tab_tuple_coef_match


def max_tab_ind1(tab):
    max = tab[0][1]
    ind_max = 0
    for ind in range(len(tab)):
        if tab[ind][1]>max:
            max = tab[ind][1]
            ind_max = ind
    return ind_max


def classement_match(format):
    tab_tuple_coef_match = attribution_coef(tout_match(format), format)
    tab_match_copy = tab_tuple_coef_match.copy()
    classemt_match = []

    for i in range(len(tab_tuple_coef_match)):
        ind_max = max_tab_ind1(tab_match_copy)
        classemt_match += tab_match_copy[ind_max]
        del tab_match_copy[ind_max]
    
    return classemt_match

def affich_classement(format):
    print(classement_match(format))



