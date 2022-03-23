import random
import json

from arena.database import DatabaseServices


def punch(attacker, defend_name):
    dmg = 0
    with DatabaseServices() as dbase:
        # attacker = json.loads(dbase.get_figure_by_name(attack_name))[0]
        defender = json.loads(dbase.get_figure_by_name(defend_name))[0]
    rolls = [random.randrange(1, 7) for i in range(0,3)]
    roll_total = sum(rolls)
    if roll_total > attacker["dexterity"] + 4:
        message = "%s attacks %s but misses with a roll of %s %s" %\
            (attacker["figure_name"], defender["figure_name"], roll_total, rolls)
    else:
        if attacker['hasDagger'] == True:
            dmg_mod = 2
        elif attacker['strength'] > defender['strength']:
            dmg_mod = -2
        elif attacker['strength'] < defender['strength']:
            dmg_mod = -4
        else:
            dmg_mod = -3
        roll = random.randrange(1, 7)
        dmg = roll + dmg_mod
        message = f"{attacker['figure_name']} attacks {defend_name} and hits with a roll of {roll_total}({rolls}). "
        if dmg > 0:
            message += f'Doing {dmg} damage.({roll} + {dmg_mod})'
        else:
            dmg = 0
            message += f'But does not hit hard enought to do damage.({roll} + {dmg_mod})'

    return { "message": message, "damage": dmg }


def attempt_pull(puller):
    roll = random.randrange(1, 7)
    if roll > 3:
        message = f'{puller} attempts to draw a dagger, rolled {roll} and is unsuccessful.'
        result = False
    else:
        message = f'{puller} attempts to draw a dagger, rolled {roll} and is successful!!!'
        result = True
    return { "message": message, "result": result, "puller": puller }
