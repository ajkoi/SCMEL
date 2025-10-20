# SCMEL
Systeme de Classement et de Matchmaking par Elo du LIPPS

## Utiliser le shell:
`python shell.py`

## Commandes 
`classement [clé du tri] [ordre]`
`fin_de_partie nom1 prenom1 nom2 prénom2 issue format`
        issue : 1 ou 0.5 ou 0, du point de vue du joueur 1 (1 est une victoire, 0.5 est un match nul et 0 est une défaite).
        format: bullet ou rapide ou blitz.
`nouveau_joueur nom prenom`
        Crée un nouveau joueur si le nom et le prénom sont libre.
