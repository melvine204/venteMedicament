# VenteMedicament

## Description du Projet

Application web django pour la gestion et la vente des medicaments en ligne. Notre application utilise le SGBD **SQLite**

## Prérequis

- Python 3.9+
- Django 5.2+
- pip

## Installation

### 1. Cloner le Répertoire

```bash
git clone https://github.com/melvine204/venteMedicament.git
cd venteMedicament
```

### 2. Créer un Environnement Virtuel

```bash
python -m venv venv
source venv/bin/activate  # Sur Unix/macOS
# ou 
venv\Scripts\activate  # Sur Windows
```

### 3. Installer les Dépendances

```bash
pip install -r requirements.txt
```

### 4. Configuration de la Base de Données

```bash
cd src
python manage.py makemigrations
python manage.py migrate
```

### 5. Importer les categories dans la bd

```bash
python manage.py loaddata categories.json
```

### 6. Créer un Utilisateur Administrateur

```bash
python manage.py createsuperuser
```

## Lancement du Serveur de Développement

```bash
python manage.py runserver
```

L'application sera accessible à l'adresse : `http://127.0.0.1:8000/`

## Structure du Projet

```
venteMedicament/
│
├── src/
│   ├── App/
│   │   ├── fixtures/
│   │   ├── └── categories.json
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   │   
│   ├── pharmacie/
│   │   ├── asgi.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   │   
│   ├── static/
│   │   
│   ├── templates/
│   │   ├── admin/
│   │   └── pharmacy/
│   │   
│   ├── db.sqlite3
│   └── manage.py
│
├── .gitignore
├── desktop.ini
├── README.md
└── requirements.txt
```

## Déploiement

Instructions spécifiques pour le déploiement (Heroku, AWS, etc.)

## Contribution

1. Forker le projet
2. Créer une branche pour votre fonctionnalité (`git checkout -b feature/AmazingFeature`)
3. Commit vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Push sur la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## Licence

Spécifiez la licence (MIT, Apache, etc.)

## Contact

- melvine204
- email@gmail.com
- Lien du Projet : https://github.com/melvine204/venteMedicament
