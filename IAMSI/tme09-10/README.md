# TME 9 - Planification

Pour les planificateurs en PDDL, le domaine se trouve dans `{nom}_domain.pddl` et le problème dans `{nom}_problem.pddl`.

Dans le dossier `exo2`, on trouve le problème du monde des blocs en PDDL avec 2 problèmes. Les solutions sont dans les fichiers `plan_problem1.txt` et `plan_problem2.txt` respectivement.

Dans le dossier `satplan`, on trouve l'exercice 3 du TD9 (planification d'avions) en PDDL. La solution est dans `plan_avions.txt`.

Dans le dossier `asp`, l'exercice 3 du TD9 en ASP, de deux manières : 
- la première en faisant une méthode "parseur PDDL vers ASP-STRIPS" (comme décrit dans l'annexe, à mon sens la manière la plus simple). Comme pour PDDL, les fichiers ont été séparés en `domain` et `problem` et le planificateur dans `strips.lp`. La solution est indiquée en commentaire dans `avion_problem.lp`. Cette méthode permet de réutiliser `strips.lp` avec d'autres domaines et problèmes. Il y a aussi le domaine et le problème pour le monde des blocs.
- le deuxième en ASP "pur", un peu plus compliqué.
