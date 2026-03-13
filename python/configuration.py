# connexion neo4j et requetes Cypher du projet

# connexion
URI_DEFAUT = "bolt://localhost:7687"
UTILISATEUR_DEFAUT = "neo4j"
MOT_DE_PASSE_DEFAUT = "test@123"


# importation initiale des donnees CSV
REQUETES_IMPORTATION = {
    "toutSuppr" : {
        "description" : "Supprimer tous les noeuds et relations",
        "requete" : "MATCH (n) DETACH DELETE n;",
    },
    "etudiant" : {
        "description" : "Importer les etudiants depuis students.csv",
        "requete" : (
            "LOAD CSV WITH HEADERS FROM 'file:///students.csv' AS row\n"
            "CREATE (:Etudiant {\n"
            "    id: row.id,\n"
            "    age: toInteger(row.age),\n"
            "    filiere: row.filiere,\n"
            "    annee: toInteger(row.annee),\n"
            "    logement: row.logement,\n"
            "    stress_score: toInteger(row.stress_score),\n"
            "    consomme_cannabis: toLower(trim(row.consomme_cannabis))\n"
            "                        IN ['true', '1', 'oui'],\n"
            "    frequence_cannabis: row.frequence_cannabis,\n"
            "    date_import: date()\n"
            "});\n"
            "CREATE INDEX etudiant_id IF NOT EXISTS FOR (e:Etudiant) ON (e.id);"
        ),
    },
    "groupe" : {
        "description" : "Importer les groupes depuis groups.csv",
        "requete" : (
            "LOAD CSV WITH HEADERS FROM 'file:///groups.csv' AS row\n"
            "CREATE (:Groupe {\n"
            "    group_id: row.group_id,\n"
            "    type: row.type,\n"
            "    taille: toInteger(row.taille)\n"
            "});\n"
            "CREATE INDEX groupe_id IF NOT EXISTS FOR (g:Groupe) ON (g.group_id);"
        ),
    },
    "connait" : {
        "description" : "Creer les relations CONNAIT depuis friendships.csv",
        "requete" : (
            "LOAD CSV WITH HEADERS FROM 'file:///friendships.csv' AS row\n"
            "MATCH (a:Etudiant {id: row.source})\n"
            "MATCH (b:Etudiant {id: row.target})\n"
            "CREATE (a)-[:CONNAIT {\n"
            "    type: row.type,\n"
            "    intensite: toInteger(row.intensite),\n"
            "    date_debut: date(),\n"
            "    date_fin: null\n"
            "}]->(b);"
        ),
    },
    "appartientA" : {
        "description" : "Creer les relations APPARTIENT_A depuis memberships.csv",
        "requete" : (
            "LOAD CSV WITH HEADERS FROM 'file:///memberships.csv' AS row\n"
            "MATCH (e:Etudiant {id: row.student_id})\n"
            "MATCH (g:Groupe {group_id: row.group_id})\n"
            "CREATE (e)-[:APPARTIENT_A]->(g);"
        ),
    },
}


