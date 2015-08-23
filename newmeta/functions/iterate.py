from apps.main.models import *
from functions.util import *
import json


def count_champ_normal_5x5(version, region):

    gamemode = 'NORMAL_5X5'
    region = region.upper()
    assert(assertVersionGamemodeRegion(version=version,region=region))

    region_object = Region.objects.get(name=region)
    version_object = Version.objects.get(name=version)
    gamemode_object = Gamemode.objects.get(name=gamemode)

    matches = Match.objects.filter(
        region=region_object,
        version=version_object,
        gamemode=gamemode_object
    )
    total = matches.count()

    champions = Champion.objects.filter(
        region=region_object,
        version=version_object,
        gamemode=gamemode_object
    )
    champions.update(wins=0,picks=0,bans=0)

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

            champ = champions.get(key=champ_id)
            
            champ.picks += 1
            
            if teams[team_id]:
                champ.wins += 1
            
            champ.save()