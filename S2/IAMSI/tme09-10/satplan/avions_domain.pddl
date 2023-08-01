(define (domain avions)
  (:requirements :strips :typing)

  (:types
    avion cargaison aeroport)

  (:predicates
    (situe ?x - (either avion cargaison) ?y - aeroport)
    (dans ?x - cargaison ?y - avion)
    (vide ?x - avion))

  (:action charger
    :parameters (?x - cargaison ?y - avion ?z - aeroport)
    :precondition (and (situe ?x ?z) (situe ?y ?z) (vide ?y))
    :effect (and (not (situe ?x ?z)) (not (vide ?y)) (dans ?x ?y)))

  (:action voler
    :parameters (?x - avion ?y - aeroport ?z - aeroport)
    :precondition (situe ?x ?y)
    :effect (and (not (situe ?x ?y)) (situe ?x ?z)))

  (:action decharger
    :parameters (?x - cargaison ?y - avion ?z - aeroport)
    :precondition (and (dans ?x ?y) (situe ?y ?z))
    :effect (and (not (dans ?x ?y)) (situe ?x ?z) (vide ?y)))
)
