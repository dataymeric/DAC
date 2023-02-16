
Charge la base de règles et de faits.
```
CLIPS> (load "famille.clp")
Defining defrule: my_init +j+j
Defining defrule: grand_pere1 +j+j+j
Defining defrule: grand_pere2 +j+j+j
Defining defrule: parent1 =j+j
Defining defrule: parent2 =j+j
Defining defrule: frere_et_soeur +j+j+j
TRUE
```

Réinitialise le moteur d'inférence à l'état initial :
```
CLIPS> (reset)
```

Liste les règles de la base de règles :
```
CLIPS> (rules)
my_init
grand_pere1
grand_pere2
parent1
parent2
frere_et_soeur
For a total of 6 defrules.
```

Liste les faits de la base de faits :
```
CLIPS> (facts) 
f-0     (initial-fact)
For a total of 1 fact.
```

Donne l'ensemble des règles déclenchables lors de la prochaine inférence.
```
CLIPS> (agenda)
0      my_init: f-0
For a total of 1 activation.
```

Démarre le moteur d'inférence.
```
CLIPS> (run)
==> f-1     (pere claire jean)
==> f-2     (pere bob jean)
==> f-3     (pere yves bob)
==> f-4     (mere yves zoe)
==> f-5     (mere luc claire)
==> f-6     (mere alain claire)
FIRE    2 grand_pere2: f-6,f-1
==> f-7     (grand_pere alain jean)
FIRE    3 parent2: f-6
==> f-8     (parent alain claire)
FIRE    4 grand_pere2: f-5,f-1
==> f-9     (grand_pere luc jean)
FIRE    5 parent2: f-5
==> f-10    (parent luc claire)
FIRE    6 frere_et_soeur: f-10,f-8
==> f-11    (frere_et_soeur luc alain)
==> f-12    (frere_et_soeur alain luc)
FIRE    7 frere_et_soeur: f-8,f-10
FIRE    8 parent2: f-4
==> f-13    (parent yves zoe)
FIRE    9 grand_pere1: f-3,f-2
==> f-14    (grand_pere yves jean)
FIRE   10 parent1: f-3
==> f-15    (parent yves bob)
FIRE   11 parent1: f-2
==> f-16    (parent bob jean)
FIRE   12 parent1: f-1
==> f-17    (parent claire jean)
FIRE   13 frere_et_soeur: f-17,f-16
==> f-18    (frere_et_soeur claire bob)
==> f-19    (frere_et_soeur bob claire)
FIRE   14 frere_et_soeur: f-16,f-17
``` 

```
CLIPS> (watch facts)
CLIPS> (watch rules)
CLIPS> (run)
FIRE    1 my_init: f-0
==> f-1     (pere claire jean)
==> f-2     (pere bob jean)
==> f-3     (pere yves bob)
==> f-4     (mere yves zoe)
==> f-5     (mere luc claire)
==> f-6     (mere alain claire)
FIRE    2 grand_pere2: f-6,f-1
==> f-7     (grand_pere alain jean)
FIRE    3 parent2: f-6
==> f-8     (parent alain claire)
FIRE    4 grand_pere2: f-5,f-1
==> f-9     (grand_pere luc jean)
FIRE    5 parent2: f-5
==> f-10    (parent luc claire)
FIRE    6 frere_et_soeur: f-10,f-8
==> f-11    (frere_et_soeur luc alain)
==> f-12    (frere_et_soeur alain luc)
FIRE    7 frere_et_soeur: f-8,f-10
FIRE    8 parent2: f-4
==> f-13    (parent yves zoe)
FIRE    9 grand_pere1: f-3,f-2
==> f-14    (grand_pere yves jean)
FIRE   10 parent1: f-3
==> f-15    (parent yves bob)
FIRE   11 parent1: f-2
==> f-16    (parent bob jean)
FIRE   12 parent1: f-1
==> f-17    (parent claire jean)
FIRE   13 frere_et_soeur: f-17,f-16
==> f-18    (frere_et_soeur claire bob)
==> f-19    (frere_et_soeur bob claire)
FIRE   14 frere_et_soeur: f-16,f-17
```


Q5
On retire le fait 0, juste après `(reset)` et avant de lancer les inférences : vu qu'il n'y a plus de faits dans la base de faits initiale, on ne peut forcément déclencher aucune règle.
```
CLIPS> (reset)
CLIPS> (retract 0)
<== f-0     (initial-fact)
CLIPS> (run)
```

```
CLIPS>(clear)
CLIPS>(rules)
CLIPS>(facts)
CLIPS>(reset)
CLIPS>(facts)
``` 

# Q8
résultat pas correct :
on a bob, alain, yves, or seul yves est enfant unique.