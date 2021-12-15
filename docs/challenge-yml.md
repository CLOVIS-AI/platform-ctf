# Le fichier `challenge.yml`

Le fichier `challenge.yml` décrit la configuration d'un challenge.

Voici un exemple :
```yml
---
challenge:
  name: Le nom du challenge
  short_name: un_identifiant
  author: Les auteurs
  description: |
    <p>La description du challenge,
    qui peut être multiligne et contenir du <i>HTML</i>.</p>
  category: SCENARIO

resource:
  type: terraform
  args: |
    La VM du challenge est disponible à l'addresse <a href='https://ctf.rsr.enseirb-matmeca.fr:{port}' target='_blank'>https://ctf.rsr.enseirb-matmeca.fr:{port}</a>
  start_duration: 7
  is_vpn_needed: yes

sections:
  - section:
      title: Le titre de la première section 
      description: |
        <p>La description de cette section.</p>
        <button onclick="alert('Indice 1 : Dirb')" type="submit"> Indice 1 </button>
        <button onclick="alert('Indice 2 : Sauvegarde')" type="submit"> Indice 2 </button>
        <button onclick="alert('Indice 3 : Linux')" type="submit"> Indice 3 </button>

    steps:
      - description: |
          Le flag est de la forme flag_{***}.
        validation_type: string
        validation_arg: flag_{event_en_b33r_to_b33r}
        points: 20

      - description: |
          Le flag est de la forme flag_{***}.
        validation_type: string
        validation_arg: flag_{Balthazar_beer>Grizzly_mousse}
        points: 10
```

## Référence

### challenge

Le fichier `challenge.yml` doit obligatoirement contenir cette clé.

#### challenge:name

Le nom du challenge, qui sera utilisé pour l'affichage.
Obligatoire.

#### challenge:short_name

Le nom du dossier dans lequel se trouve le challenge.
Doit être un sous-dossier de `challenges` à la racine du dépôt.
Il doit être composé uniquement des caractères `a-z` et `_`.
Il est aussi utilisé dans la base de données.
Obligatoire.

#### challenge:author

Le nom de l'auteur du challenge.
Obligatoire.

#### challenge:description

La description du challenge.
Peut contenir du HTML, qui sera affiché à l'utilisateur sur la page du challenge.
La description permet de présenter le contexte, l'objectif et les outils utiles.
Obligatoire.

#### challenge:category

La catégorie dans laquelle le challenge va se placer.
Le nom de la catégorie est libre, mais il est recommandé d'utiliser une des catégories suivantes : `Cryptographie`, `Sténographie`, `Web`, `Réseau`, `SCENARIO`, `TRAININGS`.
Les deux dernières catégories correspondent aux onglets scénario et entraînement.
Obligatoire.

### resource

Le fichier `challenge.yml` *peut* contenir une clé `resource` qui décrit les ressources nécessaires à la validation du challenge.

#### resource:type

Le type de ressource.
Actuellement, les types `file` et `terraform` sont supportés.

- `file` : un fichier que l'utilisateur peut télécharger. Permet d'afficher un bouton "Download" sur la page du challenge.
- `terraform` : une ressource qui peut être lancée via Terraform. Permet d'afficher les boutons "Start" et "Stop". Lorsque l'utilisateur appuie sur "Start", la configuration placée dans `instance/start.tf` du challenge est lancée.

#### resource:arg

Un argument donné à la ressource.

- Pour une ressource de type `file` : un chemin dans le dossier `static` du challenge.
- Pour une ressource de type `terraform` : un message affiché à l'utilisateur à la fin du déploiement des ressources.
  Il est possible d'utiliser les _format string_ de Python (`{}`) pour rendre ce message dynamique et inclure une adresse IP ou un port sur lequel la ressource déployée est accessible.
  Les variables utilisables sont celles marquées par l'objet `output` dans la configuration de Terraform.

#### resource:start_duration

La durée approximative en secondes nécessaire à l'instanciation de la ressource.

En pratique, cet argument n'est utilisé que pour le type `terraform` et vaut en général 5 secondes si la ressource lancée est un conteneur, et 60 secondes s'il s'agit d'une machine virtuelle.

#### resource:is_vpn_needed

Argument booléen conditionnant l'affichage d'un bouton "Download VPN" sur la page du challenge.

### sections

Le fichier `challenge.yml` *peut* contenir une clé `sections` comportant une liste d'étapes de validation.

Chaque étape est un objet contenant une clé `section` et une clé `steps`; cette clé a donc la forme suivante :
```yml
sections:
  - section: …
    steps: …
  - section: …
    steps: …
```

#### sections:section:title

Le titre de la section.

#### sections:section:description

La question posée à l'utilisateur pour valider cette section.

#### sections:section:validation_type

La méthode de validation de l'entrée utilisateur.

- `dynamic`: lors du déploiement de la ressource, le flag est généré et enregistré dans le dossier `instance/flags`. La saisie de l'utilisateur est comparée avec le contenu d'un de ces fichiers.
- `file` : la saisie est comparée au contenu d'un fichier.
- `string`: la saisie est comparée à une chaîne de caractères.
- `script`: la saisie est passée à un script. Elle est considérée comme valide si le code de retour du script est 42.

#### sections:section:validation_arg

Un argument fourni à la validation.

- Type de validation `dynamic` : le nom du fichier contenant le flag, dans `instance/flags/`
- Type de validation `file` : le nom du fichier contenant le flag
- Type de validation `string` : le flag
- Type de validation `script` : le début de la ligne de commande à exécuter
