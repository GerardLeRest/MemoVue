#!/usr/bin/python2
# -*- coding: utf-8 -*

##########################################
# afficher la photo de l'élève sélecctionné
# et ses informations
##########################################


import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QGridLayout, QLabel, QHBoxLayout, QPushButton, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QSize, Qt
from ModifierBDD import  ModifierBDD

repertoire_racine=os.path.dirname(os.path.abspath(__file__)) # répetoire du fichier pyw
icones=["Gnome-go-first.png","Gnome-go-previous.png","Gnome-go-next.png","Gnome-go-last.png", ]

class FrameGauche (QWidget):
    """ Créer la partie gauche de l'interface """
        
    def __init__(self,fenetre=None, listeEleves:list=[]):
        """Constructeur de la frame de gauche et de ses éléments"""
        super().__init__(fenetre) # constructeur de la classe parente
        layoutGauche = QVBoxLayout()  
        # poisition de LayoutGauche dans la fenetre principale de la fenêtreself.LayoutPrincipal(row=0,column=0,rowspan=3,padx=10,pady=2)
        self.listeEleves=listeEleves #liste des élèves
        self.rang=0     #rang de l'élève dans la classe
        self.modif_bdd = ModifierBDD("fichiers/eleves.db")
        self.nbreElev=0 # nbre élèves
        self.resize(150, 100) # définir une taille fixe pour la fenêtre

       
        # Partie haute du layout
        # QGridLayout
        # prenom
        layoutGrille = QGridLayout()
        self.prenom = QLabel("-")
        self.prenom.setText("Prénom")
        self.prenom.setStyleSheet("color: #006060; font-weight: bold;")
        layoutGrille.addWidget(self.prenom, 0, 1)
        layoutGrille.addWidget(QLabel("Prenom: "), 0, 0)
        # nom
        self.nom = QLabel()
        self.nom.setText("Nom")
        self.nom.setStyleSheet("color: #336699; font-weight: bold;")
        layoutGrille.addWidget(self.nom, 1, 1)
        layoutGrille.addWidget(QLabel("Nom:"), 1, 0) 
        # attachement à layoutGauche
        layoutGauche.addLayout(layoutGrille)
        
        # --- Nouveau layout du milieu ---
        layoutMilieu = QVBoxLayout()
        # Photo de l'élève
        self.labelImage = QLabel()
        self.labelImage.setStyleSheet("""border: 1px solid #666; background-color: #f0f0f0; """)
        self.image = QPixmap(repertoire_racine + os.sep + "fichiers" + os.sep + "images" + os.sep + "inconnu.jpg")
        self.labelImage.setPixmap(self.image)
        self.labelImage.setAlignment(Qt.AlignCenter)
        # Boutons fléchés
        layoutBoutons = QHBoxLayout()
        fonctions = [self.accederPremier, self.accederPrecedent, self.accederSuivant, self.accederDernier]
        icones = ["Gnome-go-first.png", "Gnome-go-previous.png", "Gnome-go-next.png", "Gnome-go-last.png"]
        self.boutons = []
        for i in range(4):
            bouton = QPushButton()
            bouton.setIcon(QIcon(repertoire_racine + os.sep + "fichiers" + os.sep + "icones" + os.sep + icones[i]))
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
        self.numOrdreElev=QLabel() # permet de changer le texte du label
        self.numOrdreElev.setText("rang/effectif ")
        layoutBas.addWidget(self.numOrdreElev, alignment=Qt.AlignCenter)
        # affichage de la classe 
        self.classe=QLabel() # permet de changer le texte du label
        self.classe.setText("CLASSE-CATÉGORIE")
        self.classe.setStyleSheet("color: #6A8FA0; font-weight: bold; font-size: 9pt;")
        layoutBas.addWidget(self.classe, alignment=Qt.AlignCenter)
        # affichage des options
        self.options = QLabel() # permet de changer le texte du label
        self.options.setText("OPTIONS")
        layoutBas.addWidget(self.options, alignment=Qt.AlignCenter)
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
        if (self.rang<len(self.listeEleves)-1):
            self.rang=self.rang+1
        self.maj()
                
    def accederDernier(self):
        """accéder au dernier élève"""
        self.rang=len(self.listeEleves)-1
        self.maj()
        
    def maj(self) -> None:
        """Mettre à jour l'affichage de l'élève courant si la liste est valide"""
        if not self.listeEleves or self.rang >= len(self.listeEleves):
            return  # on ne fait rien si la liste est vide ou le rang est hors limites
        self.majNomPrenom()
        self.majClasseOptions()
        self.majPhoto()
        self.majNumOrdreElev()

    def effacer_affichage(self) -> None:
        """Effacer les informations affichées en cas de données manquantes"""
        self.prenom.setText("-")
        self.nom.setText("-")
        self.classe.setText("-")
        self.options.setText("-")
        self.numOrdreElev.setText("-")
        image_par_defaut = os.path.join(repertoire_racine, "fichiers", "images", "inconnu.jpg")
        self.labelImage.setPixmap(QPixmap(image_par_defaut))   
            
    def majPhoto(self) -> None:
        chemin_rel = self.listeEleves[self.rang][4]
        chemin_image = os.path.join(repertoire_racine, chemin_rel)
        self.labelImage.setPixmap(QPixmap(chemin_image))

    def majNomPrenom(self):
        self.prenom.setText(self.listeEleves[self.rang][0])
        self.nom.setText(self.listeEleves[self.rang][1])
            
    def majClasseOptions(self):
        self.classe.setText(self.listeEleves[self.rang][2])
        # Options (colonne 3), sous forme de liste
        options = self.listeEleves[self.rang][3]
        # transforme une liste d’options en chaîne de caractères lisible :
        #['ESP2', 'THE'] devient "ESP2, THE"
        texteOptions = "- ".join(options)
        self.options.setText(texteOptions)

    def majNumOrdreElev(self) -> None:
        """mettre à jour le numéro d'ordre de l'élève"""
        if self.nbreElev==len(self.listeEleves): # apprentissage
            self.numOrdreElev.setText(str(self.rang+1)+"/"+str(self.nbreElev))
        else: # test mental
            self.numOrdreElev.setText(str(self.rang//2+1)+"/"+str(self.nbreElev))  
                
# ----------------------------------------------------
        
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    liste = [
        ['Sarah', 'Fernandez', '1S1', ['CAM', 'THE'], 'fichiers/photos/1S1/Fernandez_Sarah.jpg'],
        ['Clement', 'Henry', '1S1', ['CAM'], 'fichiers/photos/1S1/Henry_Clement.jpg'],
        ['Emma', 'Petit', 'PSTI2D1', ['ESP'], 'fichiers/photos/PSTI2D1/Petit_Emma.jpg']
    ]
    fenetre = FrameGauche(listeEleves=liste)
    fenetre.nbreElev = len(liste)
    fenetre.show()
    sys.exit(app.exec_())
