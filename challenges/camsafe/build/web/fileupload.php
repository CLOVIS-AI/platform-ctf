<html>

<head>
    <meta charset="utf-8">
</head>

<body>
    <?php
    $nomOrigine = $_FILES['file']['name'];
    $elementsChemin = pathinfo($nomOrigine);
    $extensionFichier = $elementsChemin['extension'];
    $allowedType = array("application/pdf", "image/jpeg", "image/png");
    if (!in_array($_FILES['file']["type"], $allowedType)) {
        echo "Le fichier n'a pas l'extension attendue";
    } else {
        $repertoireDestination = dirname(__FILE__) . "/uploads/";
        $nomDestination = "CV_" . date("YmdHis") . "." . $extensionFichier;

        if (move_uploaded_file($_FILES["file"]["tmp_name"], $repertoireDestination . $nomDestination))
            echo "File uploaded to ./uploads/" . $nomDestination;
        else 
            echo "Error uploading file";
    }
    ?>
</body>

</html>
