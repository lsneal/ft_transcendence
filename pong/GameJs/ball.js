var ball = document.getElementById("ball");
var posX = 265; //horizontale
var posY = 500; //verticale
var hit = 0;
var PointJ1 = 0;
var PointJ2 = 0;
var i = 5;
var ballmoov;// front || up || down

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function game () {
	
	//var leftBox = document.getElementById("leftBox");	
	 
	while (hit != 1)
	{
		const rightBox = document.querySelector('#rightBox');
		const rightBoxStyleValue = getComputedStyle(rightBox);
		posX += 10;
		posX.toString()
		ball.style.left = posX + "px";
		if (parseInt(rightBoxStyleValue.left) - posX <= 50 && parseInt(rightBoxStyleValue.top) - posY >= -90 && parseInt(rightBoxStyleValue.top) - posY <= 30)
		{
			hit = 1;
			console.log(parseInt(rightBoxStyleValue.top) - posY);
			if (parseInt(rightBoxStyleValue.top) - posY == 0 || parseInt(rightBoxStyleValue.top) - posY == 30)
				ballmoov = "up";
			if (parseInt(rightBoxStyleValue.top) - posY == -30)
				ballmoov = "front";
			if (parseInt(rightBoxStyleValue.top) - posY == -60 || parseInt(rightBoxStyleValue.top) - posY == -90)
				ballmoov = "down";					
		}
		await sleep(i * 10);
	}
	console.log("end first loop");
	var goal = 0;
	while (goal != 1)
	{
		hit = 0;
		if (ballmoov == "up")
		{
			if (posX > 265)
			{
				console.log("bonjour");
				ballMoovToUpLeft(posX, posY);
				goal = 1;
				//mooov up to left
			}
			if (posX < 265)
			{
				// moov up to right
			}
		}
		if (ballmoov == "front")
		{
			if (posX > 265)
			{
				//mooov front to left
			}
			if (posX < 265)
			{
				// moov front to right
			}
		}
		if (ballmoov == "down")
		{
			if (posX > 265)
			{
				//down up to left
			}
			if (posX < 265)
			{
				//down up to right
			}
		}
	}
//	console.log("ball posx = ", posX, "poxY = ", posY);

}

async function ballMoovToUpLeft(posX, posY) {
	
	hit = 1;
	while (hit != 1)
	{
		
		posX -= 10;
		posX.toString();
		ball.style.left = posX + "px";
		
		posY -= 10;
		posY.toString();
		ball.style.top = posY + "px";
		await sleep(i * 10);
	}
}

game();
//while (hit != 1)
//{
//	hit = 1;
//}
