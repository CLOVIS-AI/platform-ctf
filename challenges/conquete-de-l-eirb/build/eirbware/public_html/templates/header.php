<!DOCTYPE html>
<html lang="fr" dir="ltr">
<header>
  <nav class="navbar" onClick="toggleNavbar()">
    <img class="logo" src="<?php echo $page == 'tutoriels' ? '../' : ''?>assets/logo_small.svg">
    <ul class="navbar-nav">
      <li class="nav-item"><a class="nav-link <?php echo $page == 'index' ? 'selected' : ''?>" href="<?php echo $page == 'tutoriels' ? '../' : ''?>index.php"><img src="<?php echo $page == 'tutoriels' ? '../' : ''?>assets/navbar/home.svg"><span class="nav-link-text">Accueil</span></a></li>
      <li class="nav-item"><a class="nav-link <?php echo $page == 'location' ? 'selected' : ''?>" href="<?php echo $page == 'tutoriels' ? '../' : ''?>location.php"><img src="<?php echo $page == 'tutoriels' ? '../' : ''?>assets/navbar/location.svg"><span class="nav-link-text">Localisation</span></a></li>
      <li class="nav-item"><a class="nav-link <?php echo $page == 'tutoriels' ? 'selected' : ''?>" href="<?php echo $page == 'tutoriels' ? '../' : ''?>tutoriels/index.php"><img src="<?php echo $page == 'tutoriels' ? '../' : ''?>assets/navbar/tuto.svg"><span class="nav-link-text">Tutoriels</span></a></li>
    </ul>
    <div class="nav-toggle">
      <svg
        aria-hidden="true"
        focusable="false"
        data-prefix="fad"
        data-icon="angle-double-right"
        role="img"
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 448 512"
        class="svg-inline--fa fa-angle-double-right fa-w-14 fa-5x">
        <g class="fa-group">
          <path
            fill="currentColor"
            d="M224 273L88.37 409a23.78 23.78 0 0 1-33.8 0L32 386.36a23.94 23.94 0 0 1 0-33.89l96.13-96.37L32 159.73a23.94 23.94 0 0 1 0-33.89l22.44-22.79a23.78 23.78 0 0 1 33.8 0L223.88 239a23.94 23.94 0 0 1 .1 34z"
            class="fa-secondary"
          ></path>
          <path
            fill="currentColor"
            d="M415.89 273L280.34 409a23.77 23.77 0 0 1-33.79 0L224 386.26a23.94 23.94 0 0 1 0-33.89L320.11 256l-96-96.47a23.94 23.94 0 0 1 0-33.89l22.52-22.59a23.77 23.77 0 0 1 33.79 0L416 239a24 24 0 0 1-.11 34z"
            class="fa-primary"
          ></path>
        </g>
      </svg>
    </div>
  </nav>
</header>

<script>
let active = false;
function toggleNavbar() {
  let navbar = document.querySelector('.navbar');
  let navlink = document.querySelectorAll('.nav-link-text');
  let svg = document.querySelector('.nav-toggle svg');
  if (active) {
    navbar.style.height = "4rem";
    for (let i = 0; i < navlink.length; i++)
      navlink[i].style.display = "none";
    svg.style.transform = "rotate(270deg)";
    svg.style.filter = "grayscale(100%) opacity(0.7)";
  } else {
    navbar.style.height = "auto";
    for (let i = 0; i < navlink.length; i++)
      navlink[i].style.display = "inline";
    svg.style.transform = "rotate(90deg)";
    svg.style.filter = "grayscale(0%) opacity(1)";
  }
  active = !active;
}
</script>


<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <title>Eirbware</title>

    <!-- CSS -->
    <link rel="stylesheet" href="<?php echo $page == 'tutoriels' ? '../' : ''?>css/navbar.css">
    <link rel="stylesheet" href="<?php echo $page == 'tutoriels' ? '../' : ''?>css/style.css">
    <link rel="stylesheet" href="<?php echo $page == 'tutoriels' ? '../' : ''?>css/vitrine.css">

    <!-- FAV -->
    <link rel="icon" href="<?php echo $page == 'tutoriels' ? '../' : ''?>favicon.ico" sizes="16x16 24x24 32x32 48x48 64x64 128x128" type="image/vnd.microsoft.icon">
    <!-- <input id="button" class="button" type="image" src="images/arrow-up.svg" alt="Remonter" width="50"> -->
</head>

<!--<script src="includes/jquery.js"></script>

<script>
$(function(){
  $("#button").click(function(){
    $("html, body").animate({scrollTop: 0},"slow");
  });
});
</script>-->

<body ontouchstart="">
  <main>
    
