import tkinter as tk
from tkinter import ttk , messagebox , scrolledtext
import threading
import queue

from configuration import (URI_DEFAUT , UTILISATEUR_DEFAUT , MOT_DE_PASSE_DEFAUT , REQUETES_IMPORTATION , REQUETES_ANALYSE , REQUETES_GDS ,)
from connexion import ConnexionNeo4j


class FenetrePrincipale(tk.Tk) :

    def __init__(self) :
        super().__init__()
        self.title("Detection avec Neo4j")
        self.geometry("1100x720")
        self.minsize(900 , 600)
        self.configure(bg="#f0f0f0")

        self.connexion = ConnexionNeo4j()
        self.file_attente = queue.Queue()

        self.construire_barre_connexion()
        self.construire_zone_principale()
        self.verifier_file_attente()


    def construire_barre_connexion(self) :
        barre = tk.LabelFrame(self , text="Connexion Neo4j" , bg="#f0f0f0" , font=("Arial" , 10 , "bold") , fg="#1B4F8A")
        barre.pack(fill="x" , padx=10 , pady=(8 , 4))

        tk.Label(barre , text="URI :" , bg="#f0f0f0" , font=("Arial" , 10)).grid(row=0 , column=0 , padx=(8 , 2) , pady=6)
        self.champ_uri = tk.Entry(barre , width=28 , font=("Arial" , 10))
        self.champ_uri.insert(0 , URI_DEFAUT)
        self.champ_uri.grid(row=0 , column=1 , padx=2 , pady=6)

        tk.Label(barre , text="Utilisateur :" , bg="#f0f0f0" , font=("Arial" , 10)).grid(row=0 , column=2 , padx=(12 , 2))
        self.champ_utilisateur = tk.Entry(barre , width=14 , font=("Arial" , 10))
        self.champ_utilisateur.insert(0 , UTILISATEUR_DEFAUT)
        self.champ_utilisateur.grid(row=0 , column=3 , padx=2)

        tk.Label(barre , text="Mot de passe :" , bg="#f0f0f0" , font=("Arial" , 10)).grid(row=0 , column=4 , padx=(12 , 2))
        self.champ_mot_de_passe = tk.Entry(barre , width=16 , show="*" , font=("Arial" , 10))
        self.champ_mot_de_passe.insert(0 , MOT_DE_PASSE_DEFAUT)
        self.champ_mot_de_passe.grid(row=0 , column=5 , padx=2)

        self.bouton_connexion = tk.Button( barre , text="Connecter" ,
            font=("Arial" , 10 , "bold") , bg="#2E75B6" , fg="white" , relief="flat" , padx=12,
            command=self.lancer_connexion)
        self.bouton_connexion.grid(row=0 , column=6 , padx=(12 , 4))

        self.label_statut = tk.Label(barre , text="Non connecte" , bg="#f0f0f0" , font=("Arial" , 10) , fg="#888888")
        self.label_statut.grid(row=0 , column=7 , padx=8)

    def construire_zone_principale(self) :
        cadre = tk.Frame(self , bg="#f0f0f0")
        cadre.pack(fill="both" , expand=True , padx=10 , pady=(0 , 10))

        cadre_gauche = tk.Frame(cadre , bg="#f0f0f0" , width=320)
        cadre_gauche.pack(side="left" , fill="y" , padx=(0 , 8))
        cadre_gauche.pack_propagate(False)
        self.construire_onglets(cadre_gauche)

        cadre_droit = tk.Frame(cadre , bg="#f0f0f0")
        cadre_droit.pack(side="left" , fill="both" , expand=True)
        self.construire_zone_resultat(cadre_droit)

    def construire_onglets(self , parent) :
        onglets = ttk.Notebook(parent)
        onglets.pack(fill="both" , expand=True)

        groupes = [
            ("Importation" , REQUETES_IMPORTATION),
            ("Analyse" , REQUETES_ANALYSE),
            ("GDS" , REQUETES_GDS),]
        for titre , dictionnaire in groupes :
            cadre_onglet = tk.Frame(onglets , bg="#ffffff")
            onglets.add(cadre_onglet , text=titre)
            self.remplir_onglet(cadre_onglet , dictionnaire)

    def remplir_onglet(self , parent , dictionnaire_requetes) :
        cadre_interne = tk.Frame(parent , bg="#ffffff")
        cadre_interne.pack(fill="both" , expand=True , padx=6 , pady=6)

        for nom , contenu in dictionnaire_requetes.items() :
            cadre_bouton = tk.Frame(cadre_interne , bg="#ffffff" , relief="groove" , bd=1)
            cadre_bouton.pack(fill="x" , pady=3)

            tk.Label(cadre_bouton , text=nom , bg="#ffffff" , font=("Arial" , 10 , "bold") , fg="#1B4F8A" , anchor="w"
            ).pack(fill="x" , padx=8 , pady=(6 , 0))

            tk.Label(cadre_bouton , text=contenu["description"] , bg="#ffffff" , font=("Arial" , 9) , fg="#555555" ,
                anchor="w" , wraplength=260 , justify="left"
            ).pack(fill="x" , padx=8 , pady=(0 , 4))

            tk.Button(cadre_bouton , text="Executer" , font=("Arial" , 9) , bg="#1B4F8A" , fg="white" , relief="flat" , padx=8 , pady=2 ,
                command=lambda r=contenu["requete"] , n=nom: (self.lancer_requete(n , r))
            ).pack(anchor="e" , padx=8 , pady=(0 , 6))

    def construire_zone_resultat(self , parent) :
        self.label_titre_requete = tk.Label(parent , text="Aucune requete executee" ,
            bg="#f0f0f0" , font=("Arial" , 12 , "bold") , fg="#1B4F8A" , anchor="w")
        self.label_titre_requete.pack(fill="x" , pady=(0 , 4))

        cadre_tableau = tk.Frame(parent , bg="#f0f0f0")
        cadre_tableau.pack(fill="both" , expand=True)

        self.tableau = ttk.Treeview(cadre_tableau , show="headings" , selectmode="browse")
        defilement_v = ttk.Scrollbar(cadre_tableau , orient="vertical" , command=self.tableau.yview)
        defilement_h = ttk.Scrollbar(cadre_tableau , orient="horizontal" , command=self.tableau.xview)

        self.tableau.configure(yscrollcommand=defilement_v.set , xscrollcommand=defilement_h.set)
        defilement_v.pack(side="right" , fill="y")
        defilement_h.pack(side="bottom" , fill="x")
        self.tableau.pack(fill="both" , expand=True)

        self.label_nb_resultats = tk.Label(parent , text="" ,
            bg="#f0f0f0" , font=("Arial" , 9) , fg="#555555" , anchor="w")
        self.label_nb_resultats.pack(fill="x" , pady=(4 , 0))

        tk.Label(parent , text="Journal d'execution" ,
            bg="#f0f0f0" , font=("Arial",9,"bold") , fg="#555555" , anchor="w"
        ).pack(fill="x" , pady=(8 , 0))

        self.console = scrolledtext.ScrolledText(parent , height=7 , state="disabled" ,
            font=("Courier" , 9) , bg="#1a1a1a" , fg="#00cc66" , insertbackground="white")
        self.console.pack(fill="x" , pady=(2 , 0))


    def lancer_connexion(self) :
        uri = self.champ_uri.get().strip()
        utilisateur = self.champ_utilisateur.get().strip()
        mot_de_passe = self.champ_mot_de_passe.get()

        self.label_statut.config(text="Connexion..." , fg="#888888")
        self.bouton_connexion.config(state="disabled")

        def tache() :
            try:
                self.connexion.connecter(uri , utilisateur , mot_de_passe)
                self.file_attente.put(("connexion_ok" , None))
            except Exception as erreur:
                self.file_attente.put(("connexion_erreur" , str(erreur)))

        threading.Thread(target=tache , daemon=True).start()


    def lancer_requete(self , nom_requete , texte_requete) :
        if not self.connexion.est_connecte() :
            messagebox.showwarning("Non connecte" , "Veuillez d'abord vous connecter a Neo4j !")
            return

        self.journaliser(f"Execution : {nom_requete}")
        self.label_titre_requete.config(text=nom_requete)
        self.vider_tableau()

        def tache() :
            try:
                enregistrements , resume = self.connexion.executer(texte_requete)
                self.file_attente.put(("requete_ok" , (nom_requete , enregistrements , resume)))
            except Exception as erreur:
                self.file_attente.put(("requete_erreur" , str(erreur)))

        threading.Thread(target=tache , daemon=True).start()

    def afficher_resultats(self , nom_requete , enregistrements , resume) :
        self.vider_tableau()

        if not enregistrements :
            lignes_resume = self.connexion.extraire_resume(resume)
            self.tableau["columns"] = ("information",)
            self.tableau.heading("information" , text="Resultat")
            self.tableau.column("information" , width=500 , anchor="w")
            for ligne in lignes_resume :
                self.tableau.insert("" , "end" , values=(ligne,))

            self.label_nb_resultats.config(text=f"{len(lignes_resume)} information(s)")
            self.journaliser(f"OK -- {nom_requete}")
            return

        colonnes = list(enregistrements[0].keys())
        self.tableau["columns"] = colonnes
        for col in colonnes :
            self.tableau.heading(col , text=col)
            self.tableau.column(col , width=max(80 , len(col) * 10) , anchor="w")

        for enregistrement in enregistrements :
            valeurs = [str(enregistrement.get(col , "")) for col in colonnes]
            self.tableau.insert("" , "end" , values=valeurs)

        self.label_nb_resultats.config(text=f"{len(enregistrements)} ligne(s) retournee(s)")
        self.journaliser(f"OK -- {nom_requete} -- {len(enregistrements)} ligne(s)")

    def vider_tableau(self) :
        for ligne in self.tableau.get_children() :
            self.tableau.delete(ligne)
        self.tableau["columns"] = ()
        self.label_nb_resultats.config(text="")

    def journaliser(self , message) :
        self.console.config(state="normal")
        self.console.insert("end" , f">> {message}\n")
        self.console.see("end")
        self.console.config(state="disabled")

    def verifier_file_attente(self) :
        try:
            while True:
                type_message , donnees = self.file_attente.get_nowait()

                if type_message == "connexion_ok" :
                    self.label_statut.config(text="Connecte" , fg="#1E6B35")
                    self.bouton_connexion.config(state="normal")
                    self.journaliser("Connexion Neo4j etablie")

                elif type_message == "connexion_erreur" :
                    self.label_statut.config(text="Erreur" , fg="#8B1A1A")
                    self.bouton_connexion.config(state="normal")
                    self.journaliser(f"Erreur connexion : {donnees}")
                    messagebox.showerror("Erreur de connexion" , donnees)

                elif type_message == "requete_ok" :
                    nom , enregistrements , resume = donnees
                    self.afficher_resultats(nom , enregistrements , resume)

                elif type_message == "requete_erreur" :
                    self.journaliser(f"Erreur : {donnees}")
                    messagebox.showerror("Erreur requete" , donnees)

        except queue.Empty :
            pass

        self.after(100 , self.verifier_file_attente)
