<?php
$page = "tutoriels";
chdir("../");
include("templates/header.php");
?>

<ul class="center">
  <li>
      <a href="ubuntu-on-windows.php"><img class="tuto-svg" src="../assets/tuto/linux.svg"></a>
      <div class="new">NOUVEAU !</div>
      <p>Apprends à utliser un terminal ou une machine virtuelle Ubuntu directement dans Windows.
Ceci te permet de travailler sur Ubuntu sans devoir installer un dual boot.
      </p>
  </li>
    <li>
    <a href="ssh.php"><img class="tuto-svg" src="../assets/tuto/ssh.svg"></a>
    <p>Apprends à te connecter en ssh au serveur de l'école. 
Ceci te permet de travailler en ligne de commande depuis ton ordinateur comme si tu étais sur un ordinateur à l'enseirb.
    </p>
  </li>
  <li>
    <a href="bash.php"><img class="tuto-svg" src="../assets/tuto/bash.svg"></a>
    <p>Apprends les commandes de base à utiliser dans un terminal linux ou mac.
Ceci te permet de créer des fichiers, de les lire ou encore de te balader dans un système de fichiers et bien plus.
    </p>
  </li>
  <li>
    <a href="sync.php"><img class="tuto-svg" src="../assets/tuto/upload.svg"></a>
    <p>Apprends à synchroniser tes fichiers en local avec ceux de l'enseirb. 
Ceci te permet de travailler sur ton ordinateur personnel tout en retrouvant tes fichiers directement à l'école et inversement.</p>
  </li>
</ul>


<?php
include("templates/footer.php");
?>
