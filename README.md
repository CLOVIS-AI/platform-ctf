# Plateforme CTF

Ce dépôt contient le code de la plateforme CTF de la filière RSR de l'ENSEIRB-MATMECA.

Pour configurer la plateforme :
```shell
$ cp web/secret.exemple.properties web/secret.properties
```
Puis modifier `secret.properties`. Ne jamais inclure ce fichier dans le dépôt.

Pour exécuter la plateforme, on peut utiliser les commandes :
```shell
# Démarrer la plateforme
$ make start

# Arrêter la plateforme
$ make stop
```

Les commandes suivantes peuvent aussi être utiles :
```shell
# Créer l'image Docker de la plateforme sans l'exécuter
$ make

# Nettoyer les fichiers générés
$ make clean

# Vérifier le coding style Python
$ make web/lint

# Forcer la création de l'image Docker
$ rm web/venv/docker; make web/venv/docker

# Forcer le téléchargement de l'image Docker Alpine
$ rm /tmp/node_pull; make /tmp/node_pull

# Installer les dépendances Python localement (par exemple pour avoir l'auto-complétion dans PyCharm)
$ make web/venv/install

# Forcer le téléchargement des dépendances Python
$ rm web/venv/install; make web/venv/install
```
