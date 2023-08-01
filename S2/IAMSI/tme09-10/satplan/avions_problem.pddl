(define (problem avions-problem)
  (:domain avions)
  
  (:objects
    a1 a2 - avion
    c1 c2 c3 - cargaison
    teg cdg bar - aeroport)

  (:init
    (situe a1 teg)
    (situe a2 teg)
    (situe c1 teg)
    (situe c2 teg)
    (situe c3 teg)
    (vide a1)
    (vide a2))

  (:goal
    (and
      (situe a1 cdg)
      (situe a2 cdg)
      (situe c1 bar)
      (situe c2 bar)
      (situe c3 bar)
    )
  )
)
