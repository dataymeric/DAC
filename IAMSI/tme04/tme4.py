# -*- coding: utf-8 -*-
"""
IAMSI - TME4
Programmation SAT - Générateur de championnat
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

    Examples
    --------
    >>> encodage(3, 4, 1, 0, 1)
    11
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

    Examples
    --------
    >>> decodage(11, 3)
    (1, 0, 1)
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

    Examples
    --------
    >>> variables = [1, 2, 3]
    >>> au_moins_un(variables)
    ['1 2 3 0']
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

    Examples
    --------
    >>> variables = [1, 2, 3]
    >>> au_plus_un(variables)
    ['-1 -2 0', '-1 -3 0', '-2 -3 0']
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

    Examples
    --------
    >>> variables = [1, 2, 3]
    >>> au_plus_k(variables, 2)
    ['-1 -2 -3 0']

    On peut vérifier que cette contrainte est satisfaite lorsque 1 ou 2 (mais
    pas 3) variables sont vraies (au plus 2).
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

    Examples
    --------
    >>> variables = [1, 2, 3]
    >>> au_moins_k(variables, 2)
    ['1 2 0', '1 3 0', '2 3 0', '1 2 3 0']

    On peut vérifier que ces contraintes de cardinalités ne sont satisfaites
    que si 2 ou 3 (mais pas 1) variables sont vraies (au moins 2).
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


def encoderC3(ne, nj, pext=50, pdom=40):
    """Renvoie des contraintes (au format DIMACS) correspondant aux contraintes
    des matchs le dimanche.
    On considère que le dimanche est le deuxième jour de la semaine (chiffres impairs).

    Parameters
    ----------
    ne : int
        Nombre d'équipes.
    nj : int
        Nombre de jours.
    pext : int, default=50
        Pourcentage de matchs à l'extérieur.
    pdom : int, default=40
        Pourcentage de matchs à domicile.

    Returns
    -------
    clauses : liste de str
        Contraintes générées.
    """
    kext = int((ne - 1) * 2 * pext / 100)
    kdom = int((ne - 1) * 2 * pdom / 100)
    clauses = []
    for x in range(ne):
        for y in range(ne):
            if x != y:
                # tous les matchs à domicile joués le dimanche
                domicile = [encodage(ne, nj, j, x, y) for j in range(1, nj, 2)]
                clauses.extend(au_moins_k(domicile, kdom))
                # tous les matchs à l'extérieur joués le dimanche
                exterieur = [encodage(ne, nj, j, y, x) for j in range(1, nj, 2)]
                clauses.extend(au_moins_k(exterieur, kext))
    return clauses


def encoderC4(ne, nj):
    """Renvoie des contraintes (au format DIMACS) correspondant aux contraintes
    des matchs consécutifs.

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
            domicile = [encodage(ne, nj, j, x, y) for y in range(ne) if y != x]
            clauses.extend(au_plus_k(domicile, 2))
            exterieur = [encodage(ne, nj, j, y, x) for y in range(ne) if y != x]
            clauses.extend(au_plus_k(exterieur, 2))
    return clauses


def encoder(ne, nj, extension=False):
    """Encode toutes les contraintes C1 et C2 dans un fichier 'championnat.cnf'.

    Parameters
    ----------
    ne : int
        Nombre d'équipes.
    nj : int
        Nombre de jours.
    extension : bool, optional
        Rajoute les contraintes afin d'étendre le problème avec l'équilibrage
        des déplacements et des week-ends.

    Returns
    -------
    contraintes : liste de str
        Contraintes C1 et C2.
    """
    contraintes = encoderC1(ne, nj) + encoderC2(ne, nj)
    if extension:
        contraintes.extend(encoderC3(ne, nj) + encoderC4(ne, nj))
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
        d'un dictionnaire et de listes (car plusieurs matchs peuvent avoir lieu
        le même jour !) {"Domicile": [x_1, x_2, ...], "Extérieur": [y_1, y_2, ...]}.
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
    planning = {j: {"Domicile": [], "Extérieur": []} for j in range(nj)}

    for literal in model:
        literal = int(literal)
        if literal > 0:
            j, x, y = decodage(literal, ne)
            if team_names_file is not None:
                x = team_names[x]
                y = team_names[y]
            planning[j]["Domicile"].append(x)
            planning[j]["Extérieur"].append(y)

    return planning


