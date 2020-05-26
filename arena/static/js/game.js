// Support TLS-specific URLs, when appropriate.


if (window.location.protocol == "https:") {
  var ws_scheme = "wss://";
} else {
  var ws_scheme = "ws://"
};
  
var inbox = new ReconnectingWebSocket(ws_scheme + location.host + "/receive");
var outbox = new ReconnectingWebSocket(ws_scheme + location.host + "/submit");

var players = JSON.parse(figures)
var player = JSON.parse(figure)
var nextPlayer = null

window.onload = (event) => {
  //console.log('page is fully loaded');

  nextPlayer = players.shift()
  players.push(nextPlayer)

  var myBut = document.querySelector("#myButton")
  if (player[3] === nextPlayer[0]) {
    myBut.disabled = false
    myBut.textContent = "Punch"
  } else {
    myBut.disabled = true
    myBut.textContent = `${nextPlayer[0]}'s turn`
  }
};

inbox.onmessage = function(message) {
  my_data_promise = message.data.text()
  my_data_promise.then( value => {
    //console.log(JSON.parse(value))
    my_data = JSON.parse(value)
    //console.log(player)
    //console.log(players)
    nextPlayer = players.shift()
    players.push(nextPlayer)
    statusStr = `${my_data.result_message}`
    myBut = document.querySelector("#myButton")
    if (document.querySelector("#player1").textContent === nextPlayer[0]) {
      myBut.disabled = false
      myBut.textContent = "Punch"
    } else {
      myBut.disabled = true
      myBut.textContent = `${nextPlayer[0]}'s turn`
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
          players.pop()
        }
      } else {
        new_val = `Hits Remaining: ${digit}`
      }
      player_hits.textContent = new_val
    }
    document.querySelector("#status").textContent += my_data.result_message + "\n"
    document.getElementById("status").scrollTop = document.getElementById("status").scrollHeight
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
    "action": "punch",
    "attacker": attacker,
    "attackee": selection
  }
  outbox.send(JSON.stringify(punch));
});

