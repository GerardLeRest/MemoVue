import sqlite3

class ModifierBDD:
    def __init__(self, chemin_fichier):
        self.chemin_fichier = chemin_fichier
        self.conn = sqlite3.connect(self.chemin_fichier)
        self.curs = self.conn.cursor()

        # Activer les clés étrangères
        self.curs.execute("PRAGMA foreign_keys=on;")

        # Structures internes
        self.listeEleves = []  
        self.eleves = []  # liste globale de tous les élèves
        self.ElevesParClasses = {}  # Par classe (utile pour la recherche)

        # Charger les élèves et les classes
        self.charger_eleves_et_classes()

    def charger_eleves_et_classes(self):
        """Charge tous les élèves classés par classe dans un dictionnaire, et une liste globale"""
        self.eleves = []
        self.ElevesParClasses = {}

        self.curs.execute("SELECT classe FROM classes")
        classes = [ligne[0] for ligne in self.curs.fetchall()]

        for classe_nom in classes:
            self.curs.execute('''
                SELECT 
                    e.prenom, 
                    e.nom, 
                    GROUP_CONCAT(o.option, ', '), 
                    e.photo
                FROM eleves e
                JOIN eleves_classes_options eco ON eco.id_eleve = e.id
                JOIN classes c ON c.id = eco.id_classe
                LEFT JOIN options o ON o.id = eco.id_option
                WHERE c.classe = ?
                GROUP BY e.id
            ''', (classe_nom,))

            tableau = []
            for prenom, nom, options, photo in self.curs.fetchall():
                print(f"{prenom} {nom} | Options : {options} | Photo : {photo}")
                tableau.append([prenom, nom, options or "", photo])

            self.ElevesParClasses[classe_nom] = tableau
            # évite les doublons d'éléments'
            self.eleves.extend([e for e in tableau if e not in self.eleves])


    def lister_classes(self):
        """Retourne la liste des noms de classes"""
        self.curs.execute("SELECT classe FROM classes")
        return [val[0] for val in self.curs.fetchall()]

    def determiner_classe(self, prenom, nom):
        """Retourne le nom de la classe d'un élève à partir de son prénom et nom"""
        self.curs.execute('''
            SELECT c.classe
            FROM eleves e
            JOIN eleves_classes_options eco ON eco.id_eleve = e.id
            JOIN classes c ON eco.id_classe = c.id
            WHERE LOWER(e.prenom) = LOWER(?) AND LOWER(e.nom) = LOWER(?)
        ''', (prenom, nom))
        resultat = self.curs.fetchone()
        return resultat[0] if resultat else None

    def eleves_classe(self, classeNom):
        """Charge les élèves d'une classe spécifique dans self.eleves et self.listeEleves"""

        self.eleves = []

        self.curs.execute('''
            SELECT 
                e.prenom,
                e.nom,
                GROUP_CONCAT(o.option, ', ') AS options,
                e.photo
            FROM eleves e
            JOIN eleves_classes_options eco ON eco.id_eleve = e.id
            JOIN classes c ON c.id = eco.id_classe
            LEFT JOIN options o ON o.id = eco.id_option
            WHERE c.classe = ?
            GROUP BY e.id
        ''', (classeNom,))

        tableau_final = []

        for prenom, nom, options, photo in self.curs.fetchall():
            print(f"{prenom} {nom} | Classe : {classeNom} | Options : {options} | Photo : {photo}")
            tab_options = options.split(', ') if options else []
            tableau_final.append([prenom, nom, tab_options, photo])

        print("tableau final :", tableau_final)

        self.eleves = tableau_final
        self.listeEleves = tableau_final

    def fermer_connexion(self):
        """Ferme la connexion à la base"""
        self.conn.close()

# ------------------------------------------------------------------------------
if __name__ == "__main__":
    bdd = ModifierBDD("fichiers/eleves.db")
    bdd.charger_eleves_et_classes()

