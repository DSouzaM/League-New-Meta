from apps.main.models import *
from functions.util import *
import json


def getChampionWinLoss(version, region):

    gamemode = 'NORMAL_5X5'
    region = region.upper()
    assert(assertVersionGamemodeRegion(version=version,region=region))

    matches = Match.objects.filter(region__name=region,version__name=version,gamemode__name=gamemode)
    total = matches.count()

    Champion.objects.filter(
        region__name=region,
        version__name=version,
        gamemode__name=gamemode
    ).update(wins=0,picks=0,bans=0)

    for i in xrange(total):

        print "Processing match {i} / {total}".format(i=i,total=total)

        match = matches[i]
        data = json.loads(match.data)

        teams = {
            data['teams'][0]['teamId']:data['teams'][0]['winner'],
            data['teams'][1]['teamId']:data['teams'][1]['winner']
        }

        for player in data['participants']:

            champ_id = player['championId']
            team_id = player['teamId']

            champ = Champion.objects.get(key=champ_id,region__name=region,version__name=version,gamemode__name=gamemode)
            
            champ.picks += 1
            
            if teams[team_id]:
                champ.wins += 1
            
            champ.save()