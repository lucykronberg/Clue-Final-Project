
const suspects = ["Ms.Adams", "Tormey", "Ms.Barr", "Mr.Lotze", "Mr. Reussner", "Jose"];
const weapons = ["Wires", "Calculator", "Diet Dr Pepper", "Pencil", "Stapler", "Barbie"];
const rooms = ["Quad", "Gym", "Hallways", "Senior Lawn", "Library", "Cafeteria", "VADA building", "Theater"];

$(document).ready(function() {
	$("#waltergeist").hide();
	$(".imagetoggler").click(function(){
		$("#waltergeist").toggle();
	});
	 
	$("#randomS").hide();
	$("#randomR").hide();
	$("#randomW").hide();

	$(".pageLinks").click(function(){
		$(this).next().toggle();
	});
	
	$("#buttonS").click(function() {
		$("#randomS").show();
		$("#buttonS").addClass("disabled");
	});
	$("#buttonR").click(function() {
		$("#randomR").show();
		$("#buttonR").addClass("disabled");
	});
	$("#buttonW").click(function() {
		$("#randomW").show();
		$("#buttonW").addClass("disabled");
	});
	$("#imagetoggler").click(function(){
		$("#waltergeist").toggle();
	});
});