def affichage(planning):
    """Affiche un planning de matchs sous la forme d'un tableau ASCII dans la console.

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
        column_lengths = {"Jour": len("Jour")}
        for row in planning.values():
            for column, values in row.items():
                if values:  # cas liste vide
                    column_lengths[column] = max(
                        column_lengths.get(column, 0),
                        len(column),
                        max(len(str(value)) for value in values),
                    )
                else:
                    column_lengths[column] = max(
                        column_lengths.get(column, 0), len(column)
                    )

        # Calcule la largeur totale de la table
        total_width = sum(column_lengths.values()) + len(column_lengths) * 3 + 1

        # Affiche le titre
        title = "Planning des matchs"
        print(f"\n{title:^{total_width}}")

        # Affiche la bordure supérieure du tableau
        columns = sorted(planning[0].keys())
        headers = ["Jour"] + columns
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
            row_length = max(len(value) for value in row.values())
            for i in range(row_length):
                row_values = [str(row_name)]
                for column in columns:
                    if i < len(row[column]):
                        value = row[column][i]
                        row_values.append(str(value))
                    else:
                        row_values.append("")
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


def glucose():
    """Appel le solveur SAT glucose. Considére qu'il fait parti de l'environnement
    (e.g. /usr/local/bin/). Travaille dans le répertoire courant, à partir des fichiers
    générés à l'aide de la fonction `encoder`. Enregistre les résultats dans un fichier
    `planning.cnf`.
    """
    import subprocess

    cmd = "glucose championnat.cnf planning.cnf"
    subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL)


def optimisation(ne, nj_min, nj_max, timeout=10):
    """Trouve le nombre de jours minimal pour pouvoir planifier tous les matchs
    de championnat pour un nombre d'équipes donné. Utilise des appels SAT (glucose) de
    façon itérative. Si le solveur met plus de 10 secondes à traiter le problème,
    on passe à une itération suivante. Si la fonction ne renvoie rien, c'est que
    le problème est trop lourd pour être trouvé en 10 secondes (une solution existe
    forcément dans notre problème). Le programme dure au maximum (nj_max - nj_min) * 10
    secondes.

    Parameters
    ----------
    ne : int
        Nombre d'équipes.
    nj_min : int
        Borne minimale de la recherche.
    nj_max : int
        Borne maximale de la recherche.
    timeout : int, default=10
        Valeur du timeout (en secondes).

    Returns
    -------
    j : int
        Nombre de jours optimal.

    Examples
    --------
    >>> optimisation(3, 3, 10)
    6

    >>> optimisation(10, 10, 20)
    18

    >>> optimisation(20, 20, 40)
    None

    Le timeout est trop bas pour permettre à glucose de résoudre le problème avec ne=20.
    """
    import multiprocessing

    for j in range(nj_min, nj_max + 1):
        encoder(ne, j)
        p = multiprocessing.Process(target=glucose)
        p.start()
        p.join(timeout)  # on attend 10 secondes
        if p.is_alive():  # si le processus est toujours vivant après 10 secondes
            print("timeout atteint...")
            p.terminate()  # on le termine
            continue  # on passe à l'itération suivante
        # sinon, c'est qu'il a fini : on regarde si le modèle est satisfiable, et si
        # c'est le cas, on renvoie j
        if decoder("planning.cnf", ne, j) is not None:
            return j


if __name__ == "__main__":
    """Programme principal. Permet à l'utilisateur de saisir le nombre d'équipes,
    le nombre de jours, préciser s'il y a un fichier texte contenant le nom des équipes,
    avec la possibilité de nettoyer les fichiers générés par glucose. Affiche le
    planning s'il y a une solution au problème.
    """
    import os

    # Saisie
    ne = int(input("Saisir le nombre d'équipes : "))
    nj = int(input("Saisir le nombre de jours : "))
    teams = input(
        "Nom du fichier donnant le nom des équipes "
        + "(appuyer sur la touche 'enter' pour passer ou s'il n'y en a pas) : "
    )
    janitor = input(
        "Voulez vous nettoyer les fichiers de travail à la fin du programme ?"
        + "(o/oui, appuyer sur la touche 'enter' pour passer)"
    )
    # Checks
    if teams == "":
        teams = None
    elif not os.path.isfile(teams):
        raise ValueError(f"Le fichier '{teams}' n'existe pas.")

    # Programme
    encoder(ne, nj)  # Encodage du problème
    glucose()  # Résolution grâce à glucose
    planning = decoder("planning.cnf", ne, nj, teams)  # Décodage le résultat
    affichage(planning)  # Affichage du résultat sous la forme d'un tableau

    if janitor.lower() in ("o", "oui"):
        os.remove("planning.cnf")
        os.remove("championnat.cnf")

"""---- Résultats ----

Pour ne=3, nj=6, et le nom des équipes étant stockées dans 'equipes.txt' on 
obtient le résultat suivant à l'aide de glucose et du programme :

                Planning des matchs                 
