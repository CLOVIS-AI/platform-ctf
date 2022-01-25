<?php 
  include("database.php"); 

  function ReadData()  
    {  
        try  
        {  
            $conn = OpenConnection();
            $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
	    $login = $_POST['search'];
            $sql = "SELECT login,description FROM users where login='" . $login . "';";
	    #$stmt = $conn->prepare('SELECT login,description FROM users WHERE login = :login');
	    #echo($_POST['search']);
            #echo($stmt);
 	    #$stmt->execute([ 'login' => $login ]);
	    $res = $conn->query($sql);
	    $nb_row = $res->rowCount();
            /* Récupère le nombre de lignes qui correspond à la requête SELECT */
            if ( $nb_row > 0) {
		if ( $nb_row == 1)
			echo($res->rowCount() . " résultat trouvé <br>");
		else
			echo($res->rowCount() . " résultats trouvés <br>");
                foreach ($res as $row) {
			if ($row['login'] == "Julien")
				echo ("Description indisponible");
			else if ($row['login'] == "")
				echo ("Login/password par défaut pour mon compte");
			else
                       		print "Login: " .  $row['login'] . "    Description: " .$row['description'] . "<br>";
                   }
                }
            /* Aucune ligne ne correspond -- faire quelque chose d'autre */
            else {
                echo("Aucune ligne ne correspond à la requête.<br><br>");
            }
        }  
        catch(PDOException $e)  
        {  
            echo("Error ReadData():" . $e);  
        }  
    }
?>

<!DOCTYPE html>
<html lang="fr">

<head>
    <title>Challenge Reverse shell docker</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!--===============================================================================================-->
    <link rel="icon" type="image/png" href="img/icons/favicon.ico" />
    <!--===============================================================================================-->
    <link rel="stylesheet" type="text/css" href="css/util.css">
    <link rel="stylesheet" type="text/css" href="css/main.css">
    <!--===============================================================================================-->
    <link rel="stylesheet" type="text/css" href="fonts/font-awesome-4.7.0/css/font-awesome.min.css">
    <!--===============================================================================================-->
</head>

<body>

    <div class="limiter">
        <div class="container-login100">
            <div class="wrap-result">
                <a class="bottom" href="index.php"> Retourner à l'accueil </a>
                <h1 > Résultats de la recherche "<?php echo($_POST['search']) ?>" </h1>
                <?php
                    ReadData();
                ?>
            </div>
        </div>
    </div>
</body>

</html>
