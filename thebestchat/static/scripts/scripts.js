function updateDialogColor()
{
	let color = document.getElementById('exampleColorInput').value;
	document.getElementById('dialog').style.background = color;
};

function viewDialog()
{
  document.getElementById("dialogContent").style.display = "block";
};