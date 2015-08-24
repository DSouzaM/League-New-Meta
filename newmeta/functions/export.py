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
            'pre_wr': round( (f_pre_wins / f_pre_picks) * 100 , 2),
            'post_wr': round( (f_post_wins / f_post_picks) * 100 , 2),
            'pre_pr': round( f_pre_picks / 100.0 , 2),
            'post_pr': round( f_post_picks / 100.0 , 2),
            'pre_role': pre_champ.role,
            'post_role': post_champ.role
        }
        dict_to_add['d_wr'] = round(dict_to_add['post_wr'] - dict_to_add['pre_wr'], 2)
        dict_to_add['d_pr'] = round(dict_to_add['post_pr'] - dict_to_add['pre_pr'], 2)

        result.append(dict_to_add)

    dataToWrite = json.dumps(result, sort_keys=True, indent=4, separators=(',', ': '))
    writeAllToFile("./jsons/" + gamemode + "_" + region + ".json", dataToWrite)