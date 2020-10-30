// Support TLS-specific URLs, when appropriate.
if (window.location.protocol == "https:") {
  var ws_scheme = "wss://";
} else {
  var ws_scheme = "ws://"
};

// var inbox = new ReconnectingWebSocket(ws_scheme + location.host + "/lobby/receive");
// var outbox = new ReconnectingWebSocket(ws_scheme + location.host + "/lobby/submit");

var inbox = new WebSocket(ws_scheme + location.host + "/lobby/receive");
var outbox = new WebSocket(ws_scheme + location.host + "/lobby/submit");

var thisUser = JSON.parse(thisUser)
var refreshGames = refreshGames

inbox.onmessage = function(message) {
  my_data_promise = message.data.text()
  my_data_promise.then( value => {
    my_data = JSON.parse(value)
    console.log(my_data)
    if(my_data["action"] === "join-lobby") {
      // TODO: change name of 'theDiv'
      theDiv = document.getElementById("otherUsers")
      theDiv.innerHTML = ""
      for(user of users){
        var newNode = document.createElement('p');      
        newNode.innerHTML = user.username;
        theDiv.appendChild( newNode );
      }
      msg = '%s has joined the lobby' + user.username
      document.querySelector("#status").textContent += msg + "\n"
      document.getElementById("status").scrollTop = document.getElementById("status").scrollHeight
    }
    else if(my_data["action"] === "refresh-games") {
      // we get the updated game list from the dealer
      games = JSON.parse(my_data['games'])
      gamesList = document.getElementById("gamesList")
      gamesList.innerHTML = ""
      for(game of games) {
        var gameNode = document.createElement('h3')
        gameNode.innerHTML = 'Game ' + game.id + '<br>'
        console.log("comparing " + thisUser.username + " to " + game.owner)
        if (thisUser.username == game.owner) {
          var deleteNode = document.createElement('form');
          deleteNode.setAttribute('action', '/game/' + game.id + '/delete')
          deleteNode.setAttribute('method', 'post')
          var deleteButton = document.createElement('input')
          deleteButton.setAttribute('type', 'submit')
          deleteButton.setAttribute('name', 'delete')
          deleteButton.setAttribute('value', 'Delete')
          deleteNode.appendChild(deleteButton)
          gameNode.appendChild(deleteNode)
        }
        var joinNode = document.createElement('form')
          joinNode.setAttribute('action', '/game/' + game.id + '/join/' + thisUser.id)
          joinNode.setAttribute('method', 'post')
          var joinButton = document.createElement('input')
          joinButton.setAttribute('type', 'submit')
          joinButton.setAttribute('name', 'join')
          joinButton.setAttribute('value', 'Join')
          joinNode.appendChild(joinButton)
          gameNode.appendChild(joinNode)
        gamesList.appendChild( gameNode )
      }
    }
  })
};

inbox.onclose = function(){
    console.log('inbox closed');
    // this.inbox = new ReconnectingWebSocket(inbox.url);
    this.inbox = new WebSocket(inbox.url);
};

outbox.onclose = function(){
    console.log('outbox closed');
    // this.outbox = new ReconnectingWebSocket(outbox.url);
    this.outbox = new WebSocket(outbox.url);
};

window.setTimeout(doRefresh, 1000)

function doRefresh() {
  console.log("Refrsh: " + refreshGames)
  if( refreshGames === "True" ){
    refresh_games = {
      "action": "refresh-games",
      "games": games
    }
    console.log("attempting to send..." + refresh_games)
    outbox.send(JSON.stringify(refresh_games));
  }
  refreshGames = "False"
}

// document.addEventListener('readystatechange', (event) => {
//   event.preventDefault();
  // joinLobby = {
  //   "action": "join-lobby",
  // }
  // outbox.send(JSON.stringify(joinLobby));


//});
