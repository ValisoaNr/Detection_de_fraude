def cliques_rec(R , P , X , adj_sets , cliques) :
    if len(P) == 0 and len(X) == 0 :
        if len(R) >= 3 :
            cliques.append(R.copy())
        return

    union_P_X = P.union(X)
    pivot = -1
    meilleur_score = -1
    for v in union_P_X :
        score = 0
        for voisin in adj_sets[v] :
            if voisin in P :
                score = score + 1
        if score > meilleur_score :
            meilleur_score = score
            pivot = v

    non_voisins_pivot = P.difference(adj_sets[pivot])
    for v in list(non_voisins_pivot) :
        nouveau_R = R.union({v})
        nouveau_P = P.intersection(adj_sets[v])
        nouveau_X = X.intersection(adj_sets[v])

        cliques_rec(nouveau_R , nouveau_P , nouveau_X , adj_sets , cliques)
        P.remove(v)
        X.add(v)


def classification(adj , n) :
    def nombre_de_voisins(sommet) :
        return len(adj[sommet])

    sommets_tries = sorted(range(n) , key=nombre_de_voisins , reverse=True)
    couleur = [-1] * n
    for u in sommets_tries :
        couleurs_interdites = set()
        for v in adj[u] :
            if couleur[v] != -1 :
                couleurs_interdites.add(couleur[v])

        c = 0
        while c in couleurs_interdites:
            c = c + 1
        couleur[u] = c

    adj_sets = []
    for voisins in adj :
        adj_sets.append(set(voisins))

    cliques = []
    tous_les_sommets = set(range(n))
    cliques_rec(set() , tous_les_sommets, set() , adj_sets , cliques)

    return couleur , cliques
