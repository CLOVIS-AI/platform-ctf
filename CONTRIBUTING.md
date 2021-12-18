# Guide de contribution

Ce document décrit le processus de contribution à la plateforme.

La nouvelle plateforme CTF est développée et déployée depuis GitLab.
Pour cela, la filière RSR 2022 possède [un groupe GitLab](https://gitlab.com/rsr22).
Seuls les élèves de cette promotion y ont accès en écriture.

Ce document décrit donc trois manières de contribuer :
- Pour les élèves de la promotion RSR 2022, propriétaire de ce dépôt,
- Pour les élèves d'autres promotions RSR,
- Pour les contributions externes.

## Je suis un élève de la filière RSR 2022

La gestion de projet sur GitLab s'organise de la façon suivante :
- les “issues” représentent la liste des tâches
- les “milestones” représentent des catégories de tâches en rapport les unes avec les autres, ce qui permet de suivre l'avancement vers un objectif particulier
- les “merge requests” représentent des propositions de modifications au projet

### Liste des tâches

Avant de pouvoir modifier la plateforme, il faut s'assigner une tâche.
Cela permet d'éviter que plusieurs personnes travaillent sur la même chose en même temps.
Cela permet aussi à tout le monde de savoir où on est le projet.

Pour cela, il faut se rendre dans l'onglet “Issues” de GitLab.
Il faut soit créer une tâche, ou en choisir une existante.
Chaque issue possède un champ “assignee” (dans la barre de droite) désignant la personne responsable de la réalisation de cette tâche.

Quand vous vous êtes assigné à une tâche, vous pouvez passer à l'étape suivante.

### Workflow par branches

Pour pouvoir travailler sur plusieurs choses à la fois sans se poser de problèmes, on crée une branche par issue.
Par convention, cette branche est nommée sur la forme `123-branch-name`, où `123` est le numéro de l'issue.

##### Créer la branche dans le terminal

```shell
$ git switch -c 123-branch-name origin/main
```

##### Créer la branche dans l'interface GitLab

Dans chaque issue, utiliser le bouton “Create merge request”.
Ensuite, il suffit de mettre à jour les données, et se déplacer sur la branche.

```shell
$ git fetch --all
$ git switch 123-branch-name  # n'hésitez pas à utiliser l'auto-complétion
```

Vous pouvez ensuite travailler dans cette branche.
Le style de commit recommandé est le [BrainDot Git Style](https://gitlab.com/braindot/legal/-/blob/master/coding-style/STYLE_Git.md), parce qu'il est compatible avec les scripts de génération du changelog, mais ce n'est pas une obligation.

### Merge requests

À chaque `push`, GitLab affiche dans le terminal le lien vers la merge request (ou pour la créer, si elle n'existe pas encore).

Il faut vérifier que la merge request est bien reliée à l'issue : pour cela, elle doit contenir `Closes #123` ou `Fixes #123`, où `123` est le nom de l'issue.
Si la branche a été nommée correctement, cela devrait être automatique.

Une merge request permet de regrouper une proposition de modification, et d'en discuter.
C'est aussi là que se passent les vérifications automatiques (tests unitaires, coding style…) ainsi que le déploiement automatisé sur le serveur de la plateforme.

Pour en apprendre plus sur le merge requests, voir la [documentation GitLab](https://docs.gitlab.com/ee/user/project/merge_requests/getting_started.html).
Quand la modification est acceptée par un mainteneur (typiquement, un délégué de la filière), il a la possibilité de la “merge”, ce qui lance automatiquement le déploiement sur le serveur.

## Je suis un élève de la filière RSR d'une autre promotion

<!-- TODO créer un groupe pour la promotion -->
<!-- TODO créer un fork du dépôt -->
<!-- TODO suivre la procédure normale -->

## Je ne suis pas un élève de la filière RSR

Vous n'avez donc pas accès en écriture au dépôt GitLab.
Pour pouvoir suggérer des modifications, il va donc vous falloir configurer une copie du dépôt vous appartenant, effectuer les modifications que vous souhaitez, puis les envoyer à la promotion RSR actuelle.

<!-- TODO créer un fork personnel -->
<!-- TODO cloner le dépôt, ajouter les différentes remotes -->
<!-- TODO suivre la procédure normale -->
