document.getElementById("messages").scrollTop = document.getElementById("messages").scrollHeight;

let input = document.querySelector("#message-input")
let btnSubmit = document.querySelector("#btn-submit")

const chatId = JSON.parse(document.getElementById('json-chat').textContent);
const profileId = JSON.parse(document.getElementById('json-profile').textContent);

userColors = JSON.parse(getCookie('userColors'));
if (userColors) {
    selectedColor = userColors.find(o => (o.chat === chatId && o.profile === profileId));
    if (selectedColor) {
        document.getElementById('exampleColorInput').value = selectedColor.color;
        document.getElementById('dialog').style.background = selectedColor.color;
    }
}

let wsStart = 'ws://';
if (window.location.protocol == 'https:') {
     wsStart = 'wss://'
}

const chatSocket = new WebSocket(
  wsStart
  + window.location.host
  + '/ws/'
  + chatId
  + '/'
);

chatSocket.onmessage = function(e) {

    const data = JSON.parse(e.data);
    let chat = document.querySelector("#chat")

    text = data.message.text
    date = data.message.date
    avatar = data.profile.avatar ? data.profile.avatar : 'https://i.pinimg.com/originals/cc/6c/07/cc6c07880dfd0c337c875b3cdc6821c8.png'

    if (data.profile.id == profileId) {
        //сообщение от меня
        chat.innerHTML +=
            '<div class="row mt-1 d-flex justify-content-start">' +
                 '<div class="col-3 d-flex justify-content-end">' +
                      '<div class="avatar rounded-pill d-inline-block align-text-top" style="width: 40px; height: 40px; background:url(\'' + avatar +'\'), no-repeat; background-size: cover;"></div>' +
                 '</div>' +
                 '<div class="col-4">' +
                    '<p class="text-justify my-message text-break" style="float: left">' +
                        text +
                        '<br><span class="text-muted" style="font-size: 12px;">' + date + '</span>' +
                    '</p>' +
                 '</div>' +
            '</div>';

    } else {
        //сообщение от друга
        chat.innerHTML +=
            '<div class="row mt-1 d-flex justify-content-end">' +
                '<div class="col-4">' +
                    '<p class="text-justify friend-message text-break" style="float: right">' +
                        text +
                        '<br><span class="text-muted" style="font-size: 12px;">' + date + '</span>' +
                    '</p>' +
                '</div>' +
                '<div class="col-3 d-flex justify-content-start">' +
                    '<div class="avatar rounded-pill d-inline-block align-text-top" style="width: 40px; height: 40px; background:url(\'' + avatar + '\'), no-repeat; background-size: cover;"></div>' +
                '</div>'+
            '</div>';

        new Audio('/static/audio/uvok.mp3').play()
    }


    document.getElementById("messages").scrollTop = document.getElementById("messages").scrollHeight;
};

chatSocket.onclose = function(e) {
  console.error('The socket closed unexpectedly');
};

btnSubmit.addEventListener("click", () => {
    message = input.value;
    chatSocket.send(JSON.stringify({
        'message': message,
        'profileId': profileId,
        'chatId': chatId
    }));
    input.value = '';
})

input.addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        message = input.value;
        chatSocket.send(JSON.stringify({
            'message': message,
            'profileId': profileId,
            'chatId': chatId
        }));
        input.value = '';
        document.getSelection().removeAllRanges();
    }
});