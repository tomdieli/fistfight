var players = JSON.parse(figures);
var player = JSON.parse(figure);
var game_id = JSON.parse(game_id);
var nextPlayer = null;

player.hasDagger = false;

window.onload = function() {
  getNextPlayer();
};

var url = new URL('https://' + document.domain + '/arena');

socket = io.connect(url);


socket.on('connect', function() {
  socket.emit('starting', game_id);
});

socket.on('attack', function(message) {
  attackee = message.attackee;
  dmg = message.dmg;
  msg = message.msg;
  if(dmg !== 0) {
    player_hits = document.getElementById(attackee + "_hits");
    player_stat = player_hits.textContent;

    digit = parseInt(player_stat.match(/: \d+/g)[0].split(' ')[1]);
    digit -= dmg;
    
    if ( digit <= 0) {
      new_val = "DEAD";
      for(i=0; i < players.length; ++i){
        if(players[i]['figure_name'] === attackee){
          players.splice(i, 1);
        }
      }
    }
    else {
      new_val = `Hits Remaining: ${digit}`;
      player_hits.textContent = new_val;
    }
  }
  announce(msg);
  getNextPlayer();
});

socket.on('pull-dagger', function(message){
  puller = message.puller;
  result = message.result;
  msg = message.msg;
  if(player.figure_name === puller){
    player.hasDagger = result;
  }
  announce(msg);
  getNextPlayer();
});

function getNextPlayer() {
  nextPlayer = players.shift()
  players.push(nextPlayer)
  var actions = document.getElementById('actions')
  actions.innerHTML = ""
  if( players.length === 1 ){
    actions.textContent = `${nextPlayer.figure_name} wins!!!`
    return null
  }
  else if(player.id === nextPlayer.id) {
    attackButton = getAttackButton(players, player)
    attackButton.addEventListener("submit", function(event) {
      event.preventDefault();
      var attacker = player;
      var selection  = document.querySelector("#opponent").value;
      socket.emit('attack', attacker, selection, game_id)
    });
    actions.append(attackButton)
    if(player.hasDagger === false) {
      daggerButton = document.createElement('button');
      daggerButton.innerHTML = 'Pull Dagger'
      daggerButton.addEventListener('click', function(event) {
        event.preventDefault();
        var attacker = player.figure_name;
        socket.emit('pull-dagger', attacker, game_id);
      });
      actions.append(daggerButton);
    }
  }
  else {
    actions.textContent = `${nextPlayer.figure_name}'s turn`;
  }
}

function getAttackButton(figures, userFigure) {
  const attackNode = document.createElement('form');
  attackNode.id = 'attack';
  const selectNode = document.createElement('select');
  selectNode.id = 'opponent';
  for(var figure of figures) {
    if(figure.figure_name != userFigure.figure_name) {
        var option = document.createElement("option");
        option.value = figure.figure_name;
        option.text = figure.figure_name;
        selectNode.appendChild(option);
    } 
  }
  if(selectNode.length > 0){
    selectNode.firstChild.selected = true;
  }
  // <button id="punch_button" type="submit">Throw the Fist Punch</button>
  const attackButton = document.createElement('input')
  attackButton.type = 'submit';
  attackNode.appendChild(selectNode)
  attackNode.appendChild(attackButton)
  return attackNode
}

function announce(sentence) {
  document.querySelector("#status").textContent += sentence + "\n"
  document.getElementById("status").scrollTop = document.getElementById("status").scrollHeight
}







