function updateDialogColor()
{
	let color = document.getElementById('exampleColorInput').value;
	document.getElementById('dialog').style.background = color;
};

function viewDialog(chat_id)
{
    window.location.replace('/chat/' + chat_id);
//  document.getElementById("dialogContent").style.display = "block";
};