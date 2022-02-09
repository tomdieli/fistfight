function getJoinButton(user, game) {
    const joinNode = document.createElement('form');
    joinNode.setAttribute('action', '/' + game.id + '/join/' + user.id);
    joinNode.setAttribute('method', 'post')
    joinNode.setAttribute('id', 'join' + game.id)
    const joinButton = document.createElement('button')
    joinButton.setAttribute('type', 'submit')
    joinNode.appendChild(joinButton)
    return joinNode;
}

function getAttackButton(figures, userFigure) {
    const attackNode = document.createElement('form');
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
    attackNode.appendChild(selectNode)
}

{/* <form id="input-form" class="form-inline">
      <select name="opponent" id="opponent" width="300px" aria-placeholder="Select someone to punch">
        {% for x in figures %}
          {% if x.figure_name != figure.figure_name %}
            <option value="{{ x.figure_name }}"{% if loop.first %} SELECTED{% endif %}>{{ x.figure_name }}</option>
          {% endif %}
        {% endfor %}
      </select>
      <button id="punch_button" type="submit">Throw the Fist Punch</button>
    </form> */}