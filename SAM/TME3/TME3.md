```
 Plan hash value: 1761007982

------------------------------------------------------------------------------------------

| Id | Operation | Name | Rows | Bytes | Cost (%CPU)|

------------------------------------------------------------------------------------------

| 0 | SELECT STATEMENT | | 490 | 8820 | 197 (3)|

| 1 | TABLE ACCESS BY INDEX ROWID | ACHATPRODUIT | 490 | 8820 | 197 (3)|

| 2 | BITMAP CONVERSION TO ROWIDS | | | | |

| 3 | BITMAP AND | | | | |

| 4 | BITMAP CONVERSION FROM ROWIDS| | | | |

| 5 | SORT ORDER BY | | | | |

|* 6 | INDEX RANGE SCAN | I_ACHAT_PRIX | | | 7 (0)|

| 7 | BITMAP CONVERSION FROM ROWIDS| | | | |

| 8 | SORT ORDER BY | | | | |

|* 9 | INDEX RANGE SCAN | I_ACHAT_QUANTITE | | | 92 (0)|

------------------------------------------------------------------------------------------

Predicate Information (identified by operation id):

---------------------------------------------------

6 - access("PRIX"<2000)

filter("PRIX"<2000)

9 - access("QUANTITE">40)

filter("QUANTITE">40)

Column Projection Information (identified by operation id):

-----------------------------------------------------------

1 - "NUMCDE"[NUMBER,22], "NUMACHAT"[NUMBER,22]

2 - "A".ROWID[ROWID,10]

3 - STRDEF[BM VAR, 10], STRDEF[BM VAR, 10], STRDEF[BM VAR, 32496]

4 - STRDEF[BM VAR, 10], STRDEF[BM VAR, 10], STRDEF[BM VAR, 32496]

5 - (#keys=1) "A".ROWID[ROWID,10]

6 - "A".ROWID[ROWID,10]

7 - STRDEF[BM VAR, 10], STRDEF[BM VAR, 10], STRDEF[BM VAR, 32496]

8 - (#keys=1) "A".ROWID[ROWID,10]

9 - "A".ROWID[ROWID,10]
```

f)
```
Plan hash value: 938908017

---------------------------------------------------------------------------------

| Id | Operation | Name | Rows | Bytes | Cost (%CPU)|

---------------------------------------------------------------------------------

| 0 | SELECT STATEMENT | | 490 | 8820 | 1098 (1)|

|* 1 | VIEW | index$_join$_001 | 490 | 8820 | 1098 (1)|

|* 2 | HASH JOIN | | | | |

|* 3 | HASH JOIN | | | | |

|* 4 | HASH JOIN | | | | |

|* 5 | INDEX RANGE SCAN | I_ACHAT_PRIX | 490 | 8820 | 8 (13)|

|* 6 | INDEX RANGE SCAN | I_ACHAT_QUANTITE | 490 | 8820 | 95 (4)|

| 7 | INDEX FAST FULL SCAN| I_ACHAT_NUMACHAT | 490 | 8820 | 557 (1)|

| 8 | INDEX FAST FULL SCAN | I_ACHAT_NUMCDE | 490 | 8820 | 670 (1)|

---------------------------------------------------------------------------------

Predicate Information (identified by operation id):

---------------------------------------------------

1 - filter("PRIX"<2000 AND "QUANTITE">40)

2 - access(ROWID=ROWID)

3 - access(ROWID=ROWID)

4 - access(ROWID=ROWID)

5 - access("PRIX"<2000)

6 - access("QUANTITE">40)

Column Projection Information (identified by operation id):

-----------------------------------------------------------

1 - "NUMCDE"[NUMBER,22], "NUMACHAT"[NUMBER,22],

"QUANTITE"[NUMBER,22], "PRIX"[NUMBER,22]
```

Comparer les plans d’exécution pour deux situations différentes lorsque les index existants sont :  
- I_achat_prix, I_achat_quantite, I_achat_numCde  
- I_achat_prix, I_achat_quantite, I_achat_numCde et I_achat_numAchat  
Dans quelle situation peut‐on dire que les index couvrent la requête ?
couvre dans les 2 cas par jointure

a) prix < 1000 and quantite =2  
direct access
b) quantite = 2  
filtre
c) prix < 1000  
range scan
d) prix > 1000
filtre .???
