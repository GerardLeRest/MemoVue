#!/usr/bin/python2
# -*- coding: utf-8 -*

#####################################################
# selection du mode de fonctionnement
# (apprentissage, test mental, test ecrit, Rechercher)
# choix de la classe et de l'option
#####################################################
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QRadioButton, QPushButton, QGridLayout, QLabel, QComboBox, QCheckBox, QButtonGroup
from ModifierBDD import ModifierBDD
from PySide6.QtWidgets import QApplication
import sys

class FrameDroiteBasse (QWidget):
    """ Créer la partie droite basse de l'interface """
    def __init__(self, fenetre = None):
        """Constructeur de la frame de droite et de ses éléments"""
        # constructeur de la classe parente
        super().__init__(fenetre)
        self.listeEleves = []  # liste des élèves de la classe sélectionnée
        self.listeOptions = []  # liste des options des élèves de la classese
        #self.modifier_bdd = ModifierBDD("fichiers/eleves.bdd") -faux?
        self.modifier_bdd = ModifierBDD("fichiers/eleves.db")
        self.optionSelectionnee = ""  # option sélectionnée

        layoutBasDroit = QVBoxLayout()
        layoutBasDroit.setSpacing(10)
        layoutBoutonsRadiosHaut = QHBoxLayout()
        # boutons radio des modes
        self.boutonRadioHaut1 = QRadioButton("Apprentissage")
        self.boutonRadioHaut2 = QRadioButton("Test mental")
        self.boutonRadioHaut3 = QRadioButton("Test ecrit")
        self.boutonRadioHaut4 = QRadioButton("Rechercher")
        # regroupement
        self.groupeHaut = QButtonGroup()
        self.groupeHaut.addButton(self.boutonRadioHaut1)
        self.groupeHaut.addButton(self.boutonRadioHaut2)
        self.groupeHaut.addButton(self.boutonRadioHaut3)
        self.groupeHaut.addButton(self.boutonRadioHaut4)
        # insetion dans le layout
        layoutBoutonsRadiosHaut.addWidget(self.boutonRadioHaut1)
        layoutBoutonsRadiosHaut.addWidget(self.boutonRadioHaut2)
        layoutBoutonsRadiosHaut.addWidget(self.boutonRadioHaut3)
        layoutBoutonsRadiosHaut.addWidget(self.boutonRadioHaut4)
         #bouton radi 1 est sélectionné
        self.boutonRadioHaut1.setChecked(True)
        #rattachement au layout principal de la classe
        layoutBasDroit.addLayout(layoutBoutonsRadiosHaut)
        
        # Combobox - QGridLayout
        layoutGrille = QGridLayout()
        layoutGrille.setSpacing(10)
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
        self.checkBox = QCheckBox("Aleatoire")
        layoutCheckBox.addWidget(self.checkBox)
        layoutBasDroit.addLayout(layoutCheckBox)
        
        # boutons radios avec/sans nom prénoms
        layoutBoutonsRadiosBas = QHBoxLayout()
        self.groupeBas = QButtonGroup()
        self.boutonRadioBas1 = QRadioButton("Prenom+Nom")
        self.boutonRadioBas2 = QRadioButton("Prenom")
        self.boutonRadioBas3 = QRadioButton("Nom")
        # regroupement
        self.groupeBas.addButton(self.boutonRadioBas1)
        self.groupeBas.addButton(self.boutonRadioBas2)
        self.groupeBas.addButton(self.boutonRadioBas3)
        # attachement au layout horizontal
        layoutBoutonsRadiosBas.addWidget(self.boutonRadioBas1)
        layoutBoutonsRadiosBas.addWidget(self.boutonRadioBas2)
        layoutBoutonsRadiosBas.addWidget(self.boutonRadioBas3)
         #bouton radi 1 est sélectionné
        self.boutonRadioBas1.setChecked(True)
        layoutBasDroit.addLayout(layoutBoutonsRadiosBas)
        
        # Bouton pour valider le choix
        bouton_style = """
        QPushButton {
            background-color: #e0e0e0;
            border: 1px solid #888;
            border-radius: 6px;
            padding: 6px 14px;
        }
        QPushButton:hover {
            background-color: #d0d0d0;
        }
        QPushButton:pressed {
            background-color: #c0c0c0;
        }
        """
        # Créer le bouton "Valider"
        self.boutonVal = QPushButton("Valider")
        self.boutonVal.setFixedWidth(120)
        self.boutonVal.setStyleSheet(bouton_style)
        self.boutonVal.clicked.connect(self.configRechercher)

        # Centrer le bouton
        layoutBouton = QHBoxLayout()
        layoutBouton.addStretch()
        layoutBouton.addWidget(self.boutonVal)
        layoutBouton.addStretch()

        # Ajouter au layout principal du bas
        layoutBasDroit.addSpacing(10)  # petit espace avant le bouton
        layoutBasDroit.addLayout(layoutBouton)
        # créer la liste des options
        self.creerComboOptions()

    # ancrer le layout principal à la fenêtre
        self.setLayout(layoutBasDroit)

        self.show()
        
    def liste_des_classes(self) -> list:
        """Renvoie la liste des classes de l'établissement"""
        classes = self.modifier_bdd.listerClasses()
        classes.insert(0,"- choisir une classe -")
        return classes

    def configRechercher(self) -> None:
        """activer/désactiver les listes les comboBox, des radiobuttons
           et des labels"""
        if self.boutonRadioHaut4.isChecked():
            # désactiver les radiobuttons
            # self.boutonRadioHaut1.setEnabled(False)
            # self.boutonRadioHaut2.setEnabled(False)
            # self.boutonRadioHaut3.setEnabled(False)
            # self.boutonRadioHaut4.setEnabled(False)
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

    def choisir_classe_options(self, event=None) -> None:
        """Choisir la classe et mettre à jour les élèves et les options"""
        classeSelectionnee = self.comboBoxGauche.currentText()

        # Met à jour les élèves via la BDD
        self.modifier_bdd.elevesClasse(classeSelectionnee)
        self.listeEleves = self.modifier_bdd.listeEleves

        # Crée les options présentes uniquement dans cette classe
        self.listeOptions = self.creerOptions()

        # Met à jour la combobox des options
        self.creerComboOptions()

    def creerOptions(self) -> list:
        """Créer la liste des options présentes uniquement dans la classe sélectionnée"""
        listeOptions = []
        for eleve in self.listeEleves:
            options = eleve[3]  # Index 2 = liste des options (ex: ['ALL2', 'CAM'])
            for option in options:
                if option not in listeOptions:
                    listeOptions.append(option)
        listeOptions = sorted(listeOptions)
        listeOptions.insert(0, "TOUS")
        self.listeOptions = listeOptions
        return listeOptions
    
    def creerComboOptions(self) -> None:
        """Créer la liste déroulante des options sans déclencher d'événement parasite"""
        #self.comboBoxDroite.blockSignals(True)  # Empêche les signaux lors de la modification
        self.comboBoxDroite.clear()
        self.comboBoxDroite.addItems(self.listeOptions)
        self.comboBoxDroite.setCurrentIndex(0)  # Facultatif : force "TOUS" si besoin
        #self.comboBoxDroite.blockSignals(False)
        self.comboBoxDroite.currentTextChanged.connect(self.choisirOption)

    def choisirOption(self, event=None) -> None:
        """Sélectionner une option"""
        self.optionSelectionnee = self.comboBoxDroite.currentText()
        print("Option sélectionnée :", self.optionSelectionnee)

# ----------------------------------------------------

if __name__ == '__main__':
   
    app = QApplication(sys.argv)
    fenetre = FrameDroiteBasse()
    fenetre.show()
    app.exec()