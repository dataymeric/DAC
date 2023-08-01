---
annotation-target: SAM6-fragmentation_2023.pdf
---

## Conception de base de données réparties, fragmentation


### s
Simplifier les choses à l'aide d'une "surcouche".
Pas d'hypothèse sur l'homogénéité des données contrairement à des BDD parallèles. Montrer ce qu'il y a dans la "boite bleue" (SGBDR) => comment les applications puissent se connecter à la boite bleue et avoir accès à leur boite locale.
Trouver les façons d'exécuter ces requêtes = minimiser le temps de communication (bases géo-distribuées (avec beaucoup d'écart géographique))

Migration vers une BDR
Représentation plus simple : deux approches :
- approche par **intégration** : on a une contrainte sur le fait que les bases existent à tel endroit
	- approche graduelles : architecture fédérée (pas l'essentiel du cours)
- approche par **décomposition** : adapter en fonction des données que l'on veut

fragmentation : découpage d'un ensemble en sous-ensembles disjoints
allocation : la partie jaune des données peut se retrouver à plusieurs endroits

### Fragmentation
Aider à gagner en performance, en faciité d'accès aux données.

Plusieurs façons de découper les données : 
- horizontale : 

>%%
>```annotation-json
>{"created":"2023-03-21T15:39:32.609Z","text":"Essayer de composer des prédicats pour obtenir des fragmants qui conviendront le mieux possible.","updated":"2023-03-21T15:39:32.609Z","document":{"title":"Microsoft PowerPoint - SAM6-fragmentation_2023.pptx","link":[{"href":"urn:x-pdf:468ca9827762f0c253d83c12b2556b5a"},{"href":"vault:/S2/SAM/SAM6-fragmentation_2023.pdf"}],"documentFingerprint":"468ca9827762f0c253d83c12b2556b5a"},"uri":"vault:/S2/SAM/SAM6-fragmentation_2023.pdf"}
>```
>%%
>*%%PREFIX%%%%HIGHLIGHT%% ==== %%POSTFIX%%*
>%%LINK%%[[#^629i8re71m5|show annotation]]
>%%COMMENT%%
>Essayer de composer des prédicats pour obtenir des fragmants qui conviendront le mieux possible.
>%%TAGS%%
>
^629i8re71m5


>%%
>```annotation-json
>{"created":"2023-03-21T15:40:45.246Z","text":"On prend les commandes de Paris et les commandes d'ailleurs. Mais ça veut dire quoi la ville d'une commande ? => c'est la ville du client qui commande","updated":"2023-03-21T15:40:45.246Z","document":{"title":"Microsoft PowerPoint - SAM6-fragmentation_2023.pptx","link":[{"href":"urn:x-pdf:468ca9827762f0c253d83c12b2556b5a"},{"href":"vault:/S2/SAM/SAM6-fragmentation_2023.pdf"}],"documentFingerprint":"468ca9827762f0c253d83c12b2556b5a"},"uri":"vault:/S2/SAM/SAM6-fragmentation_2023.pdf","target":[{"source":"vault:/S2/SAM/SAM6-fragmentation_2023.pdf","selector":[{"type":"TextPositionSelector","start":8045,"end":8048},{"type":"TextQuoteSelector","exact":"Cde","prefix":" 2D 3D 4C 1C 1C 2C 4P 1P 2P 3P 4","suffix":"qté1020 5 10ncdenclientproduitD "}]}]}
>```
>%%
>*%%PREFIX%%2D 3D 4C 1C 1C 2C 4P 1P 2P 3P 4%%HIGHLIGHT%% ==Cde== %%POSTFIX%%qté1020 5 10ncdenclientproduitD*
>%%LINK%%[[#^x4rqa395vaj|show annotation]]
>%%COMMENT%%
>On prend les commandes de Paris et les commandes d'ailleurs. Mais ça veut dire quoi la ville d'une commande ? => c'est la ville du client qui commande
>%%TAGS%%
>
^x4rqa395vaj


>%%
>```annotation-json
>{"created":"2023-03-21T15:41:21.098Z","text":"Requête de jointure, mais la table client est là juste pour filtrer. Ce qui m'intéresse c'est les tuples de commandes.","updated":"2023-03-21T15:41:21.098Z","document":{"title":"Microsoft PowerPoint - SAM6-fragmentation_2023.pptx","link":[{"href":"urn:x-pdf:468ca9827762f0c253d83c12b2556b5a"},{"href":"vault:/S2/SAM/SAM6-fragmentation_2023.pdf"}],"documentFingerprint":"468ca9827762f0c253d83c12b2556b5a"},"uri":"vault:/S2/SAM/SAM6-fragmentation_2023.pdf","target":[{"source":"vault:/S2/SAM/SAM6-fragmentation_2023.pdf","selector":[{"type":"TextPositionSelector","start":7886,"end":7898},{"type":"TextQuoteSelector","exact":"select Cde.*","prefix":"définis par semi jointureCde1 = ","suffix":" from Cde, Client 1where Cde.ncl"}]}]}
>```
>%%
>*%%PREFIX%%définis par semi jointureCde1 =%%HIGHLIGHT%% ==select Cde.*== %%POSTFIX%%from Cde, Client 1where Cde.ncl*
>%%LINK%%[[#^0nuf1o9m9pm|show annotation]]
>%%COMMENT%%
>Requête de jointure, mais la table client est là juste pour filtrer. Ce qui m'intéresse c'est les tuples de commandes.
>%%TAGS%%
>
^0nuf1o9m9pm


>%%
>```annotation-json
>{"created":"2023-03-21T15:41:42.794Z","text":"Semi-jointure","updated":"2023-03-21T15:41:42.794Z","document":{"title":"Microsoft PowerPoint - SAM6-fragmentation_2023.pptx","link":[{"href":"urn:x-pdf:468ca9827762f0c253d83c12b2556b5a"},{"href":"vault:/S2/SAM/SAM6-fragmentation_2023.pdf"}],"documentFingerprint":"468ca9827762f0c253d83c12b2556b5a"},"uri":"vault:/S2/SAM/SAM6-fragmentation_2023.pdf","target":[{"source":"vault:/S2/SAM/SAM6-fragmentation_2023.pdf","selector":[{"type":"TextPositionSelector","start":7963,"end":7964},{"type":"TextQuoteSelector","exact":"⋉","prefix":"ent = Client1.nclientCde i= Cde ","suffix":"Client ipour i dans{1; 2}25ncden"}]}]}
>```
>%%
>*%%PREFIX%%ent = Client1.nclientCde i= Cde%%HIGHLIGHT%% ==⋉== %%POSTFIX%%Client ipour i dans{1; 2}25ncden*
>%%LINK%%[[#^cbun0cbih9e|show annotation]]
>%%COMMENT%%
>Semi-jointure
>%%TAGS%%
>
^cbun0cbih9e


>%%
>```annotation-json
>{"created":"2023-03-21T15:42:13.295Z","text":"Union pour retrouver la structure intiale.","updated":"2023-03-21T15:42:13.295Z","document":{"title":"Microsoft PowerPoint - SAM6-fragmentation_2023.pptx","link":[{"href":"urn:x-pdf:468ca9827762f0c253d83c12b2556b5a"},{"href":"vault:/S2/SAM/SAM6-fragmentation_2023.pdf"}],"documentFingerprint":"468ca9827762f0c253d83c12b2556b5a"},"uri":"vault:/S2/SAM/SAM6-fragmentation_2023.pdf","target":[{"source":"vault:/S2/SAM/SAM6-fragmentation_2023.pdf","selector":[{"type":"TextPositionSelector","start":8173,"end":8178},{"type":"TextQuoteSelector","exact":"union","prefix":" 4Cde2qté 510Reconstruction par ","suffix":"Cde = Cde 1⋃Cde 2= ⋃iCde iFragme"}]}]}
>```
>%%
>*%%PREFIX%%4Cde2qté 510Reconstruction par%%HIGHLIGHT%% ==union== %%POSTFIX%%Cde = Cde 1⋃Cde 2= ⋃iCde iFragme*
>%%LINK%%[[#^rho3opmslaf|show annotation]]
>%%COMMENT%%
>Union pour retrouver la structure intiale.
>%%TAGS%%
>
^rho3opmslaf


>%%
>```annotation-json
>{"created":"2023-03-21T15:42:53.584Z","text":"$n$ semi-jointures","updated":"2023-03-21T15:42:53.584Z","document":{"title":"Microsoft PowerPoint - SAM6-fragmentation_2023.pptx","link":[{"href":"urn:x-pdf:468ca9827762f0c253d83c12b2556b5a"},{"href":"vault:/S2/SAM/SAM6-fragmentation_2023.pdf"}],"documentFingerprint":"468ca9827762f0c253d83c12b2556b5a"},"uri":"vault:/S2/SAM/SAM6-fragmentation_2023.pdf","target":[{"source":"vault:/S2/SAM/SAM6-fragmentation_2023.pdf","selector":[{"type":"TextPositionSelector","start":8376,"end":8392},{"type":"TextQuoteSelector","exact":"Semi‐jointure(s)","prefix":"s dans la relation à fragmenter•","suffix":"Exemple avec2semi‐jointures•Pers"}]}]}
>```
>%%
>*%%PREFIX%%s dans la relation à fragmenter•%%HIGHLIGHT%% ==Semi‐jointure(s)== %%POSTFIX%%Exemple avec2semi‐jointures•Pers*
>%%LINK%%[[#^dww2rs1fcof|show annotation]]
>%%COMMENT%%
>$n$ semi-jointures
>%%TAGS%%
>
^dww2rs1fcof



>%%
>```annotation-json
>{"created":"2023-03-21T15:43:47.025Z","text":"+ age","updated":"2023-03-21T15:43:47.025Z","document":{"title":"Microsoft PowerPoint - SAM6-fragmentation_2023.pptx","link":[{"href":"urn:x-pdf:468ca9827762f0c253d83c12b2556b5a"},{"href":"vault:/S2/SAM/SAM6-fragmentation_2023.pdf"}],"documentFingerprint":"468ca9827762f0c253d83c12b2556b5a"},"uri":"vault:/S2/SAM/SAM6-fragmentation_2023.pdf","target":[{"source":"vault:/S2/SAM/SAM6-fragmentation_2023.pdf","selector":[{"type":"TextPositionSelector","start":8420,"end":8447},{"type":"TextQuoteSelector","exact":"Personne(numP, nom, premon)","prefix":"e(s)Exemple avec2semi‐jointures•","suffix":"•4 fragments pour a=[0,18,25,60,"}]}]}
>```
>%%
>*%%PREFIX%%e(s)Exemple avec2semi‐jointures•%%HIGHLIGHT%% ==Personne(numP, nom, premon)== %%POSTFIX%%•4 fragments pour a=[0,18,25,60,*
>%%LINK%%[[#^yaw7ykr9oc|show annotation]]
>%%COMMENT%%
>+ age
>%%TAGS%%
>
^yaw7ykr9oc


>%%
>```annotation-json
>{"created":"2023-03-21T15:44:43.208Z","text":"Faire une semi-jointure préserve les propriétés.","updated":"2023-03-21T15:44:43.208Z","document":{"title":"Microsoft PowerPoint - SAM6-fragmentation_2023.pptx","link":[{"href":"urn:x-pdf:468ca9827762f0c253d83c12b2556b5a"},{"href":"vault:/S2/SAM/SAM6-fragmentation_2023.pdf"}],"documentFingerprint":"468ca9827762f0c253d83c12b2556b5a"},"uri":"vault:/S2/SAM/SAM6-fragmentation_2023.pdf"}
>```
>%%
>*%%PREFIX%%%%HIGHLIGHT%% ==== %%POSTFIX%%*
>%%LINK%%[[#^plvjr1p0gee|show annotation]]
>%%COMMENT%%
>Faire une semi-jointure préserve les propriétés.
>%%TAGS%%
>
^plvjr1p0gee


>%%
>```annotation-json
>{"created":"2023-03-21T15:45:38.181Z","text":"Les requêtes vont utilisées un petit pourcent de ces attributs (sur des centaines) => réduire la largeur des tables.\n\nOn projette sur le numéro de commande \n\nComment choisir la liste des attributs ? Doivent être utiles aux requêtes, plein de techniques qui permettent de mesurer l'utilité conjointe de deux attributs = affinité entre attributs.","updated":"2023-03-21T15:45:38.181Z","document":{"title":"Microsoft PowerPoint - SAM6-fragmentation_2023.pptx","link":[{"href":"urn:x-pdf:468ca9827762f0c253d83c12b2556b5a"},{"href":"vault:/S2/SAM/SAM6-fragmentation_2023.pdf"}],"documentFingerprint":"468ca9827762f0c253d83c12b2556b5a"},"uri":"vault:/S2/SAM/SAM6-fragmentation_2023.pdf"}
>```
>%%
>*%%PREFIX%%%%HIGHLIGHT%% ==== %%POSTFIX%%*
>%%LINK%%[[#^h46bh2vkeb|show annotation]]
>%%COMMENT%%
>Les requêtes vont utilisées un petit pourcent de ces attributs (sur des centaines) => réduire la largeur des tables.
>
>On projette sur le numéro de commande 
>
>Comment choisir la liste des attributs ? Doivent être utiles aux requêtes, plein de techniques qui permettent de mesurer l'utilité conjointe de deux attributs = affinité entre attributs.
>%%TAGS%%
>
^h46bh2vkeb


>%%
>```annotation-json
>{"created":"2023-03-21T15:49:31.569Z","text":"Comment allouer mes fragments ? Technique d'optimisation classique","updated":"2023-03-21T15:49:31.569Z","document":{"title":"Microsoft PowerPoint - SAM6-fragmentation_2023.pptx","link":[{"href":"urn:x-pdf:468ca9827762f0c253d83c12b2556b5a"},{"href":"vault:/S2/SAM/SAM6-fragmentation_2023.pdf"}],"documentFingerprint":"468ca9827762f0c253d83c12b2556b5a"},"uri":"vault:/S2/SAM/SAM6-fragmentation_2023.pdf"}
>```
>%%
>*%%PREFIX%%%%HIGHLIGHT%% ==== %%POSTFIX%%*
>%%LINK%%[[#^upx97lr5k3|show annotation]]
>%%COMMENT%%
>Comment allouer mes fragments ? Technique d'optimisation classique
>%%TAGS%%
>
^upx97lr5k3
