// Support TLS-specific URLs, when appropriate.


if (window.location.protocol == "https:") {
  var ws_scheme = "wss://";
} else {
  var ws_scheme = "ws://"
};
  
var inbox = new ReconnectingWebSocket(ws_scheme + location.host + "/receive");
var outbox = new ReconnectingWebSocket(ws_scheme + location.host + "/submit");
var turn = true

inbox.onmessage = function(message) {
  my_data_promise = message.data.text()
  my_data_promise.then( value => {
    console.log(JSON.parse(value))
    my_data = JSON.parse(value)
    statusStr = `${my_data.result_message}`
    myBut = document.querySelector("#myButton")
    if (document.querySelector("#player1").textContent === my_data.attacker) {
      myBut.disabled = true
      myBut.textContent = `${my_data.attackee}'s turn`
    }
    if (document.querySelector("#player1").textContent === my_data.attackee) {
      myBut.disabled = false
      myBut.textContent = "Punch"
    }
    if (parseInt(my_data.damage) !== 0) {
      player_hits = document.querySelector("#" + my_data.attackee + "_hits")
      if (player_hits === null) {
        player_hits = document.querySelector("#player1_hits")
      }
      player_stat = player_hits.textContent
      digit = parseInt(player_stat.match(/: \d+/g)[0].split(' ')[1]);
      digit -= my_data.damage
      if ( digit <= 0){
        new_val = "DEAD"
        if (document.querySelector("#player1").textContent === my_data.attackee) {
          myBut.disabled = true
        }
      } else {
        new_val = `Hits Remaining: ${digit}`
      }
      player_hits.textContent = new_val
    }
    //$("#chat-text").append("<div class='panel panel-default'><div class='panel-heading'>" + $('<span/>').text(my_data.attacker + " Attacks" + my_data.attackee).html() + "</div><div class='panel-body'>" + $('<span/>').text(my_data.result_message).html() + "</div></div>");
    document.querySelector("#status").textContent += my_data.result_message + "\n"
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
  punch = {
    "attacker": attacker,
    "attackee": selection
  }
  outbox.send(JSON.stringify(punch));
});

