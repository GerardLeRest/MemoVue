import sqlite3

class ModifierBDD:
    """Manipulation de la BDD"""
    def __init__(self, cheminFichier):
        self.cheminFichier = cheminFichier
        self.conn = sqlite3.connect(self.cheminFichier)
        self.curs = self.conn.cursor()
        self.curs.execute("PRAGMA foreign_keys=on;")

        self.listesPersonnes = []          # Toutes les personnes de la BDD
        self.listePersonnes = []           # Personnes filtrées
        self.personnesParStructure = {}    # Trie par structure (anciennement "classe")

        self.chargerPersonnesEtStructures()


    def chargerPersonnesEtStructures(self):
        """Charge toutes les personnes et les organise par structure"""
        self.listesPersonnes.clear()
        self.personnesParStructure.clear()

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
            listeOptions = optionsStr.split(', ') if optionsStr else []
            personne = [prenom, nom, structure, listeOptions, photo]

            self.listesPersonnes.append(personne)

            if structure not in self.personnesParStructure:
                self.personnesParStructure[structure] = []
            self.personnesParStructure[structure].append(personne)

    def personnesStructure(self, structureNom):
        """Filtrer les personnes d’une structure spécifique"""
        self.listePersonnes = self.personnesParStructure.get(structureNom, []).copy()

    def listerStructures(self):
        """Retourne la liste des noms de structures"""
        return list(self.personnesParStructure.keys())

    def fermerConnexion(self):
        self.conn.close()


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    bdd = ModifierBDD("eleves.db")
    bdd.chargerPersonnesEtStructures()
