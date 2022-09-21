var thisUser = JSON.parse(thisUser);
var games = JSON.parse(games);
var users = JSON.parse(users);

socket = io.connect(document.domain + ':' + location.port + '/lobby');

document.querySelector("#new_game").addEventListener("click", function(event) {
  event.preventDefault();
  socket.emit('create', thisUser);
});

socket.on('connect', function() {
  socket.emit('joined', thisUser.username);
});

socket.on('joined', function(message) {
  announce(message.msg);
  refreshUsers(JSON.parse(message.users), thisUser);
  refreshGames(games);
});

socket.on('create', function(message) {
  const newGames = JSON.parse(message.games);
  announce(message.msg);
  refreshGames(newGames);
});

socket.on('delete', function(message) {
  const newGames = JSON.parse(message.games);
  announce(message.msg);
  refreshGames(newGames);
});

function refreshUsers(updatedUsers) {
  theDiv = document.getElementById("otherUsers")
  for(var user of updatedUsers){
    var newNode = document.createElement('p');   
    newNode.innerHTML = user.username;
    theDiv.appendChild( newNode );
  }
}

function refreshGames(updated_games) {
  gamesList = document.getElementById("gamesList")
  gamesList.innerHTML = ""
  for(var game of updated_games) {
    const gameNode = document.createElement('li')
    gameNode.className = "list-group-item d-flex justify-content-between align-items-start"
    const contentNode = document.createElement('div')
    contentNode.className = "ms-2 me-auto";
    contentNode.innerHTML = '<div class="fw-bold"></div>'
    contentNode.innerText = 'Game ' + game.id;
    const spanNode = document.createElement('span')
    spanNode.class="badge bg-secondary rounded-pill"
    gameNode.appendChild(contentNode);
    joinNode = getJoinButton(thisUser, game);
    spanNode.append(joinNode)
    //contentNode.appendChild(joinNode)
    contentNode.appendChild(spanNode)
    if (thisUser.username == game.owner) {
      deleteButton = getDeleteGame();
      deleteButton.onclick = function(event) {
        event.preventDefault();
        socket.emit('delete', {'game_id': game.id, 'user': thisUser.username});
      }
      spanNode.append(deleteButton);
    }
    gamesList.appendChild(gameNode);
  }
}

function announce(sentence) {
  document.querySelector("#status").textContent += sentence + "\n"
  document.getElementById("status").scrollTop = document.getElementById("status").scrollHeight
}
