from apps.main.models import *
from time import sleep
import requests
import json

API_KEY = "a006f23d-e3f6-4e80-89d3-f93238f66236"

# getMatchIDs(5.11, 'NORMAL_5X5', 'NA')
def getMatchIDs(version, gamemode, region):

    with open('AP_ITEM_DATASET/{v}/{g}/{r}.json'.format(v=version,g=gamemode.upper(),r=region.upper()), 'r') as content_file:
        content = content_file.read()

    return json.loads(content)
# from apps.functions.Pull import *
# downloadData(5.11, 'NORMAL_5X5', 'NA')
def downloadData(version, gamemode, region):

    matchIDs = getMatchIDs(version, gamemode, region)[0:2]

    for mid in matchIDs:

        try:
            Match.objects.get(pk=mid)
            continue
        except:
            pass

        r = requests.get(
            "https://na.api.pvp.net/api/lol/na/v2.2/match/{mid}?api_key={key}&includeTimeline=true".format(
                mid=mid,
                key=API_KEY
            )
        )

        data = r.json()

        Match(match_id=data['matchId'],region=data['region'],data=data).save()