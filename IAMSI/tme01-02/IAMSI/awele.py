# -*- coding: utf-8 -*-

"""
Package: IAMSI
File: awele.py
Année: IAMSI - semestre 2 - 2022-2023, Sorbonne Université
"""

# - - - - - - - - - - - - - - - TYPES UTILISES
# POSITION : dictionnaire non vide qui contient différentes informations sur
#            une position, associées au nom de leur champ.
# COUP : valeur entière comprise entre 1 et le nombre de colonnes du tablier
#
#
# - - - - - - - - - - - - - - - INITIALISATION
def position_initiale(n, nb_graines=4):
    """int * int -> POSITION
    Hypothèse : n > 0
    
    Définit la position de départ pour n colonnes avec nb_graines dans chaque
    case. Par défaut : 4 graines dans chaque case.
    """
    position = dict()  # initialisation
    position["plateau"] = [nb_graines for k in range(0, 2 * n)] # on met les graines dans chaque case
    position["dimension"] = n  # le nombre de colonnes du plateau
    position["nb_total"] = 2 * n * nb_graines # nombre de graines total au début du jeu sur tout le plateau
    position["trait"] = "SUD"  # le joueur qui doit jouer : 'SUD' ou 'NORD'
    position["gain"] = {"SUD": 0, "NORD": 0}  # graines prises par chaque joueur
    return position


# - - - - - - - - - - - - - - - AFFICHAGE (TEXTE)
def affichage(position):
    """POSITION ->
    Affiche la position de façon textuelle.
    """
    print("* * * * * * * * * * * * * * * * * * * *")
    n = position["dimension"]
    buffercol = "colonnes:"
    for i in range(0, n):
        buffercol += "\t " + str(i + 1) + " "
    buffer = ""
    # print(buffer)
    print("\t\tNORD (prises: " + str(position["gain"]["NORD"]) + ")")
    print("< - - - - - - - - - - - - - - -")
    buffer = buffercol + "\n" + "        "
    for i in range(2 * n - 1, n - 1, -1):  # indices n..(2n-1) pour les cases NORD
        buffer += "\t[" + str(position["plateau"][i]) + "]"
    print(buffer)
    buffer = "        "
    for i in range(0, n):  # indices 0..(n-1) pour les cases SUD
        buffer += "\t[" + str(position["plateau"][i]) + "]"
    print(buffer)
    print(buffercol + "\n")
    print("- - - - - - - - - - - - - - - >")
    print("\t\tSUD (prises: " + str(position["gain"]["SUD"]) + ")")
    print("\n-> camp au trait: " + position["trait"] + "\n")


# - - - - - - - - - - - - - - - RECOPIE
import copy


def duplique(position):
    """POSITION -> POSITION
    Retourne une copie dupliquée de la position (qui peut être alors 
    modifié sans altérer l'originale).
    """
    leclone = dict()
    leclone["plateau"] = copy.deepcopy(position["plateau"])
    leclone["dimension"] = position["dimension"]
    leclone["nb_total"] = position["nb_total"]
    leclone["trait"] = position["trait"]
    leclone["gain"] = copy.deepcopy(position["gain"])
    return leclone


# - - - - - - - - - - - - - - - JOUE UN COUP
def joue_un_coup(position, coup):
    """POSITION * COUP -> POSITION
    Hypothèse : coup est correct.
    Cette fonction retourne la position obtenue une fois le coup joué.
    """
    nouvelle_pos = duplique(position)  # on duplique pour ne pas modifier l'original
    n = nouvelle_pos["dimension"]
    trait = nouvelle_pos["trait"]
    # on transforme coup en indice
    if trait == "SUD":
        indice_depart = coup - 1
    else:
        indice_depart = 2 * n - coup
    # retrait des graines de la case de départ
    nbGraines = nouvelle_pos["plateau"][indice_depart]
    nouvelle_pos["plateau"][indice_depart] = 0
    # on sème les graines dans les cases à partir de celle de départ
    indice_courant = indice_depart
    while nbGraines > 0:
        indice_courant = (indice_courant + 1) % (2 * n)
        if (indice_courant != indice_depart):  # si ce n'est pas la case de départ
            nouvelle_pos["plateau"][indice_courant] += 1  # on sème une graine
            nbGraines -= 1
    # la case d'arrivée est dans le camp ennemi ?
    if trait == "NORD":
        estChezEnnemi = indice_courant < n
    else:
        estChezEnnemi = indice_courant >= n
    # réalisation des prises éventuelles
    while estChezEnnemi and (nouvelle_pos["plateau"][indice_courant] in range(2, 4)):
        nouvelle_pos["gain"][trait] += nouvelle_pos["plateau"][indice_courant]
        nouvelle_pos["plateau"][indice_courant] = 0
        indice_courant = (indice_courant - 1) % (2 * n)
        if trait == "NORD":
            estChezEnnemi = indice_courant < n
        else:
            estChezEnnemi = indice_courant >= n
    # mise à jour du camp au trait
    if trait == "SUD":
        nouvelle_pos["trait"] = "NORD"
    else:
        nouvelle_pos["trait"] = "SUD"
    return nouvelle_pos
# - - - - - - - - - -
