(deftemplate patient
    ;; symptomes
    (slot boutons (type SYMBOL) (allowed-symbols non peu beaucoup)
    (slot rougeur (type SYMBOL) (allowed-symbols oui non))
    (slot fievre (type SYMBOL) (allowed-symbols forte non))
    (slot rougeur (type SYMBOL) (allowed-symbols oui non))
    (slot sensation (type SYMBOL) (allowed-symbols froid chaud normal))
    (slot amygdales (type SYMBOL) (allowed-symbols rouges normales))
    (slot taches (type SYMBOL) (allowed-symbols rouges non))
    (slot peau (type SYMBOL) (allowed-symbols pele normale))
)

(defrule eruption_cutanee
    (or (boutons beaucoup)
        (boutons peu)
    =>
    (assert (eruption-cutanne))
)

(defrule exantheme
    (or (eruption_cutanee)
        (rougeur ?patient)
    =>
    (assert (exanthme ?patient))
)

(defrule etat_febrile
    (or (fievre ?patient forte)
        (sensation ?patient froid)
    =>
    (assert (etat_febrile ?patient))
)

(defrule signe_suspect
    (amygdales ?patient rouges)
    (taches ?patient rouges)
    (peau ?patient pele)
    =>
    (assert (signe_suspect ?patient))
)

(defrule rougeole
    (or (and (etat_febrile ?patient)
             (yeux_douloureux ?patient)
             (exantheme ?patient))
        (and (signe_suspect ?patient)
             (yeux_douloureux ?patient))
        (and (neq (fievre ?patient faible))
             (neq (boutons ?patient peu))))
    =>
    (assert (rougeole ?patient))
)

(defrule))peu
