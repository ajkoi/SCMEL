# SCMEL
Systeme de Classement et de Matchmaking par Elo du LIPPS

## Utiliser le shell:
```
python shell.py
```

## Commandes 
```
classement [clé du tri] [ordre]
```

[clé du tri] : argument optionnel pour trie en fonction d'une des colonnes (valeures : nom, prenom, bullet, nb_bullet, blitz, nb_blitz, rapide, nb_rapide)

[orde] : trier de manière croissante ou décroissante (valeures : croissant/decroissant)

Afficher le classement

```f
in_de_partie nom1 prenom1 nom2 prénom2 issue format
```

issue : 1 ou 0.5 ou 0, du point de vue du joueur 1 (1 est une victoire, 0.5 est un match nul et 0 est une défaite).

format: bullet ou rapide ou blitz.

Permet d'actualiser le classement et l'élo des joueurs

```
nouveau_joueur nom prenom
```

Crée un nouveau joueur si le nom et le prénom sont libre.
