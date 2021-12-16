# Structure des challenges

L'objectif de ce document est de présenter le fonctionnement d'un challenge lorsqu'il est intégré à la plateforme.

Les challenges sont stockés dans le dossier `challenges` de ce dépôt. Dans la suite, nous ferons l'amalgame entre les termes `Challenge`, `Scénario` et `Training`. En effet, ces trois termes se distinguent seulement par la façon dont ils sont affichés à l'utilisateur.

## Structure de fichier

Chaque challenge doit suivre la structure suivante :
```text
├─ challenge.yml
├─ static
├─ build
│  ├─ build.sh
│  └─ Dockerfile
└─ instance
   └─ start.tf
```

### Le fichier `challenge.yml`

Le fichier `challenge.yml` contient la configuration globale du challenge.
Sa documentation [est disponible ici](challenge-yml.md).

### Le dossier `static`

Ce dossier permet de stocker des ressources statiques pouvant être téléchargées par l'utilisateur ;
par exemple lorsque le challenge est de type `file`, ou pour pouvoir inclure des images dans les descriptions des challenges, des sections ou des étapes. 

Ce dossier est facultatif.

### Le dossier `build`

Fichiers nécessaires à la construction des ressources lors du lancement de la plateforme.
Cela permet de préparer les ressources en avance pour qu'elles n'aient qu'à être lancées lorsque l'utilisateur appuie sur le bouton "Start".

Ce dossier doit contenir un script `build.sh` préparant les ressources du challenge. Il est appelé par la commande `flask challenge build` ([documentation](../web/src/commands/challenge_commands.md)).

Par exemple, ce script peut créer une image Docker, qui sera ensuite lancée par Terraform :
```shell
#!/usr/bin/env bash

challenge_name=training_platform

# Se connecter à l'hôte SSH et y créer l'image
docker -H "ssh://$ssh_docker_user@$ssh_docker_hostname:$ssh_docker_port" build -t $challenge_name "$server_challenges"/$challenge_name/build
```
Le script peut utiliser toutes les variables présentes dans `secret.properties` ([documentation](development.md), [liste des variables](../web/secret.example.properties)).

Ce dossier est facultatif.

### Le dossier `instance`

Les sources nécessaires à l'instanciation d'une ressource.
Pendant cette instanciation, il est copié dans un répertoire temporaire avant que son contenu ne soit utilisé.

Dans le cas d'un challenge de type `terraform`, les commandes suivantes seront exécutées par la plateforme dans la copie temporaire du dossier :
```shell
$ terraform init
$ terraform plan
$ terraform apply
```

Si l'une des étapes du challenge est de type `dynamic`, un fichier contenant le flag doit être créé dans le sous-dossier `flags` de la copie temporaire.

## Intégration à la plateforme

La commande `flask challenge` peut être utilisée pour interagir avec les challenges. Voir la commande `flask challenge --help` et [la documentation](../web/src/commands/challenge_commands.md).
