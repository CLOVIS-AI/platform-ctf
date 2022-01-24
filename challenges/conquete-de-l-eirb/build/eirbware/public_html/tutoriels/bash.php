<?php
$page = "tutoriels";
chdir("../");
include("templates/header.php");
?>

<div class="padding">
        <h2>Les commandes de base</h2>
        <ul class="arrow">
                <li><img id="arrow1" class="arrow" src="../assets/arrow.svg" onClick="afficher(1)">
                        <h3 class="underline" onClick="afficher(1)">Principes de base d'un système de fichier</h3>
                        <ul id="hide1">
                                <li>Il n'y a pas de distinction entre un fichier standard et un dossier, un dossier n'est rien d'autre qu'un fichier particulié contenant un lien vers un emplacement.</li>
                                <li>Un système de fichier est un arbre, c'est à dire que tous les fichiers sont rangés dans des dossiers partant d'un dossier racine représenté par le symbole "/"</li>
                                <li>Lorsque vous ouvrez un terminal, vous vous situez à un emplacement particulier qui est votre "home" et qui est représenté par le symbole "~"</li>
                                <li>Pour faire référence à l'endroit où vous vous situez, le symbole est "." et pour faire référence au dossier parrent le symbole est ".."</li>
                        </ul>
                </li>
                <li><img id="arrow2" class="arrow" src="../assets/arrow.svg" onClick="afficher(2)">
                        <h3 class="underline" onClick="afficher(2)">Navigation dans le système de fichier</h3>
                        <ul id="hide2">
                                <li>Tout d'abord ouvrez un terminal en appuyant sur les touches CTRL + ALT + t.</li>
                                <li>Pour afficher les fichiers du dossier courant utilisez la commande suivante :
                                        <p class="command">$ ls</p>
                                </li>
                                <li>Pour lister tous les fichiers du dossier courant (y compris les fichiers cachés) utilisez la commande suivante :
                                        <p class="command">$ ls -la</p>
                                </li>
                                <li>Pour vous déplacer du dossier courant à un autre dossier utilisez :
                                        <p class="command">cd {{path}}</p>
                                        En veillant à remplacer {{path}} par le chemin vers le dossier voulu.
                                </li>
                                <li>Pour toute information supplémentaire sur la façon d'utiliser une certaine commande tapez :
                                        <p class="command">man {{commande}}</p>
                                        Et vous obtiendrez le manuel correspondant à la {{commande}} en question.
                                </li>
                        </ul>
                </li>
                <li><img id="arrow3" class="arrow" src="../assets/arrow.svg" onClick="afficher(3)">
                        <h3 class="underline" onClick="afficher(3)">Création et lecture de fichier</h3>
                        <ul id="hide3">
                                <li>Pour créer un {{fichier}} vide utilisez :
                                        <p class="command">touch {{fichier}}</p>
                                </li>
                                <li>Pour créer un {{fichier}} contenant le mot toto utilisez :
                                        <p class="command">echo "toto" > {{fichier}}</p>
                                </li>
                                <li>Pour créer un {{dossier}} utilisez :
                                        <p class="command">mkdir {{dossier}}</p>
                                </li>
                                <li>Pour afficher le contenu d'un {{fichier}} :
                                        <p class="command">cat {{fichier}}</p>
                                </li>
                                <li>Enfin pour éditer un fichier utilisez une des commandes suivantes suivant l'éditeur de texte dont vous disposez :
                                        <p class="command">emacs -nw {{fichier}}</p>
                                        <p class="command">nano {{fichier}}</p>
                                        <p class="command">vim {{fichier}}</p>
                                        <p class="command">vi {{fichier}}</p>
                                </li>
                        </ul>
                </li>
                <li><img id="arrow4" class="arrow" src="../assets/arrow.svg" onClick="afficher(4)">
                        <h3 class="underline" onClick="afficher(4)">Copie, mouvement et suppression de fichier</h3>
                        <ul id="hide4">
                                <li>Pour modifier l'emplacement d'un fichier utilisez :
                                        <p class="command">mv {{path}} {{newPath}}</p>
                                        En remplaçant {{path}} par le chemin vers le fichier actuel et {{newPath}} par le nouveau chemin.
                                </li>
                                <li>Pour renommer un {{fichier}} utilisez :
                                        <p class="command">mv {{fichier}} {{newName}}</p>
                                        Ceci est un cas particulier de la commande précédente où le dossier de départ et d'arrivé sont les mêmes
                                </li>
                                <li>Pour copier un {{fichier}} utilisez :
                                        <p class="command">cp {{fichier}} {{path}}</p>
                                </li>
                                <li>Pour copier un dossier ainsi que son contenu utilisez :
                                        <p class="command">cp -r {{dossier}} {{path}}</p>
                                </li>
                                <li>Pour supprimer un fichier utilisez :
                                        <p class="command">rm {{fichier}}</p>
                                </li>
                                <li>Pour supprimer un dossier ainsi que son contenu utilisez :
                                        <p class="command">rm -r {{dossier}}</p>
                                </li>
                        </ul>
                </li>
                <li><img id="arrow5" class="arrow" src="../assets/arrow.svg" onClick="afficher(5)">
                        <h3 class="underline" onClick="afficher(5)">Gestion des droits d'accès</h3>
                        <ul id="hide5">
                                <li>Pour afficher toutes les informations sur un {{fichier}} utilisez :
                                        <p class="command">ls -la {{fichier}}</p>
                                </li>
                                <li>Les droits d'accès pour un fichier comprennent les droits pour la personne qui possède le fichier puis pour le groupe et enfin pour tous les autres utilisateurs.</li>
                                <li>Il y a trois types de droit : en premier la lecture "r", puis l'écriture "w" et enfin l'éxécution "x".
                                        Chaque type de droit correspond à une puissance de 2. Ainsi on obtient: 4 pour "r", 2 pour "w" et 1 pour "x".
                                        Il ne reste plus qu'à additionner ces chiffres pour obtenir le chiffre qui correspond à des droits d'accès.
                                        Par exemple les droits d'accès 754 signifient que le possesseur peut lire, écrire et éxécuter le fichier ; le groupe peut seulement lire et éxécuter ; enfin les autres ne peuvent que lire.</li>
                                <li>Pour donner les {{droits}} à un {{fichier}}/dossier utilisez :
                                        <p class="command">chmod {{droits}} {{fichier}}</p>
                                </li>
                                <li>Pour donner les droits à un {{dossier}} et tous les dossiers et fichiers qu'il contient utilisez :
                                        <p class="command">chmod -R {{droits}} {{dossier}}</p>
                                </li>
                                <li>Pour changer le {{possesseur}} d'un {{fichier}} utilisez :
                                        <p class="command">chown {{possesseur}} {{fichier}}</p>
                                </li>
                                <li>Enfin pour avoir les droits d'administrateur à l'éxécution d'une {{commande}} tapez :
                                        <p class="command">sudo {{commande}}</p>
                                </li>
                        </ul>
                </li>
        </ul>
</div>

<?php
include("hint.php");
include("templates/footer.php");
?>