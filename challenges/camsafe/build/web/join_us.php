<html>

<head>
    <title>CamSafe</title>
    <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Inconsolata">
    <link rel="stylesheet" href="./header.css">
</head>

<body>
    <?php include "./header.html" ?>
    <div class="w3-container" id="join_us">
        <div class="w3-content" style="max-width:700px">
            <h2 class="w3-center w3-padding-16"><span class="w3-tag w3-wide">Join us</span></h2>
            <p class="w3-center">If you want to join us, please upload your CV here.</p>
            <form class="center" enctype="multipart/form-data" action="fileupload.php" method="post">
                <input type="file" name="file" id="file" />
		        <label for="file">Choose a file</label>
		        <span id="filename" style="margin-bottom: 10px; text-align: center"></span>
                <input type="submit" value="Send"/>
            </form>
        </div>
    </div>
    <script>
    	let input = document.querySelector('input');
    	input.addEventListener('change', (event) => {
    	    console.log(event);
    		let fileNames = "";
    		for (let i = 0; i < event.srcElement.files.length; i++)
    		    fileNames += event.srcElement.files[i].name + ", ";
    		document.getElementById('filename').textContent = fileNames.slice(0, -2);  
    	})
    </script>
</body>

</html>
