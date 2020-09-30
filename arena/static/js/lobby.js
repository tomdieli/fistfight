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
    my_data = JSON.parse(value)
    console.log(my_data)
    if (my_data["action"] === "join-lobby") {
      theDiv = document.getElementById("otherUsers")
      theDiv.innerHTML = ""
      for(user of users){
        var newNode = document.createElement('p');      
        newNode.innerHTML = player;
        theDiv.appendChild( newNode )
      }
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

document.addEventListener('readystatechange', (event) => {
  event.preventDefault();
  selection  = document.querySelector("#figure").value;
  console.log("Before: " + username)
  joinLobby = {
    "action": "join-lobby",
    "user_name": username
  }
  outbox.send(JSON.stringify(joinLobby));

  if( refreshGames === true ){
      refresh_games = {
        "action": "refresh-games",
      }
      outbox.send(JSON.stringify(refresh_games));
    }
    new_game = false
});
