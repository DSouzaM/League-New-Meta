from apps.main.models import *
from time import sleep
import requests
import json

API_KEY = "7ef5d6cc-917a-4ffe-b31e-1abd46f70374"

# getMatchIDs(5.11, 'NORMAL_5X5', 'NA')
def getMatchIDs(version, gamemode, region):

    with open('AP_ITEM_DATASET/{v}/{g}/{r}.json'.format(v=version,g=gamemode.upper(),r=region.upper()), 'r') as content_file:
        content = content_file.read()

    return json.loads(content)
# from apps.functions.Pull import *
# downloadData(5.11, 'NORMAL_5X5', 'NA')
def downloadData(version, gamemode, region):

    gamemode = gamemode.upper()
    region = region.upper()

    matchIDs = getMatchIDs(version, gamemode, region)
    numMatches = len(matchIDs)

    had_errors = True

    while had_errors:

        had_errors = False

        for i in range(numMatches):

            print "Processing match {i} / {total}".format(i=i,total=numMatches),

            mid = matchIDs[i]

            try:
                Match.objects.get(match_id=mid,region=region)
                print "~ skipped"
                continue
            except:
                pass

            r = requests.get(
                "https://na.api.pvp.net/api/lol/na/v2.2/match/{mid}?api_key={key}&includeTimeline=true".format(
                    mid=mid,
                    key=API_KEY
                )
            )

            if r.status_code is not 200:
                had_errors = True
                print "~ ERROR"
                continue

            try: 
                data = r.json()
                Match(match_id=data['matchId'],region=data['region'],data=data).save()
                print
            except:
                had_errors = True
                print "~ ERROR"
                continue