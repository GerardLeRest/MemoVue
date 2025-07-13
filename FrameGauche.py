#!/usr/bin/python2
# -*- coding: utf-8 -*

##########################################
# afficher la photo de l'élève sélecctionné
# et ses informations
##########################################


import os
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QGridLayout, QLabel, QHBoxLayout, QPushButton, QSpacerItem, QSizePolicy
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import QSize, Qt
from ModifierBDD import  ModifierBDD

repertoireRacine=os.path.dirname(os.path.abspath(__file__)) # répetoire du fichier pyw
icones=["Gnome-go-first.png","Gnome-go-previous.png","Gnome-go-next.png","Gnome-go-last.png", ]

class FrameGauche (QWidget):
    """ Créer la partie gauche de l'interface """
        
    def __init__(self, listePersonnes, fenetre, config):
        """Constructeur de la frame de gauche et de ses éléments"""
        super().__init__(fenetre) # constructeur de la classe parente
        self.config = config # configuration de l'interface - json
        layoutGauche = QVBoxLayout()  
        # poisition de LayoutGauche dans la fenetre principale de la fenêtreself.LayoutPrincipal(row=0,column=0,rowspan=3,padx=10,pady=2)
        self.listePersonnes=listePersonnes #liste des élèves
        self.rang=0     #rang de l'élève dans la classe
        self.modif_bdd = ModifierBDD(config,config["BaseDonnees"])
        self.nbrePers=0 # nbre élèves
        self.resize(150, 100) # définir une taille fixe pour la fenêtre

       
        # Partie haute du layout
        # QGridLayout
        # prenom
        layoutGrille = QGridLayout()
        self.prenom = QLabel("-")
        self.prenom.setText("Prénom")
        self.prenom.setStyleSheet("color: #446069; font-weight: bold; font-size: 16px")
        layoutGrille.addWidget(self.prenom, 0, 1)
        layoutGrille.addWidget(QLabel("Prénom :"), 0, 0, alignment=Qt.AlignRight)
        # nom
        self.nom = QLabel()
        self.nom.setText("Nom")
        self.nom.setStyleSheet("color: #446069; font-weight: bold; font-size: 16px")
        layoutGrille.addWidget(self.nom, 1, 1)
        layoutGrille.addWidget(QLabel("Nom :"), 1, 0, alignment=Qt.AlignRight)
        # attachement à layoutGauche
        layoutGauche.addLayout(layoutGrille)
        
        # Layout principal vertical
        layoutMilieu = QVBoxLayout()

        # Création du QLabel de l'image
        self.labelImage = QLabel()
        self.labelImage.setFixedSize(128, 128)
        self.labelImage.setStyleSheet("border: 1px solid #666; background-color: #f0f0f0;")
        self.labelImage.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Chargement de l'image par défaut
        cheminDefaut = os.path.join(repertoireRacine, "fichiers", "images", "inconnu.jpg")
        pixmapDefaut = QPixmap(cheminDefaut).scaled(
            128, 128,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.labelImage.setPixmap(pixmapDefaut)
        # Puis ajout dans layout vertical principal
        layoutBoutons = QHBoxLayout()

        # boutons de défilement
        fonctions = [self.accederPremier, self.accederPrecedent, self.accederSuivant, self.accederDernier]
        icones = ["Gnome-go-first.png", "Gnome-go-previous.png", "Gnome-go-next.png", "Gnome-go-last.png"]
        self.boutons = []
        for i in range(4):
            bouton = QPushButton()
            bouton.setIcon(QIcon(os.path.join(repertoireRacine, "fichiers", "icones", icones[i])))
            bouton.setIconSize(QSize(24, 24))
            bouton.clicked.connect(fonctions[i])
            layoutBoutons.addWidget(bouton)
            self.boutons.append(bouton)
        layoutBoutons.setSpacing(6)  # espace horizontal entre flèches

        # Bloc vertical (photo + boutons), avec marges
        blocPhoto = QVBoxLayout()
        blocPhoto.setContentsMargins(10, 10, 10, 10)  # marges autour du bloc
        blocPhoto.setSpacing(10)  # espace entre photo et boutons
        blocPhoto.addWidget(self.labelImage, alignment=Qt.AlignCenter)
        blocPhoto.addLayout(layoutBoutons)
        # Encapsule le tout dans un widget
        photoWidget = QWidget()
        photoWidget.setLayout(blocPhoto)
        # Ajoute à layoutMilieu
        layoutMilieu.addWidget(photoWidget)
        # Ajoute à layoutGauche (comme avant)
        layoutGauche.addLayout(layoutMilieu)
		
		# layout bas
        # affichage des élèves restants
        layoutBas = QVBoxLayout()
        self.numOrdrePers=QLabel() # rang de la Personne
        self.numOrdrePers.setText("rang/effectif ")
        layoutBas.addWidget(self.numOrdrePers, alignment=Qt.AlignCenter)
        # affichage de la structure 
        self.structure=QLabel() # label de la structure
        self.structure.setText(config["Structure"])
        self.structure.setStyleSheet("color: #76aeba; font-weight: bold; font-size: 11pt;")
        layoutBas.addWidget(self.structure, alignment=Qt.AlignCenter)
        # affichage des options
        self.specialites = QLabel() # permet de changer le texte du label
        self.specialites.setText(config["Specialite"])
        self.specialites.setStyleSheet("font-size: 10pt;")
        layoutBas.addWidget(self.specialites, alignment=Qt.AlignCenter)
        # attachement au layout gauche
        layoutGauche.addLayout(layoutBas)

        # Espace vertical fixe de 10 pixels
        spacer = QSpacerItem(0, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        layoutGauche.addItem(spacer)
        # attachement à la fenêtre principale
        self.setLayout(layoutGauche)

        self.show()

    def accederPremier(self) -> None:
        """accéder au Premier élève de la liste"""
        self.rang=0
        self.maj()
        
    def accederPrecedent(self) -> None:
        """accéder à l'élève précédent"""
        if (self.rang>0):
            self.rang=self.rang-1
        self.maj()
                
    def accederSuivant(self) -> None:
        """accéder à l'élève suivant"""
        if (self.rang<len(self.listePersonnes)-1):
            self.rang=self.rang+1
        self.maj()
                
    def accederDernier(self):
        """accéder au dernier élève"""
        self.rang=len(self.listePersonnes)-1
        self.maj()
        
    def maj(self) -> None:
        """Mettre à jour l'affichage de l'élève courant si la liste est valide"""
        if not self.listePersonnes or self.rang >= len(self.listePersonnes):
            return  # on ne fait rien si la liste est vide ou le rang est hors limites
        self.majNomPrenom()
        self.majClasseOptions()
        self.majPhoto()
        self.majnumOrdrePers()

    def effacer_affichage(self) -> None:
        """Effacer les informations affichées en cas de données manquantes"""
        self.prenom.setText("-")
        self.nom.setText("-")
        self.structure.setText("-")
        self.specialites.setText("-")
        self.numOrdrePers.setText("-")
        image_par_defaut = os.path.join(repertoireRacine, "fichiers", "images", "inconnu.jpg")
        self.labelImage.setPixmap(QPixmap(image_par_defaut))   
            
    def majPhoto(self) -> None:
        """Mise à jour de la photo"""
        nomImage = self.listePersonnes[self.rang][4]
        cheminImage = os.path.join(repertoireRacine, "fichiers", self.config["CheminPhotos"], nomImage)

        if os.path.exists(cheminImage):
            pixmap = QPixmap(cheminImage)
        else:
            # En cas d’image manquante, image par défaut
            cheminDefaut = os.path.join(repertoireRacine, "fichiers", "images", "inconnu.jpg")
            pixmap = QPixmap(cheminDefaut)
        self.labelImage.setPixmap(pixmap)

    def majNomPrenom(self):
        self.prenom.setText(self.listePersonnes[self.rang][0])
        self.nom.setText(self.listePersonnes[self.rang][1])
            
    def majClasseOptions(self):
        self.structure.setText(self.listePersonnes[self.rang][2])
        # Options (colonne 3), sous forme de liste
        options = self.listePersonnes[self.rang][3]
        # transforme une liste d’options en chaîne de caractères lisible :
        #['ESP2', 'THE'] devient "ESP2, THE"
        texteOptions = "- ".join(options)
        self.specialites.setText(texteOptions)

    def majnumOrdrePers(self) -> None:
        """mettre à jour le numéro d'ordre de l'élève"""
        if self.nbrePers==len(self.listePersonnes): # apprentissage
            self.numOrdrePers.setText(str(self.rang+1)+"/"+str(self.nbrePers))
        else: # test mental
            self.numOrdrePers.setText(str(self.rang//2+1)+"/"+str(self.nbrePers))  
                
# ----------------------------------------------------
        
from PySide6.QtWidgets import QApplication

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    listePersonnes = [
        ['Sarah', 'Fernandez', '1S1', ['CAM', 'THE'], 'fichiers/photos/1S1/Fernandez_Sarah.jpg'],
        ['Clement', 'Henry', '1S1', ['CAM'], 'fichiers/photos/1S1/Henry_Clement.jpg'],
        ['Emma', 'Petit', 'PSTI2D1', ['ESP'], 'fichiers/photos/PSTI2D1/Petit_Emma.jpg']
    ]
    config = {
        "Organisme": "Entreprise",
        "Structure": "Département",
        "Personne": "Salarié",
        "Specialite": "Fonctions",
        "BaseDonnees": "salaries.db",
        "CheminPhotos": "photos/salaries/"
    }
    fenetre = FrameGauche(listePersonnes, config)
    fenetre.nbrePers = len(listePersonnes)
    fenetre.show()
    sys.exit(app.exec_())
