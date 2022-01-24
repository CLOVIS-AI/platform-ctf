<?php

// Stores the $FLAG
require __DIR__ . "/conf.php";

$SECRET_KEY = 'o9jXoZR1gHcxslBp9e0aKtAKvFk5IQxn42sTEb29';

$current_user = array(
    'username' => NULL,
    'is_admin' => false
);
$error = NULL;

// Display the source code
if(isset($_GET['showsourcecode'])){
    show_source(__FILE__);
    die();
}

// The user is logging out
if(isset($_GET['logout'])){
    if(isset($_COOKIE['type_juggling__user_info'])) {
        unset($_COOKIE['type_juggling__user_info']);
        setcookie('type_juggling__user_info', null, -1, '/');
    }
}

// The user is registering
if(isset($_POST['username'])){
    $username = $_POST['username'];
    $is_admin = false;
    $creation_date = date("d-m-Y h:i:s");

    $string_to_sign = $username . ($is_admin ? 'true' : 'false') . $creation_date;

    $hmac = hash_hmac('sha256', $string_to_sign, $SECRET_KEY);

    $info_user = array(
        'username' => $username,
        'is_admin' => $is_admin,
        'creation_date' => $creation_date,
        'hmac' => $hmac
    );

    // Set the cookie
    setcookie('type_juggling__user_info', base64_encode(json_encode($info_user)), time() + 1800);

    // Creates the cookie for the current session
    $_COOKIE['type_juggling__user_info'] = base64_encode(json_encode($info_user));
}


// The user is logged with a cookie
if(isset($_COOKIE['type_juggling__user_info'])){
    $info_user = json_decode(base64_decode($_COOKIE['type_juggling__user_info']), true);

    $string_to_sign = $info_user['username'] . ($info_user['is_admin'] ? 'true' : 'false') . $info_user['creation_date'];

    $hmac = hash_hmac('sha256', $string_to_sign, $SECRET_KEY);

    if($info_user['hmac'] == $hmac){
        $current_user['username'] = $info_user['username'];
        $current_user['is_admin'] = $info_user['is_admin'];
    }else{
        $error = 'Integrity check failed.';
    }
}
?>

<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Type Juggling Challenge</title>
  <link rel="stylesheet" href="style.css">
  <script src="script.js"></script>
</head>
<body>

    <?php if($error != NULL) { echo '<p style="color:red">' . $error . '</p>'; } ?>

    <?php if($current_user['username'] != NULL) { ?>

        <h2>Welcome <?php echo htmlentities($current_user['username']) ?></h2>
        You are successfully logged in!

        <br/><br/>

        <a href='index.php?logout'>Logout</a>

        <?php if($current_user['is_admin']) { ?>
            <br/><br/><h3>You are the administrator</h3>
            The flag is <b><?php echo $FLAG ?></b>
        <?php } else { ?>
            <br/><br/><h3>You are not the administrator</h3>
        <?php } ?>
    <?php } else { ?>

        <h2>Register as a new user</h2>
        <form action="index.php" method="post">
            <label for="username">Username : </label>
            <input type="text" id="username" name="username"><br>
            <input type="submit" value="Register">
        </form>

    <?php } ?>

    <br/><br/>
    <a href='index.php?showsourcecode'>Souce code for this page</a>
</body>
</html>
