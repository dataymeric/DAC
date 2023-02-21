; Note : (initial-fact) a été retiré depuis CLIPS 6.40
(deffacts initialisation
    (taches rouges)
    (boutons peu)
    (sensation froid)
    (fievre forte)
    (yeux douloureux)
    (amygdales rouges)
    (peau pele seche)
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
;;;;

;;;; Diagnostics à partir des symptômes déclarés par le patient
; le patient a une éruption cutanée s'il a peu ou beaucoup de boutons 
(defrule eruption-cutanee
    (or (boutons peu) (boutons beaucoup))
    =>
    (assert (eruption-cutanee))
)

; le patient a un exanthème s'il a des éruptions cutanées ou des rougeurs
(defrule exantheme
    (or (eruption-cutanee) (rougeur))
    =>
    (assert (exantheme))
)

; le patient est dans un état fébrile s'il a une forte fièvre ou s'il ressent une sensation de froid
(defrule etat-febrile
    (or (fievre forte) (sensation froid))
    =>
    (assert (etat-febrile))
)

; le patient présente un signe suspect s'il a les amygdales rouges, des tâches rouges et la peau qui pèle
(defrule signe-suspect
    (and (amygdales rouges) (taches rouges) (peau pele ?))
    =>
    (assert (signe-suspect))
)

; le patient a la rougeole si : 
;   - il est dans un état fébrile, a des yeux douloureux et un exanthème
;   - il présente un signe supect et a une forte fièvre
; il n'a pas la rougeole s'il a peu de fièvre et peu de boutons
(defrule rougeole
    (or (and (etat-febrile) (yeux douloureux) (exantheme))
        (and (signe-suspect) (fievre forte))
        (and (neq ?fievre faible) (neq ?boutons peu)))
    =>
    (assert (rougeole))
)

; on relève une douleur si le patient a les yeux ou le dos douloureux
(defrule douleur
    (or (yeux douloureux) (dos douloureux))
    =>
    (assert (douleur))
)

; le patient a la grippe s'il a le dos douloureux et est dans un état fébrile
(defrule grippe
    (and (dos douloureux) (etat-febrile))
    =>
    (assert (grippe))
)

; si le patient a de fortes démangeaisons, des pustules et qu'on a déjà déterminé qu'il
; ne s'agissait pas de la rougeole, il a la varicelle
(defrule varicelle
    (not (rougeole ?))
    (and (demangeaisons fortes) (pustules))
    =>
    (assert (varicelle))
)

; si le patient a la peau sèche, une inflammation des ganglions, n'a ni pustules ni sensation de froid
; et qu'on a déjà déterminé qu'il ne s'agissait pas de la rougeole, il a la rubéole
(defrule rubeole
    ?sensation <- sensation
    (not (rougeole ?))
    (not (pustules ?))
    (neq ?sensation froid)
    (and (peau ? seche) (inflammation-ganglions))
    =>
    (assert (rubeole))
)
