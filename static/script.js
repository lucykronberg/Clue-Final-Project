const suspects = ["Col. Mustard", "Miss Scarlett", "Mrs. White", "Prof. Plum", "Mrs. Peacock", "Mr. Green"];
const weapons = ["Rope", "Revolver", "Dagger", "Candlestick", "Wrench", "Lead Pipe"];
const rooms = ["Lounge", "Hall", "Conservatory", "Study", "Library", "Billiard Room", "Kitchen", "Ballroom", "Dining Room"];

$(document).ready(function() {
	$("#guidedvid").click(function(){
		$(this).next().toggle();
	});

	$(".pageLinks").click(function(){
		$(this).next().toggle();
	});
	
	$("#buttonS").click(function() {
		$("#randomS").text(suspects[Math.floor(Math.random() * suspects.length)]);
	});
	$("#buttonW").click(function() {
		$("#randomW").text(weapons[Math.floor(Math.random() * weapons.length)]);
	});
	$("#buttonR").click(function() {
		$("#randomR").text(rooms[Math.floor(Math.random() * rooms.length)]);
	});


	
});