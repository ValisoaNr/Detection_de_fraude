# connexion neo4j et requetes cypher

# connexion
URI_DEFAUT           = "bolt://localhost:7687"
UTILISATEUR_DEFAUT   = "neo4j"
MOT_DE_PASSE_DEFAUT  = "test@123"


# importation des donnees CSV
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
            "    id : row.id,\n"
            "    age : toInteger(row.age),\n"
            "    filiere : row.filiere,\n"
            "    annee : toInteger(row.annee),\n"
            "    logement : row.logement,\n"
            "    stress_score : toInteger(row.stress_score),\n"
            "    consomme_cannabis : toLower(trim(row.consomme_cannabis))\n"
            "                       IN ['true', '1', 'oui'],\n"
            "    frequence_cannabis : row.frequence_cannabis\n"
            "});\n"
            "CREATE INDEX etudiant_id IF NOT EXISTS FOR (e:Etudiant) ON (e.id);"
        ),
    },
    "groupe" : {
        "description" : "Importer les groupes depuis groups.csv",
        "requete" : (
            "LOAD CSV WITH HEADERS FROM 'file:///groups.csv' AS row\n"
            "CREATE (:Groupe {\n"
            "    group_id : row.group_id,\n"
            "    type : row.type,\n"
            "    taille : toInteger(row.taille)\n"
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
            "    type : row.type,\n"
            "    intensite : toInteger(row.intensite)\n"
            "}]->(b);"
        ),
    },
    "appartientA" : {
        "description" : "Creer les relations APPARTIENT_A depuis memberships.csv",
        "requete" : (
            "LOAD CSV WITH HEADERS FROM 'file:///memberships.csv' AS row\n"
            "MATCH (e:Etudiant  {id: row.student_id})\n"
            "MATCH (g:Groupe    {group_id: row.group_id})\n"
            "CREATE (e)-[:APPARTIENT_A]->(g);"
        ),
    },
}

# requetes d'analyse
REQUETES_ANALYSE = {
    "compteEtudiant" : {
        "description" : "Compter les noeuds Etudiant",
        "requete" : "MATCH (e:Etudiant) RETURN count(e) AS nb_etudiants;",
    },
    "compteRelation" : {
        "description" : "Compter les relations CONNAIT",
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
}


# Les requetes qui utilise GDS
REQUETES_GDS = {
    "projectionGDSsocial" : {
        "description" : "Projeter le graphe en memoire (requis avant tout algorithme GDS)",
        "requete" : (
            "CALL gds.graph.project(\n"
            "    'graphe_sociale',\n"
            "    'Etudiant',\n"
            "    {\n"
            "        CONNAIT : {\n"
            "            orientation : 'UNDIRECTED',\n"
            "            properties : ['intensite']\n"
            "        }\n"
            "    }\n"
            ");"
        ),
    },
    "EcrirePR" : {
        "description" : "Calculer et ecrire le PageRank sur chaque noeud",
        "requete" : (
            "CALL gds.pageRank.write('graphe_sociale', {\n"
            "    writeProperty : 'pagerank',\n"
            "    maxIterations : 20,\n"
            "    dampingFactor : 0.85\n"
            "})\n"
            "YIELD nodePropertiesWritten, ranIterations;"
        ),
    },
    "GDSlouvain" : {
        "description" : "Detecter les communautes avec l'algorithme de Louvain",
        "requete" : (
            "CALL gds.louvain.write('graphe_sociale', {\n"
            "    writeProperty : 'communaute'\n"
            "})\n"
            "YIELD communityCount, modularity;"
        ),
    },
    "ponts_comm" : {
        "description" : "Calculer la Betweenness Centrality (ponts entre communautes)",
        "requete" : (
            "CALL gds.betweenness.write('graphe_sociale', {\n"
            "    writeProperty : 'betweenness'\n"
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
