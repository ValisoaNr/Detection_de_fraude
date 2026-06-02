# Détection de fraude par analyse de graphe

Projet L2 — Mai 2026

## Description

Construction d'un graphe aleatoire connexe , non orienté et sans boucle , puis identification des sous graphes complets (cliques)

## Structure du projet

```
projet/
├── generation_graphe.py
├── classification.py
├── main.py
└── Readme.md
```

## Utilisation

```python
python3 main.py
```

ou bien :

```python
from generation_graphe import generer_graphe
from classification import classification

adj = generer_graphe(n=1000)
couleur , cliques = classification(adj , n=1000)
```

## Etapes du projet

1. Calcul de `p` selon `n`
2. Construction de `G` aleatoirement selon `p`
3. Verification et correction de la connexité (parcours en largeur)
4. Classification : coloration + detection des cliques (Bron-Kerbosch avec pivot)

## Detail des fonctions

### `generation_graphe.py`

| Fonction | Rôle |
|---|---|
| `calculer_p(n , alpha)` | calcule la probabilité d'arete selon `n` |
| `ajouter_aretes(n , p , d_max)` | construit le graphe aleatoire |
| `corriger_connexite(n , adj)` | garantit la connexité par BFS |
| `generer_graphe(n , alpha , d_max)` | fonction principale : retourne `adj` |

### `classification.py`

| Fonction | Rôle |
|---|---|
| `cliques_rec(R , P , X , adj_sets , cliques)` | Bron-Kerbosch recursif avec pivot |
| `classification(adj , n)` | coloration gloutonne + detection des cliques |

## Dependances

Python 3.x — aucune bibliotheque externe n'est requise

## Livrable

```
https://fr.overleaf.com/read/zfxnbgfhdbyr#b4d2ae
```
