#!/usr/bin/python2
# -*- coding: utf-8 -*

##########################################
# afficher la photo de l'élève sélecctionné
# et ses informations
##########################################


from PIL import Image, ImageTk
import tkinter as tk
import os
from ModifierBDD import  ModifierBDD

repertoire_racine=os.path.dirname(os.path.abspath(__file__)) # répetoire du fichier pyw
icones=["Gnome-go-first.png","Gnome-go-previous.png","Gnome-go-next.png","Gnome-go-last.png", ]

class FrameGauche (tk.Frame):
    """ Créer la partie gauche de l'interface """
        
    def __init__(self,fenetre: tk.Widget, listeEleves:list=[]):
        """Constructeur de la frame de gauche et de ses éléments"""
        tk.Frame.__init__(self, fenetre) # constructeur de la classe parente
        self.grid(row=0,column=0,rowspan=3,padx=10,pady=2)
        self.listeEleves=listeEleves #liste des élèves
        self.rang=0     #rang de l'élève dans la classe
        self.modif_bdd = ModifierBDD("fichiers/eleves.db")
        self.nbreElev=0 # nbre élèves
       # Identification des élèves
        frameHaut = tk.Frame(self, relief=tk.GROOVE, bd=3)
        frameHaut.pack(pady=3)

        # Définir les StringVar
        self.nom = tk.StringVar()
        self.nom.set("Nom")
        self.prenom = tk.StringVar()
        self.prenom.set("Prénom")

        # Associer les bons labels avec les bons StringVar
        tk.Label(frameHaut, text="Nom:").grid(row=0, column=0, sticky=tk.W)
        tk.Label(frameHaut, textvariable=self.nom, fg="brown", width=25, font=("Arial", 11)).grid(row=0, column=1, sticky=tk.W, padx=4, pady=4)
        tk.Label(frameHaut, text="Prénom:").grid(row=1, column=0, sticky=tk.W)
        tk.Label(frameHaut, textvariable=self.prenom, fg="brown", width=25, font=("Arial", 11)).grid(row=1, column=1, sticky=tk.W, padx=4, pady=4)

        # Insertion de la photo de l'inconnu       
        self.image = Image.open(repertoire_racine+os.sep+"fichiers"+os.sep+"images"+os.sep+"inconnu.jpg")  
        self.photo = ImageTk.PhotoImage(self.image)  
        self.index_photo = 3 # les photos sont dans la quatrième colonne
        self.canvas = tk.Canvas(self, width = self.image.size[0], height = self.image.size[1])  
        self.photoSurCanvas=self.canvas.create_image(0,0, anchor = tk.NW, image=self.photo) 
        self.canvas.pack(pady=2)  
        # boutons - choix de l'élève
        frameBoutons = tk.Frame(self)
        frameBoutons.pack(pady=2)
        self.photos, self.boutons=[], []
        fonctions=[self.accederPremier,self.accederPrecedent,self.accederSuivant,self.accederDernier]
        for i in range(len(icones)):
            image=Image.open(repertoire_racine+os.sep+"fichiers"+os.sep+"icones"+os.sep+icones[i])
            self.photos.append(ImageTk.PhotoImage(image)) 
            self.boutons.append(tk.Button(frameBoutons, image=self.photos[i], command=fonctions[i]))
            self.boutons[i].pack(side=tk.LEFT, pady=2)
            self.boutons[i].configure(state="disabled")
        # affichage des élèves restants
        self.numOrdreElev=tk.StringVar() # permet de changer le texte du label
        self.numOrdreElev.set("rang/effectif ")
        labelNumOrdreElev=tk.Label(self, textvariable=self.numOrdreElev,fg="black")
        labelNumOrdreElev.pack(pady=2)
        # affichage de la classe et des options
        self.classe=tk.StringVar() # permet de changer le texte du label
        self.classe.set("CLASSE-CATÉGORIE")
        tk.Label(self, textvariable=self.classe, fg="darkorange",width=40, font=("Arial", 8)).pack(pady=2)
        self.options=tk.StringVar() # permet de changer le texte du label
        self.options.set("Options-Fonctions")
        tk.Label(self, textvariable=self.options, fg="seagreen",width=40, font=("Arial", 8)).pack(pady=2)
        
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
        chemin_rel = self.listeEleves[self.rang][self.index_photo]
        self.image = Image.open(chemin_rel)
        self.photo = ImageTk.PhotoImage(self.image)
        self.canvas.itemconfig(self.photoSurCanvas, image=self.photo)
    
    def majNomPrenom(self) -> None:
        """Met à jour le nom et le prénom dans l'interface"""
        # Index [0] = prénom, [1] = nom
        self.prenom.set(self.listeEleves[self.rang][0])  # Prénom
        self.nom.set(self.listeEleves[self.rang][1])     # Nom

        
    def majClasseOptions(self) -> None:
        """Mettre à jour la classe et les options dans l'interface"""

        prenom = self.prenom.get().strip().capitalize()
        nom = self.nom.get().strip().upper()
        classe_nom = self.modif_bdd.determiner_classe(prenom, nom)
        self.classe.set(classe_nom if classe_nom else "Classe inconnue")
        
        # résolution de -C-A-M- au lieu de CAM
        donnees = self.listeEleves[self.rang][2]
        if isinstance(donnees, str):
            listeOptions = [opt.strip() for opt in donnees.split(',') if opt.strip()]
        else:
            listeOptions = donnees

        texte = " - ".join(listeOptions)
        self.options.set(texte)
        
    def majNumOrdreElev(self) -> None:
        """mettre à jour le numéro d'ordre de l'élève"""
        if self.nbreElev==len(self.listeEleves): # apprentissage
            self.numOrdreElev.set(str(self.rang+1)+"/"+str(self.nbreElev))
        else: # test mental
            self.numOrdreElev.set(str(self.rang//2+1)+"/"+str(self.nbreElev))  
                
# ----------------------------------------------------
        
if __name__ == '__main__':     
    fenetre = tk.Tk()
    liste = []
    liste = [['Sarah', 'Fernandez', ['CAM', 'THE'], 'fichiers/photos/1S1/Fernandez Sarah.jpg'], ['Clément', 'Henry', ['CAM'], 'fichiers/photos/1S1/Henry Clément.jpg'], ['Tom', 'Lemoine', ['CAM'], 'fichiers/photos/TSTI2D2/Lemoine Tom.jpg']]
    Application= FrameGauche(fenetre,liste) 
    # activer les boutons frame gauche
    for i in range(len(icones)):
        Application.boutons[i].configure(state="active") 
    # nombre d'élèves dans la classe
    Application.nbreElev=len(liste)
    print (Application.nbreElev)
    fenetre.mainloop()