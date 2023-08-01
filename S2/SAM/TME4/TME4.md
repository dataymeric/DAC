# SAM - TME5
## Q1
### Jointure par hachage
(J4) coût( R ⋈a S ) = coût(R) + coût(S)
ici R = AchatProduit
S = Commande

cout(R) = P(R) = 2119 * 0.27 = 572
cout(S) = P(S) = 906 = 244

donc cout(a) = 2119+906 = 3025 * 0.27 = 816 MAIS on a un cout total à 1902, donc un peu plus de deux fois par rapport à un requete opti mais 1.5 fois moins par rapport à un cout sans optimisation... c'est parce que c'est une jointure par hachage externe car la requête ne tient pas en mémoire. donc ici en théorie, taille de la mémoire : ouais je saps pcq oracle a pas le même algo que le notre dans le cours

hypothèse lecture séquentielle : optimisation * 0.27

Plan d'exécution
```
PLAN_TABLE_OUTPUT                                                               
--------------------------------------------------------------------------------
Plan hash value: 2856117398                                                     
                    able are in sequence and the index on the join column of the inner table is clustered, or the number of rows retrieved in the inner table through the index is small.                                                            
--------------------------------------------------------------------------------
| Id  | Operation          | Name         | Rows  | Bytes |TempSpc| Cost (%CPU)|
--------------------------------------------------------------------------------
|   0 | SELECT STATEMENT   |              |   226K|    36M|       |  1902   (1)|
|*  1 |  HASH JOIN         |              |   226K|    36M|  6656K|  1902   (1)|
|   2 |   TABLE ACCESS FULL| COMMANDE     | 56741 |  5984K|       |   243   (1)|
|   3 |   TABLE ACCESS FULL| ACHATPRODUIT |   226K|    13M|       |   567   (1)|
--------------------------------------------------------------------------------
                                                                                
Predicate Information (identified by operation id):                             
---------------------------------------------------                             
                                                                                
   1 - access("A"."NUMCDE"="C"."NUMCDE")                                        
                                                              
```

foreach tuple 

### Jointure par boucles imbriquées  
(J1) coût( R ⋈a S ) = coût(R) + card(R) × card(σ a=v (S)) si index S(a)  
(J2) OU = coût(R) + P(R) × P(S) si S est une table sans index S(a)  
Si S n’est pas une table mais est une expression, il faut rajouter son coût d’évaluation et le coût de la stocker.  
(J3) coût(R ⋈ a S) = coût(S) + P(S) + coût(R) + P(R) × P(S)

JOINTURE SUR NUMCDE + on a index S(a) ici Commande(numCde) qui est notre index CLE_COMMANDE
On applique J1
2119 + 226736 * card(S) / n_valeurs_distinctes 
2119 + 226736 * 56741 / 56741 = 228855

très couteux 

```
PLAN_TABLE_OUTPUT                                                                   
------------------------------------------------------------------------------------
Plan hash value: 1269448014                                                         
                                                                                    
------------------------------------------------------------------------------------
| Id  | Operation                    | Name           | Rows  | Bytes | Cost (%CPU)|
------------------------------------------------------------------------------------
|   0 | SELECT STATEMENT             |                |   226K|    36M|   170K  (1)|
|   1 |  NESTED LOOPS                |                |       |       |            |
|   2 |   NESTED LOOPS               |                |   226K|    36M|   170K  (1)|
|   3 |    TABLE ACCESS FULL         | COMMANDE       | 56741 |  5984K|   243   (1)|
|*  4 |    INDEX RANGE SCAN          | I_ACHAT_NUMCDE |     4 |       |     2   (0)|
|   5 |   TABLE ACCESS BY INDEX ROWID| ACHATPRODUIT   |     4 |   252 |     3   (0)|	​￼for s in R	​￼for s in R	​￼for s in R
------------------------------------------------------------------------------------
                                                                                    
Predicate Information (identified by operation id):                                 
---------------------------------------------------                                 
                                                                                    
   4 - access("A"."NUMCDE"="C"."NUMCDE")                                            
                                                                                                                               
```

