function setCookie(name,value,days) {
    var expires = "";
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days*24*60*60*1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "")  + expires + "; path=/";
}
function getCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for(var i=0;i < ca.length;i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1,c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
    }
    return null;
}
function eraseCookie(name) {
    document.cookie = name +'=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;';
}

function updateDialogColor(chat_id, profile_id)
{
	let color = document.getElementById('exampleColorInput').value;
	document.getElementById('dialog').style.background = color;

	userColorsCookie = getCookie('userColors');
	if (!userColorsCookie) {
	    userColorsArray = []
	} else {
	    userColorsArray = JSON.parse(userColorsCookie)
	}

	existingColorSettings = userColorsArray.findIndex((obj => obj.chat == chat_id && obj.profile == profile_id));
	if (existingColorSettings !== -1) {
	    userColorsArray[existingColorSettings].color = color;
	} else {
	    userColorsArray.push({color: color, profile: profile_id, chat: chat_id})
	}

	setCookie('userColors',JSON.stringify(userColorsArray), 7);
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

/*  ==========================================
    SHOW UPLOADED IMAGE
* ========================================== */
function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            url = e.target.result
            $('#button-addon-avatar')
                .attr('style', 'background:url("'+url+'"), no-repeat; background-size: cover;');
        };
        reader.readAsDataURL(input.files[0]);
    }
}


//document.getElementById('night-mode').addEventListener('click', function()
//{
//    let a = document.getElementsByTagName('a');
//
//    console.log(a);
//    for (let i = 0; i < a.length; i++)
//    {
//        a[i].style.color = "white";
//    }
//});
