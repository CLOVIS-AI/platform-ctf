<html lang="en">

<head>
    <title>CamSafe</title>
    <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Inconsolata">
    <link rel="stylesheet" href="https://www.w3schools.com/lib/w3-theme-black.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
</head>

<body>

<div class="w3-row w3-center w3-theme-l1" style="height: 100%;">
  <button class="w3-col m1 w3-dark-grey w3-hover-grey" 
          style="height: 90%; display: flex; align-items: center; justify-content: center;"
          id="button-left"><i class="w3-jumbo fa fa-chevron-left"></i></button>
  <div class="w3-col m10">
    <iframe src="load.php" class="frame" style="height: 100%; width: 100%; border: none" id="iframe"></iframe>
  </div>
  <button class="w3-col m1 w3-dark-grey w3-hover-grey" style="height: 90%; display: flex; align-items: center; justify-content: center;" id="button-right"><i class="w3-jumbo fa fa-chevron-right"></i></button>
</div>
<div style="text-align: center">
<?php
    echo file_get_contents('flag.txt');
?>
</div>
</body>
<script>
	let id_camera = 0 ;
	document.getElementById("button-left").addEventListener("click", () => {
		id_camera--;
		if (id_camera < 0)
			id_camera = 2;
		document.getElementById("iframe").src = "load.php?id=" + id_camera;
		console.log(document.getElementById("iframe").src)
	})
	document.getElementById("button-right").addEventListener("click", () => {
		id_camera++;
		id_camera = id_camera % 3;
		document.getElementById("iframe").src = "load.php?id=" + id_camera;
		console.log(document.getElementById("iframe").src)
	})
</script>

</html>
