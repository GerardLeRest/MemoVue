#!/usr/bin/python2
# -*- coding: utf-8 -*

##########################################
# afficher la photo de l'élève sélecctionné
# et ses informations
##########################################


import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QGridLayout, QLabel, QHBoxLayout, QPushButton
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
        self.prenom.setStyleSheet("border: 1px solid gray; padding: 2px;") # décoration
        layoutGrille.addWidget(self.prenom, 0, 1)
        layoutGrille.addWidget(QLabel("Prenom"), 0, 0)
        # nom
        self.nom = QLabel()
        self.nom.setText("Nom")
        self.nom.setStyleSheet("border: 1px solid gray; padding: 2px;") # décoration
        layoutGrille.addWidget(self.nom, 1, 1)
        layoutGrille.addWidget(QLabel("Nom"), 1, 0) 
        # attachement à layoutGauche
        layoutGauche.addLayout(layoutGrille)
        
        # Layout du milieu
        layoutMilieu = QVBoxLayout()
        # Insertion de la photo de l'inconnu
        self.labelImage = QLabel()
        self.image = QPixmap(repertoire_racine+os.sep+"fichiers"+os.sep+"images"+os.sep+"inconnu.jpg")
        self.labelImage.setPixmap(self.image) 
        layoutMilieu.addWidget(self.labelImage,  alignment=Qt.AlignCenter)   
        # QHBoxLayout - icones
        layoutBoutons = QHBoxLayout()
        # mise en place des quatre boutons 
        fonctions=[self.accederPremier,self.accederPrecedent,self.accederSuivant,self.accederDernier]
        icones=["Gnome-go-first.png","Gnome-go-previous.png","Gnome-go-next.png","Gnome-go-last.png", ]
        self.boutons = [QPushButton() for _ in range(4)] # 4 boutons indépendants
        for i in range(len(icones)):
            self.boutons[i].setIcon(QIcon(repertoire_racine+os.sep+"fichiers"+os.sep+"icones"+os.sep+icones[i]))
            self.boutons[i].setIconSize(QSize(24, 24))  # taille d'affichage de l'image
            self.boutons[i].clicked.connect(fonctions[i])
            layoutBoutons.addWidget(self.boutons[i])
        layoutMilieu.addLayout(layoutBoutons)
        # attachement à layoutGauche
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
        layoutBas.addWidget(self.classe, alignment=Qt.AlignCenter)
        # affichage des options
        self.options = QLabel() # permet de changer le texte du label
        self.options.setText("OPTIONS")
        layoutBas.addWidget(self.options, alignment=Qt.AlignCenter)
        # attachement au layout gauche
        layoutGauche.addLayout(layoutBas)

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
        """ metrre à jour le nom, le prénom, l'option, la classe,
        la photo et le numéro d'ordre de l'élève """
        self.majNomPrenom()
        self.majClasseOptions()
        self.majPhoto()
        self.majNumOrdreElev()
            
    def majPhoto(self) -> None:
        """ Met à jour la photo dans l'interface """
        chemin_rel = self.listeEleves[self.rang][3]  # ← Exemple : 'fichiers/photos/1S1/Henry_Clement.jpg'
        chemin_image = os.path.join(repertoire_racine, chemin_rel)  # ← Construction du chemin absolu
        pixmap = QPixmap(chemin_image)
        self.labelImage.setPixmap(pixmap)    

    def majNomPrenom(self) -> None:
        """Met à jour le nom et le prénom dans l'interface"""
        # Index [0] = prénom, [1] = nom
        self.prenom.setText(self.listeEleves[self.rang][0])  # Prénom
        self.nom.setText(self.listeEleves[self.rang][1])     # Nom

        
    def majClasseOptions(self) -> None:
        """Mettre à jour la classe et les options dans l'interface"""
        prenom = self.prenom.text().strip().capitalize()
        nom = self.nom.text().strip().upper()
        classe_nom = self.modif_bdd.determiner_classe(prenom, nom)
        self.classe.setText(classe_nom if classe_nom else "Classe inconnue")
        
        # résolution de -C-A-M- au lieu de CAM
        donnees = self.listeEleves[self.rang][2]
        if isinstance(donnees, str):
            listeOptions = [opt.strip() for opt in donnees.split(',') if opt.strip()]
        else:
            listeOptions = donnees

        texte = " - ".join(listeOptions)
        self.options.setText(texte)
        
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
        ['Sarah', 'Fernandez', ['CAM', 'THE'], 'fichiers/photos/1S1/Fernandez_Sarah.jpg'],
        ['Clement', 'Henry', ['CAM'], 'fichiers/photos/1S1/Henry_Clement.jpg'],
        ['Emma', 'Petit', ['ESP'], 'fichiers/photos/PSTI2D1/Petit_Emma.jpg']
    ]
    fenetre = FrameGauche(listeEleves=liste)
    fenetre.nbreElev = len(liste)
    fenetre.show()
    sys.exit(app.exec_())
