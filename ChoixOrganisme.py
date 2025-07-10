from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QRadioButton,
    QPushButton, QSpacerItem, QSizePolicy, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
import sys
import json
from MemoVue import Fenetre  # Importer la classe MemoVue

class ChoixOrganisme(QWidget):
    """Choisir l'organisme - Parlement - École - Entreprise"""

    def __init__(self):
        super().__init__()
        self.interface()

    def interface(self) -> None:
        """création de l'interface"""
        self.setWindowTitle("MemoVue")
        self.setStyleSheet("background-color: white;")  # fond blanc propre
        layout = QVBoxLayout() # layout général
        layout.setContentsMargins(20, 20, 20, 20)  # marges internes propres

        # Titre centré
        label = QLabel("Mode de fonctionnement")
        label.setStyleSheet("""
            color: #2F4F4F;
            font-weight: bold;
            font-size: 20px;
        """)
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        layout.addSpacing(10)

        # Boutons radios
        self.radioEcole = QRadioButton("Ecole")
        self.radioEntreprise = QRadioButton("Entreprise")
        self.radioParlement = QRadioButton("Parlement")

        for radio in [self.radioEcole, self.radioEntreprise, self.radioParlement]:
            radio.setStyleSheet("font-size: 18px; margin: 2px 0;")
            layout.addWidget(radio)

        layout.addSpacing(15)

        # Bouton OK centré et stylisé
        bouton = QPushButton("OK")
        bouton.setFixedWidth(80)
        bouton.setStyleSheet("""
            QPushButton {
                background-color: #4682B4;
                color: white;
                border-radius: 8px;
                padding: 5px 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5A9BD5;
            }
        """)
        layout.addWidget(bouton, alignment=Qt.AlignCenter)
        bouton.clicked.connect(self.lancerMemoVue)

        layout.addSpacing(15)

        # Logo centré
        labelLogo = QLabel()
        pixmap = QPixmap("fichiers/logos/logoMemoVue.png")
        if not pixmap.isNull():
            pixmap = pixmap.scaledToWidth(100, Qt.SmoothTransformation)
            labelLogo.setPixmap(pixmap)
        labelLogo.setAlignment(Qt.AlignCenter)
        layout.addWidget(labelLogo)

        self.setLayout(layout)

    def lancerMemoVue(self):
        "lancement de la classe MemoVue"
        if self.radioEcole.isChecked():
            fichier = "ConfigEcole.json"
        elif self.radioEntreprise.isChecked():
            fichier = "ConfigEntreprise.json"
        elif self.radioParlement.isChecked():
            fichier = "ConfigParlement.json"
        else:
            fichier = None
        try:
            with open(fichier, "r", encoding="utf-8") as f:
                config = json.load(f)
        except Exception as e:
            print(f"Erreur lors du chargement du fichier : {e}")
            return

        self.memoVue = Fenetre(config=config)
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    fenetre = ChoixOrganisme()
    fenetre.show()
    app.exec()