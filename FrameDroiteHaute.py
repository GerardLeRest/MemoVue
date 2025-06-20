#!/usr/bin/python3
# -*- coding: utf-8 -*

#####################################################
# rechercher une ou plusieurs personnes dans 
# l'établissement
#####################################################


from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel, QLineEdit, QHBoxLayout, QPushButton, QApplication
from PyQt5.QtGui import QPixmap
import os, sys

repertoire_racine=os.path.dirname(os.path.abspath(__file__)) # répetoire du fichier pyw

class FrameDroiteHaute(QWidget):
    """ Créer la partie droite haute de l'interface """
        
    def __init__(self, fenetre = None):
        """Constructeur de la frame de droite et de ses éléments"""
        super().__init__(fenetre)  # ← Important 
        # layout de la classe
        layoutDroitHaut = QVBoxLayout()        

        # zone de saisie - GrdGidLayout - partie haue
        # prenom
        layoutGrille = QGridLayout()
        self.labelPrenom = QLabel("Prénom")
        layoutGrille.addWidget(self.labelPrenom,0,0)
        self.prenomEntry = QLineEdit()  # Removed undefined widget
        self.prenomEntry.setPlaceholderText("Prenom")
        layoutGrille.addWidget(self.prenomEntry,0, 1)
        # nom
        self.labelNom = QLabel("Nom")
        layoutGrille.addWidget(self.labelNom,1,0)
        self.nomEntry = QLineEdit()  # Removed undefined widget
        self.nomEntry.setPlaceholderText("Nom")
        layoutGrille.addWidget(self.nomEntry,1, 1)
        layoutDroitHaut.addLayout(layoutGrille)

        # Zone boutons - QHBoxLayout
        layoutBoutons = QHBoxLayout()
        # bouton valider
        self.boutVal = QPushButton ("Valider", self)
        layoutBoutons.addWidget(self.boutVal)
        # bouton effacer
        self.boutEff = QPushButton ("Effacer", self)
        layoutBoutons.addWidget(self.boutEff)
        # bouton Suite
        self.boutSuite = QPushButton ("Suite", self)
        layoutBoutons.addWidget(self.boutSuite)
        layoutDroitHaut.addLayout(layoutBoutons)
        # désativer les boutons
        self.boutVal.setEnabled(False)
        self.boutEff.setEnabled(False)
        self.boutSuite.setEnabled(False)

        # partie du bas - 2 images
        layoutImages = QHBoxLayout()
        # image de validation
        self.labelImageGauche = QLabel()
        self.image = QPixmap(repertoire_racine+os.sep+"fichiers"+os.sep+"icones"+os.sep+"transparent.png")
        self.labelImageGauche.setPixmap(self.image) 
        layoutImages.addWidget(self.labelImageGauche)
        # affichage des bonnes réponses
        self.nbreRep=QLabel("0/0") 
        self.nbreRep.setStyleSheet("color: grey;")
        self.nbreRepExactes=0 
        layoutDroitHaut.addLayout(layoutImages)

        self.setLayout(layoutDroitHaut)

        self.show()
        
                
    def configRechercher(self) -> None:
        """configurer - mode Rechercher"""
        # changer couleur label
        self.labelPrenom.setStyleSheet("color: black;")
        self.labelNom.setStyleSheet("color: black;")
        self.nbreRep.setStyleSheet("color: grey;")
        # Désactiver l'affichage des bonnes réponses
        self.DesAffichRep()
        # activer/désactiver boutons 
        self.boutVal.setUpdatesEnabled(True)
        self.boutEff.setEnabled(True)
        self.boutSuite.setEnabled(False)
    
    def DesAffichRep(self) -> None:
        """ désactiver l'affichage des bonnes réponses"""
        self.nbreRep.setStyleSheet("color: grey;") #nbre bonnes reponses en gris
        self.nbreRepExactes=0  # nbre de réponses exactes
        # maj nbrebonnes réponses
        self.nbreRep.setText(str(self.nbreRepExactes)+os.sep+"0")    
    
    def desFrameDrHa(self) -> None:
        """désactiver des boutons et les entry de la frameDB"""     
        self.prenomEntry.setEnabled(False)
        self.nomEntry.setEnabled(False)
        self.boutVal.setEnabled(False)
        self.boutEff.setEnabled(False)
        self.boutSuite.setEnabled(False)
        
    def effacerReponses(self) -> None:
        """effacer réponses"""
        # effacer champs des noms et prénom
        self.prenomEntry.setEnabled(True)
        self.prenomEntry.clear()
        self.nomEntry.setEnabled(True)
        self.nomEntry.clear()
        # effacer icone
        self.image = QPixmap(repertoire_racine+os.sep+"fichiers"+os.sep+"icones"+os.sep+"transparent.png")
        self.labelImageGauche.setPixmap(self.image)    
        
    def configTestEcrit(self) -> None:
        """ configurer - Test écrit """
        # changer couleur label
        self.labelPrenom.setStyleSheet("color: black;")
        self.labelNom.setStyleSheet("color: black;")
        self.nomEntry.setStyleSheet("color: brown") 
        # effacer réponses
        self.effacerReponses()        
        # activer boutons 
        self.boutVal.setEnabled(True)
        self.boutEff.setEnabled(True)
        self.boutSuite.setEnabled(True)   
        
# ----------------------------------------------------
if __name__ == "__main__":

    app = QApplication(sys.argv)
    fenetre = FrameDroiteHaute(None)
    fenetre.prenomEntry.setEnabled(True)
    fenetre.nomEntry.setEnabled(True)
    fenetre.boutVal.setEnabled(True)
    fenetre.boutEff.setEnabled(False)
    fenetre.boutSuite.setEnabled(False)    
    app.exec()