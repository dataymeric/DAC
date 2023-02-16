
## 3a
 les scores de chacun des mots pour produire un seul vecteur
somme, avg, min, max

pas mal de trucs qui explain que ça marche pas si bien
vecteur bcp plus petit à la fin (600 ou 300 contre 500000 examples) => underfitting, donc pas des bonnes perf contrairement à un BoW 

pour ces taches de classification, phrases assez longues et pas juste "oui j'ai bien aimé lol" donc on moyenne sur des phrases longues et on dilue forément l'information utile
avec des transformers on reste dans cette étape mais on a une etape de pulling attentionnelle 
token particulier : token CLS qui est utilisé dans les embedding vectoriel pour faire de la pred mais sera appris en le mettant en relation avec tous les autres vecteurs (moyenne pondérée par l'attention = plus fin que ce qu'on fait ici)

## 3b
embedding vectoriel pour caractériser chaque mot : est-ce que je suis capable de prédire un mot 
CRF
capture aussi un espace sémantique 


on travaille sur PoS : mot1 PoS, mot2 chunking

faire une prédiction pour chaque mot, tokens bizarres pas dans le vocabulaire : il faut lesprendre en compte, on propose ici de les initialiser aléatoirement pour pred dans dimension d=300
