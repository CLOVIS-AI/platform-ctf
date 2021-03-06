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

## Je suis un élève d'une promotion RSR différente

Pour les élèves d'une promotion passée, il n'est pas utile de créer un groupe de promotion.
S'il s'agit de votre cas, vous pouvez suivre les étapes pour les contributions externes à RSR.

Pour les promotions futures, il faut créer un groupe pour la promotion et mettre en place le déploiement automatique.

### Configuration initiale

Les étapes sont les suivantes :
- [Créer un groupe GitLab](https://docs.gitlab.com/ee/user/group/) pour la promotion
- Ajouter les membres de la promotion au groupe en leur donnant le rôle “developer”
- Copier le dépôt en appuyant sur le bouton “fork” (en haut à droite de la page d'accueil du projet), puis en sélectionnant le groupe créé dans les étapes précédentes

Les paramètres suivants peuvent être intéressants à changer, dans la page de la copie du projet, appartenant au nouveau groupe :
- Settings » General » Visibility : si la copie est publique ou non
- Settings » General » Merge Requests » Merge checks : activer “Pipelines must succeed” et “All discussions must be resolved”
- Settings » General » Merge Requests Approval : activer “Merge request results” et “Merge train”
- Settings » Repository » Protected branches : personne n'a le droit de push sur `main` (il est obligatoire de créer une merge request et donc de valider les tests unitaires etc). À décider si uniquement les maintainers (les délégués) ou les developers (tous élèves) ont le droit de merge (eg. accepter une merge request).

Pour activer les tests et le déploiement automatisé, lire le guide de déploiement. <!-- TODO in #78 -->

### Développement

Quand le groupe a été créé et paramétré, vous pouvez suivre le processus décrit plus haut pour contribuer à la plateforme en tant qu'un élève de la promotion actuelle.

Lors de la création d'une merge request, il faudra faire attention à choisir la destination des modifications : il faut choisir le nouveau groupe, et non l'ancien.

## Je ne suis pas un élève de la filière RSR

Vous n'avez donc pas accès en écriture au dépôt GitLab.
Pour pouvoir suggérer des modifications, il va donc vous falloir configurer une copie du dépôt vous appartenant, effectuer les modifications que vous souhaitez, puis les envoyer à la promotion RSR actuelle.

Sur la page d'accueil du projet, vous pouvez utiliser le bouton “fork” pour créer une copie du projet sur laquelle vous avez tous les droits.
Pour paramétrer les tests et/ou le déploiement automatisé sur votre copie, lisez le guide de déploiement. <!-- TODO in #78 -->

Pour pouvoir accéder à la fois à vos propres branches ainsi qu'à celles du dépôt officiel, vous pouvez ajouter les deux dépôts à Git :
```shell
$ git clone git@gitlab.com:rsr22/plateforme-ctf.git  # ou https://gitlab.com/rsr22/plateforme-ctf.git
$ cd plateforme-ctf
$ git remote rename origin rsr22
$ git remote add [votre nom] [URL de clone de votre dépôt]
$ git fetch --all  # se connecter à toutes les remotes et télécharger les branches et commits
```

Vous pouvez ensuite suivre les étapes de développement suivies par les élèves, à l'exception de :
- vous ne pouvez pas utiliser `origin`, il faut choisir entre une des deux disponibles
- lors de la création d'une merge request, il faut choisir la branche de destination comme étant celle du dépôt vers lequel vous voulez envoyer la modification.
