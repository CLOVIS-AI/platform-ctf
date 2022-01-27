<?php
$page = "tutoriels";
chdir("../");
include("templates/header.php");
?>

<div class="padding">
  <h2>Comment se connecter au serveur de l'école depuis votre ordinateur personnel?</h2>
  <ul class="arrow">
    <li><img id="arrow1" class="arrow" src="../assets/arrow.svg" onClick="afficher(1)">
      <h3 class="underline" onClick="afficher(1)">La connexion SSH en ligne de commande avec mot de passe</h3>
      <ul id="hide1">
        <li>Tout d'abord ouvrez un terminal en appuyant sur les touches CTRL + ALT + t.</li>
        <li>Puis taper la commande suivante: 
<p class="command">ssh {{login}}@ssh.enseirb.fr</p>
En veillant à remplacer {{login}} par votre nom d'utilisateur composé de la première lettre de votre prénom suivi de votre nom et parfois d'un numéro (C'est le même qu'à l'école). </li>
        <li>Enfin entrez votre mot de passe lorsqu'il vous est demandé (Encore une fois c'est le même mot de passe qu'à l'école). Et vous voilà connecté au serveur de l'école où vous pouvez retrouver tous vos documents.</li>
        <p>Attention tout de même avec SSH vous n'avez accès qu'à un terminal et non pas à l'interface graphique d'un PC de l'école.
Pour tout travail (autre que de la copie de fichiers ou l'exploration de documents) sur le serveur de l'école veillez à vous connecter à la machine travail64.</p>
        <li>Pour cela, une fois connecté en ssh au serveur de l'école, tapez la comande suivante:
<p class="command">ssh {{login}}@travail64</p>
Puis entrez votre mot de passe et vous voilà fin prêt à travailler.</li>
        <p>Si vous êtes un flemmard et que taper votre mot de passe à chaque nouvelle connexion vous ennuie, suivez la procédure suivante.</p>
      </ul>
    </li>
    <li><img id="arrow2" class="arrow" src="../assets/arrow.svg" onClick="afficher(2)">
      <h3 class="underline" onClick="afficher(2)">Mise en place d'une paire de clefs SSH afin de ne plus avoir à taper de mot de passe</h3>
      <ul id="hide2">
        <li>La première chose à faire est de créer une paire de clefs SSH. 
Pour cela tapez la commande suivante sur votre PC :
<p class="command">ssh-keygen</p>
Et suivez les instructions à l'écran. Une précision tout de même, il est possible de mettre une passphrase sur votre clef privée. Ce qui signifie que cette phrase vous sera demandée pour déverouiller la clef à chaque démarrage de l'ordinateur. Si vous n'en voulez pas, laissez simplement la passphrase vide. (Pour la suite du tutoriel ne changez pas les valeurs par défaut pour le nom ou l'emplacement des clefs).</li>


        <li>Une fois l'éxécution terminée, vous aurez à disposition deux clefs (par défaut elles se situent dans ~/.ssh et s'appellent id_rsa et id_rsa.pub). 
La clef contenue dans le fichier .pub est comme son nom l'indique votre clef publique, et peut être partagée à n'importe qui. Voyez la comme une serrure que vous pouvez donner.
Par contre la deuxième clef ne doit en aucun cas être partagée avec qui que ce soit. C'est grâce à elle que vous pouvez vous connecter partout où votre clef publique a été partagée.</li>
        <li>Cette petite explication étant faite, allons mettre la clef publique sur le serveur de l'enseirb avec la commande:
<p class="command">ssh-copy-id -i ~/.ssh/id_rsa {{login}}@ssh.enseirb.fr</p>
Entrez votre mot de passe lorsqu'il vous est demandé et le tour est joué, ce sera la dernière fois que votre mot de passe sera demandé.</li>
        <p>Dernièrement pour les plus flemmards d'entre vous qui souhaiteraient raccoursir la commande à taper pour se connecter à l'école, suivez la suite du tutoriel.</p>
      </ul>
    </li>
    <li><img id="arrow3" class="arrow" src="../assets/arrow.svg" onClick="afficher(3)">
      <h3 class="underline" onClick="afficher(3)">Configuration d'un nom de serveur</h3>
      <ul id="hide3">
        <p>Avec SSH il est possible d'ajouter des serveurs connus à un fichier de configuration.</p>
        <li> Pour cela il faut créer le fichier ~/.ssh/config et le remplir de la façon suivante:
<p class="command">Host enseirb
HostName = "ssh.enseirb.fr"
User = "{{login}}"
IdentityFile = "~/.ssh/id_rsa"</p>
En veillant à remplacer {{login}} par votre login évidemment.</li>
        <li>Et voila, il ne vous reste plus qu'à utiliser la commande suivante pour vous connecter à l'enseirb:
<p class="command">ssh enseirb</p></li>
      </ul>
    </li>
  </ul>
</div>

<?php
include("hint.php");
include("templates/footer.php");
?>
