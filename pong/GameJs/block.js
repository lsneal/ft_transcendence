var numRight = 500;
var numLeft = 500;
window.onkeydown = checkKey;

function checkKey(e)
{	
	var leftBox = document.getElementById("leftBox");	
	var rightBox = document.getElementById("rightBox");
	if (e.key == 'w')
	{
		numLeft -= 30;
		numLeft.toString();

		leftBox.style.top = numLeft + "px";
	}
	if (e.key == 's')
	{
		numLeft += 30; 
		numLeft.toString();
		
		leftBox.style.top = numLeft + "px";
	}
	if (e.keyCode == '38')
	{
		numRight -= 30;
		numRight.toString();

		rightBox.style.top = numRight + "px";
	}
	else if (e.keyCode == '40') 
	{
		numRight += 30; 
		numRight.toString();
		
		rightBox.style.top = numRight + "px";
	}
}