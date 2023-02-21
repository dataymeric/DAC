;;; IAMSI : TME 3
;;; maladie.clp

(def rule my_init
    (initial-fact)
=>
    (watch facts)
    (watch rules)
)

; Si le sujet a peu de boutons, il a comme symtômes une éruption cutanée
(def rule eruption_cutanee1
    (peu_bouton ?x)
=>
    (assert (eruption_cutanee ?x))
)

; Si le sujet a beaucoup de boutons, il a comme symtômes une éruption cutanée
(def rule eruption_cutanee2
    (beaucoup_bouton ?x)
=>
    (assert (eruption_cutanee ?x))
)

(def rule exantheme1
    (eruption_cutanne ?x)
=>
    (assert (exantheme ?x))
)

(def rule exantheme1
    (rougeur ?x)
=>
    (assert (exantheme ?x))
)

(defrule etat_febrile1
    (forte_fievre ?x)
=>
    (assert (etat_febrile ?x))
)

(defrule etat_febrile2
    (sensation_froid ?x)
=>
    (assert (etat_febrile ?x))
)

(defrule signe_suspect
    (amygdales_rouges ?x)
    (taches_rouges ?x)
    (peau_qui_pele ?x)
=>
    (assert (signe_suspect ?x))
)

(defrule rougeole1
    (etat_febrile ?x)
    (yeux_douloureux ?x)
    (exantheme ?x)
=>
    (assert (rougeole ?x))
)

(defrule rougeole2
    (signe_suspect ?x)
    (forte_fievre ?x)
=>
    (assert (rougeole ?x))
)

(defrule not_rougeole
    (peu_fievre ?x)
    (peu_bouton ?x)
=>
    (assert (not_rougeole ?x))
)

(defrule douleur1
    (yeux_douloureux ?x)
=> 
    (assert (douleur ?x))
)

(defrule douleur2
    (dos_douloureux ?x)
=> 
    (assert (douleur ?x))
)

(defrule grippe
    (dos_douloureux ?x)
    (etat_febrile ?x)
=>
    (grippe ?x)    
)

(defrule varicelle
    (not_rougeole ?x))
)