const suspects = ["adams", "tormey", "barr", "lotze", "reussner", "jose"];
const weapons = ["Wires", "Calculator", "Diet Dr Pepper", "Pencil", "Stapler", "Barbie"];
const rooms = ["Quad", "Gym", "Hallways", "Senior Lawn", "Library", "Cafeteria", "VADA building", "Theater"];

const rherrings = ["I couldn’t see anything! The lights went out… and the next thing I know Mr. Al is dead!", "I’m not sure of anything anymore. Except for one thing, you can’t trust anyone around this school.", "I don’t know! One minute Mr. Al was here next to us… and the next he’s gone!", "This kind of publicity is going to ruin the school!", "I don’t what happened! All I do know is… I’m going to have to find a job at SM now. Bleh.", "The lights must’ve gone out because of the nearby fire. Poor Mr. Al."]
const mBarr = ["I only got a quick glimpse of the murderer, but they were wearing a red collared shirt", "The murderer looked tall, and blonde I think? I can’t really remember it all happened so fast.", "The murderer wore blue…and I swore I heard murmurs of hate for war?", "I could only see a dark silhouette, but i know for sure the murderer had long hair tied in the back and wore boots.", "The murderer wore green, I’m sure of it. Weirdly also, I swore they had some dirt on them. Like actual dirt."]
const mAdams = ["I thought I heard someone running just outside of the classrooms.", "I saw some shifty stuff going on in the quad, but it might have just been some afterschool band kids.", "The murder occurred someplace very dark…in the rooms with no windows.", "I couldn’t anything. Wherever Mr. Al was murdered, it must’ve been quiet.", "I was away from Mr. Al when it all happened. But I swear I heard his screams echo near the stadium.", "I found a trail of dirt all around the high school. Someone must’ve gone through the gardens…", "I heard something loud coming from the cafeteria. Better go check it out.", "I could’ve sworn I saw grass stains on Mr. Al’s blazer when we found him…", "I heard I commotion in the theater right before the lights went out."]
const mReussner = ["Did you hear that noise out in the hallways, or was that just me?", "I definitely heard something going on outside. I might need Murphy for some moral support…", "I swore I saw Mr. Stewart running for help. Something must’ve happened around him…", "Hold on, I need to use my think time…Mr. Al had talked about wanting to visit Mrs. Bryans earlier. I pretty sure.", "I heard a scream from the gym…I didn’t think there was a home game today?", "Why is it always VADA involved in murder mysteries? The prom a couple years ago, and now this!", "I didn’t think the school food was THAT bad…", "I can’t believe someone would fall asleep on the senior lawn? Someone must’ve been up way past their bedtime...", "Mr. Al was always in the spotlight, but I didn’t think he would die in it. This is not a boo yeah moment."]
const Jose = ["The only thing that’s REALLY being murdered right now is the climate. Although I think I did see something going on inside the school earlier.", "I thought I saw something in the quad… or someone. Darwin, my beloved, is that you?", "We need to spend more time in nature and less around technology…Mr.Al sort of proves my point.", "Are the dons winning? Who’s playing in the gym today?…oh.", "Do crime scenes count as art?", "I knew there were too many GMOs in today’s meals!", "At least a body’s nutrients will be good for soil? *cries*", "It’s a dramatic way to go, for sure. I’m sorry I can’t really talk right now."]
const Tormey = ["I heard clicking sounds before a scream. Clacking ones too if you will.", "I’m so mad. First someone steals my Aztec death whistle now my Barbie. I was going to auction it!", "I heard a pop and maybe a fizz? Riiiight before the screaming started…", "You should be taking down notes.", "Now my plays can’t be held together!", "Is this why I had trouble turning on the TV to show my slides today?"]
const Lotze = ["I swear students are always stealing my calculators.", "This murderer has taste!", "I’m pretty sure that’s in unit 4 of physics? We didn’t get to that though because of the block schedule.", "I found a sample of the  murder weapon, which was made of polyvinyl chloride, or PVC. Total feta.", "The murder weapon looked like a gun, but none of us were given anything like that…were we?", "It’s not LEAD it’s GRAPHITE people."]

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