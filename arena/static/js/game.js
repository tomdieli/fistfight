var players = JSON.parse(figures)
var player = JSON.parse(figure)
var game_id = JSON.parse(game_id)
var nextPlayer = null

window.onload = function() {
  getNextPlayer()
};

socket = io.connect('http://' + document.domain + ':' + location.port + '/arena');

socket.on('connect', function() {
  socket.emit('starting', game_id);
});

socket.on('attack', function(message) {
  console.log(message);
  attackee = message.attackee
  dmg = message.dmg
  msg = message.msg
  console.log(attackee + '_hits')
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
  announce(msg)
  getNextPlayer()
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
      var attacker = player.figure_name;
      var selection  = document.querySelector("#opponent").value;
      console.log(attacker, selection)
      socket.emit('attack', attacker, selection, game_id)
    });
    actions.append(attackButton)
  }
  else {
    actions.textContent = `${nextPlayer.figure_name}'s turn`
  }
}

function getAttackButton(figures, userFigure) {
  const attackNode = document.createElement('form');
  attackNode.id = 'attack'
  const selectNode = document.createElement('select')
  selectNode.id = 'opponent'
  for(var figure of figures) {
      if(figure.figure_name != userFigure.figure_name) {
          var option = document.createElement("option");
          option.value = figure.figure_name;
          option.text = figure.figure_name;
          selectNode.appendChild(option)
      }
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







