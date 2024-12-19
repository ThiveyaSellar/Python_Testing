# GÜDLFT Application de réservation pour les compétitions de force

Application de réservation de compétions de force pour les clubs régionaux réalisée avec le micro-framework flask.

## Installation

Cloner le dépôt : ```git clone https://github.com/ThiveyaSellar/Python_Testing.git```

Créer un environnement virtuel python : ```python -m venv env```

 Activer l'environnement virtuel :
- Windows :
```venv\Scripts\activate```
- Linux :
```source venv/bin/activate```

Installer les paquets du fichier requirements.txt : ```pip install -r requirements.txt```

Indiquer à Flask quelle application exécuter
```set FLASK_APP=server.py```

Démarrer le serveur 
```flask run```

## Tests

A la racine du projet : ``pytest``

Pour un test en particulier : ``pytest <fichier de test>``

Avec les prints : ``pytest -s <fichier_de_test>``

- Pour les tests fonctionnels et de performance, il faut s'assurer d'avoir un pilote chromedriver qui soit compatible avec la version du navigateur et lancer le serveur flask dans un terminal puis lancer les tests dans un autre terminal

Tester la couverture :

Se placer à la racine du projet :  ```pytest --cov=répertoire_du_code_source```

Générer un rapport html de la couverture : ```pytest --cov=. --cov-report html```
```