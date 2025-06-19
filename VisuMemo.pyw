#!/usr/bin/python3
# -*- coding: utf-8 -*

##################################################
# Apprendre ou retrouver le nom/prénom des élèves
# du lycée
##################################################

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

import tkinter.filedialog, os, random, tkinter.messagebox, sys, locale, webbrowser, copy
from FrameGauche import *
from FrameDroiteHaute import *
from FrameDroiteBasse import *

repertoire_racine = os.path.dirname(os.path.abspath(__file__)) # répetoire du fichier pyw

class Application(tk.Tk):
    """ Créer l'interface graphique et lier les diffentes classes entre elles"""
    
    def __init__(self, frameDroiteBasse = None) :
        """Constructeur de la fenêtre principale"""
        super().__init__()   # constructeur de la classe parente
        self.FrameDrBa = FrameDroiteBasse(self)
        self.FrameDrHa = FrameDoiteHaute(self)
        self.FrameG = FrameGauche (self,self.FrameDrBa.listeEleves)
        self.FrameDrBa.boutVal.bind("<Button-1>",self.configurer)
        self.FrameDrHa.boutVal.bind("<Button-1>",self.verifierRechercher)
        self.FrameDrHa.boutEff.bind("<Button-1>",self.effacer)
        self.FrameDrHa.boutSuite.bind("<Button-1>",self.AllerALaSuite)
        self.FrameDrHa.repPrenomEntry.bind('<Return>',self.validerRepNom)
        self.FrameDrHa.reponseNomEntry.bind('<Return>',self.verifierRechercher)
        # bouton info
        self.boutonInfo = tk.Button(self, text="Info")
        self.boutonInfo.grid(row=2,column=1,pady=2)
        self.boutonInfo.bind("<Button-1>",self.information)
       
    def configurer(self,event) -> None:
        """ configurer l'application"""
        self.FrameDrHa.effacerReponses()
        if (self.FrameDrBa.SelectModes.get()=="4"): # mode "Rechercher"
            self.FrameDrHa.configRechercher()
            # activer/désactiver zones de saisie 
            self.actDesZonesSaisies()            
        else:
            self.configAutresModes()           
        
    def actDesZonesSaisies(self) -> None:
        """Activer ou désactiver les zones de saisie selon le mode"""

        if self.FrameDrBa.selectPrenNom.get() == "2":  # prénom seul
            self.FrameDrHa.reponseNomEntry.config(state=tk.DISABLED)
            self.FrameDrHa.repPrenomEntry.config(state=tk.NORMAL)
            self.FrameDrHa.repPrenomEntry.focus_set()

        elif self.FrameDrBa.selectPrenNom.get() == "3":  # nom seul
            self.FrameDrHa.repPrenomEntry.config(state=tk.DISABLED)
            self.FrameDrHa.reponseNomEntry.config(state=tk.NORMAL)
            self.FrameDrHa.reponseNomEntry.focus_set()

        else:  # nom + prénom
            self.FrameDrHa.repPrenomEntry.config(state=tk.NORMAL)
            self.FrameDrHa.reponseNomEntry.config(state=tk.NORMAL)
            self.FrameDrHa.repPrenomEntry.focus_set()
            
    def DonnerNomPrenom(self) -> None:
        """Donner le nom/prénom si la photo est absente"""
        # valeur du dernier rang dans les fichiers de configuration csv
        dernier_rang=len(self.FrameG.listeEleves[self.FrameG.rang])-1 # rang: rang de l'élève dans la classe
        # activer/désactiver zone de saisie
        if self.FrameDrBa.selectPrenNom.get()=="2": # prénom seul
            # donner le prénom si il n'y a pa de photo
            if self.FrameG.listeEleves[self.FrameG.rang][dernier_rang]=="pas_de_photo":
                self.FrameDrHa.repPrenom.set(self.FrameG.listeEleves[self.FrameG.rang+1][1])
        elif self.FrameDrBa.selectPrenNom.get()=="3": # nom seul
            # donner le nom si il n'y a pa de photo
            if self.FrameG.listeEleves[self.FrameG.rang][dernier_rang]=="pas_de_photo":
                self.FrameDrHa.repNom.set(self.FrameG.listeEleves[self.FrameG.rang+1][0])
        else: # nom et prénom
            # donner le prénom si il n'y a pa de photo
            if self.FrameG.listeEleves[self.FrameG.rang][dernier_rang]=="pas_de_photo":
                self.FrameDrHa.repPrenom.set(self.FrameG.listeEleves[self.FrameG.rang+1][1])
                self.FrameDrHa.repNom.set(self.FrameG.listeEleves[self.FrameG.rang+1][0])
                
    def configAutresModes(self) -> None:
        """configurations modes Apprentissage - Test Mental - Test écrit"""
        # try:
        # liste des élèves
        #self.FrameDrBa.listeEleves=copy.deepcopy(self.FrameDrBa.choisir_classe()) # appel de la méthode choisirClasse
        self.FrameG.listeEleves=copy.deepcopy(self.FrameDrBa.listeEleves) # copie profonde de la liste        
        if self.FrameDrBa.optionSelectionnee!="TOUS":
            self.enleverEleves()
        self.FrameG.nbreElev=len(self.FrameG.listeEleves) # nbre élèves
        self.FrameG.rang=0  
        # N° de l'élève en cours (frame gauche)
        self.FrameG.numOrdreElev.set(str(self.FrameG.rang//2+1)+"/"+str(self.FrameG.nbreElev))
        #désactiver l'affichage des bonnes réponses
        self.FrameDrHa.DesAffichRep()
        # changer l'ordre des élèves
        if (self.FrameDrBa.ordreAleatoire=="oui"):
            random.shuffle(self.FrameG.listeEleves) 
        # effacer noms dans la liste  
        if (self.FrameDrBa.selectPrenNom.get()=="2"): # Prénom seul
            self.effacerNomsOuPrenoms(self.FrameG.listeEleves,1)
        # effacer prénoms dans la liste   
        if (self.FrameDrBa.selectPrenNom.get()=="3"): # nom seul
            self.effacerNomsOuPrenoms(self.FrameG.listeEleves,0)
            # ajouter les ???
        if (self.FrameDrBa.SelectModes.get()>"1"): 
            self.ajouterBlancsListes(self.FrameG.listeEleves)  
        # configuration des boutons champs, etc
        if (self.FrameDrBa.SelectModes.get()=="3"): # Test écrit
            self.FrameDrHa.configTestEcrit()
            self.configTestEcrit()
        else: # apprentissage et test oral
            self.configApprentissageTestOral()
        self.FrameG.majNomPrenom()
        self.FrameG.majClasseOptions()
        self.FrameG.majPhoto()
        # except IOError:
        #     tkinter.messagebox.showwarning("Attention","Sélectionner une classe")
        # except OSError:
        #     tkinter.messagebox.showwarning("Attention","Sélectionner une classe")
        # except AttributeError:
        #     tkinter.messagebox.showwarning("Attention","Sélectionner une classe")

    def configTestEcrit(self) -> None:
        """Configurer le mode Test Écrit"""
        # Désactiver les boutons (Frame gauche)
        for bouton in self.FrameG.boutons:
            bouton.configure(state="disabled")
        
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
                self.FrameG.boutons[i].configure(state="active") 
        else:
            for i in range(len(icones)):
                self.FrameG.boutons[i].configure(state="disabled") 
        
    def effacer(self,event) -> None:
        """Effacer après appui sur le bouton "effacer" de la frame haute droite"""
        expression=self.FrameG.rang % 2 == 0 and self.FrameDrBa.SelectModes.get()=="3" # rang paire et test écrit
        if (expression or self.FrameDrBa.SelectModes.get()=="4" ): #  mode "Rechercher"
            self.FrameDrHa.effacerReponses()
            self.actDesZonesSaisies()
    def enleverEleves(self) -> None:
        """enlever les élèves ne faisant pas l'option sélectionnée"""
        # i=0
        # while i< len(self.FrameG.listeEleves):
        #     if self.FrameDrBa.optionSelectionnee in self.FrameG.listeEleves[i]:    
        #         i=i+1
        #     else:
        #         self.FrameG.listeEleves.remove( self.FrameG.listeEleves[i])
        """Enlever les élèves ne faisant pas l'option sélectionnée"""
        self.FrameG.listeEleves = [
            eleve for eleve in self.FrameG.listeEleves
            if self.FrameDrBa.optionSelectionnee in eleve[2]
        ]
    
    def effacerNomsOuPrenoms(self,liste:list,rang: int) -> None:
        """effacer les noms ou les prénoms"""
        for i in range(len(liste)):
                liste[i][rang]=" "
                   
    def ajouterBlancsListes(self,liste:list) -> None:
        """ajouter des blancs ou des ??? dans la liste"""
        i=0        
        while i<(len(liste)):
            tab=list(liste[i])# copie de liste[i]
            if (self.FrameDrBa.selectPrenNom.get()=="1"): #nom et prénom
                tab[0]="???"
                tab[1]="???"
            elif (self.FrameDrBa.selectPrenNom.get()=="2"): # prénom seul
                tab[0]=" "
                tab[1]="???"
            else:               # nom seul
                tab[0]="???"
                tab[1]=" "
            liste.insert(i,tab)
            i=i+2
            
    def verifierRechercher(self,event) -> None:
        """lancer la vérification de la réponse"""
        if self.FrameDrBa.SelectModes.get()=="3": # mode "Test écrit"
            self.verifier()
        elif self.FrameDrBa.SelectModes.get()=="4": # mode "Rechercher"
            self.rechercher()
        
    def verifier(self) -> None:
        """Vérifier la réponse dans le mode Test Écrit"""

        if self.FrameG.rang % 2 != 0:
            return  # ne rien faire si ce n’est pas un rang pair

        # Récupération des réponses utilisateur
        nom = self.FrameDrHa.reponseNomEntry.get().strip()
        prenom = self.FrameDrHa.repPrenomEntry.get().strip()

        # Réponses attendues
        nomAttendu = self.FrameG.listeEleves[self.FrameG.rang + 1][1].strip()
        prenomAttendu = self.FrameG.listeEleves[self.FrameG.rang + 1][0].strip()

        mode = self.FrameDrBa.selectPrenNom.get()
        match = True

        if mode in ["1", "3"]:  # le nom doit être vérifié
            match &= nom.lower() == nomAttendu.lower()
        if mode in ["1", "2"]:  # le prénom doit être vérifié
            match &= prenom.lower() == prenomAttendu.lower()

        # Affichage des résultats
        icone = "check.png" if match else "cross.png"
        image = Image.open(os.path.join(repertoire_racine, "fichiers", "icones", icone))
        self.photo = ImageTk.PhotoImage(image)
        self.FrameDrHa.canvas.itemconfig(self.FrameDrHa.photoSurCanvas, image=self.photo)

        if match:
            self.FrameDrHa.nbreRepExactes += 1

        # Mise à jour du score I / J
        score = f"{self.FrameDrHa.nbreRepExactes}/{self.FrameG.rang // 2 + 1}"
        self.FrameDrHa.nbreRep.set(score)

        # Avancer dans la liste
        self.FrameG.rang += 1
        if self.FrameG.rang > len(self.FrameG.listeEleves) - 2:
            self.FrameDrHa.desFrameDrHa()
        else:
            self.FrameG.majNomPrenom()
            self.FrameG.majClasseOptions()
            self.FrameDrHa.boutVal.config(state=tk.DISABLED)
            self.FrameDrHa.boutEff.config(state=tk.DISABLED)
            self.FrameDrHa.reponseNomEntry.config(state=tk.DISABLED)
            self.FrameDrHa.repPrenomEntry.config(state=tk.DISABLED)


    def AllerALaSuite(self,event) -> None:
        """voir la réponse et passer à l'élève suivant"""
        if (self.FrameDrBa.SelectModes.get()=="3"): #Test écrit
            self.FrameDrHa.effacerReponses()
            if (self.FrameG.rang >= len(self.FrameG.listeEleves)-1):
                pass
            else:
                self.FrameG.rang=self.FrameG.rang+1
            # avancer
            if (self.FrameG.rang<len(self.FrameG.listeEleves)):
                #réactivation des boutons
                self.FrameDrHa.boutVal.config(state=tk.NORMAL)
                self.FrameDrHa.boutEff.config(state=tk.NORMAL)
                # maj bonnes réponses
                self.FrameDrHa.nbreRep.set(str(self.FrameDrHa.nbreRepExactes)+"/"+str(self.FrameG.rang//2+1))
                # N° de l'élève en cours
                self.FrameG.numOrdreElev.set(str(self.FrameG.rang//2+1)+"/"+str(self.FrameG.nbreElev))
                # maj des noms te des prénoms
                self.FrameG.majNomPrenom()
                self.FrameG.majClasseOptions()
                # activation/désactivation des zones de saisie
                if (self.FrameG.listeEleves[self.FrameG.rang][1]=="???") or (self.FrameG.listeEleves[self.FrameG.rang][0]=="???"):
                    self.actDesZonesSaisies() #activer/désactiver zones de saisie
                else:
                    self.FrameDrHa.repPrenomEntry.config(state=tk.DISABLED)
                    self.FrameDrHa.reponseNomEntry.config(state=tk.DISABLED)
                    self.FrameDrHa.boutVal.config(state=tk.DISABLED)
                    self.FrameDrHa.boutEff.config(state=tk.DISABLED)
                # maj des photos
                self.FrameG.majPhoto()
                if (self.FrameG.rang==len(self.FrameG.listeEleves)-1):
                    self.FrameDrHa.desFrameDrHa()
        else:
            pass
    
    def rechercher(self):
        """Rechercher un élève dans tout l'établissement selon le nom, prénom ou les deux (avec print de débogage)"""

        self.FrameG.listeEleves = []
        self.FrameG.rang = 0
        resultat = "pas trouvé"

        # Lecture et nettoyage
        nom = self.FrameDrHa.reponseNomEntry.get().strip().lower()
        prenom = self.FrameDrHa.repPrenomEntry.get().strip().lower()
        mode = self.FrameDrBa.selectPrenNom.get()


        for classe, liste_eleves in self.FrameDrBa.modifier_bdd.ElevesParClasses.items():
            for eleve in liste_eleves:
                prenomEleve = eleve[0].strip().lower()
                nomEleve = eleve[1].strip().lower()

                if mode == "2":  # prénom seul
                    condition = (prenom == prenomEleve)
                elif mode == "3":  # nom seul
                    condition = (nom == nomEleve)
                else:  # nom + prénom
                    condition = (prenom == prenomEleve and nom == nomEleve)

                if condition:
                    self.FrameG.listeEleves.append(eleve)
                    self.FrameG.nbreElev = len(self.FrameG.listeEleves)
                    self.FrameG.rang = 0
                    self.FrameG.numOrdreElev.set(f"1/{self.FrameG.nbreElev}")
                    self.FrameG.majNomPrenom()
                    self.FrameG.majClasseOptions()
                    self.FrameG.majPhoto()
                    resultat = "trouvé"

    def validerRepNom(self, event):
        """Valider l'entrée prénom selon le mode sélectionné, ou passer au champ nom"""

        mode_recherche = self.FrameDrBa.selectPrenNom.get()
        mode_general = self.FrameDrBa.SelectModes.get()

        if mode_recherche == "2":  # Prénom seul
            if mode_general == "3":  # Test écrit
                self.verifier()
            else:
                # Activer les boutons dans FrameG
                for bouton in self.FrameG.boutons:
                    bouton.configure(state="normal")
                self.rechercher()
        else:
            # Passer au champ Nom
            self.FrameDrHa.reponseNomEntry.focus_set()

                        
    def information(self,event) -> None:
        """ Informer sur le programme """
        self.fenPropos = tk.Toplevel()
        #bloque la fenêtre parente pour éviter de créer une deuxième fenêtre information        
        while 1:
            try:
                self.fenPropos.grab_set()
                break
            except tk.TclError:
                self.fenPropos.after(100) 
        self.fenPropos.title("À propos de: ")
        self.fenPropos.transient(self.fenPropos.master) # fenetre provisoire 
                            # qui ne sera pas afficher dans la barre de tâche
        frame1 = tk.Frame(self.fenPropos, padx=5, pady=1)
        frame1.pack()
        partie1=" Mémo_Lycée * v0.52 \n\n Copyrigth (c) - G LE REST - "
        partie2="\n <gerard.lerest@orange.fr>"
        partie3="\n 2016 - 2025 \n\n"
        partie4=" Cliquer sur l'image pour plus d'infos"
        message=partie1+partie2+partie3+partie4
        tk.Message(frame1, width=275, aspect=50, justify="center", pady=2,
        text = message).pack()
        # image gplv3.png
        image = Image.open(repertoire_racine+os.sep+"fichiers"+os.sep+"icones"+os.sep+"gplv3.png")  
        self.photo = ImageTk.PhotoImage(image)  
        boutGPLv3=tk.Button(frame1, image=self.photo, command=self.pageWebGPLv3)
        boutGPLv3.pack(pady=2)  
        # bouton
        boutonInfo = tk.Button(frame1, text="Quitter", 
                                    command=self.fenPropos.destroy)
        boutonInfo.pack(pady=2)
        #blocage du dimensionnement de la fenêtre
        self.fenPropos.resizable(width=False, height=False)
    
    def pageWebGPLv3(self):
        """ accéder à la page web de la licence GPLv3 """
        webbrowser.open('https://www.gnu.org/licenses/gpl-3.0.fr.html')
        
# ----------------------------------------------------
        
if __name__ == '__main__':
    App=Application()
    App.resizable(width=False,height=False)
    App.title('VisuMemo')
    App.mainloop()
