# MémoVue

MémoLycée est une application éducative développée en Python avec une interface graphique Pyside6.  
Elle permet d’apprendre ou de retrouver les noms et prénoms de pesonnes à partir d'une base de données SQLite3.

## Fonction du projet

L'interface comporte trois zones. La zone gauche donne des informations sur la personne. La zone en haut à droite permet de répondre aux questions. Et la zone en bas à droite permet d'effectuer les réglages (n'oublier pas le bouton Valider!) 

L’application propose plusieurs modes d’utilisation :

- **Apprentissage** : affichage des personnes et de leurs informations.
- **Test écrit** : l’utilisateur doit saisir les noms ou prénoms.
- **Test oral** : Affichage d’une photo L’utilisateur pour chercher mentalement avant de voir la correction.
- **Recherche** : permet de retrouver un élève à partir d’un nom ou prénom.

On peut rechercher seulement les prénoms, ou seulement les noms ou les noms+prénoms

MémoLycée permet aussi de filtrer les personnes par structures et spécialités.

## Installation

1. **Cloner le dépôt** :
   
   ```bash
   git clone https://github.com/GerardLeRest/MemoVue
   cd memolycee
   ```

2. **Créer un environnement virtuel** :
   Venv doit être installé. mon_env est le nom de l'environnement python
  - Sous Ubuntu 
   ```bash
   python3 -m venv mon_env 
   source mon_env/bin/activate  
   ```
   - Sous windows:
   => CTRL + Shift + P
   => Python: Select Interpreter
   =>Create Virtual Environnement

## Dépendances

Le programme nécessite des bibliothèques suivantes :

- `sqlite3` (intégré à Python3 pour la gestion de la base de données - ne pas installer)
- 'PySide6' (bibliothèque graphique à installer)

Pour installer PySide6:

```bash
pip install pyside6
```

## Données utilisées

Le programme utilise :

- Une base de données SQLite (`eleves.db`, 'deputes.db' ou salaries.db - à la racine du projet)
- Des images des personnes (dans un dossier `fichiers/photos/`)
- Des fichiers CSV pour l'importation initiale (dossier fichiers/deputes par exemple)
Il y a bien donc trois organismes indépendants les uns des autres.

## Lancement

Lance le programme principal :

```bash
python ChoixOrganisme.pyw
```

## Remarques

- Compatible Python 3.8+
- Testé sous Ubuntu
- L’application est en cours d’amélioration (v0.51)

## Site web

https://gerardlerest.github.io/memovue/

## Licence _ photos

Ce projet est distribué sous licence GPL-v3.  
© 2025 Gérard LE REST

Les portraits utilisés dans ce projet proviennent de **Generated Photos**  
→ https://generated.photos  

Images générées par intelligence artificielle, utilisées dans un cadre pédagogique non commercial.  
Mention requise :  
**“Image by Generated Photos (https://generated.photos), used with permission.”**
