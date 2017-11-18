// old, sad code from old sad webcam.lekvam.no
//
var api = "https://webcam.lekvam.no/"

$(document).ready(function(){ 
   $('#loadingbar').hide();
   getLog();
   $( "#x-slider" ).slider({
      min: 1,
      max: 100,
      value: 50
   });
   $( "#y-slider" ).slider({
      orientation: "vertical",
      min: 1,
      max: 100,
      value: 50
   });
   $("#take-picture").click(function () {
      $('#take-picture').prop('disabled', true);
      $('#loadingbar').show();
      picture();
      $('#take-picture').prop('disabled', false);
   })
   $("#redesign").click(function () {
      redesign();
   })
});


function loadLatestPics() {
	$.ajax({
	   url: api + "api.php?get=latestpics",
	   type:'get',
	   success: function(data){
	       $('#container').html("<div id='inner'>" + data + "</div>");
		$(".votable").click(function() {
		   vote($(this).attr('id'));
		   loadLatestPics();
		})
	   }
	})
}

function picture() {
	var x = $( "#x-slider" ).slider( "value" )
	var y = $( "#y-slider" ).slider( "value" )
	$.ajax({
	   url: api + "api.php",
	   type:'GET',
	   data: "get=picture&x=" + x + "&y=" + y,
	   success: function(newphoto){
	       $('#latest').html(newphoto);
   	       $('#loadingbar').hide();
	       getLog();
	   }
	})
}

function getLog() {
	$.ajax({
	   url: api + "api.php",
	   type:'GET',
	   data: "get=log",
	   success: function(log){
	       $('#log').html(log);
	   }
	})
}

function redesign() {
	var safeColors = ['00','33','66','99','cc','ff'];
	var rand = function() {
	    return Math.floor(Math.random()*6);
	};
	var randomColor = function() {
	    var r = safeColors[rand()];
	    var g = safeColors[rand()];
	    var b = safeColors[rand()];
	    return "#"+r+g+b;
	};
	$("body").css('background',randomColor());
	$("#buttons").css('border-radius', '15px');

}


