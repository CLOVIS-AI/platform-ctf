<?php 
if (!array_key_exists('id', $_GET))
    $_GET['id'] = 0;
    
$auth = base64_encode("camsafe:CamSafeM@ster");
$context = stream_context_create([
    "http" => [
        "header" => "Authorization: Basic $auth"
    ]
]);
$ip = file_get_contents('/ip');
$port = file_get_contents('/port');
echo file_get_contents("http://. $ip . ':' . $port ./Cam" . $_GET["id"], false, $context);
?>
