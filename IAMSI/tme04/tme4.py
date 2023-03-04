# -*- coding: utf-8 -*-
"""
IAMSI - TME4
Programmation SAT - Générateur de chamionnat
2022-2023

@author: Aymeric Delefosse
"""


def encodage(ne, nj, j, x, y):
    """Code une variable m_{j, x, y} par k.

    Parameters
    ----------
    ne : int
        Nombre d'équipes.
    nj : int
        Nombre de jours.
    j : int
        Jour.
    x : int
        Equipe jouant à domicile.
    y : int
        Equipe jouant à l'extérieur.

    Returns
    -------
    k : int
        Variable encodée.
    """
    return j * ne**2 + x * ne + y + 1


def decodage(k, ne):
    """Retrouve j, x et y à partir de k, ne.

    Parameters
    ----------
    k : int
        Variable encodée.
    ne : int
        Nombre d'équipes.

    Returns
    -------
    j : int
        Jour.
    x : int
        Equipe jouant à domicile.
    y : int
        Equipe jouant à l'extérieur.
    """
    y = (k - 1) % ne
    x = ((k - 1 - y) // ne) % ne
    j = (k - 1 - y - x * ne) // (ne * ne)
    return j, x, y


def au_moins_un(variables):
    """Renvoie une clause (au format DIMACS) correspondant à la contrainte
    "au moins une de ces variables est vraie".

    Parameters
    ----------
    variables : liste d'int
        Variables à encoder sous la contrainte de cardinalité "au moins 1".

    Returns
    -------
    clause : liste de str de taille (1,)
        Clause encodée sous la contrainte de cardinalité "au moins 1".
    """
    clause = [str(v) for v in variables] + ["0"]
    return [" ".join(clause)]


def au_plus_un(variables):
    """Renvoie une clause (au format DIMACS) correspondant à la contrainte
    "au plus une de ces variables est vraie".

    Parameters
    ----------
    variables : liste d'int
        Variables à encoder sous la contrainte de cardinalité "au plus 1".

    Returns
    -------
    clauses : liste de str
        Clauses encodées sous la contrainte de cardinalité "au plus 1".
    """
    clauses = []
    n = len(variables)
    for i in range(n):
        for j in range(i + 1, n):
            clauses.append(f"{-variables[i]} {-variables[j]} 0")
    return clauses


def au_plus_k(variables, k):
    """Renvoie une clause (au format DIMACS) correspondant à la contrainte
    "au plus k de ces variables est vraie".

    Parameters
    ----------
    variables : liste d'int
        Variables à encoder.
    k : int
        Limite.

    Returns
    -------
    clauses : liste de str
        Clauses encodées.
    """
    from itertools import combinations

    clauses = []
    n = len(variables)
    for i in range(k + 1, n + 1):
        for c in combinations(variables, i):
            clause = [str(-x) for x in c] + ["0"]
            clauses.append(" ".join(clause))
    return clauses


def au_moins_k(variables, k):
    """Renvoie une clause (au format DIMACS) correspondant à la contrainte
    "au moins k de ces variables est vraie".

    Parameters
    ----------
    variables : liste d'int
        Variables à encoder.
    k : int
        Limite.

    Returns
    -------
    liste de str
        Clauses encodées.
    """
    n = len(variables)
    neg_variables = [-x for x in variables]
    return au_plus_k(neg_variables, n - k)


def encoderC1(ne, nj):
    """Renvoie des contraintes (au format DIMACS) correspondant à la contrainte
    C1 : "chaque équipe ne peut jouer plus d'un match par jour".

    Indication : pour 3 équipes et 4 jours, cela génère 72 contraintes.

    Parameters
    ----------
    ne : int
        Nombre d'équipes.
    nj : int
        Nombre de jours.

    Returns
    -------
    clauses : liste de str
        Contraintes générées.
    """
    clauses = []
    for j in range(nj):
        for x in range(ne):
            # Contrainte "au plus 1" pour chaque équipe x et chaque jour j
            domicile = [encodage(ne, nj, j, x, y) for y in range(ne) if y != x]
            exterieur = [encodage(ne, nj, j, y, x) for y in range(ne) if y != x]
            clauses.extend(au_plus_un(domicile + exterieur))
    return clauses


def encoderC2(ne, nj):
    """Renvoie des contraintes (au format DIMACS) correspondant à la contrainte
    C2 : "sur la durée d'un championnat, chaque équipe doit rencontrer l'ensemble
    des autres équipes une fois à domicile et une fois à l'extérieur, soit
    exactement 2 matchs par équipe adverse".

    Indication : pour 3 équipes et 4 jours, cela génère 42 contraintes.

    Parameters
    ----------
    ne : int
        Nombre d'équipes.
    nj : int
        Nombre de jours.

    Returns
    -------
    clauses : liste de str
        Contraintes générées.
    """
    clauses = []
    for x in range(ne):
        for y in range(ne):
            if x != y:
                list_match = [encodage(ne, nj, j, x, y) for j in range(nj)]
                clauses.extend(au_moins_un(list_match))
                clauses.extend(au_plus_un(list_match))
    return clauses


def encoder(ne, nj):
    """Encode toutes les contraintes C1 et C2 dans un fichier 'championnat.cnf'.

    Parameters
    ----------
    ne : int
        Nombre d'équipes.
    nj : int
        Nombre de jours.

    Returns
    -------
    contraintes : liste de str
        Contraintes C1 et C2.
    """
    contraintes = encoderC1(ne, nj) + encoderC2(ne, nj)
    with open("championnat.cnf", "w") as f:
        # Ecrire l'en-tête du fichier DIMACS
        f.write(f"p cnf {ne**2 * nj - 1} {len(contraintes)}\n")
        # Ecrire les contraintes
        for contrainte in contraintes:
            f.write(contrainte + "\n")
    return contraintes


def decoder(output_file, ne, nj, team_names_file=None):
    """Traduit le modèle en un planning. Si le modèle est insatisfiable, renvoie
    None. Sinon, renvoie un dictionnaire.

    Parameters
    ----------
    output_file : str
        Nom du fichier généré par glucose.
    ne : int
        Nombre d'équipes.
    nj : int
        Nombre de jours.
    team_names_file : str, optionnel
        Nom du fichier contenant le nom des équipes.

    Returns
    -------
    planning : dict
        Planning du championnat.
        Les clés correspondent aux jours (0, nj - 1).
        Les items correspondent aux équipes devant jouer ce jour-là, sous la forme
        d'un dictionnaire {"Domicile": x, "Extérieur": y}.

    """
    # Ouvrir le fichier contenant les noms d'équipe
    if team_names_file is not None:
        with open(team_names_file, "r") as f:
            team_names = [line.strip() for line in f]
        assert len(team_names) == ne, "Le nombre d'équipes ne correspondent pas."

    # Ouvrir le fichier de sortie de glucose
    with open(output_file, "r") as f:
        output_lines = f.readlines()

    # Extraire le modèle s'il existe
    model = output_lines[0].split()

    # Si aucun modèle n'a été trouvé, il n'y a pas de solution
    if "UNSAT" in model:
        return None

    # Cas SAT : initialisation du planning sous forme de dictionnaire
    planning = {j: {"Domicile": "", "Extérieur": ""} for j in range(nj)}

    for literal in model:
        literal = int(literal)
        if literal > 0:
            j, x, y = decodage(literal, ne)
            if team_names_file is not None:
                x = team_names[x]
                y = team_names[y]
            planning[j]["Domicile"] = x
            planning[j]["Extérieur"] = y

    return planning


def affichage(planning):
    """Affiche  un planning de matchs sous la forme d'un tableau ASCII dans la console.

    Parameters
    ----------
    planning : dict
        Planning des matchs.

    Returns
    -------
    None (stdout)
        Affichage console.
    """
    if planning is None:
        print("Le problème posé n'a pas de solutions. :(")
    else:
        # Détermine la largeur maximale de chaque colonne
        column_lengths = {"Jour": 4}
        for row in planning.values():
            for column, value in row.items():
                column_lengths[column] = max(
                    column_lengths.get(column, 0), max(len(column), len(str(value)))
                )

        # Calcule la largeur totale de la table
        total_width = sum(column_lengths.values()) + len(column_lengths) * 3 + 1

        # Affiche le titre
        title = "Planning des matchs"
        print(f"\n{title:^{total_width}}")

        # Affiche la bordure supérieure du tableau
        headers = ["Jour"] + sorted(planning[0].keys())
        print(
            "+"
            + "+".join("-" * (column_lengths[column] + 2) for column in headers)
            + "+"
        )

        # Affiche le header
        print(
            "| "
            + " | ".join(f"{header:^{column_lengths[header]}}" for header in headers)
            + " |"
        )

        # Affiche le séparateur du header
        print(
            "+"
            + "+".join("-" * (column_lengths[column] + 2) for column in headers)
            + "+"
        )

        # Affiche chaque ligne
        for row_name, row in planning.items():
            row_values = [str(row_name + 1)]
            row_values.extend(str(value) for value in row.values())
            print(
                "| "
                + " | ".join(
                    f"{value:^{column_lengths[column]}}"
                    for column, value in zip(headers, row_values)
                )
                + " |"
            )

        # Affiche la bordure inférieure du tableau
        print(
            "+"
            + "+".join("-" * (column_lengths[column] + 2) for column in headers)
            + "+"
        )


def glucose(output=False):
    """Appel le solveur SAT glucose. Considére qu'il fait parti de l'environnement.
    Travaille dans le répertoire courant, à partir des fichiers générés à l'aide
    de la fonction `encoder`. Enregistre les résultats dans un fichier `output.txt`.
    """
    import subprocess

    cmd = "glucose championnat.cnf output.txt"
    subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL)


