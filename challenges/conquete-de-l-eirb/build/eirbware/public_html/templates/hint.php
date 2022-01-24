<div id="hint" class="hint">Clique sur une flèche pour faire apparaitre le contenu d'une section!</div>
<script>
let AFK = true;
function afficher(num) {
  AFK = false;
  document.getElementById("hint").style.display = "none";
  let texte = document.getElementById('hide' + num);
  if (texte.style.display == "none" || texte.style.display == "") {
    texte.style.display = "inline";
    document.getElementById('arrow' + num).style.transform = "rotate(90deg)";
  } else {
    texte.style.display = "none";
    document.getElementById('arrow' + num).style.transform = "rotate(0deg)";
  }
}
function hint() {
  if (AFK) 
    document.getElementById("hint").style.display = "block";
}
setTimeout(hint, 3000);
</script>