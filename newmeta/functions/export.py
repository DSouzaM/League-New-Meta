from apps.main.models import *
from functions.util import *
import json


def exportChampions(gamemode, region):
    
    gamemode = gamemode.upper()
    region = region.upper()
    assert(assertVersionGamemodeRegion(gamemode=gamemode,region=region))

    pre_champs = Champion.objects.filter(
        version__name=5.11,
        gamemode__name=gamemode,
        region__name=region
    ).order_by("name")
    
    result = []

    for pre_champ in pre_champs:

        if pre_champ.wins == 0 or pre_champ.picks == 0:
            continue

        post_champ = Champion.objects.get(
            key=pre_champ.key,
            version__name=5.14,
            gamemode__name=gamemode,
            region__name=region
        )

        if post_champ.wins == 0 or post_champ.picks == 0:
            continue

        f_pre_picks = float(pre_champ.picks)
        f_pre_wins = float(pre_champ.wins)

        f_post_picks = float(post_champ.picks)
        f_post_wins = float(post_champ.wins)

        dict_to_add = {
            'name': pre_champ.name,
            'picks': round( (f_post_picks / f_pre_picks - 1) * 100.0, 2 ),
            'wins': round( (f_post_wins / f_post_picks - f_pre_wins / f_pre_picks) * 100.0, 2 ),
            '5.11': {
                'picks': pre_champ.picks,
                'wins': pre_champ.wins
            },
            '5.14': {
                'picks': post_champ.picks,
                'wins': post_champ.wins
            }
        }

        result.append(dict_to_add)

    with open(gamemode + "_" + region + ".json", 'w') as data_file:    
        data_file.write(json.dumps(result))