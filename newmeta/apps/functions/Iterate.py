from apps.main.models import *
import json

#from apps.functions.Iterate import *
#tallyWLB(5.11, 'NORMAL_5X5', 'NA')
def tallyWLB(version, gamemode, region):

    gamemode = gamemode.upper()
    region = region.upper()

    assert(version in [5.11,5.14])
    assert(gamemode in ["NORMAL_5X5","RANKED_SOLO"])
    assert(region in ["BR","EUNE","EUW","KR","LAN","LAS","NA","OCE","RU","TR"])
 
    ver = Version.objects.get(name=version)
    gm = Gamemode.objects.get(name=gamemode)
    reg = Region.objects.get(name=region)

    matches = Match.objects.filter(region=reg,version=ver,gamemode=gm)
    total = matches.count()

    for champ in Champion.objects.filter(region=reg,version=ver,gamemode=gm):
        champ.wins = 0
        champ.picks = 0
        champ.bans = 0
        champ.save()

    for i in xrange(total):
        print i,total
        match = matches[i]
        data = json.loads(match.data)
        teams = {
            data['teams'][0]['teamId']:data['teams'][0]['winner'],
            data['teams'][1]['teamId']:data['teams'][1]['winner']
        }
        for x in data['participants']:
            cid = x['championId']
            tid = x['teamId']
            champ = Champion.objects.get(key=cid,region=reg,version=ver,gamemode=gm)
            champ.picks += 1
            if teams[tid]:
                champ.wins += 1
            champ.save()