# Détection de fraude par analyse de graphe

Projet L2 — Mai 2026

## Description

Ce projet est une construction de graphe aléatoire connexe, non orienté et sans boucle ; et d'identifier les sous-graphes complets au sein de ce graphe.

## Structure du projet

```
projet/
├── generation_graphe.py   
├── classification.py
└── README.md
```

## Utilisation

**Générer le graphe aléatoire**
La création de graphe aléatoire connexe , non orienté et sans boucle se fait par l'utilisation des fonctions dans `generation_graphe.py`.

**Classifier les sommets du graphe**
La classification des sommets et la détection des sous-graphes complets se fait via `classification.py`.

```python
from generation_graphe import generer_graphe
from classification import classification

adj = generer_graphe(n=1000)
couleur , cliques = classification(adj, n=1000)

for i , c in enumerate(couleur):
    print(f"sommet {i} -> couleur {c}")
for cl in cliques:
    print(f"clique : {sorted(cl)}")
```

## Étapes du projet

1. Calcul de `p` selon `n`
2. Construction de `G` aléatoirement selon `p`
3. Vérification et correction de la connexité (parcours en largeur)
4. Classification — coloration gloutonne et détection des sous-graphes complets

## Détail des fonctions

### `generation_graphe.py`

| Fonction | Rôle |
|---|---|
| `calculer_p(n , alpha)` | Calcule la probabilité d'arête selon `n` |
| `ajouter_aretes(n , p , d_max)` | Construit le graphe aléatoire |
| `corriger_connexite(n , adj)` | Garantit la connexité par BFS |
| `generer_graphe(n , alpha , d_max)` | Fonction principale — retourne `adj` |

### `classification.py`

| Fonction | Rôle |
|---|---|
| `tous_voisins(v , candidats , adj_sets)` | Vérifie que `v` est voisin de chaque sommet dans `candidats` |
| `classification(adj , n)` | Coloration gloutonne + détection des cliques |

## Dépendances

Python 3.x — aucune bibliothèque externe requise.

## Livrable de ce projet

```
https://fr.overleaf.com/read/zfxnbgfhdbyr#b4d2ae
```
