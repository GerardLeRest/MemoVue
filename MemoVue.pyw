#!/usr/bin/python3
# -*- coding: utf-8 -*

##################################################
# Apprendre ou retrouver le nom/prénom des élèves
# du lycée
##################################################

import os, random, copy, sys
from FrameGauche import *
from FrameDroiteHaute import *
from FrameDroiteBasse import *

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel,
    QVBoxLayout, QMenu, QMessageBox
)
from PySide6.QtGui import QPixmap, QAction
import sys

repertoire_racine = os.path.dirname(os.path.abspath(__file__)) # répetoire du fichier pyw

class Fenetre(QMainWindow):
    """ Créer l'interface graphique et lier les diffentes classes entre elles"""
    
    def __init__(self):
        super().__init__()   # constructeur de la classe parente
        self.setWindowTitle("MemoVue")  # Titre de la fenêtre
        self.setMaximumSize(self.width(), self.height()) # empêchement d'aggranissement de la fenêtre
        
        # Création des 3 frames
        self.FrameDrBa = FrameDroiteBasse(self)
        self.FrameDrHa = FrameDroiteHaute(self)
        self.FrameG = FrameGauche(self, self.FrameDrBa.listeEleves)

        # Créer un widget central et y appliquer le layout principal
        widget_central = QWidget()
        layoutPrincipal = QGridLayout(widget_central)  # layout appliqué ici

        layoutPrincipal.addWidget(self.FrameG, 0, 0, 2, 1)
        layoutPrincipal.addWidget(self.FrameDrHa, 0, 1)
        layoutPrincipal.addWidget(self.FrameDrBa, 1, 1)

        self.setCentralWidget(widget_central)  # c’est ici que tout s'affiche

        # Connexions
        self.FrameDrBa.boutonVal.clicked.connect(self.configurer)
        self.FrameDrHa.boutVal.clicked.connect(self.verifierRechercher)
        self.FrameDrHa.boutEff.clicked.connect(self.effacer)
        self.FrameDrHa.boutSuite.clicked.connect(self.AllerALaSuite)
        self.FrameDrHa.prenomEntry.returnPressed.connect(self.validerRepNom)
        self.FrameDrHa.nomEntry.returnPressed.connect(self.verifierRechercher)

        # Menu Aide
        menu_bar = self.menuBar()
        menu_aide = QMenu("Menu", self)
        menu_bar.addMenu(menu_aide)
        # Licence
        actionLicence = QAction("Licence GPL-v3", self)
        actionLicence.triggered.connect(self.afficherLicence)
        menu_aide.addAction(actionLicence)
        # Quitter
        action_quitter = QAction("Quitter", self)
        action_quitter.triggered.connect(self.quitter)
        menu_aide.addAction(action_quitter)
                
        self.show()
       
    def configurer(self) -> None:
        """ configurer l'application"""
        self.FrameDrHa.effacerReponses()
        if self.FrameDrBa.boutonRadioHaut4.isChecked(): # mode "Rechercher"
            self.FrameDrHa.configRechercher()
            # activer/désactiver zones de saisie 
            self.actDesZonesSaisies()          
        else:
            self.configAutresModes()           
        
    def actDesZonesSaisies(self) -> None:
        """Activer ou désactiver les zones de saisie selon le mode"""
        
        if self.FrameDrBa.boutonRadioBas2.isChecked():  # prénom seul
            self.FrameDrHa.nomEntry.setEnabled(False)
            self.FrameDrHa.prenomEntry.setEnabled(True)
            self.FrameDrHa.prenomEntry.setFocus()
            
        elif self.FrameDrBa.boutonRadioBas3.isChecked():  # nom seul
            self.FrameDrHa.prenomEntry.setEnabled(False)
            self.FrameDrHa.nomEntry.setEnabled(True)
            self.FrameDrHa.nomEntry.setFocus()
           
        else:  # nom + prénom
            self.FrameDrHa.prenomEntry.setEnabled(True)
            self.FrameDrHa.nomEntry.setEnabled(True)
            self.FrameDrHa.prenomEntry.setFocus()
            
    def configAutresModes(self) -> None:
        self.FrameDrBa.choisirOption()  # ⚠️ force la mise à jour
        self.FrameG.listeEleves = copy.deepcopy(self.FrameDrBa.listeEleves)

        # Filtrage par option choisie
        if self.FrameDrBa.optionSelectionnee != "TOUS":
            self.enleverEleves()
        
        self.FrameG.nbreElev = len(self.FrameG.listeEleves)
        self.FrameG.rang = 0
        self.FrameG.numOrdreElev.setText(f"{self.FrameG.rang // 2 + 1}/{self.FrameG.nbreElev}")
        self.FrameDrHa.DesAffichRep()
        if self.FrameDrBa.checkBox.isChecked():
            random.shuffle(self.FrameG.listeEleves)
        if self.FrameDrBa.boutonRadioBas2.isChecked():  # Prénom seul
            self.effacerNomsOuPrenoms(self.FrameG.listeEleves, 1)
        if self.FrameDrBa.boutonRadioBas3.isChecked():  # Nom seul
            self.effacerNomsOuPrenoms(self.FrameG.listeEleves, 0)
        if self.FrameDrBa.boutonRadioHaut2.isChecked():  # Test oral
            self.ajouterBlancsListes(self.FrameG.listeEleves)
        if self.FrameDrBa.boutonRadioHaut3.isChecked():  # Test écrit
            self.ajouterBlancsListes(self.FrameG.listeEleves)
            self.FrameDrHa.configTestEcrit()
            self.configTestEcrit()
        else:
            self.configApprentissageTestOral()
        print(f"==> rang = {self.FrameG.rang}, taille = {len(self.FrameG.listeEleves)}")
        if self.FrameG.listeEleves and all(len(eleve) >= 4 for eleve in self.FrameG.listeEleves):
            self.FrameG.maj()
        else:
            print("Données incomplètes ou non chargées, affichage annulé.")


    def configTestEcrit(self) -> None:
        """Configurer le mode Test Écrit"""
        # Désactiver les boutons (Frame gauche)
        for bouton in self.FrameG.boutons:
            bouton.setEnabled(False)
        # Activer ou désactiver les zones de saisie en fonction du mode
        self.actDesZonesSaisies()

    def configApprentissageTestOral(self) -> None:
        """configurer dans les modes Apprentissage et Test Oral """
        #activer ou désactiver les boutons de la frame de gauche
        self.actDesBoutFrameG()
        self.FrameDrHa.effacerReponses() # effacer réponses
        self.FrameDrHa.desFrameDrHa() #désactiver les boutons et zones de saisie de la frame DH
        
    def actDesBoutFrameG(self) -> None:
        """ activer ou désactiver les boutons de la frame de gauche"""
        # activer les boutons frame gauche si la liste des élèves n'est pas vide
        if len(self.FrameG.listeEleves)>1:
            for i in range(len(icones)):
                self.FrameG.boutons[i].setEnabled(True) 
        else:
            for i in range(len(icones)):
                self.FrameG.boutons[i].setEnabled(False)
        
    def effacer(self) -> None:
        """Effacer après appui sur le bouton "effacer" de la frame haute droite"""
        expression=self.FrameG.rang % 2 == 0 and self.FrameDrBa.boutonRadioHaut3.isChecked() # rang paire et test écrit
        if expression or self.FrameDrBa.boutonRadioHaut4: #  mode "Rechercher"
            self.FrameDrHa.effacerReponses()
            self.actDesZonesSaisies()

    def enleverEleves(self) -> None:
        """enlever les élèves ne faisant pas l'option sélectionnée"""
        self.FrameG.listeEleves = [
            eleve for eleve in self.FrameG.listeEleves
            if self.FrameDrBa.optionSelectionnee in eleve[3]
        ]
    
    def effacerNomsOuPrenoms(self,liste ,rang: int):
        """effacer les noms ou les prénoms"""
        for i in range(len(liste)):
                liste[i][rang]=" "
                   
    def ajouterBlancsListes(self,liste:list) -> None:
        """ajouter des blancs ou des ??? dans la liste"""
        i=0        
        while i<(len(liste)):
            tab=list(liste[i])# copie de liste[i]
            if self.FrameDrBa.boutonRadioBas1.isChecked(): #nom et prénom
                tab[0]="???"
                tab[1]="???"
            elif self.FrameDrBa.boutonRadioBas2.isChecked(): # prénom seul
                tab[0]="???"
                tab[1]=""
            else:               # nom seul
                tab[0]=""
                tab[1]="???"
            liste.insert(i,tab)
            i=i+2
            
    def verifierRechercher(self) -> None:
        """lancer la vérification de la réponse"""
        if self.FrameDrBa.boutonRadioHaut3.isChecked(): # mode - Test écrit
            self.verifier()
        elif self.FrameDrBa.boutonRadioHaut4.isChecked(): # mode "Rechercher"
            self.rechercher()
        
    def verifier(self) -> None:
        """Vérifier la réponse dans le mode Test Écrit"""

        if self.FrameG.rang % 2 != 0:
            return  # ne rien faire si ce n’est pas un rang pair

        # Récupération des réponses utilisateur
        nom = self.FrameDrHa.nomEntry.text()
        prenom = self.FrameDrHa.prenomEntry.text()

        # Réponses attendues
        nomAttendu = self.FrameG.listeEleves[self.FrameG.rang + 1][1]
        prenomAttendu = self.FrameG.listeEleves[self.FrameG.rang + 1][0]

        mode = self.FrameDrBa.groupeBas.checkedButton().text() 
        match = True

        if mode in ["Prenom+Nom", "Nom"]:  # le nom doit être vérifié
            match &= nom.lower() == nomAttendu.lower()
        if mode in ["Prenom+Nom", "Prenom"]:  # le prénom doit être vérifié
            self.FrameDrHa.nomEntry.setEnabled(False) # désactivation du nom
            match &= prenom.lower() == prenomAttendu.lower()

        # Affichage des icones
        icone = "check.png" if match else "cross.png"
        image = QPixmap(os.path.join(repertoire_racine, "fichiers", "icones", icone))
        self.FrameDrHa.labelImageGauche.setPixmap(image)
   
        if match:
            self.FrameDrHa.nbreRepExactes += 1

        # Mise à jour du score I / J
        score = f"{self.FrameDrHa.nbreRepExactes}/{self.FrameG.rang // 2 + 1}"
        self.FrameDrHa.nbreRep.setText(score)

        # Avancer dans la liste
        self.FrameG.rang += 1
        if self.FrameG.rang > len(self.FrameG.listeEleves) - 2:
            self.FrameDrHa.desFrameDrHa()
        else:
            self.FrameG.majNomPrenom()
            self.FrameG.majClasseOptions()
            self.FrameDrHa.boutVal.setEnabled(False)
            self.FrameDrHa.boutEff.setEnabled(False)
            self.FrameDrHa.nomEntry.setEnabled(False)
            self.FrameDrHa.prenomEntry.setEnabled(False)

    def AllerALaSuite(self,event) -> None:
        """voir la réponse et passer à l'élève suivant"""
        if self.FrameDrBa.boutonRadioHaut3.isChecked(): #Test écrit
            self.FrameDrHa.effacerReponses()
            if (self.FrameG.rang >= len(self.FrameG.listeEleves)-1):
                pass
            else:
                self.FrameG.rang=self.FrameG.rang+1
            # avancer
            if (self.FrameG.rang<len(self.FrameG.listeEleves)):
                #réactivation des boutons
                self.FrameDrHa.boutVal.setEnabled(True)
                self.FrameDrHa.boutEff.setEnabled(True)
                # maj bonnes réponses
                self.FrameDrHa.nbreRep.setText(str(self.FrameDrHa.nbreRepExactes)+"/"+str(self.FrameG.rang//2+1))
                # N° de l'élève en cours
                self.FrameG.numOrdreElev.setText(str(self.FrameG.rang//2+1)+"/"+str(self.FrameG.nbreElev))
                # maj des noms te des prénoms
                self.FrameG.majNomPrenom()
                self.FrameG.majClasseOptions()
                # activation/désactivation des zones de saisie
                if (self.FrameG.listeEleves[self.FrameG.rang][1]=="???") or (self.FrameG.listeEleves[self.FrameG.rang][0]=="???"):
                    self.actDesZonesSaisies() #activer/désactiver zones de saisie
                else:
                    self.FrameDrHa.prenomEntry.setEnabled(False)
                    self.FrameDrHa.nomEntry.setEnabled(False)
                    self.FrameDrHa.boutVal.setEnabled(False)
                    self.FrameDrHa.boutEff.setEnabled(False)
                # maj des photos
                self.FrameG.majPhoto()
                if (self.FrameG.rang==len(self.FrameG.listeEleves)-1):
                    self.FrameDrHa.desFrameDrHa()
        else:
            pass
    
    def rechercher(self):
        """Rechercher un ou plusieurs élèves dans tout l'établissement selon le nom, prénom ou les deux"""

        self.FrameG.listeEleves = []
        self.FrameG.rang = 0

        # Lecture des champs et mise en forme
        nom = self.FrameDrHa.nomEntry.text().lower().strip()
        prenom = self.FrameDrHa.prenomEntry.text().lower().strip()
        mode = self.FrameDrBa.groupeBas.checkedButton().text()

        # Boucle sur tous les élèves de l'établissement
        for eleve in self.FrameDrBa.modifier_bdd.listesPersonnes:
            prenom_eleve = eleve[0].lower().strip()
            nom_eleve = eleve[1].lower().strip()

            if mode == "Prenom":
                condition = (prenom == prenom_eleve)
            elif mode == "Nom":
                condition = (nom == nom_eleve)
            else:
                condition = (prenom == prenom_eleve and nom == nom_eleve)

            if condition:
                self.FrameG.listeEleves.append(eleve)

        # Après avoir collecté tous les résultats, mise à jour
        self.FrameG.nbreElev = len(self.FrameG.listeEleves)

        if self.FrameG.nbreElev > 0:
            self.FrameG.rang = 0
            self.FrameG.numOrdreElev.setText(f"1/{self.FrameG.nbreElev}")
            self.FrameG.majNomPrenom()
            self.FrameG.majClasseOptions()
            self.FrameG.majPhoto()
            # activation/désactivation boutons sous image - rechercher
            if self.FrameG.nbreElev<=1:
                for bouton in self.FrameG.boutons:
                    bouton.setEnabled(False)
            else:
                for bouton in self.FrameG.boutons:
                    bouton.setEnabled(True)
        else:
            self.FrameG.numOrdreElev.setText("0/0")
            QMessageBox.information(self, "Aucun résultat", "Aucun élève trouvé.")


    def validerRepNom(self):
        """Valider l'entrée prénom selon le mode sélectionné, ou passer au champ nom"""

        modeRecherche = self.FrameDrBa.groupeBas.checkedButton().text()
        modeGeneral = self.FrameDrBa.groupeHaut.checkedButton().text()

        if modeRecherche == "Prenom":  # Prénom seul
            if modeGeneral == "Test ecrit":  # Test écrit
                self.verifier()
            else:
                self.rechercher()
        else:
            # Passer au champ Nom
            self.focusNextChild()

                        
    def afficherLicence(self):
        texte = (
            "Ce logiciel est distribué sous licence GNU GPL version 3.\n\n"
            "Vous pouvez le redistribuer et/ou le modifier selon les termes de cette licence.\n\n"
            "Plus d'informations : https://www.gnu.org/licenses/gpl-3.0.html"
        )
        QMessageBox.information(self, "Licence GPL-v3", texte)
    
    def quitter(self):
        print ("Quitter")
        self.close()
           
# ----------------------------------------------------
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    fenetre = Fenetre()
    fenetre.show()
    app.exec()
