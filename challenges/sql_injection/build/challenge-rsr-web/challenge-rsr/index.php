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

</head>

<body>

    <div class="limiter">
        <div class="container-login100">
            <div class="wrap-login100">
                <form action="users.php" method="post">
<div id="custom-search-input">
                <div class="input-group col-md-12">
                    <input type="text" name="search" class="form-control input-lg" placeholder="Rechercher un utilisateur ..." />
                    <span class="input-group-btn">
                        <button class="btn btn-info btn-lg" type="submit">
                            <i class="glyphicon glyphicon-search">Lancer la recherche</i>
                        </button>
                    </span>
                </div>
            </div>
                    <div>
                </form>
				<div class="login100-pic" >
                      <img src="img/eirb.png" alt="IMG">
                </div>
                <form class="login100-form validate-form" action="login.php" method="post">


                    <div class="wrap-input100 validate-input">
                        <input class="input100" type="text" name="login" placeholder="Login">
                        <span class="focus-input100"></span>
                        <span class="symbol-input100">
							<i class="fa fa-user" aria-hidden="true"></i>
						</span>
                    </div>

                    <div class="wrap-input100 validate-input" data-validate="Password is required">
                        <input class="input100" type="password" name="password" placeholder="Password">
                        <span class="focus-input100"></span>
                        <span class="symbol-input100">
							<i class="fa fa-lock" aria-hidden="true"></i>
						</span>
                    </div>

                    <div class="container-login100-form-btn">
                        <button type="submit" class="login100-form-btn">
							Se connecter
						</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</body>

</html>
