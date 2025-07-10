import sqlite3

class ModifierBDD:
    """Manipulation de la BDD"""
    def __init__(self, config, cheminFichier):
        self.config = config  # configuration de l'interface - json
        self.cheminFichier = cheminFichier
        self.conn = sqlite3.connect(self.cheminFichier)
        self.curs = self.conn.cursor()
        self.curs.execute("PRAGMA foreign_keys=on;")

        self.listesPersonnes = []  # Toutes les personnes de la BDD

        self.chargerPersonnes()

    def chargerPersonnes(self):
        """Charge toutes les personnes depuis la BDD"""
        self.listesPersonnes.clear()

        self.curs.execute('''
            SELECT 
                e.prenom, 
                e.nom, 
                e.structure, 
                GROUP_CONCAT(o.specialite, ', '), 
                e.photo
            FROM personnes e
            LEFT JOIN personnes_specialites eo ON eo.id_personne = e.id
            LEFT JOIN specialites o ON o.id = eo.id_specialite
            GROUP BY e.id
        ''')

        for prenom, nom, structure, optionsStr, photo in self.curs.fetchall():
            listeSpecialites = optionsStr.split(', ') if optionsStr else []
            personne = [prenom, nom, structure, listeSpecialites, photo]
            self.listesPersonnes.append(personne)

    def listerStructures(self):
        """Retourne la liste des noms de structures uniques"""
        return sorted(set(personne[2] for personne in self.listesPersonnes))

    def personnesStructure(self, structureNom):
        """Retourne les personnes d’une structure spécifique"""
        return [
            personne for personne in self.listesPersonnes
            if personne[2] == structureNom
        ]
    
    def fermerConnexion(self):
        self.conn.close()


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    config = {
        "Organisme": "Entreprise",
        "Structure": "Département",
        "Personne": "Salarié",
        "Specialite": "Fonctions",
        "BaseDonnees": "salaries.db",
        "CheminPhotos": "photos/salaries/"
    }
    modifier_bdd = ModifierBDD(config, config["BaseDonnees"])
    print(modifier_bdd.listerStructures())

