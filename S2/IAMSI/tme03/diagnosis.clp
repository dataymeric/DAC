;;;; IAMSI - TME3

; Note : (initial-fact) a été retiré depuis CLIPS 6.40
(deffacts initialisation
    (taches rouges)
    (boutons peu)
    (sensation froid)
    (fievre forte)
    (yeux douloureux)
    (amygdales rouges)
    (peau pele seche)
    ;(dos douloureux)
    ;(pustules)
    ;(demangeaisons fortes)
)

;;;; Symptômes potentiels du patient
; Le patient a-t-il peu ou beaucoup de boutons ?
; Le patient a-t-il des rougeurs ?
; Le patient a-t-il peu ou beaucoup de fièvre ? 
; Le patient a-t-il une sensation de froid ?
; Le patient a-t-il les amygdales rouges ?
; Le patient a-t-il des tâches rouges ?
; Le patient a-t-il la peau sèche ?
; Le patient a-t-il la peau qui pèle ?
; Le patient a-t-il les yeux douloureux ?
; Le patient a-t-il le dos douleureux ?
; Le patient a-t-il des démangeaisons ?
; Le patient a-t-il des pustules ?

;;;; Diagnostics possibles à partir des symptômes déclarés par le patient
; le patient a une éruption cutanée s'il a peu ou beaucoup de boutons 
(defrule eruption-cutanee
    (or (boutons peu) (boutons beaucoup))
    =>
    (printout t "Le patient a une eruption cutanee." crlf)
    (assert (eruption-cutanee))
)

; le patient a un exanthème s'il a des éruptions cutanées ou des rougeurs
(defrule exantheme
    (or (eruption-cutanee) (rougeur))
    =>
    (printout t "Le patient a un exantheme." crlf)
    (assert (exantheme))
)

; le patient est dans un état fébrile s'il a une forte fièvre ou s'il ressent une sensation de froid
(defrule etat-febrile
    (or (fievre forte) (sensation froid))
    =>
    (printout t "Le patient est dans un etat febrile." crlf)
    (assert (etat-febrile))
)

; le patient présente un signe suspect s'il a les amygdales rouges, des tâches rouges et la peau qui pèle
(defrule signe-suspect
    (and (amygdales rouges) (taches rouges) (peau pele ?))
    =>
    (printout t "Le patient presente un signe suspect." crlf)
    (assert (signe-suspect))
)

; le patient a la rougeole si : 
;   - il est dans un état fébrile, a des yeux douloureux et un exanthème
;   - il présente un signe supect et a une forte fièvre
(defrule rougeole
    (not (rougeole non))  ; permet de s'assurer que (pas-rougeole) s'est déclenchée si elle devait se déclencher (et de ne pas utiliser de salience)
    (or (and (etat-febrile) (yeux douloureux) (exantheme))
        (and (signe-suspect) (fievre forte)))
    =>
    (printout t "Le patient a la rougeole." crlf)
    (assert (rougeole oui))
)

; le patient n'a pas la rougeole s'il a peu de fièvre et peu de boutons
; on souhaite la déclencher avant rougeole pour ne pas avoir à faire des manipulations
; de faits avec des (retract)
(defrule pas-rougeole
    (declare (salience 10))
    ;?rougeole <- (rougeole oui)  ; je laisse ces bouts de code pour la postérité
    (and (fievre faible) (boutons peu))
    =>
    (printout t "Le patient n'a pas la rougeole." crlf)
    (assert (rougeole non))
    ;(retract ?rougeole)
)

; on relève une douleur si le patient a les yeux ou le dos douloureux
(defrule douleur
    (or (yeux douloureux) (dos douloureux))
    =>
    (printout t "Le patient a une douleur." crlf)
    (assert (douleur))
)

; le patient a la grippe s'il a le dos douloureux et est dans un état fébrile
(defrule grippe
    (and (dos douloureux) (etat-febrile))
    =>
    (printout t "Le patient a la grippe." crlf)
    (assert (grippe))
)

; ce n'est pas précisé dans l'énoncé si une inflammation des ganglions est un fait
; ou une règle... je ne suis pas médecin mais on considérera ici qu'avoir des amygdales
; rouges est un signe d'une inflammation des ganglions.
(defrule inflammation-ganglions
    (amygdales rouges)
    =>
    (assert (inflammation-ganglions))
)

; si le patient a de fortes démangeaisons, des pustules et qu'on a déjà déterminé qu'il
; ne s'agissait pas de la rougeole, il a la varicelle
; le fait d'utiliser une valeur oui / non sur (rougeole) au lieu de juste vérifier si
; le fait existe permet de ne pas avoir à configurer une salience pour varicelle et rubéole
(defrule varicelle
    (and (demangeaisons fortes) (pustules) (rougeole non))
    =>
    (printout t "Le patient a la varicelle." crlf)
    (assert (varicelle))
)

; si le patient a la peau sèche, une inflammation des ganglions, n'a ni pustules ni sensation de froid
; et qu'on a déjà déterminé qu'il ne s'agissait pas de la rougeole, il a la rubéole
(defrule rubeole
    (and (peau ? seche) (inflammation-ganglions) (rougeole non))
    (not (sensation froid))
    (not (pustules))
    =>
    (printout t "Le patient a la rubeole." crlf)
    (assert (rubeole))
)

