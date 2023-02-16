;;; IAMSI 2023 : séance TME 3
;;; famille.clp

; La règle qui permet de remplir la base de faits
; elle est facultative si on décide d'entrer les faits à la
; main dans CLIPS
(defrule my_init
	(initial-fact)
=>
	(watch facts)
	(watch rules)

	(assert (pere claire jean))
	(assert (pere bob jean))
	(assert (pere yves bob))
	(assert (mere yves zoe))
	(assert (mere luc claire))
	(assert (mere alain claire))
)

; Grand-père par le père
(defrule grand_pere1
	(pere ?enf ?papa)
	(pere ?papa ?papa2papa)
=>
	(assert (grand_pere ?enf ?papa2papa))
)

; Grand-père par ma mère
(defrule grand_pere2
	(mere ?enf ?maman)
	(pere ?maman ?papa2maman)
=>
	(assert (grand_pere ?enf ?papa2maman))
)

; Parent : lien entre un enfant et son père ou sa mère
(defrule parent1
	(pere ?enf ?papa)
=>
	(assert (parent ?enf ?papa))
)

(defrule parent2
	(mere ?enf ?maman)
=>
	(assert (parent ?enf ?maman))
)

; Frère ou soeur
(defrule frere_et_soeur
	(parent ?enf1 ?pereOuMere)
	(parent ?enf2 ?pereOuMere)
	(test (neq ?enf1 ?enf2))
=>
	(assert (frere_et_soeur ?enf1 ?enf2))
	(assert (frere_et_soeur ?enf2 ?enf1))
)
; ----- fin fichier famille.clp

; Oncle ou tante : frère ou soeur de mes parents
(defrule oncle_ou_tante
	(parent ?enf ?parent)
	(frere_et_soeur ?parent ?oncle_tante)
	(test (neq ?parent ?oncle_tante))
=>
	(assert (oncle_ou_tante ?enf ?oncle_tante))
)

; Cousin ou cousine : un enfant de mon oncle ou ma tante
(defrule cousin_cousine
	(oncle_ou_tante ?enf1 ?oncle_tante)
	(parent ?enf2 ?oncle_tante)
=>
	(assert (cousin_cousine ?enf1 ?enf2))
)

(defrule enfant_unique_bad
	(parent ?enf ?papaOuMaman)
	(not (frere_et_soeur ?enf ?autre))
	=>
	(assert (enfant_unique_bad ?enf))
)

(defrule enfant_unique_priorite
	(declare (salience -1000))
	(parent ?enf ?papaOuMaman)
	(not (frere_et_soeur ?enf ?autre))
	=>
	(assert (enfant_unique_priorite ?enf))
)