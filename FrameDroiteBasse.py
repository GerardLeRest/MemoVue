#!/usr/bin/python2
# -*- coding: utf-8 -*

#####################################################
# selection du mode de fonctionnement
# (apprentissage, test mental, test ecrit, Rechercher)
# choix de la classe et de l'option
#####################################################
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QRadioButton, QPushButton, QGridLayout, QLabel, QComboBox, QCheckBox
import copy, sqlite3, os  # fichier Excel de l'établissement
from ModifierBDD import ModifierBDD

class FrameDroiteBasse (QWidget):
    """ Créer la partie droite basse de l'interface """
    def __init__(self, fenetre = None):
        """Constructeur de la frame de droite et de ses éléments"""
        # constructeur de la classe parente
        super().__init__(fenetre)
        self.listeEleves = []  # liste des élèves de la classe sélectionnée
        self.listeOptions = []  # liste des options des élèves de la classeself/
        #self.modifier_bdd = ModifierBDD("fichiers/eleves.bdd") -faux?
        self.modifier_bdd = ModifierBDD("fichiers/eleves.db")
        self.optionSelectionnee = "TOUS"  # optionsélectionnée

        layoutBasDroit = QVBoxLayout()
        layoutBoutonsRadiosHaut = QHBoxLayout()
        # boutons radio des modes
        self.boutonRadioHaut1 = QRadioButton("Apprentissage")
        layoutBoutonsRadiosHaut.addWidget(self.boutonRadioHaut1)
        self.boutonRadioHaut2 = QRadioButton("Test mental")
        layoutBoutonsRadiosHaut.addWidget(self.boutonRadioHaut2)
        self.boutonRadioHaut3 = QRadioButton("Test écrit")
        layoutBoutonsRadiosHaut.addWidget(self.boutonRadioHaut3)
        self.boutonRadioHaut4 = QRadioButton("Rechercher")
        layoutBoutonsRadiosHaut.addWidget(self.boutonRadioHaut4)
         #bouton radi 1 est sélectionné
        self.boutonRadioHaut1.setChecked(True)
        layoutBasDroit.addLayout(layoutBoutonsRadiosHaut)
        
        # Combobox - QGridLayout
        layoutGrille = QGridLayout()
         # labels)
        layoutGrille.addWidget(QLabel("Classe/Catégorie"), 0,0)
        layoutGrille.addWidget(QLabel("Option/Spécialité"),0,1)
        ## ComboBox
        self.comboBoxGauche = QComboBox()
        self.comboBoxDroite = QComboBox()
        layoutGrille.addWidget(self.comboBoxGauche,1,0)
        layoutGrille.addWidget(self.comboBoxDroite,1,1)
        layoutBasDroit.addLayout(layoutGrille)

        # création de la liste des classes
        classesRangees = sorted(self.liste_des_classes())  # crée une nouvelle liste triée
        self.comboBoxGauche.addItems(classesRangees)
        self.comboBoxGauche.currentTextChanged.connect(self.choisir_classe_options)
        
        # checkbutton Aléatoite
        layoutCheckBox = QHBoxLayout()
        self.checkBox = QCheckBox("AAleatoire")
        layoutCheckBox.addWidget(self.checkBox)
        layoutBasDroit.addLayout(layoutCheckBox)
        self.checkBox.setEnabled(False) # désactiver le bouron checkBox
        
        # boutons radios avec/sans nom prénoms
        layoutRadioBoutonsBas = QHBoxLayout()
        self.boutonRadioBas1 = QRadioButton("Prenom+Nom")
        layoutRadioBoutonsBas.addWidget(self.boutonRadioBas1)
        self.boutonRadioBas2 = QRadioButton("Prenom")
        layoutRadioBoutonsBas.addWidget(self.boutonRadioBas2)
        self.boutonRadioBas3 = QRadioButton("Nom")
        layoutRadioBoutonsBas.addWidget(self.boutonRadioBas3)
         #bouton radi 1 est sélectionné
        self.boutonRadioBas1.setChecked(True)
        layoutBasDroit.addLayout(layoutRadioBoutonsBas)
        
    # Bouton pour valider le choix
        layoutBouton = QHBoxLayout()
        self.boutonVal = QPushButton("Valider")
        self.boutonVal.clicked.connect(self.configRechercher)
        layoutBouton.addWidget(self.boutonVal)
        layoutBasDroit.addLayout(layoutBouton)
        # créer la liste des options
        self.creerComboOptions()

    # ancrer le layout principal à la fenêtre
        self.setLayout(layoutBasDroit)

        self.show()
        
    def liste_des_classes(self) -> list:
        """Renvoie la liste des classes de l'établissement"""
        classes = self.modifier_bdd.lister_classes()
        return classes

    def configRechercher(self) -> None:
        """activer/désactiver les listes les comboBox, des radiobuttons
           et des labels"""
        if self.boutonRadioHaut4.isChecked():
            # désactiver les radiobuttons
            self.boutonRadioHaut1.setEnabled(False)
            self.boutonRadioHaut2.setEnabled(False)
            self.boutonRadioHaut3.setEnabled(False)
            self.boutonRadioHaut4.setEnabled(False)
            # désactiver les listes des comboBox
            self.comboBoxGauche.setEnabled(False)
            self.comboBoxDroite.setEnabled(False)
        else:
            # activer les listes des comboBox
            self.comboBoxGauche.setEnabled(True)
            self.comboBoxDroite.setEnabled(True)
            # activer les radiobuttons
            self.boutonRadioHaut1.setEnabled(True)
            self.boutonRadioHaut2.setEnabled(True)
            self.boutonRadioHaut3.setEnabled(True)
            self.boutonRadioHaut4.setEnabled(True)

    def definirOrdreDefilement(self) -> None :
        """Définir l'ordre de défilement"""
        self.ordreAleatoire = self.checkBox.isChecked() 

    def choisir_classe_options(self, event) -> None :
        """Choisir la classe et mettre à jour les élèves et les options"""
        classeSelectionnee = self.comboBoxGauche.currentText()
        # Récupère la liste des élèves de la classe
        # recupérer la liste des élèves
        self.modifier_bdd.eleves_classe(classeSelectionnee)  # exécute la méthode (pas de retour)
        self.listeEleves = self.modifier_bdd.listeEleves
        # Récupère uniquement les options réellement présentes dans cette classe
        self.listeOptions = self.creerOptions()
        # Met à jour la combobox des options
        self.creerComboOptions()

    def creerOptions(self) -> list:
        """Créer la liste des options présentes uniquement dans la classe sélectionnée"""
        listeOptions = []
        for eleve in self.listeEleves:
            options = eleve[2]  # une liste d'options (ex: ['ALL2', 'CAM'])
            for option in options:
                if option not in listeOptions:
                    listeOptions.append(option)
        listeOptions = sorted(listeOptions)
        listeOptions.insert(0, "TOUS")
        self.listeOptions = listeOptions  # mise à jour de l’attribut utilisé par la combobox
        self.creerComboOptions()
        return listeOptions

    def creerComboOptions(self) -> None:
        """créer la liste des options"""
        self.comboBoxDroite.blockSignals(True)  # éviter appel involontaire à choisirOption
        self.comboBoxDroite.clear()  # vider l'ancienne liste
        self.comboBoxDroite.addItems(self.listeOptions)
        self.comboBoxDroite.blockSignals(False)
        self.comboBoxDroite.currentTextChanged.connect(self.choisirOption)


    def choisirOption(self, event) -> None:
        """Sélectionner l'option des élèves"""
        self.optionSelectionnee = self.comboBoxDroite.currentText()

# ----------------------------------------------------

if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    fenetre = FrameDroiteBasse()
    fenetre.show()
    app.exec()