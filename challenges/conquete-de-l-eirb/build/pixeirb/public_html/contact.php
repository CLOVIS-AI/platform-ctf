<!DOCTYPE HTML>
<html lang="en">
<head>
    <title>PixEirb | Contact</title>
    <?php include("head.php");

    $status_message = '';

    if (isset($_POST['submit'])) {
        $status_message = '
<div class="alert alert-success alert-dismissible fade show" role="alert">
  Votre mail a bien été envoyé !
  <button type="button" class="close" data-dismiss="alert" aria-label="Close">
    <span aria-hidden="true">&times;</span>
  </button>
</div>';
    }
    ?>

</head>
<body>
<?php include("menu.php"); ?>
<div class="content">
    <div class="contact-text">
        <h4>Que vous soyez un professionnel ou un particulier, que vous souhaitiez obtenir des informations ou que vous
            souhaitiez collaborer avec nous, n'hésitez pas à nous envoyer un message.</h4>
    </div>
    <?php echo $status_message; ?>
    <div class="mid-section">
        <form id="contact-form" action="" method="post">
            <div class="form-section">
                <label for="email">Votre adresse mail </label><br>
                <input class="form-control form-control-sm full-size-input" type="email" name="email" id="email"
                       required>
            </div>
            <div class="form-section">
                <label for="object">Objet </label><br>
                <input class="form-control form-control-sm full-size-input" type="text" name="object" id="object"
                       required>
            </div>
            <div class="form-section">
                <label for="message">Votre message </label><br>
                <textarea class="form-control form-control-sm full-size-input" name="message" id="message" cols="40"
                          rows="8" required></textarea>
            </div>
            <div class="form-section">
                <input type="submit" name="submit" value="Envoyer" class="btn btn-danger btn-sm form-button">
            </div>
        </form>
    </div>

    <div class="mid-section">
        <iframe src="https://www.google.com/maps/embed?pb=!1m14!1m8!1m3!1d11322.9304582694!2d-0.6051667!3d44.8066376!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0xec840415731df92e!2sEnseirb%20-%20Matmeca!5e0!3m2!1sfr!2sfr!4v1566918647561!5m2!1sfr!2sfr"
                frameborder="0" style="border:0;" allowfullscreen=""></iframe>
    </div>

</div>
<?php include("footer.php"); ?>
</body>
</html>