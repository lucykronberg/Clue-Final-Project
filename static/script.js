const suspects = ["Ms.Adams", "Tormey", "Ms.Barr", "Mr.Lotze", "Mr. Reussner", "Jose"];
const rooms = ["Quad", "Gym", "Hallways", "Senior Lawn", "Library", "Cafeteria", "VADA building", "Theater"];
const weapons = ["Wires", "Calculator", "Ruler", "Pencil", "Stapler", "Barbie"];

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
	$("#buttonR").click(function() {
		$("#randomR").text(rooms[Math.floor(Math.random() * rooms.length)]);
		$("#buttonR").addClass("disabled");
	});
	$("#buttonW").click(function() {
		$("#randomW").text(weapons[Math.floor(Math.random() * weapons.length)]);
		$("#buttonW").addClass("disabled");
	});
});