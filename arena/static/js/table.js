// Support TLS-specific URLs, when appropriate.
if (window.location.protocol == "https:") {
  var ws_scheme = "wss://";
} else {
  var ws_scheme = "ws://"
};
  
var inbox = new ReconnectingWebSocket(ws_scheme + location.host + "/receive");
var outbox = new ReconnectingWebSocket(ws_scheme + location.host + "/submit");

//var username = document.currentScript.getAttribute('user')
// game_info = document.currentScript.getAttribute('game')
// game_data = JSON.parse(game_info.replace(/'/g, '"'))
// var game_owner = game_data[1]
// var game_id = game_data[0]

inbox.onmessage = function(message) {
  my_data_promise = message.data.text()
  my_data_promise.then( value => {
    my_data = JSON.parse(value)
    console.log(my_data)
    if (my_data["action"] === "join-game") {
      // add user to game
      console.log("Fighter " + my_data['figure_name'] + " has joined game " + my_data['game_id'])
      players = my_data['players']
      console.log(my_data['players'])
      theDiv = document.getElementById("otherPlayers")
      theDiv.innerHTML = ""
      for(player of players){
        var newNode = document.createElement('p');      
        newNode.innerHTML = player;
        theDiv.appendChild( newNode )
      }
      // if this user, disable join
      if (username === my_data['user_name']){
        document.querySelector("#myButton").disabled = true
      }
      // if creator, show button TODO: add dynamically.....
      console.log("Comparing " + username + " and " + game_owner)
      if (username === game_owner) {
        // unhide start button
        document.getElementById("start-game").disabled = false
      }
      // if start,then redirect. TODO: should be POST req?
    } else if (my_data["action"] === "start-game"){
      window.location.href = '/play/' + game_id + '?figure=' + selection; //relative to domain
    }
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

document.querySelector("#join-form").addEventListener("submit", (event) => {
  event.preventDefault();
  selection  = document.querySelector("#figure").value;
  console.log("Before: " + username)
  join_game = {
    "action": "join-game",
    "game_id": game_id,
    "figure_name": selection,
    "user_name": username
  }
  outbox.send(JSON.stringify(join_game));
});

document.querySelector("#start-game").addEventListener("click", (event) => {
  event.preventDefault();
  start_game = {
    "action": "start-game",
    "game_id": game_id,
  }
  outbox.send(JSON.stringify(start_game));
})

