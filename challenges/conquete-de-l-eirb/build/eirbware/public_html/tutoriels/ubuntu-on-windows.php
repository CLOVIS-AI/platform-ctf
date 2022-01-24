<?php
$page = "tutoriels";
chdir("../");
include("templates/header.php");
?>

<div class="padding">
    <h2>Utiliser Ubuntu directement dans Windows</h2>
    <ul class="arrow">
        <li><img id="arrow1" class="arrow" src="../assets/arrow.svg" onClick="afficher(1)">
            <h3 class="underline" onClick="afficher(1)">WSL : Le terminal Ubuntu sur Windows 10 (sans interface graphique)</h3>
            <ul id="hide1">
                <p>Ce tutoriel est inspiré du <a class="download" href="https://docs.microsoft.com/fr-fr/windows/wsl/install-win10" target="_blank">guide d'installation du WSL</a> de Microsoft.</p>
                <h4>Étape 1 : Activer le sous-système Windows pour Linux</h4>
                <li>Avant de commencer, il est recommandé de faire les mises à jour de Windows (dans Paramètres > Mise à jour et sécurité > Windows Update).</li>
                <li>Ouvrez PowerShell en tant qu'administrateur et exécutez (copier-coller) : <p class="command">dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart</p></li>

                <h4>Étape 2 - Consulter la configuration requise pour exécuter WSL 2</h4>
                <li>Windows 10 doit exécuter la <em>version 1903</em> ou supérieure, avec la <em>Build 18382</em> ou supérieure. Pour vérifier votre numéro de version et de build, sélectionnez les touches <em>Windows + R</em>, tapez <em>winver</em> et sélectionnez <em>OK</em>.</li>

                <h4>Étape 3 : Activer la fonctionnalité Machine virtuelle</h4>
                <li>Ouvrez PowerShell en tant qu’administrateur et exécutez : <p class="command">dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart</p></li>
                <li>Redémarrez votre PC.</li>

                <h4>Étape 4 : Télécharger le package de mise à jour du noyau Linux</h4>
                <li>Téléchargez le <a class="download" href="https://wslstorestorage.blob.core.windows.net/wslblob/wsl_update_x64.msi" target="_blank">dernier package</a> du noyau Linux WSL2 pour machines x64.</li>
                <li>Exécutez le package (des autorisations vous seront demandées, sélectionnez <em>Oui</em>). Une fois l'installation terminée, vous pouvez passer à l'étape suivante.</li>

                <h4>Étape 5 : Définir WSL 2 comme version par défaut</h4>
                <li>Ouvrez PowerShell et exécutez : <p class="command">wsl --set-default-version 2</p></li>

                <h4>Étape 6 : Installer la distribution Linux Ubuntu</h4>
                <li>Ouvrez le lien suivant : <a class="download" href="https://www.microsoft.com/store/apps/9n6svws3rx71" target="_blank">Ubuntu 20.04 LTS</a>. Cliquez sur le bouton <em>Télécharger</em> et autorisez si nécessaire votre navigateur à ouvrir le Microsoft Store.</li>
                <li>Une fois installé, il vous suffit d'appuyer sur le bouton <em>Windows</em> et de taper "Ubuntu" et d'exécuter le premier résultat ("Ubuntu 20.04 LTS").</li>
                <li>Voilà, vous avez un terminal Ubuntu sur Windows !</li>

                <h4>Erreur : <i>WslRegisterDistribution failed with error: 0x80370102</i></h4>
                <li>Si vous avez cette erreur en démarrant le terminal Ubuntu, alors la virtualisation CPU n'est pas activée sur votre ordinateur. Il est nécessaire de l'activer sur le BIOS. Voici un <a class="download" href="https://www.bleepingcomputer.com/tutorials/how-to-enable-cpu-virtualization-in-your-computer-bios/" target="_blank">tutoriel d'exemple</a> pour les BIOS Asus.</li>
                <li>Si jamais vous avez cette erreur et ne savez pas comment activer la virtualisation CPU dans le BIOS, n'hésitez pas à contacter l'équipe Eirbware (mail et Facebook en bas de page) pour qu'on vous aide !</li>
            </ul>
        </li>
        <li><img id="arrow2" class="arrow" src="../assets/arrow.svg" onClick="afficher(2)">
            <h3 class="underline" onClick="afficher(2)">Machine virtuelle Ubuntu sous Windows avec VirtualBox</h3>
            <ul id="hide2">
                <h4>Etape 1 : Télécharger Ubuntu</h4>
                <li>Téléchargez Ubuntu <a class="download" href="https://ubuntu.com/download/desktop" target="_blank">ici</a>.</li>

                <h4>Etape 2 : Installer VirtualBox</h4>
                <li>Téléchargez VirtualBox pour Windows <a class="download" href="https://download.virtualbox.org/virtualbox/6.1.18/VirtualBox-6.1.18-142142-Win.exe" target="_blank">ici</a>, puis installez-le.</li>

                <h4>Etape 3 : Créer une nouvelle machine virtuelle</h4>
                <li>Ouvrez VirtualBox et cliquez sur "Nouvelle".</li>
                <p><img class="tuto-img" src="../assets/tuto/virtualbox/virtualbox1.png"></p>
                <li>Donnez un nom à votre VM, sélectionnez <em>Linux</em>, puis sélectionnez <em>Ubuntu 64 bits</em>. Si vous ne pouvez sélectionner que Ubuntu 32 bits, cela signifie que la virtualisation CPU n'est pas activée dans le BIOS (voir la partie <em>WSL > Erreur (à la fin)</em> de ce tutoriel).</li>
                <p><img class="tuto-img" src="../assets/tuto/virtualbox/virtualbox2.png"></p>
                <li>Pour la taille de la mémoire, choisissez 4096 MB. Si cette quantité se trouve dans la zone rouge, sélectionnez 2048 MB.</li>
                <p><img class="tuto-img" src="../assets/tuto/virtualbox/virtualbox3.png"></p>
                <li>Ensuite gardez les paramètres par défaut et continuez. Dans emplacement du fichier et taille, 10 Gio sont alloués par défaut, mais vous pouvez mettre plus (30 Gio par exemple), si vous avez la place suffisante sur votre disque dur. Enfin, créez la VM.</li>
                <p><img class="tuto-img" src="../assets/tuto/virtualbox/virtualbox5.png"></p>
                <li>Ensuite, cliquez sur <em>Démarrer</em>. VirtualBox va vous demander de choisir un disque de démarrage. Cliquez sur l'icône Dossier à droite</li>
                <p><img class="tuto-img" src="../assets/tuto/virtualbox/virtualbox7.png"></p> 
                <p>puis cliquez sur <em>Ajouter</em>, et sélectionnez l'iso Ubuntu que vous avez téléchargez à l'étape 1. Validez tout et l'installateur Ubuntu va s'allumer.</p>
                <p><img class="tuto-img" src="../assets/tuto/virtualbox/virtualbox8.png"></p>

                <h4>Etape 4 : Installer Ubuntu</h4>
                <li>Sélectionnez <em>Install Ubuntu</em>, sélectionnez votre langue et la langue du clavier, puis continuez l'installation en gardant les paramètres par défaut.</li>
                <p>ATTENTION : Parfois, le clavier reste en Qwerty tout au long de l'installation même si vous avez choisi Azerty, donc faites attention au login et au mot de passe que vous rentrez pour créer la session.</p>
                <li>Une fois l'installation terminée, Ubuntu va redémarrer. Une fois complétement allumé, si la fenêtre vous paraît petite, il vous suffit d'aller dans les paramètres Ubuntu (en haut à droite de l'écran où il y a les icônes réseau et son, puis Paramètres), dans Affichage, changez la résolution de l'écran.</li>
            </ul>
        </li>

        <li><img id="arrow3" class="arrow" src="../assets/arrow.svg" onClick="afficher(3)">
            <h3 class="underline" onClick="afficher(3)">Installez les packages pour faire du Fortran</h3>
            <ul id="hide3">
                <p>Cette partie vous explique comment installer Fortran, Emacs et Gnuplot. Ouvrez un terminal dans Ubuntu (avec Ctrl + Maj + T) ou ouvrez votre WSL Ubuntu, puis copiez la commande suivante :</p>
                <p class="command">sudo apt update && sudo apt install emacs-gtk gnuplot gnuplot-x11 gfortran</p>
                <p>Entrez votre mot de passe et tapez O (Oui) ou Y (Yes) lorsque demandé pour continuer.<p>
            </ul>
    </ul>
</div>

<?php
include("hint.php");
include("templates/footer.php");
?>
