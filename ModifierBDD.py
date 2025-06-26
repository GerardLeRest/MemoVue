import sqlite3

class ModifierBDD:
    def __init__(self, chemin_fichier):
        self.chemin_fichier = chemin_fichier
        self.conn = sqlite3.connect(self.chemin_fichier)
        self.curs = self.conn.cursor()
        self.curs.execute("PRAGMA foreign_keys=on;")

        self.listeEleves = []
        self.eleves = []
        self.ElevesParClasses = {}

        self.charger_eleves_et_classes()

    def charger_eleves_et_classes(self):
        """Charge tous les élèves classés par classe dans un dictionnaire, et une liste globale"""
        self.eleves = []
        self.ElevesParClasses = {}

        self.curs.execute('''
            SELECT 
                e.prenom, 
                e.nom, 
                c.classe, 
                GROUP_CONCAT(o.option, ', '), 
                e.photo
            FROM eleves e
            JOIN eleves_classes_options eco ON eco.id_eleve = e.id
            JOIN classes c ON c.id = eco.id_classe
            LEFT JOIN options o ON o.id = eco.id_option
            GROUP BY e.id, c.classe
        ''')

        for prenom, nom, classe, options_str, photo in self.curs.fetchall():
            liste_options = options_str.split(', ') if options_str else []
            eleve = [prenom, nom, classe, liste_options, photo]

            if classe not in self.ElevesParClasses:
                self.ElevesParClasses[classe] = []

            self.ElevesParClasses[classe].append(eleve)
            self.eleves.append(eleve)

    def eleves_classe(self, classe_nom):
        """Charge les élèves d'une classe spécifique depuis les données déjà chargées"""
        self.listeEleves = self.ElevesParClasses.get(classe_nom, [])
        self.eleves = self.listeEleves.copy()

    def lister_classes(self):
        """Retourne la liste des noms de classes"""
        return list(self.ElevesParClasses.keys())

    def fermer_connexion(self):
        self.conn.close()

# ------------------------------------------------------------------------------
if __name__ == "__main__":
    bdd = ModifierBDD("fichiers/eleves.db")
    bdd.charger_eleves_et_classes()

