# -*- coding: utf-8 -*-
import numpy as np
import exo1, exo2, exo3, exo4

print("====== Projet MOGPL - Optimisation équitable ======")
print("                 2022 - 2023                       ")
print("             Barthélémy & Aymeric                  ")

print("\n====== Partie 1 - Linéarisation ======")
print("## Calcul des composantes de L(4,7,1,3,9,2) ##")
print(exo1.calculL([4, 7, 1, 3, 9, 2]))

print("\n## Résolution de l'exemple ##")
exo1.solveExemple()

print("\n==== Partie 2 - Partage équitable de biens indivisibles ====")
print("## Résolution des exemples ##")
exo2.solveExemple()

# Enlever les commentaires pour calculer et afficher le temps de résolution moyen
# print("\n## Temps de résolution moyenne du programme ##")
# print(exo2.temps([2, 5]))

print("\n==== Partie 3 - Sélection multicritère de projets ====")
print("## Résolution des exemples ##")
exo3.solveExemple()

# Enlever les commentaires pour calculer et afficher le temps de résolution moyen
# print("\n## Temps de résolution moyen du programme ##")
# print(exo3.temps([2, 5, 10], [5, 10, 15, 20], True))

print("\n==== Partie 4 - Recherche d'un chemin robuste dans un graphe ====")
print("## Résolution des plus courts chemins ##")
exo4.plusCourtsChemins()

print("\n## Calcul du chemin robuste  ##")
exo4.solveExemple()

# Enlever les commentaires pour calculer et afficher l'impact de la robustesse
# print("\n## Impact de W sur la robustesse ##")
# robustesse = exo4.temps(20, True)
# print(robustesse)
