python -m PyInstaller --onefile --windowed ^
--add-data "fichiers;fichiers" ^
--add-data "deputes.db;deputes.db" ^
--add-data "salaries.db;salaries.db" ^
--add-data "eleves.db;eleves.db" ^
--add-data "ConfigEcole.json;ConfigEcole.json" ^
--add-data "ConfigEntreprise.json;ConfigEntreprise.json" ^
--add-data "ConfigParlement.json;ConfigParlement.json" ^
ChoixOrganisme.py