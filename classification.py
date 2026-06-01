def tous_voisins(v , candidats , adj_sets) :
    # Pour verifier si tous ce qui est dans candidats est voisin de v
    for w in candidats :
        if v not in adj_sets[w] :
            return False
    return True

def classification(adj , n) :
    couleur = [-1] * n
    for i in range(n) :
        interdites = set()
        for v in adj[i] :
            if couleur[v] != -1 :
                interdites.add(couleur[v])
        c = 0
        while c in interdites :
            c = c + 1
        couleur[i] = c

    cliques = []
    adj_sets = []
    for voisins in adj :
        adj_sets.append(set(voisins))

    for i in range(n) :
        candidats = {i}
        for v in adj[i] :
            if v <= i :
                continue
            if tous_voisins(v, candidats, adj_sets) :
                candidats.add(v)
        if len(candidats) >= 2 :
            cliques.append(candidats)

    return couleur , cliques
