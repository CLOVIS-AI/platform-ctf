# Machines virtuelles génériques

Les machines virtuelles génériques sont des installations "pures" utilisées par les challenges.
L'objectif est de mettre en commun l'espace de stockage entre les différents challenges, ainsi que d'accélérer les temps de déploiement.

Par exemple, tous les challenges nécessitant une installation d'Ubuntu peuvent partager une unique configuration dans ce dossier.

Chaque VM générique est créée grâce à l'outil `packer`.
La configuration de chaque VM générique est placée dans son propre dossier au sein de celui-ci, et doit contenir un fichier `build.pkr.hcl` qui contient la configuration de `packer`. Tous les autres fichiers nécessaires peuvent être placés dans le dossier de la VM.

Le nom des VMs génériques doit être sous la forme `generic-os-version`, par exemple `generic-alpine-3.12` ou `generic-windows-server-2019`.

Pour activer la génération d'un générique, il faut ajouter son dossier [dans la configuration de GitLab](build.gitlab-ci.yml) (`.generics:parallel:matrix:generic`).