+------+---------------------+---------------------+
| Jour |      Domicile       |      Extérieur      |
+------+---------------------+---------------------+
|  0   |    Saint-Etienne    | Paris Saint-Germain |
|  1   | Paris Saint-Germain |    Saint-Etienne    |
|  2   | Paris Saint-Germain |       Monaco        |
|  3   |    Saint-Etienne    |       Monaco        |
|  4   |       Monaco        | Paris Saint-Germain |
|  5   |       Monaco        |    Saint-Etienne    |
+------+---------------------+---------------------+

Que les meilleurs gagnent !

Pour ne=8, nj=14 (valeur trouvée par optimisation), on a 4 matchs par jour :

                   Planning des matchs                    
+------+------------------------+------------------------+
| Jour |        Domicile        |       Extérieur        |
+------+------------------------+------------------------+
|  0   |         Monaco         |        RC Lens         |
|  0   | Olympique de Marseille |     Saint-Etienne      |
|  0   |   Olympique Lyonnais   |       FC Nantes        |
|  0   |       LOSC Lille       |  Paris Saint-Germain   |
|  1   |  Paris Saint-Germain   |        RC Lens         |
|  1   |     Saint-Etienne      |       FC Nantes        |
|  1   |         Monaco         | Olympique de Marseille |
|  1   |   Olympique Lyonnais   |       LOSC Lille       |
|  2   |  Paris Saint-Germain   | Olympique de Marseille |
|  2   |     Saint-Etienne      |        RC Lens         |
|  2   |   Olympique Lyonnais   |         Monaco         |
|  2   |       LOSC Lille       |       FC Nantes        |
|  3   |         Monaco         |   Olympique Lyonnais   |
|  3   |       FC Nantes        |     Saint-Etienne      |
|  3   |        RC Lens         |  Paris Saint-Germain   |
|  3   |       LOSC Lille       | Olympique de Marseille |
|  4   |     Saint-Etienne      |  Paris Saint-Germain   |
|  4   |   Olympique Lyonnais   | Olympique de Marseille |
|  4   |       FC Nantes        |         Monaco         |
|  4   |        RC Lens         |       LOSC Lille       |
|  5   |  Paris Saint-Germain   |         Monaco         |
|  5   | Olympique de Marseille |   Olympique Lyonnais   |
|  5   |       FC Nantes        |       LOSC Lille       |
|  5   |        RC Lens         |     Saint-Etienne      |
|  6   |     Saint-Etienne      | Olympique de Marseille |
|  6   |         Monaco         |       LOSC Lille       |
|  6   |   Olympique Lyonnais   |        RC Lens         |
|  6   |       FC Nantes        |  Paris Saint-Germain   |
|  7   | Olympique de Marseille |  Paris Saint-Germain   |
|  7   |   Olympique Lyonnais   |     Saint-Etienne      |
|  7   |       FC Nantes        |        RC Lens         |
|  7   |       LOSC Lille       |         Monaco         |
|  8   |     Saint-Etienne      |   Olympique Lyonnais   |
|  8   |         Monaco         |  Paris Saint-Germain   |
|  8   | Olympique de Marseille |       LOSC Lille       |
|  8   |        RC Lens         |       FC Nantes        |
|  9   |  Paris Saint-Germain   |       LOSC Lille       |
|  9   |         Monaco         |     Saint-Etienne      |
|  9   | Olympique de Marseille |        RC Lens         |
|  9   |       FC Nantes        |   Olympique Lyonnais   |
|  10  |  Paris Saint-Germain   |   Olympique Lyonnais   |
|  10  |         Monaco         |       FC Nantes        |
|  10  |        RC Lens         | Olympique de Marseille |
|  10  |       LOSC Lille       |     Saint-Etienne      |
|  11  |  Paris Saint-Germain   |       FC Nantes        |
|  11  |     Saint-Etienne      |       LOSC Lille       |
|  11  | Olympique de Marseille |         Monaco         |
|  11  |        RC Lens         |   Olympique Lyonnais   |
|  12  |     Saint-Etienne      |         Monaco         |
|  12  |   Olympique Lyonnais   |  Paris Saint-Germain   |
|  12  |       FC Nantes        | Olympique de Marseille |
|  12  |       LOSC Lille       |        RC Lens         |
|  13  |  Paris Saint-Germain   |     Saint-Etienne      |
|  13  | Olympique de Marseille |       FC Nantes        |
|  13  |        RC Lens         |         Monaco         |
|  13  |       LOSC Lille       |   Olympique Lyonnais   |
+------+------------------------+------------------------+
"""
