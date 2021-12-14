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

document.getElementById('settings-link').addEventListener('click', function()
{
  document.getElementById('main-sector-chats').style.display = "none";
  document.getElementById('main-sector-settings').style.display = "block";
});

document.getElementById('friends-link').addEventListener('click', function()
{
  document.getElementById('main-sector-chats').style.display = "none";
  document.getElementById('main-sector-friends').style.display = "block";
});

document.getElementById('arrow-back-settings').addEventListener('click', function()
{
  document.getElementById('main-sector-chats').style.display = "block";
  document.getElementById('main-sector-settings').style.display = "none";
});

document.getElementById('arrow-back-friends').addEventListener('click', function()
{
  document.getElementById('main-sector-chats').style.display = "block";
  document.getElementById('main-sector-friends').style.display = "none";
});

document.getElementById('profile-avatar').addEventListener('click', function()
{
    let input = document.getElementById('input-profile-avatar');
    input.click();
});