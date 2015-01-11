$(function(){
    var lastchoice = '';
    $("#dropdownMenu1 li").click(function() {
	if (lastchoice != ''){
	    var id = "#hiddenmenu-" + lastchoice;
	    $(id).addClass("hidden");
	}
	var n = $(this).text();
	var id = "#hiddenmenu-" + n;
	$("input[name='numSquares']").val(n);
	$(id).removeClass("hidden");
	lastchoice = n;
    });

    $("#dropdownMenu2 li").click(function() {
	var n = $(this).text();
	$("input[name='numSolutions']").val(n);
    });


    console.log($("#dropdownMenu1"))
});

		  


