let chat = document.querySelector("#chat")
let input = document.querySelector("#message-input")
let btnSubmit = document.querySelector("#btn-submit")

const webSocket = new WebSocket("ws://localhost:80/ws/chat/");

webSocket.onmessage = function(e) {
    console.log(e)

    const data = JSON.parse(e.data);
    console.log(data)

//сообщение от меня
    chat.innerHTML +=
        '<div class="row mt-1">' +
        '<div class="col-3">' +
        '<img src="https://i.pinimg.com/originals/cc/6c/07/cc6c07880dfd0c337c875b3cdc6821c8.png" class="rounded-circle img-fluid" alt="Аватар" height="30" width="30" style="float: right;">' +
        '</div><div class="col-5"><p class="text-justify my-message" style="float: left">' +
        data.message +
        '</p></div></div>'


//сообщение от друга
    chat.innerHTML +=
        '<div class="row mt-1 d-flex flex-row-reverse">' +
        '<div class="col-3">' +
        '<img src="https://i.pinimg.com/originals/cc/6c/07/cc6c07880dfd0c337c875b3cdc6821c8.png" class="rounded-circle img-fluid" alt="Аватар" height="30" width="30" style="float: left;">' +
        '</div><div class="col-5"><p class="text-justify friend-message" style="float: right">' +
        data.message +
        '</p></div></div>'

  document.getElementById("messages").scrollTop = document.body.scrollHeight;

};


btnSubmit.addEventListener("click", () => {
    message = input.value;
    webSocket.send(JSON.stringify({
        'message': message
    }));
    input.value = '';
})

function updateDialogColor()
{
	let color = document.getElementById('exampleColorInput').value;
	document.getElementById('dialog').style.background = color;
};

function viewDialog()
{
  document.getElementById("dialogContent").style.display = "block";
};