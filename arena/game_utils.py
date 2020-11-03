import random
import json

from arena.database import DatabaseServices


def punch(attack_name, defend_name):
    with DatabaseServices() as dbase:
        attacker = json.loads(dbase.get_figure_by_name(attack_name))[0]
        defender = json.loads(dbase.get_figure_by_name(defend_name))[0]
    rolls = [random.randrange(1, 7) for i in range(0,3)]
    roll_total = sum(rolls)
    if roll_total > attacker["dexterity"]:
        damage = 0
        message = "%s attacks %s but misses with a roll of %s %s" %\
            (attacker["figure_name"], defender["figure_name"], roll_total, rolls)
    else:
        damage = random.randrange(1, 7)
        message = "%s attacks %s and hits with a roll of %s %s. Doing %s damage." %\
            (attacker["figure_name"], defender["figure_name"], roll_total, rolls, damage)

    return { "message": message, "damage": damage }