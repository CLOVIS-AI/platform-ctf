<?php 
  include("database.php");

  function ReadData()  
    {  
        try  
        {  
            $conn = OpenConnection();
            $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
            $sql = "SELECT login,password,description FROM users where login='". $_POST['login']. "' and password='" . md5($_POST['password']) ."';";
            $res = $conn->query($sql);
            if ($res->rowCount() == 0){
              header('Location: /index.php');
            }         
            else {
              foreach ($res as $row) {
                echo("<h1>Coucou " . $row['login'] ." !</h1> <br>");
                echo("<p>" . $row['description'] . "<p>");
              }
            }
        }  
        catch(Exception $e)  
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
    <link rel="icon" type="image/png" href="images/icons/favicon.ico" />
    <!--===============================================================================================-->
    <link rel="stylesheet" type="text/css" href="fonts/font-awesome-4.7.0/css/font-awesome.min.css">
    <link rel="stylesheet" type="text/css" href="css/util.css">
    <link rel="stylesheet" type="text/css" href="css/main.css">
    <!--===============================================================================================-->
</head>

<body>

    <div class="limiter">
        <div class="container-login100">
            <div class="wrap-result">
		<a href="index.php"> Retourner à l'accueil </a>
                <?php
                    ReadData();
                ?>
                <br>
                
            </div>
        </div>
    </div>
</body>

</html>
