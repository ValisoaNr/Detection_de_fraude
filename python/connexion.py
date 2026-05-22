# connexion neo4j et execution des requetes

from neo4j import GraphDatabase


class ConnexionNeo4j :

    def __init__(self) :
        self.driver = None

    def connecter(self , uri , utilisateur , mot_de_passe) :
        self.driver = GraphDatabase.driver(uri , auth = (utilisateur , mot_de_passe))
        # teste immediat pour valider les identifiants
        with self.driver.session() as session :
            session.run("RETURN 1").consume()

    def deconnecter(self) :
        if self.driver is not None :
            self.driver.close()
            self.driver = None

    def est_connecte(self) :
        # retourne True si le driver est actif.
        return self.driver is not None

    def executer(self , texte_requete) :
        if not self.est_connecte() :
            raise RuntimeError("Veuillez connecter a neo4j !")

        with self.driver.session() as session:
            resultat = session.run(texte_requete)
            enregistrements = resultat.data()
            resume = resultat.consume()

        return enregistrements , resume

    def extraire_resume(self , resume) :
        # transforme le resume neo4j en liste de chaines .
        compteurs = resume.counters
        lignes = []

        correspondances = [
            (compteurs.nodes_created , "Noeuds crees"),
            (compteurs.nodes_deleted , "Noeuds supprimes"),
            (compteurs.relationships_created , "Relations creees"),
            (compteurs.relationships_deleted , "Relations supprimees"),
            (compteurs.properties_set ,  "Proprietes modifiees"),
            (compteurs.indexes_added , "Index crees"),
        ]

        for valeur , etiquette in correspondances :
            if valeur :
                lignes.append(f"{etiquette} : {valeur}")

        if not lignes :
            lignes.append("Requete executee avec succes.")

        return lignes