# requetes d'analyse du graphe
REQUETES_ANALYSE = {
    "compteEtudiant" : {
        "description" : "Compter le nombre de noeuds Etudiant",
        "requete" : "MATCH (e:Etudiant) RETURN count(e) AS nb_etudiants;",
    },
    "compteRelation" : {
        "description" : "Compter le nombre de relations CONNAIT",
        "requete" : "MATCH ()-[r:CONNAIT]->() RETURN count(r) AS nb_relations;",
    },
    "statFiliere" : {
        "description" : "Prevalence de consommation par filiere",
        "requete" : (
            "MATCH (e:Etudiant)\n"
            "RETURN e.filiere AS filiere,\n"
            "       count(e) AS total,\n"
            "       sum(CASE WHEN e.consomme_cannabis THEN 1 ELSE 0 END) AS consommateurs,\n"
            "       round(100.0 * sum(CASE WHEN e.consomme_cannabis\n"
            "             THEN 1 ELSE 0 END) / count(e), 1) AS pct\n"
            "ORDER BY pct DESC;"
        ),
    },
    "top10Popu" : {
        "description" : "Top 10 etudiants les plus connectes",
        "requete" : (
            "MATCH (e:Etudiant)-[:CONNAIT]->()\n"
            "RETURN e.id, e.filiere, e.logement, count(*) AS degree\n"
            "ORDER BY degree DESC\n"
            "LIMIT 10;"
        ),
    },
    "topInfluenceur" : {
        "description" : "Top 15 influenceurs par PageRank",
        "requete" : (
            "MATCH (e:Etudiant)\n"
            "RETURN e.id, e.filiere, e.logement,\n"
            "       round(e.pagerank, 4) AS pagerank,\n"
            "       e.consomme_cannabis\n"
            "ORDER BY pagerank DESC\n"
            "LIMIT 15;"
        ),
    },
    "tauxLouvain" : {
        "description" : "Taux de consommation par communaute Louvain",
        "requete" : (
            "MATCH (e:Etudiant)\n"
            "WITH e.communaute AS com,\n"
            "     count(e) AS n,\n"
            "     sum(CASE WHEN e.consomme_cannabis THEN 1 ELSE 0 END) AS conso\n"
            "WHERE n >= 5\n"
            "RETURN com, n, conso,\n"
            "       round(100.0 * conso / n, 1) AS pct_cannabis\n"
            "ORDER BY pct_cannabis DESC;"
        ),
    },
    "voisinageCons" : {
        "description" : "Voisinage d'un consommateur a 2 sauts (remplacer S0001)",
        "requete" : (
            "MATCH path = (seed:Etudiant {id: 'S0001'})-[:CONNAIT*1..2]-(voisin:Etudiant)\n"
            "WHERE voisin.id <> seed.id\n"
            "RETURN DISTINCT voisin.id,\n"
            "                voisin.consomme_cannabis,\n"
            "                length(path) AS distance\n"
            "ORDER BY distance, voisin.consomme_cannabis DESC;"
        ),
    },
    "louvainCOMM" : {
        "description" : "Distribution des communautes Louvain",
        "requete" : (
            "MATCH (e:Etudiant)\n"
            "RETURN e.communaute,\n"
            "       count(e) AS taille,\n"
            "       round(100.0 * sum(CASE WHEN e.consomme_cannabis\n"
            "             THEN 1 ELSE 0 END) / count(e), 1) AS pct_cannabis\n"
            "ORDER BY taille DESC\n"
            "LIMIT 20;"
        ),
    },
}


# requetes Graph Data Science
REQUETES_GDS = {
    "projectionGDSsocial" : {
        "description" : "Projeter le graphe en memoire (requis avant tout algorithme GDS)",
        "requete" : (
            "CALL gds.graph.project(\n"
            "    'graphe_sociale',\n"
            "    'Etudiant',\n"
            "    {\n"
            "        CONNAIT: {\n"
            "            orientation: 'UNDIRECTED',\n"
            "            properties: ['intensite']\n"
            "        }\n"
            "    }\n"
            ");"
        ),
    },
    "EcrirePR" : {
        "description" : "Calculer et ecrire le PageRank sur chaque noeud",
        "requete" : (
            "CALL gds.pageRank.write('graphe_sociale', {\n"
            "    writeProperty: 'pagerank',\n"
            "    maxIterations: 20,\n"
            "    dampingFactor: 0.85\n"
            "})\n"
            "YIELD nodePropertiesWritten, ranIterations;"
        ),
    },
    "GDSlouvain" : {
        "description" : "Detecter les communautes avec l'algorithme de Louvain",
        "requete" : (
            "CALL gds.louvain.write('graphe_sociale', {\n"
            "    writeProperty: 'communaute'\n"
            "})\n"
            "YIELD communityCount, modularity;"
        ),
    },
    "ponts_comm" : {
        "description" : "Calculer la Betweenness Centrality (ponts entre communautes)",
        "requete" : (
            "CALL gds.betweenness.write('graphe_sociale', {\n"
            "    writeProperty: 'betweenness'\n"
            "})\n"
            "YIELD nodePropertiesWritten;"
        ),
    },
    "dropProjection" : {
        "description" : "Supprimer la projection de la memoire GDS",
        "requete" : (
            "CALL gds.graph.drop('graphe_sociale')\n"
            "YIELD graphName, nodeCount, relationshipCount;"
        ),
    },
}


