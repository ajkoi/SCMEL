import math
import classements


def recup_data_date_joueur():
    dico_date_j = {}
    tab_data = classements.text_to_tab("classements.csv")[1:]

    nb_joueur = len(tab_data)
    for name in tab_data:
        dico_date_j += {f"{name[1]} {name[2]}":0}
    
    tab_matchs = classements.text_to_tab("matchs.log")
    for date, joueurs,issues, formats in tab_matchs:
        j1,j2 = joueurs.split('-')
        if dico_date_j[j1] == 0:
            dico_date_j[j1] = date[-3:-1]
        if dico_date_j[j2] == 0:
            dico_date_j[j2] = date[-3:-1]




