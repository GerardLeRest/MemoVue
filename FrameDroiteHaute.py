#!/usr/bin/python2
# -*- coding: utf-8 -*

#####################################################
# rechercher une ou plusieurs personnes dans 
# l'établissement
#####################################################

import tkinter as tk
import os



from PIL import Image, ImageTk

repertoire_racine=os.path.dirname(os.path.abspath(__file__)) # répetoire du fichier pyw

class FrameDoiteHaute(tk.Frame):
    """ Créer la partie droite haute de l'interface """
        
    def __init__(self, fenetre: tk.Widget):
        """Constructeur de la frame de droite et de ses éléments"""
        tk.Frame.__init__(self,fenetre, relief=tk.GROOVE, bd=3) # constructeur de la classe parente
        self.grid(row=0,column=1,pady=3)
        # zone de saisie
        self.labelPrenom=tk.Label(self, text=" Prénom:",fg="grey") # label du prénom
        self.labelPrenom.grid(row=0, column=0, sticky="w") 
        self.repPrenom=tk.StringVar() #réponse du prénom
        self.repPrenomEntry=tk.Entry(self, state = tk.DISABLED, textvariable=self.repPrenom)
        self.repPrenomEntry.grid(row=0, column=1, sticky="w",padx=5, pady=3)
        self.labelNom=tk.Label(self, text=" Nom:",fg="grey") # label du nom
        self.labelNom.grid(row=1, column=0, sticky="w")
        self.repNom=tk.StringVar() # réponse du prénom
        self.reponseNomEntry=tk.Entry(self, state = tk.DISABLED, textvariable=self.repNom)
        self.reponseNomEntry.grid(row=1, column=1, sticky="w",padx=5, pady=3)
        #frame boutons
        frameBoutons=tk.Frame(self)
        frameBoutons.grid(row=2,columnspan=2, sticky="n",pady=5) 
        # bouton de validation 
        self.boutVal = tk.Button(frameBoutons, text="Valider", state=tk.NORMAL)
        self.boutVal.pack(side="left",padx=5)
        # bouton effacer
        self.boutEff = tk.Button(frameBoutons, text="Effacer", state=tk.DISABLED)
        self.boutEff.pack(side="left",padx=5)
        # bouton pour voir la reponse
        self.boutSuite = tk.Button(frameBoutons, text="Suite", state=tk.DISABLED)

        self.boutSuite.pack(side="right",padx=5)
        # image de validation
        repertoire_racine=os.path.dirname(os.path.abspath(__file__))
        image = Image.open(repertoire_racine+os.sep+"fichiers"+os.sep+"icones"+os.sep+"transparent.png")  
        self.photo = ImageTk.PhotoImage(image)  
        self.canvas = tk.Canvas(self, width = image.size[0], height = image.size[1])  
        self.photoSurCanvas=self.canvas.create_image(0,0, anchor = tk.NW, image=self.photo) 
        self.canvas.grid(row=4, column=1, pady=5, padx = 3, sticky="e")
        # affichage des bonnes réponses
        self.nbreRep=tk.StringVar() # permet de changer le texte du label
        self.nbreRep.set("0/0 ")
        self.nbreRepExactes=0 
        self.labelNbreRep=tk.Label(self, textvariable=self.nbreRep,fg="grey",font=("Arial", 20))
        self.labelNbreRep.grid(row=4, column=0,padx=5) 
        
    def configRechercher(self) -> None:
        """configurer - mode Rechercher"""
        # changer couleur label
        self.labelPrenom.config(fg="black")
        self.labelNom.config(fg="black")
        self.labelNbreRep.config(fg="grey") 
        # Désactiver l'affichage des bonnes réponses
        self.DesAffichRep()
        # activer/désactiver boutons 
        self.boutVal.config(state=tk.NORMAL)
        self.boutEff.config(state=tk.NORMAL)
        self.boutSuite.config(state=tk.DISABLED)
    
    def DesAffichRep(self) -> None:
        """ désactiver l'affichage des bonnes réponses"""
        self.labelNbreRep.config(fg="grey") #nbre bonnes reponses en gris
        self.nbreRepExactes=0  # nbre de réponses exactes
        # maj nbrebonnes réponses
        self.nbreRep.set(str(self.nbreRepExactes)+os.sep+"0")    
    
    def desFrameDrHa(self) -> None:
        """désactiver des boutons et les entry de la frameDB"""     
        self.repPrenomEntry.config(state=tk.DISABLED)
        self.reponseNomEntry.config(state=tk.DISABLED)
        self.boutVal.configure(state="disabled")
        self.boutEff.configure(state="disabled")
        self.boutSuite.configure(state="disabled")
        
    def effacerReponses(self) -> None:
        """effacer réponses"""
        # effacer champs des noms et prénom
        self.repPrenomEntry.configure(state="normal")
        self.repPrenomEntry.delete(0, 'end') 
        self.reponseNomEntry.configure(state="normal")
        self.reponseNomEntry.delete(0, 'end')
        # effacer icone
        image = Image.open(repertoire_racine+os.sep+"fichiers"+os.sep+"icones"+os.sep+"transparent.png")  
        self.photo = ImageTk.PhotoImage(image)  
        # remplacement de la photo
        self.canvas.itemconfig(self.photoSurCanvas, image = self.photo)   
        
    def configTestEcrit(self) -> None:
        """ configurer - Test écrit """
        # changer couleur label
        self.labelPrenom.config(fg="black")
        self.labelNom.config(fg="black")
        self.labelNbreRep.config(fg="brown") 
        # effacer réponses
        self.effacerReponses()        
        # activer boutons 
        self.boutVal.config(state=tk.NORMAL)
        self.boutEff.config(state=tk.NORMAL)
        self.boutSuite.config(state=tk.NORMAL)   
        
# ----------------------------------------------------
        
if __name__ == '__main__':     
    fenetre = tk.Tk()
    Application= FrameDoiteHaute(fenetre)
    Application.repPrenomEntry.config(state=tk.NORMAL)
    Application.reponseNomEntry.config(state=tk.NORMAL)
    Application.boutVal.configure(state="normal")
    Application.boutEff.configure(state="disabled")
    Application.boutSuite.configure(state="disabled")    
    fenetre.mainloop()