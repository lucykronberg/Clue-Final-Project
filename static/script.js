const suspects = ["Ms.Adams", "Tormey", "Ms.Barr", "Mr.Lotze", "Mr. Reussner", "Jose"];
const weapons = ["Wires", "Calculator", "Diet Dr Pepper", "Pencil", "Stapler", "Barbie"];
const rooms = ["Quad", "Gym", "Hallways", "Senior Lawn", "Library", "Cafeteria", "VADA building", "Theater"];

$(document).ready(function() {
	$("#guidedvid").click(function(){
		$(this).next().toggle();
	});

	$(".pageLinks").click(function(){
		$(this).next().toggle();
	});
	
	$("#buttonS").click(function() {
		$("#randomS").text(suspects[Math.floor(Math.random() * suspects.length)]);
		$("#buttonS").addClass("disabled");
	});
	$("#buttonW").click(function() {
		$("#randomW").text(weapons[Math.floor(Math.random() * weapons.length)]);
		$("#buttonW").addClass("disabled");
	});
	$("#buttonR").click(function() {
		$("#randomR").text(rooms[Math.floor(Math.random() * rooms.length)]);
		$("#buttonR").addClass("disabled");
	});


	
});