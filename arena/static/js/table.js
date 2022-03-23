// // Support TLS-specific URLs, when appropriate.
// if (window.location.protocol == "https:") {
//   var ws_scheme = "wss://";
// } else {
//   var ws_scheme = "ws://"
// };

var figures = figures;
var game = JSON.parse(game);
var user = user

socket = io.connect('http://' + document.domain + ':' + location.port + '/arena');

document.querySelector("#join-form").addEventListener("submit", function(event) {
  event.preventDefault();
  selection  = document.querySelector("#figure").value;
  socket.emit('ready', game, selection)
});

if(game.owner === user) {
  startButton = document.getElementById('start-game');
  startButton.disabled = false;
  startButton.addEventListener("click", function(event) {
    console.log('start button hit')
    event.preventDefault();
    socket.emit('start', game.id)
  });
}

socket.on('connect', function() {
  socket.emit('starting', game.id)
});

socket.on('joined', function(message) {
  announce(message.msg)
  refreshFigures(JSON.parse(message.figures))
});

socket.on('ready', function(message) {
  announce(message.msg)
  refreshFigures(JSON.parse(message.figures))
});

socket.on('start', function(message) {
  window.location.href = message + '?figure=' + document.querySelector("#figure").value;
})

function refreshFigures(updatedFigures) {
  theDiv = document.getElementById("playerList")
  theDiv.innerHTML = ""
  for(var user of updatedFigures){
    var newNode = document.createElement('p');   
    newNode.innerHTML = user.figure_name;
    theDiv.appendChild( newNode );
  }
}

function announce(sentence) {
  document.querySelector("#status").textContent += sentence + "\n"
  document.getElementById("status").scrollTop = document.getElementById("status").scrollHeight
}

