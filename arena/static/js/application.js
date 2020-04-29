// Support TLS-specific URLs, when appropriate.

if (window.location.protocol == "https:") {
  var ws_scheme = "wss://";
} else {
  var ws_scheme = "ws://"
};
  
var inbox = new ReconnectingWebSocket(ws_scheme + location.host + "/receive");
var outbox = new ReconnectingWebSocket(ws_scheme + location.host + "/submit");

inbox.onmessage = function(message) {
  my_data_promise = message.data.text()
  my_data_promise.then( value => {
    console.log(JSON.parse(value))
    my_data = JSON.parse(value)
    statusStr = `<br>${my_data.attacker} fake attacks ${my_data.attackee}`
    var box = document.querySelector("#chat-text")
    box.textContent += statusStr
  })
};

inbox.onclose = function(){
    console.log('inbox closed');
    this.inbox = new WebSocket(inbox.url);
};

outbox.onclose = function(){
    console.log('outbox closed');
    this.outbox = new WebSocket(outbox.url);
};

document.querySelector("#input-form").addEventListener("submit", (event) => {
  event.preventDefault();
  var attacker = document.querySelector("#player1").textContent;
  var selection  = document.querySelector("#opponent").value;
  console.log(attacker, selection)
  punch = {
    "attacker": attacker,
    "attackee": selection
  }
  outbox.send(JSON.stringify(punch));
});

