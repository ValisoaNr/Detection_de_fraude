import random
import math
from collections import deque

# definir une valeur de p selon le nombre de sommet
def calculer_p(n , alpha=2.0) :
    if n <= 100:
        return 0.3
    elif n <= 1000:
        return alpha * math.log(n) / n
    return math.log(n) / n


def ajouter_aretes(n, p, d_max) :
    # un graphe aleatoire selon p (donc l'algorihtme 2) 
    adj = [[] for _ in range(n)]
    voisins = [set() for _ in range(n)]
    for i in range(n - 1):
        for j in range(i+1 , n) : 
            if j in voisins[i]:
                continue
            if len(adj[i]) >= d_max or len(adj[j]) >= d_max:
                continue
            if random.random() < p:
                adj[i].append(j)
                adj[j].append(i)
                voisins[i].add(j)
                voisins[j].add(i)

    return adj , voisins

# Verification et correction de la connexite (algo. 3)
def corriger_connexite(n, adj):
    visite = [False] * n
    file = deque([0])
    visite[0] = True

    while file :
        u = file.popleft()
        for v in adj[u] :
            if not visite[v]: 
                visite[v] = True
                file.append(v)

    for i in range(n) :
        if visite[i]:
            continue
        u = random.choice([j for j in range(n) if visite[j]])
        adj[u].append(i)
        adj[i].append(u)
        visite[i] = True

    return adj


def generer_graphe(n , alpha=2.0 , d_max=None):
    if d_max is None:
        d_max = n - 1
    p = calculer_p(n, alpha)
    adj, _ = ajouter_aretes(n , p , d_max)
    adj = corriger_connexite(n , adj)
    return adj


if __name__ == "__main__":
    n = 10000
    g = generer_graphe(n , alpha=2.0)
    for i , v in enumerate(g) :
        print(f"{i} : {v}")
