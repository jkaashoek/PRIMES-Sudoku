console.log("Here")
var seconds = 0; // uptime in seconds
var timer = setInterval(
    function() {
        seconds++;
	console.log("x")
	document.getElmentById("timer").innerHTML=seconds+ " seconds";
    }, 1000
);
