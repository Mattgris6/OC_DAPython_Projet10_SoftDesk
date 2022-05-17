## SoftDesk

## Installation
* Python 3 doit-etre installé.
* Télécharger le package de l'application sous github, le dézipper et le ranger dans un nouveau répertoire.
* Sous windows ouvrir un terminal avec la commande cmd depuis ce répertoire.
* Créer un environnement virtuel `python -m venv env`
* Activer l'environnement virtuel `"./env/Scripts/activate.bat"`
* Installer les bibliothèques externes de Python `pip install -r requirements.txt`

_**L'application est développée avec DjangoRest. Le projet Django softdesk a une application:**_
1. itsystem

_**Les données sont sauvées dans la base de données db.sqlite3**_

## Utilisation
* Activer l'environnement virtuel `"./env/Scripts/activate.bat"`
* Aller dans le dossier softdesk `cd softdesk`
* Lancer le serveur avec la commande `python manage.py runserver`
* Dans votre navigateur, accéder à l'application à l'adresse `http:/127.0.0.1:8000`
* Créer un compte ou se connecter pour pouvoir accéder au site.
* Pour accéder à l'administratin de django `http://127.0.0.1:8000/admin`

### Utilisateurs demo
* Voici la liste de tous les utilisateurs de démo:
    * admin
* dev1
* dev2
* dev3
* * dev4
* * dev5
* Tous les utilisateurs ont le même mot de passe: password-oc
* Seul l'utilisateur admin a accès à l'administration django

