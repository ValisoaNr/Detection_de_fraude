from generation_graphe import generer_graphe
from classification import classification

adj = generer_graphe(n=1000 , alpha=3)
couleur , cliques = classification(adj , n=1000)

nb_couleurs = max(couleur) + 1
print(f"Le graphe a 1000 sommets : {nb_couleurs} couleurs utilisé et {len(cliques)} cliques detecté")

for i , c in enumerate(couleur) :
    print(f"sommet {i:4d} : couleur {c}")

for l in cliques :
    print(f"clique : {sorted(l)}")
