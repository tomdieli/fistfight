// Support TLS-specific URLs, when appropriate.
if (window.location.protocol == "https:") {
  var ws_scheme = "wss://";
} else {
  var ws_scheme = "ws://"
};

var players = JSON.parse(figures)
var player = JSON.parse(figure)
var nextPlayer = null

var inbox = new ReconnectingWebSocket(ws_scheme + location.host + "/game" + game_id + "/receive");
var outbox = new ReconnectingWebSocket(ws_scheme + location.host  + "/game" + game_id + "/submit");

const getNextPlayer = function() {
  nextPlayer = players.shift()
  players.push(nextPlayer)
  var punchButton = document.querySelector("#punch_button")
  if( players.length === 1 ){
    punchButton.disabled = true
    punchButton.textContent = `${nextPlayer.figure_name} wins!!!`
    return null
  } 
  else if(player.id === nextPlayer.id) {
    punchButton.disabled = false
    punchButton.textContent = "Punch"
  }
  else {
    punchButton.disabled = true
    punchButton.textContent = `${nextPlayer.figure_name}'s turn`
  }
}

window.onload = function() {
  getNextPlayer()
};

inbox.onmessage = function(message) {
  my_data_promise = message.data.text()
  my_data_promise.then( value => {
    my_data = JSON.parse(value)
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
        for(i=0; i < players.length; ++i){
          if(players[i]['figure_name'] === my_data.attackee){
            players.splice(i, 1)
          }
        }
        var selectobject = document.getElementById("opponent");
        for (var i=0; i<selectobject.length; i++) {
          if (selectobject.options[i].value === my_data.attackee) {
            selectobject.remove(i);
          }
        }
      } else {
        new_val = `Hits Remaining: ${digit}`
      }
      player_hits.textContent = new_val
    }
    document.querySelector("#status").textContent += my_data.result_message + "\n"
    document.getElementById("status").scrollTop = document.getElementById("status").scrollHeight
    getNextPlayer()
  })
};

inbox.onclose = function(){
    console.log('inbox closed');
};

outbox.onclose = function(){
    console.log('outbox closed');
};

document.querySelector("#input-form").addEventListener("submit", function(event) {
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

