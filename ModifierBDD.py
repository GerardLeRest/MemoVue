import sqlite3

class ModifierBDD:
    """Manipulation de la BDD"""
    def __init__(self, cheminFichier):
        self.cheminFichier = cheminFichier
        self.conn = sqlite3.connect(self.cheminFichier)
        self.curs = self.conn.cursor()
        self.curs.execute("PRAGMA foreign_keys=on;")
        self.listesEleves = []        # Tous les élèves de l'établissement
        self.listeEleves = []         # Élèves sélectionnés (par classe, recherche…)
        self.elevesParClasses = {}

        self.chargerElevesEtClasses()


    def chargerElevesEtClasses(self):
        self.listesEleves.clear()
        self.elevesParClasses.clear()

        self.curs.execute('''
            SELECT 
                e.prenom, 
                e.nom, 
                e.classe, 
                GROUP_CONCAT(o.option, ', '), 
                e.photo
            FROM eleves e
            LEFT JOIN eleves_options eo ON eo.id_eleve = e.id
            LEFT JOIN options o ON o.id = eo.id_option
            GROUP BY e.id, e.classe
        ''')

        for prenom, nom, classe, optionsStr, photo in self.curs.fetchall():
            listeOptions = optionsStr.split(', ') if optionsStr else []
            eleve = [prenom, nom, classe, listeOptions, photo]

            self.listesEleves.append(eleve)  # tous les élèves de la BDD

            if classe not in self.elevesParClasses:
                self.elevesParClasses[classe] = []
            self.elevesParClasses[classe].append(eleve)

    def elevesClasse(self, classeNom):
        """Filtrer les élèves d’une classe spécifique"""
        self.listeEleves = self.elevesParClasses.get(classeNom, []).copy()

    def listerClasses(self):
        """Retourne la liste des noms de classes"""
        return list(self.elevesParClasses.keys())

    def fermerConnexion(self):
        self.conn.close()

# ------------------------------------------------------------------------------
if __name__ == "__main__":
    bdd = ModifierBDD("fichiers/eleves.db")
    bdd.chargerElevesEtClasses()