for r in R (AchatProduit)
	for i in IndexS.getRowIds(r.a) (Commande)
		s = S.getTuple(i)
		add (r, s) in result


### Jointure par tri puis fusion
coût(R ⨝TF R.a=S.a S) = 3 (page(R) + page(S))

3 * (2119+906) = 9075

```
PLAN_TABLE_OUTPUT                                                                
---------------------------------------------------------------------------------
Plan hash value: 3783546590                                                      
                                                                                 
---------------------------------------------------------------------------------
| Id  | Operation           | Name         | Rows  | Bytes |TempSpc| Cost (%CPU)|
---------------------------------------------------------------------------------
|   0 | SELECT STATEMENT    |              |   226K|    36M|       |  5598   (1)|
|   1 |  MERGE JOIN         |              |   226K|    36M|       |  5598   (1)|
|   2 |   SORT JOIN         |              | 56741 |  5984K|    14M|  1621   (1)|
|   3 |    TABLE ACCESS FULL| COMMANDE     | 56741 |  5984K|       |   243   (1)|
|*  4 |   SORT JOIN         |              |   226K|    13M|    36M|  3977   (1)|
|   5 |    TABLE ACCESS FULL| ACHATPRODUIT |   226K|    13M|       |   567   (1)|
---------------------------------------------------------------------------------
                                                                                 
Predicate Information (identified by operation id):                              
---------------------------------------------------                              
                                                                                 
   4 - access("A"."NUMCDE"="C"."NUMCDE")                                         
       filter("A"."NUMCDE"="C"."NUMCDE")                                         

```

r <- premier tuple de R
s <- premier tuple de S
tant que r et s existent:
	si r.A = s.A 
		tmpR <- r
		tant que s existe
			si s.A = r.A
				foreach t in tmpR
					add (s, t) -> result
						S <- Suivant(S)
	si r.A < s.A
		R <- suivant(R)
	sinon si s.A < r.A
		s <- suivant(S)

LE PSEUDOCODE LE MOINS CLAIR DU MONDE !!!!!!!!!!!!!!

## Q2 : la directive ORDERED

jointure hash triée par ordre des tables dans le from (AchatProduit, Commande)
AchatProduit est à gauche, elle est lue pour construire une table de hachage temporaire (de 16 mo, plus qu'avant).

```
PLAN_TABLE_OUTPUT                                                               
--------------------------------------------------------------------------------
Plan hash value: 22724511                                                       
                                                                                
--------------------------------------------------------------------------------
| Id  | Operation          | Name         | Rows  | Bytes |TempSpc| Cost (%CPU)|
--------------------------------------------------------------------------------
|   0 | SELECT STATEMENT   |              |   226K|    36M|       |  1903   (1)|
|*  1 |  HASH JOIN         |              |   226K|    36M|    16M|  1903   (1)|
|   2 |   TABLE ACCESS FULL| ACHATPRODUIT |   226K|    13M|       |   567   (1)|
|   3 |   TABLE ACCESS FULL| COMMANDE     | 56741 |  5984K|       |   243   (1)|
--------------------------------------------------------------------------------
                                                                                
Predicate Information (identified by operation id):                             
---------------------------------------------------                             
                                                                                
   1 - access("A"."NUMCDE"="C"."NUMCDE")                                        
                                                                                
```

ouais, je sais pas trop quoi dire, à part que c'est moins opti car oracle fait un hachage ordonné  sur Commande 2022

hachage + opti sur cette requete.

## Q3 : optimalité
https://docs.oracle.com/cd/B28359_01/server.111/b28274/optimops.htm#i49183

Nested loops optimal quand très peu de données et que la jointure est bien ("a good driving condition between the two tables"). ordre des tables important.

sinon quand il ya a beaucoup de données, hash join est toujours le plus optimal. soit : il y a beaucoup de données, soit il ya beaucoup de jointures à faire.

merge join quand aucun rapport entre 2 tables (2 tables indépendantes). en généra, hash join mieux sauf si deux conditions :
les lignes sont triées, et qu'il n'y a pas d'opération de tri à effectuer.
sort merge utile si la condition de jointure n'est pas une égalité (je savais pas qu'on peut faire ça mdr)



