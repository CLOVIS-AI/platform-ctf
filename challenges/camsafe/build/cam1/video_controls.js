window.onload = function() {
	var video = document.getElementById("video");
	var playButton = document.getElementById("play");
	var pauseButton = document.getElementById("pause");
	var stopButton = document.getElementById("stop");

	playButton.addEventListener("click", function() {
		if (video.paused === true) {
			video.play();
		}
		document.getElementById("shutdown").style.display = "none"
		document.getElementById("video").style.display = ""
	});

	pauseButton.addEventListener("click", function() {
		if (video.paused === false) {
			video.pause();
		}
	});

	stopButton.addEventListener("click", function() {
		if (video.paused === false) {
			video.pause();
		}
		document.getElementById("shutdown").style.display = ""
		document.getElementById("video").style.display = "none"
	});
}
