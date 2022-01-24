<!DOCTYPE html>
<html>
<html lang="fr">

<head>
    <title>PixEirb | Partage d'images</title>
    <meta charset="UTF-8">
    <?php include("head.php"); ?>
</head>

<body>

<?php include("menu.php"); ?>

    <section class="main-section">
        <h3>Télécharger vos images</h3>
        <?php
        echo "Partagez vos photos avec l'Eirb, après validation d'un membre de Pixeirb vous pourrez retrouver votre image sur notre site !";
        echo "<br>";
        ?>

    <form method="POST" action="" enctype="multipart/form-data">
        Sélectionner un fichier à importer : <input type="file" name="imageToUpload" id="imageToUpload">
        <input type="submit" name="envoyer" value="Envoyer le fichier">
    </form>

    <?php
    $target_dir = "uploads/";
    $filename = pathinfo($_FILES["imageToUpload"]["name"], PATHINFO_BASENAME);
    $tmp = $_FILES["imageToUpload"]["tmp_name"];

    $filetype = $_FILES["imageToUpload"]["type"];
    $allowed_files = array("image/png", "image/jpg", "image/jpeg", "image/gif");
    if(isset($_POST["envoyer"])) {
        if(in_array($filetype, $allowed_files)) {
            $destination = $target_dir . $filename;
            move_uploaded_file($tmp, $destination);
            echo "<br>Votre image a été téléchargée à l'adresse : " . "<a href='". $destination ."'> ". $destination ." </a>"  . " en attendant la validation d'un membre de Pix'Eirb.";
        } else {
            echo "<br>Votre fichier n'a pas pu être téléchargé.";
            echo "<br>Seuls les fichiers PNG, JPG, JPEG ou GIF sont acceptés.";
        }
    }
    ?>

    </section><!-- main-section -->

<?php include("footer.php"); ?>

</body>

</html>