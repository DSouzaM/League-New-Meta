import json
from pprint import pprint
from apps.main.models import *

def printData():
    with open('data.json') as data_file:    
        data = json.load(data_file)
        pprint(data)

# from apps.kmeans.algor import *
# getData(1852607206, "NA")
def getData(mid, region):

    region = region.upper()
    assert(region in ["BR","EUNE","EUW","KR","LAN","LAS","NA","OCE","RU","TR"])

    reg = Region.objects.get(name=region)
    
    m = Match.objects.get(match_id=mid,region=reg)
    data = json.loads(m.data)

    for p in data['participants']:
        print Champion.objects.get(key=p['championId'],region=reg,version=m.version), p['championId']
        for i in range(7):
            if p['stats']['item'+str(i)] == 0: continue
            print Item.objects.get(key=p['stats']['item'+str(i)],region=reg,version=m.version),p['stats']['item'+str(i)]
        print "\n"