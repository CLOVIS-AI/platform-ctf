# Guide de développeur

Ce document contient des informations sur le déploiement de la plateforme et l'environnement de développement.

## Configuration

La plateforme est configurée par le fichier `web/secret.properties`.
Un fichier d'exemple contenant des valeurs par défaut [est disponible ici](../web/secret.example.properties).

Avant de pouvoir lancer la plateforme, il faut donc copier le fichier d'exemple et modifier les valeurs au besoin.
```shell
$ cp web/secret.example.properties web/secret.properties
```
Le fichier `web/secret.properties` ne doit jamais être inclus dans le dépôt.

Toutes les variables sont documentées dans le fichier.

## Organisation du projet

- `challenges`: tous les challenges, scénarios, documentation en ligne
- `web-ui`: frontend de la plateforme (JS, images, CSS…)
- `web`: backend de la plateforme (templates jinja, Python…)

La plateforme est un conteneur Docker exécuté dans une VM sur un ESXi. La plateforme interagit avec un serveur vSphere sur ce même ESXi pour lancer d'autres VMs ou conteneurs.

Un `Makefile` est présent à la racine du projet pour exécuter les différentes actions nécessaires.

```shell
# Lancer la plateforme
$ make start

# Arrêter la plateforme
$ make stop
```

## Configuration pour IntelliJ

Ce projet contient à la fois du Python et du JavaScript.
PyCharm ne permet pas actuellement de créer des projets contenant plusieurs modules.
Nous recommandons donc d'utiliser IntelliJ Ultimate.

Après avoir ouvert le projet dans IntelliJ, il faut exécuter la commande suivante :
```shell
$ make web-ui/node_modules web/venv/install
```
Cela va créer l'environnement virtuel Python, y télécharger les dépendances, ainsi que télécharger les dépendances JavaScript.
De cette manière, IntelliJ va pouvoir indexer les bibliothèques pour améliorer l'auto-complétion.

Il faut ensuite [se connecter à une SDK Python](https://www.jetbrains.com/help/idea/creating-virtual-environment.html) de type “virtual env”, en choisissant le dossier `web/venv` et en l'appelant “Python CTF”.
Il est alors possible d'utiliser les *run configurations* pour exécuter les différentes commandes du projet, utiliser le debugger, etc.

## Autres commandes utiles

```shell
# Créer l'image Docker de la plateforme sans l'exécuter
$ make

# Nettoyer l'environnement (détruire tous les fichiers générés, la base de données, etc)
$ make clean

# Validation du coding style Python
$ make web/lint

# Installer les dépendances Python en local
# Par défaut, les dépendances sont installées directement dans le conteneur
# Pour les outils comme PyCharm ou VSCode, installer les 
# dépendances localement est nécessaire pour avoir l'auto-complétion.
$ make web/venv/install
```

Le `Makefile` est écrit dans le but de ne pas exécuter inutilement des actions.
Dans le cas où cette décision serait incorrecte, il est possible de forcer certaines actions.

```shell
# Forcer la création de l'image Docker
$ rm web/venv/docker; make web/venv/docker

# Forcer le téléchargement de l'image Docker Alpine
$ rm /tmp/node_pull; make /tmp/node_pull

# Forcer le téléchargement des dépendances Python
$ rm web/venv/install; make web/venv/install
```
