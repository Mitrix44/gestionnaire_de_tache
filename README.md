# Getionnaire de tâche desktop (python)

## Description

Ce repository contient un projet d'évaluation en *développement natif*.
Ce projet est un **gestionnaire de tâche** (**todolist**).
Le projet a été réalisé en Python avec une integration graphique avec PySide6 et PySide6-designer.

## Pré-requis

- Avoir python 3 installé sur sa machine.
- Avoir git installé sur sa machine.

## Lancer le projet

Ouvrez le terminal et rendez-vous a l'endroit où vous souhaitez cloner le projet.
Executer les commandes suivante

### Je suis sur Windows

```
git clone https://github.com/Mitrix44/gestionnaire_de_tache.git
cd './gestionnaire_de_tache'
python -m venv env
.\env\Scripts\Activate.ps1
pip install PySide6
python main.py
```

### Je suis sur Mac ou Linux

```
git clone https://github.com/Mitrix44/gestionnaire_de_tache.git
cd './gestionnaire_de_tache'
python3 -m venv env
source env/bin/activate
pip install PySide6
python main.py
```

## Explications

### 1. Architecture MVC: Role, justification et structure

La structure du projet est la structure MVC:

- Main.py => Point d'entrée de l'application.
- /Controller/__init__.py => permet d'importer les controllers dans le main.py *via 'from controller import TaskController'*
- /controller/task_controller.py => permet de gérer toute la logique métier liés a des taches et leurs commentaires (CRUD)
- /data/*.json => permet de stocker toutes les données en local sur la machine (C'est la partie Model du MVC); stock la data.
- /views/inteface.ui => *Partie View du MVC* -> C'est le fichiers d'interface généré par PySide6-designer
- /views/interface.py =>  *Partie View du MVC* -> C'est les fichier d'interface généré par PySide6-designer, mais converti en python.

Cette structure permet une meilleur maintenabilité, et a n'importe quel développeur qui possède les concepts d'architecture MVC de comprendre rapidement l'architeture de l'app.

### 2. Choix techniques

J'ai choisi de stocker les données de manière locale en json pour des raisons de praticité.
Chaque tâche est stockée de manière individuelle dans son propre fichier json.

Il n'y a pas de relation entre tache et commentaire:
Les commentaire sont stockés sous forme de tableau directement dans la tâche.

Pour clôturer une tâche, il suffit de lui appliquer le staut "Terminé".

### 3. Validation/Gesiton des erreurs.

A chauque fois que l'utilisateur effectue une action qui n'est pas possible ou qui pourrait engendrer des bugs (ex: suppression/modification de tâche si aucune tâche n'est sélectionnée), un message d'avertissement apparait pour notifier l'utilisateur de ce qui n'a pas marché.

### 4. Interface utilisateur

L'interface à été généré avec PySide6-designer. J'ai néamoins dû appliquer des propriétés de style directement dans le main.py, car ces propriétés n'étaient pas disponibles dans PySide6-designer:
exemple: *vertical_layout_1.setAlignment(Qt.AlignTop)* -> Cette propriété n'est pas disponible dans le designer pour un *Layout*

### 5. Difficultés rencontrées et solutions

Au départ, dans mais layout qui n'étaient pas des *scroll-views* quand il y avait trop de tâches ou trop de commentaires, la taille de chaque élément retrécissait au fûr et à mesur qu'on ajoutait des éléments à l'intérieur.

Pour corriger ce probleme j'ai mis une *scroll-view* avec un layout à l'intérieur qui possède la propriété *max-height* à la valeur maximale. Nativement le layout prend la hauteur en fonction des éléments enfants. Ils s'affichaient par défaut au millieu de la *scroll-view*, c'est pourquoi j'ai appliqué une propriété directement dans le main.py car pas disponible dans PySide6-designer (pour les aligner en haut par défaut).