# requetes incrementales (mise a jour du graphe)
REQUETES_INCREMENTALES = {
    "nouvelEtudiant" : {
        "description" : "Ajouter un nouvel etudiant au graphe existant",
        "requete" : (
            "MERGE (e:Etudiant {id: 'NOUVEAU_ID'})\n"
            "ON CREATE SET\n"
            "    e.age = 20,\n"
            "    e.filiere = 'Info',\n"
            "    e.annee = 1,\n"
            "    e.logement = 'residence',\n"
            "    e.stress_score = 5,\n"
            "    e.consomme_cannabis = false,\n"
            "    e.frequence_cannabis = 'jamais',\n"
            "    e.date_import = date()\n"
            "RETURN e.id, e.filiere, e.date_import;"
        ),
    },
    "nouvelleRelation" : {
        "description" : "Ajouter une nouvelle relation entre deux etudiants existants",
        "requete" : (
            "MATCH (a:Etudiant {id: 'ID_SOURCE'})\n"
            "MATCH (b:Etudiant {id: 'ID_CIBLE'})\n"
            "MERGE (a)-[r:CONNAIT {type: 'amitie'}]->(b)\n"
            "ON CREATE SET\n"
            "    r.intensite = 2,\n"
            "    r.date_debut = date(),\n"
            "    r.date_fin = null\n"
            "RETURN a.id AS source, b.id AS cible,\n"
            "       r.date_debut AS depuis, r.type AS type;"
        ),
    },
    "mettreAJourComportement" : {
        "description" : "Mettre a jour le comportement d'un etudiant (sans supprimer le noeud)",
        "requete" : (
            "MATCH (e:Etudiant {id: 'ID_ETUDIANT'})\n"
            "SET e.consomme_cannabis = true,\n"
            "    e.frequence_cannabis = 'hebdo',\n"
            "    e.date_changement_comportement = date()\n"
            "RETURN e.id, e.consomme_cannabis,\n"
            "       e.frequence_cannabis,\n"
            "       e.date_changement_comportement;"
        ),
    },
    "cloturerRelation" : {
        "description" : "Marquer une relation comme terminee (sans la supprimer)",
        "requete" : (
            "MATCH (a:Etudiant {id: 'ID_SOURCE'})-[r:CONNAIT]->(b:Etudiant {id: 'ID_CIBLE'})\n"
            "SET r.date_fin = date()\n"
            "RETURN a.id AS source, b.id AS cible,\n"
            "       r.date_debut AS debut, r.date_fin AS fin;"
        ),
    },
    "relationsActives" : {
        "description" : "Afficher uniquement les relations encore actives aujourd'hui",
        "requete" : (
            "MATCH (a:Etudiant)-[r:CONNAIT]->(b:Etudiant)\n"
            "WHERE r.date_fin IS NULL\n"
            "RETURN a.id AS source, b.id AS cible,\n"
            "       r.type, r.date_debut, r.intensite\n"
            "ORDER BY r.date_debut DESC\n"
            "LIMIT 20;"
        ),
    },
    "changementsRecents" : {
        "description" : "Etudiants dont le comportement a change recemment",
        "requete" : (
            "MATCH (e:Etudiant)\n"
            "WHERE e.date_changement_comportement IS NOT NULL\n"
            "RETURN e.id, e.filiere, e.logement,\n"
            "       e.consomme_cannabis,\n"
            "       e.frequence_cannabis,\n"
            "       e.date_changement_comportement\n"
            "ORDER BY e.date_changement_comportement DESC;"
        ),
    },
    "nouvellesRelationsAujourdHui" : {
        "description" : "Relations creees aujourd'hui dans le graphe",
        "requete" : (
            "MATCH (a:Etudiant)-[r:CONNAIT]->(b:Etudiant)\n"
            "WHERE r.date_debut = date()\n"
            "RETURN a.id AS source, b.id AS cible,\n"
            "       r.type, r.intensite;"
        ),
    },
}
