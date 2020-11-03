// Support TLS-specific URLs, when appropriate.
if (window.location.protocol == "https:") {
  var ws_scheme = "wss://";
} else {
  var ws_scheme = "ws://"
};

var game = JSON.parse(game)
var my_figure = null

var inbox = new WebSocket(ws_scheme + location.host + "/game" + game.id + "/receive");
var outbox = new WebSocket(ws_scheme + location.host + "/game" + game.id + "/submit");

inbox.onmessage = function(message) {
  my_data_promise = message.data.text()
  my_data_promise.then( value => {
    my_data = JSON.parse(value)
    if (my_data["action"] === "join-game") {
      // we get the updated player list from the dealer
      players = my_data['players']
      // refresh other players list
      playerList = document.getElementById("playerList")
      playerList.innerHTML = "<ul>"
      for(player of JSON.parse(players)){
        var newNode = document.createElement('li');      
        newNode.innerHTML = player.figure_name;
        newNode.innerHTML += "<br>ST: " + player.strength;
        newNode.innerHTML += "<br>DX: " + player.dexterity; 
        playerList.appendChild( newNode )
      }
      // if this user, disable join
      if (user === my_data['user_name']){
        my_figure = my_data['figure_name']
        document.querySelector("#ready-button").disabled = true
        // if creator, show button
        if (user === game_owner) { 
          document.getElementById("start-game").disabled = false
        }
      }
      msg = my_data['figure_name'] + ' has joined the arena!'
      document.querySelector("#status").textContent += msg + "\n"
      document.getElementById("status").scrollTop = document.getElementById("status").scrollHeight
      // if start,then redirect. TODO: should be POT req?
    } else if (my_data["action"] === "start-game"){
      window.location.href = '/game/play/' + game.id + '?figure=' + my_figure;
    }
  })
};

inbox.onclose = function() {
  console.log('inbox is closed.');
};

outbox.onclose = function() {
  console.log('outbox is closed.');
};

document.querySelector("#join-form").addEventListener("submit", function(event) {
  event.preventDefault();
  selection  = document.querySelector("#figure").value;
  join_game = {
    "action": "join-game",
    "game_id": game.id,
    "game_owner": game_owner,
    "figure_name": selection,
    "user_name": user
  }
  outbox.send(JSON.stringify(join_game));
});

document.querySelector("#start-game").addEventListener("click", function(event) {
  event.preventDefault();
  selection  = document.querySelector("#figure").value;
  start_game = {
    "action": "start-game",
    "game_id": game.id
  }
  outbox.send(JSON.stringify(start_game));
})

