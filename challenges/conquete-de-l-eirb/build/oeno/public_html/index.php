<!DOCTYPE html>

<html>

<head>
    <meta charset="utf-8" />
    <link rel="stylesheet" href="style.css" />
    <title>Club Oeno - Enseirb MATMECA</title>
</head>

<body>
    <div id="bloc_page">
        <header>
            <div id="titre_principal">
                <div id="logo">
                    <img src="images/logofinal.png" alt="Logo du Club" />
                    <h1>Club Oeno</h1>
                </div>
                <h2>Enseirb Matmeca</h2>
            </div>

            <nav>
                <ul>
                    <li><a href='index.php?page=accueil.php'>
                            Accueil

                        </a></li>
                    <li><a href='index.php?page=team.php'>
                            Historique

                        </a></li>
                    <li>
                        <a href='index.php?page=photo.php'>
                            Photos
                        </a>
                    </li>
                </ul>
            </nav>
        </header>

        <div id="banniere_image">
            <div>
                <img src="images/photogroupe2.jpg" id="banner">

            </div>
        </div>

        <?php

        ini_set('display_errors', 1);
        ini_set('display_startup_errors', 1);
        error_reporting(E_ALL);

        if (isset($_GET['page'])) {
            include($_GET['page']);
        } else {
            include("accueil.php");
        }

        ?>

        <footer>

            <div id="contact">
                <h1>Contact</h1>
                <p>Facebook <a href="http://www.facebook.com" target="_blank"><img src="images/facebook.png" alt="facebook" /></a></p>
                <p>Telegram <a href="tg://join?invite=AAAAAFd7GeS1Jub29dowSQ"><img src="images/telegram.png" alt="telegram" /></p>
            </div>

            <div id="rights">
                    <p>Tout droits réservés</p>
                    <p>
                        Avec l'accord du club, le site a été modifié par @Kobh4x, @LePlanCity et @Erak.
                    </p>
            </div>

        </footer>
    </div>
</body>

</html>