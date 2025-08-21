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
    for date, joueurs,issues, format_match in tab_matchs:
        if format == format_match:

            date_jeu = date[-3:-1]
            if date[:3] == 2026:
                date_jeu += 365

            j1,j2 = joueurs.split('-')
            if dico_date_j[j1] == "---":
                dico_date_j[j1] = date_jeu
            if dico_date_j[j2] == "---":
                dico_date_j[j2] = date_jeu

    return dico_date_j




def tab_date_normalise(format):
    dico_date_j = recup_data_date_joueur(format)
    min_date = min_dico(dico_date_j)
    max_date = max_dico(dico_date_j)

    dico_cle = dico_date_j.keys()
    for cle in dico_cle:
        if dico_date_j[cle] == "---":
            dico_date_j[cle] == min_date
        dico_date_j[cle] = int(math.fabs(dico_date_j[cle]-max_date))
    
    return dico_date_j


def tab_date_coef(format):
    dico_date_j = tab_date_normalise(format)
    dico_cle = dico_date_j.keys()

    dico_coef_j = {}

    for cle in dico_cle:
        dico_coef_j[cle] = f_gauss(x = dico_date_j[cle],
                                    s = 1,
                                    µ = statistics.median(dico_date_j.values()))
        
    return dico_coef_j