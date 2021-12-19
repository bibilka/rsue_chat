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

            '<div class="row mt-1">' +
            '<div class="col-3">' +
            '<div class="avatar rounded-pill d-inline-block align-text-top"style="width: 30px; height: 30px; background:url(' + avatar + '), no-repeat; background-size: cover;"></div>' +
            '</div><div class="col-5"><p class="text-justify text-break my-message" style="float: left">' +
            text +
            '</p><span>' + date + '</span></div></div>'

    } else {
        //сообщение от друга
        chat.innerHTML +=
            '<div class="row mt-1 d-flex flex-row-reverse">' +
            '<div class="col-3">' +
            '<div class="avatar rounded-pill d-inline-block align-text-top"style="width: 30px; height: 30px; background:url(' + avatar + '), no-repeat; background-size: cover;"></div>' +
            '</div><div class="col-5">' +
            '<p class="text-justify text-break friend-message" style="float: right">' +
            text +
            '</p><span>' + date + '</span></div></div>'
    new Audio('http://talantlev.ucoz.ru/uvok.mp3').play()
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