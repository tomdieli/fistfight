function getDeleteGame(){
  deleteButton = document.createElement('button');
  deleteButton.class = "btn btn-primary"
  deleteButton.innerHTML = 'Delete';
  return deleteButton
}

function getJoinButton(user, game) {
    const joinNode = document.createElement('form');
    joinNode.setAttribute('action', '/' + game.id + '/join/' + user.id);
    joinNode.setAttribute('method', 'post')
    joinNode.setAttribute('id', 'join' + game.id)
    const joinButton = document.createElement('input')
    joinButton.setAttribute('type', 'submit')
    joinButton.value = "Join"
    joinNode.appendChild(joinButton)
    return joinNode;
}

// function getAttackButton(figures, userFigure) {
//     const attackNode = document.createElement('form');
//     const selectNode = document.createElement('select')
//     selectNode.id = 'opponent'
//     for(var figure of figures) {
//         if(figure.figure_name != userFigure.figure_name) {
//             var option = document.createElement("option");
//             option.value = figure.figure_name;
//             option.text = figure.figure_name;
//             selectNode.appendChild(option)
//         }
//     }
//     attackNode.appendChild(selectNode)
// }

