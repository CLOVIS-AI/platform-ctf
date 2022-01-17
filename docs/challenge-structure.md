# Structure des challenges

L'objectif de ce document est de présenter le fonctionnement d'un challenge lorsqu'il est intégré à la plateforme.

Les challenges sont stockés dans le dossier `challenges` de ce dépôt. Dans la suite, nous ferons l'amalgame entre les termes `Challenge`, `Scénario` et `Training`. En effet, ces trois termes se distinguent seulement par la façon dont ils sont affichés à l'utilisateur.

## Compilation et génération des challenges

La génération d'un challenge par la plateforme est composée de trois étapes :
- Génération des génériques (VM uniquement)
- Génération d'un modèle (si nécessaire)
- Lancement du challenge

Les génériques sont des machines virtuelles “propres” qui peuvent servir de base à plusieurs challenges (par exemple, une version spécifique de Debian ou Alpine).
Pour en savoir plus, voir la [documentation des generics](../generics/README.md).

Les modèles sont des machines virtuelles ou des conteneurs représentant toutes les données nécessaires pour un challenge.
Typiquement, il va s'agir d'un environnement avec toutes les dépendances nécessaires, les logiciels ayant la faille souhaitée, etc.
Quand aucun environnement n'est nécessaire, on peut utiliser cette phase pour compiler des fichiers, etc (par exemple, compiler un fichier C, qui sera ensuite fourni statiquement aux utilisateurs).

Lors du lancement du challenge, on peut configurer plusieurs réseaux, ajouter un flag dynamique…

## Structure des fichiers

Chaque challenge doit suivre la structure suivante :
```text
├─ challenge.yml
├─ build.gitlab-ci.yml
├─ static
├─ build
└─ instance
   └─ start.tf
```

### Le fichier `challenge.yml`

Le fichier `challenge.yml` contient la configuration globale du challenge.
Sa documentation [est disponible ici](challenge-yml.md).

### Le fichier `build.gitlab-ci.yml`

Ce fichier permet de donner les étapes de création des modèles d'un challenge.
Sa documentation [est disponible ici](challenge-gitlab-ci.md).

### Le dossier `static`

Ce dossier permet de stocker des ressources statiques pouvant être téléchargées par l'utilisateur ;
par exemple lorsque le challenge est de type `file`, ou pour pouvoir inclure des images dans les descriptions des challenges, des sections ou des étapes. 

Ce dossier est facultatif.

### Le dossier `build`

Par convention, ce fichier contient les informations nécessaires à la génération des modèles d'un challenge. Exemples :
- dans le cas d'un challenge Docker, on pourra y mettre le `Dockerfile` ainsi que les fichiers qui sont copiés dans le conteneur.
- dans le cas d'un challenge qui compile du C pour fabriquer un exécutable qui sera analysé par l'utilisateur, on peut y mettre les sources ainsi qu'un script les compilant.
- dans le cas d'un challenge de type VM, on pourra y mettre la configuration de Terraform et Ansible pour générer les modèles. 

Dans tous les cas, l'utilisation du contenu de ce dossier par la plateforme est configuré dans le fichier `build.gitlab-ci.yml` à la racine du challenge ([documentation](challenge-gitlab-ci.md)).

Ce dossier est facultatif.

### Le dossier `instance`

Les informations nécessaires au lancement d'un challenge.
Au lancement du challenge, il est copié dans un dossier temporaire pour chaque utilisateur.

Les commandes suivantes sont exécutées par la plateforme :
```shell
$ terraform init
$ terraform plan
$ terraform apply
```

La configuration utilisée est le fichier `start.tf` dans ce dossier, qui est obligatoire pour tous les challenges pouvant être “lancés” (obligatoire pour les VMs ou Docker, inutile pour les challenges de type fichier).

On peut utiliser cette configuration pour générer un flag différent pour chaque lancement du challenge, pour configurer des réseaux virtuels pour permettre à plusieurs VMs de communiquer, etc.

## Intégration à la plateforme

La commande `flask challenge` peut être utilisée pour interagir avec les challenges. Voir la commande `flask challenge --help` et [la documentation](../web/src/commands/challenge_commands.md).
