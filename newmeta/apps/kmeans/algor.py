import json
from pprint import pprint
from apps.main.models import *

def printData():
    with open('data.json') as data_file:    
        data = json.load(data_file)
        pprint(data)

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