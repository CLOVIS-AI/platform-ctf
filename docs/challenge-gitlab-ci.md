# Automatisation du pré-conditionnement d'un challenge

Lors de la compilation de la plateforme, tous les challenges sont automatiquement pré-conditionnés par GitLab.
Ce pré-conditionnement peut prendre la forme de la génération d'un modèle de VM qui sera ensuite cloné lors du lancement d'un challenge, la création d'une image Docker qui sera lancée par l'utilisateur, ou simplement la compilation de code C dont l'exécutable sera fourni à l'utilisateur pour qu'il l'analyse. 

Dans tous les cas, on ajoute un fichier `build.gitlab-ci.yml` dans le dossier du challenge, et on l'inclut au fichier `.gitlab-ci.yml` à la racine de la plateforme ([lien](../.gitlab-ci.yml), clef `include:local`).

Pour en savoir plus, voir la [documentation officielle](https://docs.gitlab.com/ee/ci/) ainsi que la [liste des mots-clefs](https://docs.gitlab.com/ee/ci/yaml/).
La plateforme fournit des modèles dans le dossier [automation](../automation), qui peuvent être utilisés pour simplifier les tâches communes.

En particulier, on retrouve les conventions suivantes :
- Les différentes `stages` disponibles sont :
  - `generics`: création des génériques
  - `challenges`: pré-conditionnement des challenges
  - `platform`: compilation de la plateforme elle-même
  - `publish`: publication des fichiers générés
  - `deploy`: lancement de la nouvelle version de la plateforme sur le serveur
- La variable `build_version` contient un numéro unique pour chaque pipeline, qui peut être utilisé pour préfixer des ressources créées
- Les différents tags disponibles sont :
  - `docker`: le job sera exécuté dans un environnement ou les commandes `docker` sont disponibles
  - `test-server`: le job sera exécuté sur une machine sur laquelle `packer`, `terraform` et `ansible` sont disponibles, et où le fichier `~/secret.properties` est configuré pour déployer sur l'environnement de test
  - `staging-server`: identique à `test-server`, mais pour l'environnement pré-production
  - `production-server`: identique à `test-server`, mais pour l'environnement de production

Les challenges existants peuvent servir d'exemples pour écrire un nouveau challenge.
