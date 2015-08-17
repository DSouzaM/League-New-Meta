from apps.main.models import *
from time import sleep
import requests
import json

requests.packages.urllib3.disable_warnings()

API_BASE_URL = "https://na.api.pvp.net/api/lol/"
API_KEY = "7ef5d6cc-917a-4ffe-b31e-1abd46f70374"

# getMatchIDs(5.11, 'NORMAL_5X5', 'NA')
def getMatchIDs(version, gamemode, region):

    with open('AP_ITEM_DATASET/{v}/{g}/{r}.json'.format(v=version,g=gamemode.upper(),r=region.upper()), 'r') as content_file:
        content = content_file.read()

    return json.loads(content)

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
                API_BASE_URL + "{region}/v2.2/match/{mid}?api_key={key}&includeTimeline=true".format(
                    region=region.lower(),
                    mid=mid,
                    key=API_KEY
                )
            )

            if r.status_code is not 200:
                had_errors = True
                print "~ ERROR {s_code}".format(s_code=r.status_code)
                continue

            try:
                data = r.json()
                Match(match_id=data['matchId'],region=data['region'],version=version,gamemode=gamemode,data=r.text).save()
                print
            except Exception as e:
                had_errors = True
                print "~ " + str(e)
                continue

def downloadData2(version, gamemode, region):

    gamemode = gamemode.upper()
    region = region.upper()

    matchIDs = getMatchIDs(version, gamemode, region)

    while matchIDs:
        print matchIDs
        numMatches = len(matchIDs)
        errorMatches = []

        for i in range(numMatches):

            print "Processing match {i} / {total}".format(i=i,total=numMatches),

            mid = matchIDs[i]

            try:
                if Match.objects.filter(match_id=mid,region=region):
	                print "~ skipped"
	                continue
            except Exception as e:
                print "~ " + str(e)
                errorMatches.append(mid)
                continue

            r = requests.get(
                API_BASE_URL + "{region}/v2.2/match/{mid}?api_key={key}&includeTimeline=true".format(
                    region=region.lower(),
                    mid=mid,
                    key=API_KEY
                )
            )

            if r.status_code is not 200:
                print "~ ERROR {s_code}".format(s_code=r.status_code)
                errorMatches.append(mid)
                continue

            try:
                data = r.json()
                Match(
                    match_id=data['matchId'],
                    region=data['region'],
                    version=version,
                    gamemode=gamemode,
                    data=r.text
                ).save()
                print
            except Exception as e:
                print "~ " + str(e)
                errorMatches.append(mid)
                continue

            print errorMatches

        matchIDs = errorMatches

# from apps.functions.Pull import *
# getDevData()
def getDevData():
    #downloadData2(5.11, 'NORMAL_5X5', 'NA')
    downloadData2(5.14, 'NORMAL_5X5', 'NA')