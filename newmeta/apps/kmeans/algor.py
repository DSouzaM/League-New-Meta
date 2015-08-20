import json
from pprint import pprint
from apps.main.models import *

MATCH_IDS = [1852548676, 1852558827, 1852559208, 1852560871, 1852561073, 1852561268, 1852561502, 1852561581, 1852561687, 1852561785, 1852561946, 1852562005, 1852562088, 1852562166, 1852562277, 1852562346, 1852562389, 1852562408, 1852562571, 1852562781, 1852562894, 1852563071, 1852563141, 1852563215, 1852563267, 1852563364, 1852563477, 1852563546, 1852563597, 1852563619, 1852563644, 1852563683, 1852563694, 1852563798, 1852563886, 1852563912, 1852563915, 1852563921, 1852563958, 1852563971, 1852563976, 1852563999, 1852564006, 1852564053, 1852564058, 1852564072, 1852564083, 1852564130, 1852564155, 1852564164, 1852564167, 1852564184, 1852564192, 1852564230, 1852564248, 1852564270, 1852564554, 1852564610, 1852564762, 1852564767, 1852564814, 1852564823, 1852564838, 1852564927, 1852564954, 1852564972, 1852565037, 1852565072, 1852565094, 1852565233, 1852565294, 1852565306, 1852565378, 1852565385, 1852565408, 1852565420, 1852565518, 1852565615, 1852565667, 1852565696, 1852565715, 1852565766, 1852565847, 1852565907, 1852565927, 1852566104, 1852566168, 1852566213, 1852566330, 1852566377, 1852566405, 1852566581, 1852566600, 1852566755, 1852566937, 1852566971, 1852567098, 1852567111, 1852567147, 1852567158]

def printData():
    with open('role_data_0.json') as data_file:    
        roles = json.load(data_file)
    pprint(roles)

# from apps.kmeans.algor import *
# getMatchItemData(1852607206, "NA")
def getMatchItemData(mid, region):

    region = region.upper()
    assert(region in ["BR","EUNE","EUW","KR","LAN","LAS","NA","OCE","RU","TR"])

    reg = Region.objects.get(name=region)
    
    m = Match.objects.get(match_id=mid,region=reg)
    data = json.loads(m.data)

    result = []

    for p in data['participants']:
        toAdd = {'champion': {},'items': []}
        toAdd['champion']['id'] = p['championId']
        toAdd['champion']['name'] = Champion.objects.get(key=p['championId'],region=reg,version=m.version).name
        for i in range(7):
            if p['stats']['item'+str(i)] == 0: continue
            toAdd['items'].append({'name': Item.objects.get(key=p['stats']['item'+str(i)],region=reg,version=m.version).name, 'id': p['stats']['item'+str(i)]})
        result.append(toAdd)
    return result

# from apps.kmeans.algor import *
# getMatchItemData2(1852607206, "NA")
def getMatchItemData2(mid, region):

    region = region.upper()
    assert(region in ["BR","EUNE","EUW","KR","LAN","LAS","NA","OCE","RU","TR"])

    reg = Region.objects.get(name=region)
    
    m = Match.objects.get(match_id=mid,region=reg)
    data = json.loads(m.data)

    result = []

    for p in data['participants']:
        toAdd = {}
        toAdd['champion'] = p['championId']
        toAdd['items'] = []
        for i in range(7):
            if p['stats']['item'+str(i)] == 0: continue
            toAdd['items'].append(p['stats']['item'+str(i)])
        result.append(toAdd)
    return result

def getClosenessScore(player,role):
    score = 0.0
    for role_item in role:
        iid = role_item.keys()[0]
        if int(iid) in player['items']:
            score += role_item[iid]
    return score

def getHighestScoringRole(scores):
    highestScore = 0.0
    topRole = None
    i = 0

    for combo in scores:
        if combo[1] > highestScore:
            highestScore = combo[1]
            topRole = combo[0]

    for combo in scores:
        if combo[1] == highestScore:
            i += 1
    
    if i != 1:
        return None
    else:
        return topRole

# from apps.kmeans.algor import *
# testAlgors()
def testAlgors():

    with open('/home/gary/League-New-Meta/newmeta/apps/kmeans/role_data_0.json') as data_file:    
        roles = json.load(data_file)

    clusters = {}
    clusters['tank'] = []
    clusters['support'] = []
    clusters['fighter'] = []
    clusters['marksman'] = []
    clusters['mage'] = []

    for mid in MATCH_IDS:
        playerList = getMatchItemData2(mid, 'NA')
        for player in playerList:
            scores = []
            for role in roles:
                score = getClosenessScore(player,roles[role])
                scores.append([role,score])
            highestScoringRole = getHighestScoringRole(scores)
            if highestScoringRole:
                clusters[highestScoringRole].append(player)

    for cluster in clusters[0:1]:
        print cluster,clusters[cluster]