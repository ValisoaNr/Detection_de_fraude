# Detection de fraude via etude de graphes 

Projet de recherche -- Neo4j , Python , Cypher
Annee 2025-2026

---

## Description du projet

Ce projet modelise et analyse la diffusion de comportements a risque dans
un reseau social universitaire. Chaque etudiant est represente comme un
noeud dans un graphe, et chaque relation sociale -- amitie, colocation,
cours partage -- est une arete. L'objectif est d'identifier les communautes
a risque eleve et les individus influents dans la propagation du comportement,
afin d'orienter des actions de prevention.

Le graphe est construit dans Neo4j et enrichi par des algorithmes de la
bibliotheque Graph Data Science. Une interface en Python permet de piloter
l'ensemble des operations depuis une fenetre simple.

---

## Problematique

Les approches preventives classiques traitent les individus de maniere
isolee. Elles ignorent le fait qu'un comportement comme la consommation
de cannabis se diffuse dans les reseaux de relations, pas seulement selon
les caracteristiques personnelles de chaque individu.

La question centrale du projet est la suivante : est-ce que la position
d'un etudiant dans son reseau social -- son influence, son appartenance a
un groupe, son role de pont entre communautes -- permet de predire son
exposition a un comportement a risque mieux que ses seuls attributs
individuels comme le stress ou la filiere d'etudes ?

---

## Structure du projet

```
projet/
    main.py              Point d'entree -- lance l'application
    configuration.py     Parametres de connexion et requetes Cypher
    connexion.py         Driver Neo4j et execution des requetes
    interface.py         Fenetre Tkinter et logique d'affichage

    exemple_initiale/
        students.csv         Profils des etudiants
        friendships.csv      Relations sociales entre etudiants
        groups.csv           Groupes (residences, clubs, TD)
        memberships.csv      Appartenances etudiant-groupe

    requetes/
        importation.csv      Requetes d'importation initiale
        testETgds.csv        Requetes d'analyse et GDS
        incremental.csv      Requetes de mise a jour du graphe
```

---

## Prerequis

**Neo4j 5.x Community Edition**
Telechargement : https://neo4j.com/download/
Plugins requis : Graph Data Science (GDS) 2.x

**Python 3.10 ou superieur**

**Bibliotheque Python**

```
pip install neo4j
```

Tkinter est inclus nativement dans Python, aucune installation
supplementaire n'est necessaire.

---

## Installation et lancement

**Etape 1 -- Demarrer Neo4j**

Lancer Neo4j Desktop et demarrer la base de donnees. Verifier que
le service est accessible sur bolt://localhost:7687.

**Etape 2 -- Copier les CSV dans Neo4j**

Ouvrir le dossier d'import de Neo4j via Neo4j Desktop en cliquant
sur les trois points du projet puis "Open folder" puis "Import".
Copier les quatre fichiers CSV dans ce dossier :

```
students.csv
friendships.csv
groups.csv
memberships.csv
```

**Etape 3 -- Lancer l'application**

```
python3 main.py
```

**Etape 4 -- Se connecter**

Saisir l'URI, l'utilisateur et le mot de passe dans la barre de
connexion en haut de la fenetre, puis cliquer sur Connecter.

---

## Les donnees CSV

### students.csv

Contient les profils des etudiants. Chaque ligne est un etudiant.

| Colonne            | Type    | Description                              |
|--------------------|---------|------------------------------------------|
| id                 | texte   | Identifiant unique (S0000, S0001, ...)   |
| age                | entier  | Age de l'etudiant                        |
| filiere            | texte   | Filiere d'etudes                         |
| annee              | entier  | Annee d'etudes (1 a 5)                   |
| logement           | texte   | Type de logement                         |
| stress_score       | entier  | Score de stress declare (1 a 10)         |
| consomme_cannabis  | 0 ou 1  | Comportement declare (1 = oui, 0 = non)  |
| frequence_cannabis | texte   | Frequence (jamais, rare, hebdo, quotidien)|

### friendships.csv

Contient les relations sociales entre etudiants.

| Colonne   | Type   | Description                                  |
|-----------|--------|----------------------------------------------|
| source    | texte  | Identifiant de l'etudiant source             |
| target    | texte  | Identifiant de l'etudiant cible              |
| type      | texte  | Type de relation (amitie, colocation, cours) |
| intensite | entier | Force du lien (1 = faible, 4 = fort)         |

### groups.csv

Contient les groupes auxquels les etudiants peuvent appartenir.

