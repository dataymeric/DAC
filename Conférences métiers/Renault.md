21 mars 2023
## Véhicules intelligents
How safe are current passagers cars ? 1 mort toutes les 81 millions de km, 1 blessé toutes les 1.79 millions de km.

En 2020, 32 millions de km parcourus par les véhicules autonomes de Waymo (2,3 millions en 2021).

ADAS : Advanced Driving Assistance systems, depends on perception, localisation and maps.

## Détection de piétons
ADAS, Pedestrian AEB : Perception System
_Horizon Matrix Mono Camera Vision Perception Solution_
Juste besoin d'une caméra et hop (3k -4k € à installer)

Pedestria AEB Active -> Camera, rader, Vehicle State -> Pedestrian Detection & Tracking  (reviens à camera) -> Collision prediction (reviens à caméra) -> Action -> Warniong Alarm -> ABS

Système de _machine learning_. Il y a beaucoup de sources d'incertitudes notamment quand on définit les requirements, on récolte les données, on entraine et on déploie (que se passe-t-il si le modèle évolue dans un environnement où il n'a pas appris ?)

On n'a pas les données... je veux détecter où est-ce que le système de prédiction de piétons fonctionne -> études d'accidentologie (le + : passage piétons, quelle heure de la journée ? quelle zone (urbain, rural) ? quel météo ? quel âge ? ...)
Je sais donc je peux générer des données et je peux détecter si mon système marche ou non. On génère des synthetic data pour pouvoir si on est capable d'observer des situations trouvées en accidentologie.

Connectivité dans une voiture : partage d'informations (crowdsourcing) entre des véhicules ou utilisateurs. J'élargis on champs de détection : DSRC. 

Cooperative Systems : extended awareness - information sharing
=> utiliser les autres systèmes pour ajouter de l'information qu'on perçoit pas (par exemple une moto derrière une voiture, une voiture derrière un camion) => réseau pour partager dynamiquement l'information parmi les entités sur le réseau routier.
=> Local Dynamic Map : 
Couche :
com nodes, fusion result
info sur la route (météo, etc.)
landmarks 
map from provider

V2V SAFESPOT : Emergency Vehicle Intersections
un véhicule de secours arrive une intersection, il communique sa présence et sa direction aux véhicules à proximité

Problème : localisation
Imaginons deux routes qui sont proches : le GPS n'étant pas parfait, le GPS peut nous mettre sur une autre voie (celle où y a le véhicule de secours) et le système ne marche plus.

Localization -> perception -> prediction -> planning -> control
une erreur en localisation se propage sur les autres couches

ptite courbe de gauss là

pas le droit à l'erreur, on DOIT être dans la bonne ligne et on DOIT savoir qu'on est dans la bonne ligne.

SoftSafety


situation and self awareness c inéressant comme appelation

