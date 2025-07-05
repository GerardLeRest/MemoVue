# 📚 MémoLycée

MémoLycée est une application éducative développée en Python avec une interface graphique Tkinter.  
Elle permet d’apprendre ou de retrouver les noms et prénoms de prsonnes à partir  d'une base de données SQLite.

## 📌 Fonction du projet

L’application propose plusieurs modes d’utilisation :

- **Apprentissage** : affichage des élèves et de leurs informations.
- **Test écrit** : l’utilisateur doit saisir les noms ou prénoms.
- **Test oral** : affichage d’une photo, l’utilisateur répond mentalement.
- **Recherche** : permet de retrouver un élève à partir d’un nom ou prénom.

MémoLycée permet aussi de filtrer les élèves par classe et par option, et d’intégrer des appréciations trimestrielles.

## 🛠️ Installation

1. **Cloner le dépôt** :
   
   ```bash
   git clone https://github.com/ton_pseudo/memolycee.git
   cd memolycee
   ```

2. **Créer un environnement virtuel** :
   
   ```bash
   python3 -m venv mon_env
   source mon_env/bin/activate  # sous Windows : venv\Scripts\activate
   ```

## 📦 Dépendances

Le programme nécessite les bibliothèques suivantes :

- `sqlite3` (intégré à Python pour la gestion de la base de données - ne pas installer)
- 'PySide6' (bibliothèque graphique)

Pour installer PySide6:
```bash
pip install pyside6
```

## 📂 Données utilisées

Le programme utilise :

- Une base de données SQLite (`personnes.de`)
- Des images des élèves (dans un dossier `photos/`)
- Des fichiers CSV pour l'importation initiale

## ▶️ Lancement

Lance le programme principal :

```bash
python memo_lycee.pyw
```

## 💡 Remarques

- Compatible Python 3.8+
- Testé sous Ubuntu
- L’application est en cours d’amélioration (v0.51)

## Licence _ photos

Ce projet est distribué sous licence GPL-v3.  
© 2025 Gérard LE REST

Les portraits utilisés dans ce projet proviennent de **Generated Photos**  
→ https://generated.photos  

Images générées par intelligence artificielle, utilisées dans un cadre pédagogique non commercial.  
Mention requise :  
**“Image by Generated Photos (https://generated.photos), used with permission.”**
