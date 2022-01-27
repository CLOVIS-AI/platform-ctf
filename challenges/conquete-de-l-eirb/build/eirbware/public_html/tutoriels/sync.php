<?php
$page = "tutoriels";
chdir("../");
include("templates/header.php");
?>

<div class="padding">
  <h2>Synchronisation de tes fichiers locaux avec ceux de l'école</h2>
  <ul class="arrow">
    <li><img id="arrow1" class="arrow" src="../assets/arrow.svg" onClick="afficher(1)">
      <h3 class="underline" onClick="afficher(1)">Copier des fichiers entre votre ordinateur et l'enseirb</h3>
      <ul id="hide1">
        <li>Tout d'abord ouvrez un terminal en appuyant sur les touches CTRL + ALT + t.</li>
        <li>Pour copier un fichier depuis votre ordinateur vers le serveur de l'école utilisez la commande suivante:
<p class="command">scp {{localPath}} {{login}}@ssh.enseirb.fr:{{distantPath}}</p></li>
Où {{localPath}} est l'emplacement d'un fichier sur votre ordinateur, {{login}} est votre identifiant enseirb et {{distantPath}} est l'emplacement sur le serveur.</li>
        <li>Pour copier un dossier ainsi que son contenu depuis votre ordinateur vers le serveur de l'école utilisez:
<p class="command">scp -r {{localPath}} {{login}}@ssh.enseirb.fr:{{distantPath}}</p></li>
        <li>Pour copier un fichier depuis le serveur de l'école vers votre oridnateur utilisez la commande suivante:
<p class="command">scp {{login}}@ssh.enseirb.fr:{{distantPath}} {{localPath}}</p></li>
        <li>Pour copier un dossier ainsi que son contenu depuis votre ordinateur vers le serveur de l'école utilisez:
<p class="command">scp -r {{login}}@ssh.enseirb.fr:{{distantPath}} {{localPath}}</p></li>
        <li>Une autre commande qui peut être très utile pour par exemple faire des mises à jour entre deux dépôts est la commande rsync. Allez voir la dernière section pour en savoir d'avantage.</li>
      </ul>
    </li>
    <li><img id="arrow2" class="arrow" src="../assets/arrow.svg" onClick="afficher(2)">
      <h3 class="underline" onClick="afficher(2)">Créer un pont local vers les fichiers de l'école</h3>
      <ul id="hide2">
        <li>La méthode décrite ci-après permet de créer un point de montage sur votre disque qui va servir de pont vers les fichiers de l'école en utilisant le protocol ssh.</li>
        <li>Ceci implique de disposer d'une connexion internet dès lors que vous voulez accéder à vos fichiers. Si vous souhaitez avoir accès à vos documents hors connexion allez voir la dernière section.</li>
        <li>Tout d'abord, installez le paquet sshfs grâce à la commande:
<p class="command">sudo apt update; sudo apt install sshfs</p></li>
        <li>Une fois ceci fait, choisissez un dossier vide ou créez un dossier dans lequel tous vos documents apparaîtrons comme suit:
<p class="command">mkdir {{dossier}}</p></li>
        <li>Enfin utilisez la commande suivante suivante pour créer le pont entre votre ordinateur et l'école:
<p class="command">sshfs {{login}}@ssh.enseirb.fr:{{distantPath}} {{localPath}}</p>
Où {{distantPath}} est le dossier de l'école dont vous voulez accéder au contenu et {{localPath}} est l'emplacement du dossier évoqué au point précédent.</li>
        <li>Il ne vous reste plus qu'à aller voir dans le dossier que vous avez choisi et vous devriez voir tous les fichiers contenus dans le répertoire distant.</li>
      </ul>
    </li>
    <li><img id="arrow3" class="arrow" src="../assets/arrow.svg" onClick="afficher(3)">
      <h3 class="underline" onClick="afficher(3)">Dupliquer tous les documents entre les deux plateformes avec une seule commande</h3>
      <ul id="hide3">
        <li>Tout d'abord ouvrez un terminal en appuyant sur les touches CTRL + ALT + t.</li>
        <li>Puis installez le script sur votre ordinateur en copiant la commande suivante dans votre terminal :
<p class="command">wget https://eirbware.eirb.fr/assets/setup-update -O setup-update && chmod +x setup-update && ./setup-update</p>
Ou bien téléchagez le script suivant: <a class="download" href="../assets/setup-update" download="setup-update">Update</a> et exécutez le.</li>
        <li>Suivez les instructions à l'écran: entrez votre login enseirb lorsqu'il vous est demandé et il est conseillé de mettre "~" en root path pour synchroniser absolument tous vos fichiers.</li>
        <li>Il ne vous reste plus qu'à exécuter la commande suivante sur votre ordinateur personnel à chaque fois que vous souhaitez synchroniser vos fichiers:
<p class="command">update</p></li>
        <li>Il est conseillé d'avoir effectué le tutoriel sur les clefs ssh afin de ne pas avoir à entrer son mot de passe deux fois à chaque utilisation de la commande.</li>
        <li>Pour les plus curieux, vous pouvez modifier les règles d'exclusion pour les fichiers à synchroniser en tapant:
<p class="command">gedit $(which update)</p>Ou avec nimporte quel autre éditeur de texte.</li>
      </ul>
    </li>
  </ul>
</div>

<?php
include("hint.php");
include("templates/footer.php");
?>
