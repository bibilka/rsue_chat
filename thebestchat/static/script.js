let chat = document.querySelector("#chat")
let input = document.querySelector("#message-input")
let btnSubmit = document.querySelector("#btn-submit")

const webSocket = new WebSocket("ws://localhost:80/ws/chat/");

webSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    chat.innerHTML += '<div class="msg">' + data.message + '</div>'
};


btnSubmit.addEventListener("click", () => {
    message = input.value;
    webSocket.send(JSON.stringify({
        'message': message
    }));
    input.value = '';
})

