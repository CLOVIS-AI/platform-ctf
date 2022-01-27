<?php
$page = basename($_SERVER['SCRIPT_NAME']);

function genMenuLink($pageName, $redirPage = null, $extraClasses = null)
{
    global $page;
    if ($page == $pageName) {
        echo 'href="#" class="active' . (is_null($extraClasses) ? '"' : ' ' . $extraClasses . '"');
    } else {
        echo 'href="' . (is_null($redirPage) ? $pageName : $redirPage) . '"'
            . (is_null($extraClasses) ? '' : 'class="' . $extraClasses . '"');
    }
}

?>

<header>
    <a <?php genMenuLink('index.php', '/', "logo"); ?>><img src="images/logo-black.png" alt="Logo"></a>
    <a class="menu-nav-icon" data-menu="#main-menu">
        <ion-icon name="menu"></ion-icon>
    </a>
    <ul class="main-menu" id="main-menu">
        <li><a <?php genMenuLink('index.php', '/'); ?>>Accueil</a></li>
        <li class="drop-down">
            <a href="#!" <?php if (in_array($page, array('public-gallery.php', 'private-gallery.php', 'album.php'))) echo 'class="active"'; ?>>Albums
                <ion-icon name="arrow-dropdown"></ion-icon>
            </a>
            <ul class="drop-down-menu drop-down-inner">
                <li><a <?php genMenuLink('album.php'); ?>>Albums par Pixeirb</a></li>
            </ul>
        </li>
        <li><a <?php genMenuLink('about.php'); ?>>À propos</a></li>
        <li><a <?php genMenuLink('contact.php'); ?>>Contact</a></li>
    </ul>
</header>