# SAM - TME4
## Q1
### Jointure par hachage
(J4) coût( R ⋈a S ) = coût(R) + coût(S)
ici R = AchatProduit
S = Commande

cout(R) = P(R) = 2119
cout(S) = P(S) = 906

donc cout(a) = 2119+906 = 3025

Plan d'exécution
```
PLAN_TABLE_OUTPUT                                                               
--------------------------------------------------------------------------------
Plan hash value: 2856117398                                                     
                                                                                
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
|   5 |   TABLE ACCESS BY INDEX ROWID| ACHATPRODUIT   |     4 |   252 |     3   (0)|
------------------------------------------------------------------------------------
                                                                                    
Predicate Information (identified by operation id):                                 
---------------------------------------------------                                 
                                                                                    
   4 - access("A"."NUMCDE"="C"."NUMCDE")                                            
                                                                                                                               
```

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
