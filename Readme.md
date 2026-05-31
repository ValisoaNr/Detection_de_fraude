# Détection de fraude par analyse de graphe

Projet L2 — Mai 2026

## Description

Ce projet construit un graphe aléatoire connexe, non orienté et sans boucle, puis identifie tous les sous-graphes complets au sein de ce graphe. L'objectif final est de détecter des communautés suspectes dans un réseau.

## Structure du projet

```
projet/
├── generation_graphe.py   
├── classification.py (en cours)
└── README.md
```

## Utilisation

**Generer le graphe aleatoire :**
```bash
python3 generation_graphe.py
```

Paramètres modifiables dans le `__main__` de generation\_graphe.py:
- `n` : nombre de sommets
- `alpha` : densité du graphe (par défaut 2.0)
- `d_max` : degré maximum par sommet

## Étapes du projet

1. Calcul de `p` selon `n`
2. Construction de `G` aléatoirement selon `p`
3. Vérification et correction de la connexité (Parcours en largeur)
4. Classification — détection des sous-graphes complets

## Dépendances

Python 3.x — aucune bibliothèque externe requise pour le moment.

## Livrable de ce projet
```url
https://fr.overleaf.com/read/zfxnbgfhdbyr#b4d2ae
```

