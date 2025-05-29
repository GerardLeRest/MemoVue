#!/usr/bin/python2
# -*- coding: utf-8 -*

#####################################################
# selection du mode de fonctionnement
# (apprentissage, test mental, test ecrit, Rechercher)
# choix de la classe et de l'option
#####################################################

import tkinter as tk
from tkinter import ttk
import copy, sqlite3, os  # fichier Excel de l'établissement
from modifier_bdd import ModifierBDD

class FrameDroiteBasse (tk.Frame):
    """ Créer la partie droite basse de l'interface """
    def __init__(self, fenetre: tk.Widget):
        """Constructeur de la frame de droite et de ses éléments"""
        # constructeur de la classe parente
        tk.Frame.__init__(self, fenetre, relief=tk.GROOVE, bd=3)
        self.grid(row=1, column=1, padx=10)
        self.listeEleves = []  # liste des élèves de la classe sélectionnée
        self.listeOptions = []  # liste des options des élèves de la classeself/
        #self.modifier_bdd = ModifierBDD("fichiers/eleves.bdd") -faux?
        self.modifier_bdd = ModifierBDD("fichiers/eleves.db")
        self.optionSelectionnee = "TOUS"  # optionsélectionnée
        # boutons radiCreerBDDos des modes
        frameRadio = tk.Frame(self)
        frameRadio.grid(row=1, columnspan=2, sticky="w")
        modes = [("Apprentissage", "1"), ("Test mental", "2"),
                 ("Test écrit", "3"), ("Rechercher", "4")]
        self.SelectModes = tk.StringVar()
        self.SelectModes.set("1")  # initialisation
        for text, mode in modes:
            b = tk.Radiobutton(frameRadio, text=text,
                               variable=self.SelectModes, value=mode,
                               command=self.configRechercher)
            b.pack(side="left", pady=3)
        # création de la liste des classes
        self.classes_etablissement = self.liste_des_classes()
        self.classes_etablissement.sort()
        labelCombog = ttk.Label(self, text="Classe/Catégorie")
        labelCombog.grid(column=0, row=2)
        self.combog = ttk.Combobox(self, values=self.classes_etablissement)
        self.combog.grid(row=3, column=0, sticky="w", pady=3, padx=5)
        self.combog.bind("<<ComboboxSelected>>", self.choisir_classe_options)
        # checkbutton Aléatoite
        self.ordreAleatoire = "non"
        self.aleatoire = tk.StringVar()
        methode = self.definirOrdreDefilement
        self.checkbutAleatoire = tk.Checkbutton(self, text=" Aléatoire",
                                                variable=self.aleatoire,
                                                onvalue="oui",
                                                offvalue="non",
                                                command=methode)
        self.checkbutAleatoire.grid(row=4, sticky="w")
        self.checkbutAleatoire.deselect()
        # boutons radios avec/sans nom prénoms
        frameRadio2 = tk.Frame(self)
        frameRadio2.grid(row=5, columnspan=2, sticky="w")
        choix = [("Prénom+Nom", "1"), ("Prénom", "2"), ("Nom", "3")]
        self.selectPrenNom = tk.StringVar()
        self.selectPrenNom.set("1")  # initialisation
        for texte, numero in choix:
            b = tk.Radiobutton(frameRadio2, text=texte,
                               variable=self.selectPrenNom,
                               value=numero,
                               command=self.configRechercher)
            b.pack(side="left")
        # bouton de validation 1
        self.boutVal = tk.Button(self, text="Valider")
        self.boutVal.grid(row=6, columnspan=2, pady=5)
        # créer la liste des options
        self.creerComboOptions()
        

    def liste_des_classes(self) -> list:
        """Renvoie la liste des classes de l'établissement"""
        classes = self.modifier_bdd.lister_classes()
        print("Vérification des classes :", classes)
        return classes


    def configRechercher(self) -> None:
        """activer/désactiver les listes les comboBox, des radiobuttons
           et des labels"""
        if (self.SelectModes.get() == "4"):
            # désactiver les radiobuttons
            self.checkbutAleatoire.configure(state="disabled")
            # désactiver les listes des comboBox
            self.combog.configure(state="disabled")
            self.combod.configure(state="disabled")
        else:
            # activer les listes des comboBox
            self.combog.configure(state="normal")
            self.combod.configure(state="normal")
            # activer les radiobuttons
            self.checkbutAleatoire.configure(state="normal")

    def definirOrdreDefilement(self) -> None :
        """Définir l'ordre de défilement"""
        self.ordreAleatoire = self.aleatoire.get()

    def choisir_classe_options(self, event) -> None :
        """Choisir la classe et mettre à jour les élèves et les options"""
        classeSelectionnee = self.combog.get()
        print("Classe sélectionnée (par combobox) :",classeSelectionnee)
        
        # Récupère la liste des élèves de la classe
        #ancienne version
        # self.listeEleves =  self.modifier_bdd.eleves_classe(classeSelectionnee) # voir init pour l'instanciation
        # nouvelle vesion (2lignes)
        self.modifier_bdd.eleves_classe(classeSelectionnee)  # exécute la méthode (pas de retour)
        print("Élèves récupérés :", self.modifier_bdd.listeEleves)
        self.listeEleves = self.modifier_bdd.listeEleves
        print(f"premier tableau: {self.listeEleves}")
        # deux lignes dde test
        for eleve in self.listeEleves:
            print(f"{eleve[1]} {eleve[0]} - photo : {eleve[3]}")
        # Récupère uniquement les options réellement présentes dans cette classe
        self.listeOptions = self.creerOptions()
        print("liste des options:")
        print(self.listeOptions)
        # Met à jour la combobox des options
        self.creerComboOptions()

    def creerOptions(self) -> list:
        """Créer la liste des options présentes uniquement dans la classe sélectionnée"""
        liste_options = []
        for eleve in self.listeEleves:
            options = eleve[2]  # une liste d'options (ex: ['ALL2', 'CAM'])
            for option in options:
                if option not in liste_options:
                    liste_options.append(option)
        liste_options = sorted(liste_options)
        liste_options.insert(0, "TOUS")
        self.listeOptions = liste_options  # mise à jour de l’attribut utilisé par la combobox
        self.creerComboOptions()
        return liste_options


    def creerComboOptions(self) -> None:
        """créer la liste des options"""
        labelCombod = ttk.Label(self, text="Option/Spécialité")
        labelCombod.grid(column=1, row=2)
        self.combod = ttk.Combobox(self,
                                   values=self.listeOptions)
        self.combod.grid(row=3, column=1, sticky="W", pady=3, padx=5)
        self.combod.bind("<<ComboboxSelected>>",
                         self.choisirOption)
        self.configRechercher()

    def choisirOption(self, event) -> None:
        """Sélectionner l'option des élèves"""
        self.optionSelectionnee = self.combod.get()
        print("Option sélectionnée: ", self.optionSelectionnee)

# ----------------------------------------------------

if __name__ == '__main__':
    fenetre = tk.Tk()
    Application = FrameDroiteBasse(fenetre)
    fenetre.mainloop()
    # fin du programme