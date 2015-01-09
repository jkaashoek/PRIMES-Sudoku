$( document ).ready(function(){
var seconds = 0; // uptime in seconds
var timer = setInterval(
    function() {
        seconds++;
	$( "#timer" ).text(seconds+ " seconds");
    }, 1000
);
});
