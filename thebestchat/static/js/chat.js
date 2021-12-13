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
    if (data.profileId == profileId) {
        //сообщение от меня
        chat.innerHTML +=
            '<div class="row mt-1">' +
            '<div class="col-3">' +
            '<img src="https://i.pinimg.com/originals/cc/6c/07/cc6c07880dfd0c337c875b3cdc6821c8.png" class="rounded-circle img-fluid" alt="Аватар" height="30" width="30" style="float: right;">' +
            '</div><div class="col-5"><p class="text-justify my-message" style="float: left">' +
            data.message +
            '</p></div></div>'
    } else {
        //сообщение от друга
        chat.innerHTML +=
            '<div class="row mt-1 d-flex flex-row-reverse">' +
            '<div class="col-3">' +
            '<img src="https://i.pinimg.com/originals/cc/6c/07/cc6c07880dfd0c337c875b3cdc6821c8.png" class="rounded-circle img-fluid" alt="Аватар" height="30" width="30" style="float: left;">' +
            '</div><div class="col-5"><p class="text-justify friend-message" style="float: right">' +
            data.message +
            '</p></div></div>'
    }

document.getElementById("messages").scrollTop = document.body.scrollHeight;

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