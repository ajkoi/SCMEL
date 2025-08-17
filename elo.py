def proba_de_gain(D):
    """
    Probabilité de gain en fonction de la différence de points elo entre les deux joueurs
    """
    return 1 / (1 + 10 ** (-D / 400))


def nouvel_elo(elo_actuel, proba_de_gain, resultat_de_la_partie, coeff):
    """
    Renvoie le nouvel elo du joueur.
    """
    return elo_actuel + coeff * (resultat_de_la_partie - proba_de_gain)
