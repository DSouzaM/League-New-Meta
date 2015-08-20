from apps.main.models import *
import json

# from apps.functions.Export import *
# export('NORMAL_5X5', 'NA')
def export(gamemode, region):
    
    gamemode = gamemode.upper()
    region = region.upper()

    assert(gamemode in ["NORMAL_5X5","RANKED_SOLO"])
    assert(region in ["BR","EUNE","EUW","KR","LAN","LAS","NA","OCE","RU","TR"])

    champs = Champion.objects.filter(
        version__name=5.11,
        gamemode__name=gamemode,
        region__name=region
    ).order_by("name")
    result = []

    for champ1 in champs:
        champ2 = Champion.objects.get(
            key=champ1.key,
            version__name=5.14,
            gamemode__name=gamemode,
            region__name=region
        )
        try:
            cdict = {
                'name': champ1.name,
                'picks': round((float(champ2.picks) / float(champ1.picks) - 1) * 100.0, 2),
                'wins': round((float(champ2.wins) / (float(champ2.picks) - float(champ1.wins) / float(champ1.picks)) * 100.0, 2),
                '5.11': {
                    'picks': champ1.picks,
                    'wins': champ1.wins
                },
                '5.14': {
                    'picks': champ2.picks,
                    'wins': champ2.wins
                }
            }
        except:
            continue

        result.append(cdict)

    out = open(gamemode + "_" + region + ".json", "w")
    out.write(json.dumps(result))
    out.close()