def optimisation(ne, nj_min, nj_max):
    """Trouve le nombre de jours minimal pour pouvoir planifier tous les matchs
    de championnat pour un nombre d'équipes donné. Utilise des appels SAT (glucose) de
    façon itérative. Si le solveur met plus de 10 secondes à traiter le problème,
    on passe à une itération suivante. Si la fonction ne renvoie rien, c'est que
    le problème est trop lourd pour être trouvé en 10 secondes (une solution existe
    forcément dans notre problème).

    Pour ne = 3, nj_min = 3, nj_max = 10, la fonction renvoie 6. Il faut donc prévoir au
    moins 6 jours pour organiser un championnat à 3 équipes.

    Parameters
    ----------
    ne : int
        Nombre d'équipes.
    nj_min : int
        Borne minimale de la recherche.
    nj_max : int
        Borne maximale de la recherche.

    Returns
    -------
    j : int
        Nombre de jours optimal.
    """
    import multiprocessing

    for j in range(nj_min, nj_max):
        encoder(ne, j)
        p = multiprocessing.Process(target=glucose, args=(True,))
        p.start()
        p.join(10)  # on attend 10 secondes
        if p.is_alive():  # si le processus est toujours vivant après 10 secondes
            print("timeout atteint...")
            p.terminate()  # on le termine
            continue  # on passe à l'itération suivante
        # sinon, c'est qu'il a fini. on regarde si le modèle est satisfiable, et si
        # c'est le cas, on renvoie j
        if decoder("optimisation.txt", ne, j) is not None:
            return j


if __name__ == "__main__":
    """Programme principal."""
    import os

    # Saisie
    ne = int(input("Saisir le nombre d'équipes : "))
    nj = int(input("Saisir le nombre de jours : "))
    teams = input(
        "Nom du fichier donnant le nom des équipes "
        + "(appuyer sur 'enter' s'il n'y en a pas) : "
    )
    janitor = input(
        "Voulez vous nettoyer les fichiers de travail à la fin du programme ?"
        + "(o/n, 'enter' pour passer)"
    )
    # Checks
    if teams == "":
        teams = None
    elif not os.path.isfile(teams):
        raise ValueError(f"Le fichier '{teams}' n'existe pas.")

    # Programme
    encoder(ne, nj)  # on encode
    glucose()  # on solve grâce à glucose
    planning = decoder("output.txt", ne, nj, teams)  # on décode le résultat
    affichage(planning)  # on affiche le planning

    if janitor.lower() in ("o", "oui"):
        os.remove("output.txt")
        os.remove("championnat.cnf")
