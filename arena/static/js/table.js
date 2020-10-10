// Support TLS-specific URLs, when appropriate.
if (window.location.protocol == "https:") {
  var ws_scheme = "wss://";
} else {
  var ws_scheme = "ws://"
};

var game = JSON.parse(game)
var my_figure = null

var inbox = new ReconnectingWebSocket(ws_scheme + location.host + "/game" + game.id + "/receive");
var outbox = new ReconnectingWebSocket(ws_scheme + location.host + "/game" + game.id + "/submit");

inbox.onmessage = function(message) {
  console.log("inbox.onmessage hit")
  // console.log(message.data)
  my_data_promise = message.data.text()
  my_data_promise.then( value => {
    my_data = JSON.parse(value)
    // console.log(my_data)
    if (my_data["action"] === "join-game") {
      // TODO: Better way to refresh list?
      // add user to game
      console.log("Fighter " + my_data['figure_name'] + " has joined game " + game['id'])
      // we are expecting a list of players from join-game event?
      players = my_data['players']
      //console.log(my_data['players'])
      // refresh other players list
      theDiv = document.getElementById("otherPlayers")
      theDiv.innerHTML = ""
      for(player of players){
        var newNode = document.createElement('p');      
        newNode.innerHTML = player;
        theDiv.appendChild( newNode )
      }
      // if this user, disable join
      if (user === my_data['user_name']){
        my_figure = my_data['figure_name']
        document.querySelector("#ready-button").disabled = true
        // if creator, show button
        console.log("Comparing " + user + " and " + game_owner)
        if (user === game_owner) { 
          // unhide start button
          document.getElementById("start-game").disabled = false
        }
      }
      
      // if start,then redirect. TODO: should be POT req?
    } else if (my_data["action"] === "start-game"){
      window.location.href = '/game/play/' + game.id + '?figure=' + my_figure; //relative to domain
    }
  })
};

inbox.onclose = function(e) {
  console.log('inbox Socket is closed. Reconnect will be attempted.', e.reason);
  // console.error('Chat socket closed unexpectedly');
  //this.inbox = new WebSocket(inbox.url);
  this.inbox = new ReconnectingWebSocket(inbox.url);
};

outbox.onclose = function() {
  console.log('outbox Socket is closed. Reconnect will be attempted.', e.reason);
  //console.error('Chat socket closed unexpectedly');
  //this.outbox = new WebSocket(outbox.url);
  this.outbox = new ReconnectingWebSocket(outbox.url);
};

document.querySelector("#join-form").addEventListener("submit", (event) => {
  event.preventDefault();
  console.log("someone hit the JOIN game button")
  selection  = document.querySelector("#figure").value;
  join_game = {
    "action": "join-game",
    "game_id": game.id,
    "game_owner": game_owner,
    "figure_name": selection,
    "user_name": user
  }
  console.log("sending...")
  console.log(join_game)
  outbox.send(JSON.stringify(join_game));
});

document.querySelector("#start-game").addEventListener("click", (event) => {
  event.preventDefault();
  console.log("someone hit the START game button")
  selection  = document.querySelector("#figure").value;
  start_game = {
    "action": "start-game",
    "game_id": game.id
  }
  outbox.send(JSON.stringify(start_game));
})

