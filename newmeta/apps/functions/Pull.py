from apps.main.models import *
import requests
import json

try:
    requests.packages.urllib3.disable_warnings()
except:
    pass

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

    assert(version in [5.11,5.14])
    assert(gamemode in ["NORMAL_5X5","RANKED_SOLO"])
    assert(region in ["BR","EUNE","EUW","KR","LAN","LAS","NA","OCE","RU","TR"])

    matchIDs = getMatchIDs(version, gamemode, region)

    try:
        ver = Version.objects.get(name=version)
    except:
        ver = Version(name=version)
        ver.save()

    try:
        gm = Gamemode.objects.get(name=gamemode)
    except:
        gm = Gamemode(name=gamemode)
        gm.save()

    try:
        reg = Region.objects.get(name=region)
    except:
        reg = Region(name=region)
        reg.save()

    while matchIDs:
        print matchIDs
        numMatches = len(matchIDs)
        errorMatches = []

        for i in range(numMatches):

            print "Processing match {i} / {total}".format(i=i,total=numMatches),

            mid = matchIDs[i]

            try:
                if Match.objects.filter(match_id=mid,region=reg):
	                print "~ skipped"
	                continue
            except Exception as e:
                print "~ " + str(e)
                errorMatches.append(mid)
                continue

            try:
                r = requests.get(
                    API_BASE_URL + "{region}/v2.2/match/{mid}?api_key={key}&includeTimeline=true".format(
                        region=region.lower(),
                        mid=mid,
                        key=API_KEY
                    )
                )
            except Exception as e:
                print "~ " + str(e)
                errorMatches.append(mid)
                continue

            if r.status_code is not 200:
                print "~ ERROR {s_code}".format(s_code=r.status_code)
                errorMatches.append(mid)
                continue

            try:
                data = r.json()
                Match(
                    match_id=data['matchId'],
                    region=reg,
                    version=ver,
                    gamemode=gm,
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
    # downloadData(5.11, 'NORMAL_5X5', 'NA')
    # downloadData(5.14, 'NORMAL_5X5', 'NA')
    downloadData(5.11, 'RANKED_SOLO', 'NA')
    downloadData(5.14, 'RANKED_SOLO', 'NA')


def validateData(version, gamemode, region):

    gamemode = gamemode.upper()
    region = region.upper()

    matchIDs = getMatchIDs(version, gamemode, region)

    numMatches = len(matchIDs)
    problemMatches = []

    for i in range(numMatches):

        print "Processing match {i} / {total}".format(i=i,total=numMatches),

        mid = matchIDs[i]

        if Match.objects.filter(match_id=mid,region=region).count() != 1:
            problemMatches.append(mid)
        
        print problemMatches

def validateDevData():
    validateData(5.11, 'NORMAL_5X5', 'NA')
    validateData(5.14, 'NORMAL_5X5', 'NA')




#from apps.functions.Pull import *
#initChampions(5.11,"NORMAL_5X5","NA")
def initChampions(version, gamemode, region):

    gamemode = gamemode.upper()
    region = region.upper()

    assert(version in [5.11,5.14])
    assert(gamemode in ["NORMAL_5X5","RANKED_SOLO"])
    assert(region in ["BR","EUNE","EUW","KR","LAN","LAS","NA","OCE","RU","TR"])

    try:
        ver = Version.objects.get(name=version)
    except:
        ver = Version(name=version)
        ver.save()

    try:
        gm = Gamemode.objects.get(name=gamemode)
    except:
        gm = Gamemode(name=gamemode)
        gm.save()

    try:
        reg = Region.objects.get(name=region)
    except:
        reg = Region(name=region)
        reg.save()

    r = requests.get(
        API_BASE_URL + "static-data/{region}/v1.2/champion/?api_key={key}".format(
            region=region.lower(),
            key=API_KEY
        )
    )

    if r.status_code is not 200:
        print "~ ERROR {s_code}".format(s_code=r.status_code)
        return

    data = r.json()['data']

    for champ in data:
        cid = data[champ]['id']
        cname = data[champ]['name']
        if not Champion.objects.filter(key=cid,region=reg,version=ver,gamemode=gm):
            Champion(key=cid,name=cname,region=reg,version=ver,gamemode=gm).save()





