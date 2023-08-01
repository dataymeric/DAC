(deftemplate patient
    ;; symptomes
    (slot boutons (type SYMBOL) (allowed-symbols non peu beaucoup))
    (slot rougeur (type SYMBOL) (allowed-symbols oui non))
    (slot fievre (type SYMBOL) (allowed-symbols faible forte non))
    (slot sensation (type SYMBOL) (allowed-symbols oui non))
    (slot amygdales (type SYMBOL) (allowed-symbols oui non))
    (slot taches (type SYMBOL) (allowed-symbols oui non))
    (slot desquamation (type SYMBOL) (allowed-symbols oui non))
    (slot yeux (type SYMBOL) (allowed-symbols oui non))
    (slot dos (type SYMBOL) (allowed-symbols oui non))
)

;;;; Questions générales
(defrule boutons
    (not (boutons ?))
    =>
    (printout t crlf "Le patient a-t-il des boutons ? (peu/beaucoup/non)" crlf)
	(printout t "Réponse : ")
    (assert (boutons ?boutons))
    (modify ?patient (boutons ?boutons))
)

(defrule rougeur
    (not (rougueur ?))
    =>
    (printout t crlf "Le patient a-t-il des rougeurs ? (oui/non)" crlf)
	(printout t "Réponse : ")
    (assert (rougeur ?rougeur))
    (modify ?patient (rougeur ?rougeur))
)

(defrule fievre
    (not (fievre ?))
    => 
    (printout t crlf "Le patient a-t-il de la fièvre ? (faible/forte/non)" crlf)
	(printout t "Réponse : ")
    (assert (fievre ?fievre))
    (modify ?patient (fievre ?fievre))
)

(defrule sensation
    (not (sensation ?))
    =>
    (printout t crlf "Le patient a-t-il une sensation de froid ? (oui/non)" crlf)
	(printout t "Réponse : ")
    (assert (sensation ?sensation))
    (modify ?patient (sensation ?sensation))
)

(defrule amygdales
    (not (amygdales ?))
    =>
    (printout t crlf "Le patient a-t-il les amygdales rouges ? (oui/non)" crlf)
	(printout t "Réponse : ")
    (assert (amygdales ?amygdales))
    (modify ?patient (amygdales ?amygdales))
)

(defrule taches
    (not (taches ?))
    =>
    (printout t crlf "Le patient a-t-il des taches rouges ? (oui/non)" crlf)
	(printout t "Réponse : ")
    (assert (taches ?taches))
    (modify ?patient (taches ?taches))
)

(defrule desquamation
    (not (desquamation ?))
    =>
    (printout t crlf "Le patient a-t-il la peau qui pêle ? (oui/non)" crlf)
	(printout t "Réponse : ")
    (assert (desquamation ?desquamation))
    (modify ?patient (desquamation ?desquamation))
)

(defrule peau_seche
    (not (peau_seche ?))
    =>
    (printout t crlf "Le patient a-t-il la peau sêche ? (oui/non)" crlf)
	(printout t "Réponse : ")
    (assert (peau_seche ?peau_seche))
    (modify ?patient (peau_seche ?peau_seche))
)

(defrule dos
    (not (dos ?))
    =>
    (printout t crlf "Le patient a-t-il les dos douloureux ? (oui/non)" crlf)
	(printout t "Réponse : ")
    (assert (dos ?dos))
    (modify ?patient (dos ?dos))
)

(defrule demangeaisons
    (not (demangeaisons ?))
    =>
    (printout t crlf "Le patient a-t-il des démangeaisons ? (oui/non)" crlf)
	(printout t "Réponse : ")
    (assert (demangeaisons ?demangeaisons))
    (modify ?patient (demangeaisons ?demangeaisons))
)

(defrule pustules
    (not (pustules ?))
    =>
    (printout t crlf "Le patient a-t-il des pustules ? (oui/non)" crlf)
	(printout t "Réponse : ")
    (assert (pustules ?pustules))
    (modify ?patient (pustules ?pustules))
)

(defrule ganglions
    (not (ganglions ?))
    =>
    (printout t crlf "Le patient a-t-il une inflammation des ganglions ? (oui/non)" crlf)
	(printout t "Réponse : ")
    (assert (ganglions ?ganglions))
    (modify ?patient (ganglions ?ganglions))
)

;;;; 
(defrule eruption_cutanee
	(not (eruption_cutanee ?))
    patient <- (patient (boutons ?boutons))
    (or (patient (boutons peu)) (patient (boutons beaucoup)))
    =>
    (printout t "Le patient a une éruption cutanée." crlf)
    (assert eruption_cutanne oui)
    (modify ?patient (?eruption_cutanee eruption_cutanee))
)

(defrule exantheme
    (not (exantheme ?))
    patient <- (patient (fievre ?fievre) (eruption_cutanee ?eruption_cutanee))
    (or (patient (eruption_cutanee oui)) (patient (fievre forte)))
    =>
    (printout t "Le patient a un exanthème." crlf)
    (assert (exantheme oui))
    (modify ?patient (?exantheme exantheme))
)

(defrule etat_febrile
    (not (etat_febrile ?))
    patient <- (patient (fievre ?fievre) (sensation ?sensation))
    (or (fievre forte) (sensation oui))
    =>
    (printout t "Le patient est dans un état fébrile." crlf)
    (assert (etat_febrile oui))
    (modify ?patient (?etat_febrile etat_febrile))
)

(defrule signe_suspect
    (not (signe_suspect ?))
    patient <- (patient (amygdales ?amygdales) (taches ?taches) (desquamation ?desquamation))
    (and (patient (amygdales oui)) (patient (taches oui)) (patient (desquamation oui)))
    =>
    (printout t "Le patient présente un signe suspect." crlf)
    (assert signe_suspect oui)
    (modify ?patient (?signe_suspect signe_suspect))
)

(defrule rougeole
    (not (rougeole ?))
    patient <- (patient (etat_febrile ?etat_febrile) (yeux ?yeux) (exantheme ?exantheme) (signe_suspect ?signe_suspect) (fievre ?fievre) (boutons ?boutons))
    (or (and (patient (etat_febrile oui)) (patient (yeux oui)) (patient (exantheme oui))) (and (patient (signe_suspect oui)) (patient (fievre forte))))
    =>
    (if (and (neq ?fievre peu) (neq ?boutons peu)) then
        (printout t "Le patient a la rougeole." crlf)
        (assert rougeole oui)
    else   
        (printout t "Le patient n'a pas la rougeole." crlf)
        (assert rougeole non)
    )
    (modify ?patient (?rougeole rougeole))
)

(defrule douleur
    (not (douleur ?))
    patient <- (patient (yeux ?yeux) (dos ?dos))
    (or (patient (yeux oui)) (patient (dos oui)))
    =>
    (assert douleur oui)
    (modify ?patient (?douleur douleur))
)

(defrule grippe
    (not (grippe ?))
    patient <- (patient (dos ?dos) (etat_febrile ?etat_febrile))
    (and (patient (dos oui)) (patient etat_febrile oui))
    =>
    (printout t "Le patient a la grippe." crlf)
    (assert grippe oui)
    (modify ?patient (?grippe grippe))
)

