<html lang="en">
<head>
<meta charset="utf-8"/>
    <title>CamSafe</title>
    <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Inconsolata">
    <link rel="stylesheet" href="https://www.w3schools.com/lib/w3-theme-black.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
</head>

<style>
    .icon-button:hover {
        color: gray;
    }
</style>
<body>
    <div class="w3-center w3-theme-l1" style="height: 100%;">
        <div style="height: 90%;">
            <div id="shutdown" style="height: 100%; width: 95%; margin-left: 2.5%; background-color: black; display: none;"></div>
            <video id="video" title="Wildlife" preload="auto" style="height: 100%;" autoplay muted loop>
                <?php
                $ip = file_get_contents('/ip');
                $port = file_get_contents('/port');
                if ($_SERVER['PHP_AUTH_USER'] === 'admin')
                    echo '<source src="http://camsafe:CamSafeM@ster@' . $ip . ':' . $port . '/Cam2/saved/record.webm" type="video/webm">';
                else
                    echo '<source src="http://camsafe:CamSafeM@ster@' . $ip . ':' . $port . '/Cam2/record.webm" type="video/webm">';
                ?>
            </video>
        </div>
        <div style="height: 10%; display: flex; align-items: center; justify-content: center;">
            <button id="play" class="w3-theme-l1 w3-border-0 w3-text-white" style="cursor: pointer;"><i
                class="w3-padding-small w3-xxlarge fa fa-play icon-button"></i></button>
            <button id="pause" class="w3-theme-l1 w3-border-0 w3-text-white" style="cursor: pointer;"><i
                class="w3-padding-small w3-xxlarge fa fa-pause icon-button"></i></button>
            <button id="stop" class="w3-theme-l1 w3-border-0 w3-text-white" style="cursor: pointer;"><i
                class="w3-padding-small w3-xxlarge fa fa-stop icon-button"></i></button>
        </div>
    </div>
</body>
<?php
echo '<script src="http://camsafe:CamSafeM@ster@' . $ip . ':' . $port . '/Cam2/video_controls.js"></script>'
?>

</html>