| Colonne  | Type   | Description                                  |
|----------|--------|----------------------------------------------|
| group_id | texte  | Identifiant du groupe (G000, G001, ...)      |
| type     | texte  | Type de groupe (residence, club, td_group)   |
| taille   | entier | Nombre de membres dans le groupe             |

### memberships.csv

Contient les appartenances entre etudiants et groupes.

| Colonne    | Type  | Description                      |
|------------|-------|----------------------------------|
| student_id | texte | Identifiant de l'etudiant        |
| group_id   | texte | Identifiant du groupe            |

---

## Utilisation de l'interface

L'interface est organisee en deux zones.

**A gauche -- les onglets de requetes**

Trois onglets sont disponibles.

L'onglet Importation contient les requetes pour charger les donnees
CSV dans Neo4j. Executer les requetes dans cet ordre : etudiant,
groupe, connait, appartientA.

L'onglet Analyse contient les requetes pour interroger et analyser
le graphe apres import : compter les noeuds, voir les filieres,
identifier les influenceurs.

L'onglet GDS contient les requetes pour les algorithmes de graphe.
Executer d'abord projectionGDSsocial, puis les algorithmes dans
l'ordre souhaite, et terminer par dropProjection.

L'onglet incremental contient les requetes qui rend le base de donnee
dynamique c'est a dire de la mis a jour des relations (ou groupes ou 
etudiant ou comportement) , de supprimer les relations , ou visionner 
aussi les relations ou les changements .

**A droite -- les resultats**

Le tableau affiche les resultats de chaque requete executee. Les
colonnes s'adaptent automatiquement au retour de Neo4j. Pour les
requetes sans retour de lignes (import, GDS), le tableau affiche
le resume des operations effectuees.

Le journal en bas enregistre toutes les executions avec leur statut.

---

## Ordre d'execution recommande

Pour une analyse complete, executer les requetes dans cet ordre.

**Import initial**

```
toutSuppr          Si la base contient des donnees existantes
etudiant           Charger les 500 etudiants
groupe             Charger les 40 groupes
connait            Creer les 1800 relations sociales
appartientA        Creer les 994 appartenances aux groupes
```

**Verification**

```
compteEtudiant     Doit afficher 500
compteRelation     Doit afficher 1800
```

**Algorithmes GDS**

```
projectionGDSsocial    Projeter le graphe en memoire
EcrirePR               Calculer le PageRank
GDSlouvain             Detecter les communautes
ponts_comm             Calculer la Betweenness
dropProjection         Liberer la memoire
```

**Analyse des resultats**

```
topInfluenceur     Les 15 noeuds les plus influents
tauxLouvain        Taux de consommation par communaute
statFiliere        Prevalence par filiere
voisinageCons      Exposition autour d'un noeud connu
```

---

## Le graphe incremental

Le fichier incremental.csv contient des requetes pour mettre a jour
le graphe sans tout reconstruire. Cela permet de suivre l'evolution
du reseau dans le temps.

Les principales operations disponibles sont les suivantes.

Ajouter un nouvel etudiant sans toucher les noeuds existants. Modifier
le comportement d'un etudiant avec horodatage automatique de la date
de changement. Ajouter une nouvelle relation entre deux etudiants avec
la date de creation. Cloturer une relation sans la supprimer en ajoutant
une date de fin. Supprimer definitivement un etudiant ou une relation.
Consulter uniquement les relations encore actives ou les changements
survenus recemment.

Avant d'executer ces requetes, remplacer les valeurs generiques
ID_ETUDIANT, id_a et id_b par les identifiants reels.

---

## Architecture technique

```
main.py
  Lance FenetrePrincipale depuis interface.py

configuration.py
  URI, identifiants par defaut
  REQUETES_IMPORTATION
  REQUETES_ANALYSE
  REQUETES_GDS

connexion.py
  ConnexionNeo4j.connecter()
  ConnexionNeo4j.executer()
  ConnexionNeo4j.extraire_resume()

interface.py
  FenetrePrincipale
    construire_barre_connexion()
    construire_zone_principale()
    construire_onglets()
    remplir_onglet()
    construire_zone_resultat()
    lancer_connexion()      -- thread background
    lancer_requete()        -- thread background
    afficher_resultats()
    journaliser()
    verifier_file_attente() -- boucle 100ms
```

Toutes les operations Neo4j sont executees dans des threads separes
pour que l'interface reste reactive pendant les requetes longues. La
communication entre les threads et l'interface se fait via une file
d'attente thread-safe.

---