;;;; Compte-rendu du diagnostic médical
; Quand plusieurs règles sont applicables, CLIPS marche par une méthode dite de "résolution de conflits".
; Il regarde la priorité de chaque règle déclenchable et les déclenche ensuite par plus grande priorité.
; Les priorités sont définies par (dans l'ordre) :
;   - la salience : on peut la déclarer (declare (salience int)), elle vaut 0 par défaut
;   - la spécificité : si deux règles (ou plus) ont la même salience, la règle avec 
; le plus de conditions spécifiques gagne. La spécifité est déterminée par le nombre de 
; conditions dans la règle et à quel point ces règles sont "précises" ou "détaillées".
;   - sinon, il regarde la règle qui a été rajoutée la plus récemment (= la règle la plus basse dans le fichier).
;
; CLIPS fonctionne par chainage avant : il déclenche les règles applicables au fur et à mesure.
;
; A partir des faits initiaux donnés, le patient est diagnostiqué les pathologies suivantes
; (par ordre de déclenchement des règles) :
;   - le patient présente un signe suspect ;
;   - le patient a la rougeole ;
;   - le patient a une une douleur ;
;   - le patient est dans un état fébrile ;
;   - le patient a une éruption cutanée ;
;   - le patient a un exanthème ;
; => Il était temps qu'il aille chez le médecin !
;
; En surveillant CLIPS avec (watch rules) et (watch facts) :
;;;; 1. Il déclenche (signe-suspect) à partir des faits initiaux 6, 1 et 7 et ajoute un fait 8.
; FIRE    1 signe-suspect: f-6,f-1,f-7
; ==> f-8     (signe-suspect)
;;;; 2. Il déclenche (rougeole) à partir des faits 8 et 4 et ajoute un fait 9.
;;;; Note : cette règle étant très spécifique elle prend la priorité.
; FIRE    2 rougeole: *,f-8,f-4
; ==> f-9     (rougeole oui)
;;;; 3. Il déclenche (inflammation-ganglions) à partir du fait 6 et ajoute un fait 10.
; FIRE    3 inflammation-ganglions: f-6
;==> f-10    (inflammation-ganglions)
;;;; 4. Il déclenche (douleur) à partir du fait 5 et ajoute un fait 11.
; FIRE    4 douleur: f-5
; ==> f-11    (douleur)
;;;; 5. Il déclenche (etat-febrile) à partir du fait 4 et ajoute un fait 12.
; FIRE    5 etat-febrile: f-4
; ==> f-12    (etat-febrile)
;;;; 6. Il re-déclenche (etat-febrile) à partir du fait 3 (car "ou") : possibilité d'éviter de re-déclencher une
;;;; règle en ajoutant (not (regle)) dans les règles. Il n'ajoute pas de fait car (etat_febrile) est déjà
;;;; présent.
; FIRE    6 etat-febrile: f-3
;;;; 7. Il déclenche (eruption-cutanee) à partir du fait 2 et ajoute un fait 13.
; FIRE    7 eruption-cutanee: f-2
; ==> f-13    (eruption-cutanee)
;;;; 8. Il déclenche (exantheme) à partir du fait 13 et ajoute un fait 14.
; FIRE    8 exantheme: f-13
; ==> f-14    (exantheme)
;;;; 8. Il re-déclenche (rougeole) à partir des faits 12, 5 et 14 mais n'ajoute pas de fait étant déjà présent.
; FIRE    8 rougeole: *,f-12,f-5,f-14
;
;;;; Base de faits finale
;;;; --- Base initiale
; f-1     (taches rouges)
; f-2     (boutons peu)
; f-3     (sensation froid)
; f-4     (fievre forte)
; f-5     (yeux douloureux)
; f-6     (amygdales rouges)
; f-7     (peau pele seche)
;;;; --- Base des faits ajoutés
; f-8     (signe-suspect)
; f-9     (rougeole oui)
; f-10    (inflammation-ganglions)
; f-11    (douleur)
; f-12    (etat-febrile)
; f-13    (eruption-cutanee)
; f-14    (exantheme)

; CLIPS utilise donc 6 règles pour 6 ajouts (pour 8 déclenchements ("FIRE")).
; De plus, il diagnostique rougeole en seulement 2 déclenchements : (signe-suspect) puis (rougeole), ce qui
; est le minimum d'après le chainage arrière.
; Avec le chainage arrière, on trouve 4 manières de diagnostiquer (rougeole) :
;   - (boutons peu) -> (eruption-cutanee) -> (exantheme) + (etat-febrile) + (yeux-douloureux) -> (rougeole) = 4 déclenchements
;   - (boutons beaucoup) -> (eruption-cutanee) -> (exantheme) + (etat-febrile) + (yeux-douloureux) -> (rougeole) = 4 déclenchements
;   - (rougeur) -> (exantheme) + (etat-febrile) + (yeux-douloureux) -> (rougeole) = 3 déclenchements
;   - (amygdales rouges) + (taches rouges) + (peau pele) -> (fievre forte) + (signe suspect) -> (rougeole) = 2 déclenchements
; 
; De part la construction de notre base de faits initiale, CLIPS est en mesure de diagnostiquer la rougeole de la manière
; la plus rapide (bien que techniquement, il ré-exécute une deuxième fois rougeole, après avoir ajouté (eruption-cutanee) puis (exantheme), 
; indiqué par notre cas 1 (= 4 déclenchements)).
; Si (taches rouges) et (peau pele) n'étaient pas présents dans les faits initiaux, cela n'aurait pas été le cas. 
;
; On pourra vérifier qu'avec les faits :
;   (boutons peu)
;   (fievre faible)
;   (yeux douloureux)
;   (amygdales rouges)
;   (peau normale seche)
; on diagnostique la rubeole (et pas la rougeole).
;
; Avec : 
;   (taches rouges)
;   (boutons peu)
;   (fievre faible)
;   (dos douloureux)
;   (pustules)
;   (demangeaisons fortes)
; on diagnostique la varicelle (et pas la rougeole).