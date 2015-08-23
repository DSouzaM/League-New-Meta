from apps.main.models import *
from functions.util import *
import json
import os

#######################################################
#                        VARS                         #
#######################################################

ITEMS_TO_IGNORE = set([2041,2003,2004,2047,2052,2010]) # Items we potentially want to ignore


###################################################
#                 HELPER FUNCTIONS                #
###################################################

def getMatchItems(match_id,region):
    
    region = region.upper()
    assertVersionGamemodeRegion(region=region)

    match = Match.objects.get(match_id=match_id,region__name=region)

    data = json.loads(match.data)
    result = []

    for player in data['participants']:

        player_dict = {
            'champion': int(player['championId']), 
            'items': []
        }

        for i in xrange(7):

            item = 'item'+str(i)
            itemId = int(player['stats'][item])

            if itemId:
                player_dict['items'].append(itemId)

        result.append(player_dict)

    return result


def getScore(player,role):

    score = 0.0

    for role_item in role:

        for item_id, points in role_item.iteritems():

            if int(item_id) in player['items']:
                score += points

    return score


# If the best role has a score of 0, or there is a tie
# we will skip this player.
# A better way to implement this function is to sort descending,
# take [0], and see if [1]'s score is the same.
def getBestRole(scores):

    best_role_score = [None, 0.0]
    numberOfTopRoles = 0

    for role_score in scores:

        if role_score[1] > best_role_score[1]:
            best_role_score = role_score

    for role_score in scores:

        if role_score[1] == best_role_score[1]:
            numberOfTopRoles += 1

    if numberOfTopRoles != 1:
        return None
    else:
        return best_role_score[0]


###################################################
#                PRIMARY FUNCTIONS                #
###################################################

def getClusters(match_ids,roles):

    clusters = {'marksman': [], 'support': [], 'mage': [], 'tank': [], 'fighter': []}

    total = len(match_ids)

    for i in xrange(total):

        print "Processing match {i} / {total}".format(i=i,total=total)

        match_id = match_ids[i]
        playerList = getMatchItems(match_id,'NA')

        for player in playerList:

            scores = []

            for role in roles:

                score = getScore(player,roles[role])
                scores.append([role,score])

            bestRole = getBestRole(scores)

            if bestRole:
                clusters[bestRole].append(player)

    return clusters


def generateNextIteration(iteration, version, gamemode, region):

    gamemode = gamemode.upper()
    region = region.upper()
    assert(assertVersionGamemodeRegion(version=version,gamemode=gamemode,region=region))
    assert(iteration >= 0)

    if not os.path.exists('./jsons/kmeans/{ver}'.format(ver=version)):
        os.makedirs('./jsons/kmeans/{ver}'.format(ver=version))
    if not os.path.exists('./jsons/kmeans/{ver}/{gm}'.format(ver=version,gm=gamemode)):
        os.makedirs('./jsons/kmeans/{ver}/{gm}'.format(ver=version,gm=gamemode))
    if not os.path.exists('./jsons/kmeans/{ver}/{gm}/{reg}'.format(ver=version,gm=gamemode,reg=region)):
        os.makedirs('./jsons/kmeans/{ver}/{gm}/{reg}'.format(ver=version,gm=gamemode,reg=region))
    if not os.path.exists('./jsons/kmeans/{ver}/{gm}/{reg}/0.json'.format(ver=version,gm=gamemode,reg=region)):
        initKMeansRoleJson('./jsons/kmeans/{ver}/{gm}/{reg}/0.json'.format(ver=version,gm=gamemode,reg=region))

    roles = {'marksman': [], 'support': [], 'mage': [], 'tank': [], 'fighter': []}

    roles_data = readEntireFile('./jsons/kmeans/{ver}/{gm}/{reg}/{it}.json'.format(ver=version,gm=gamemode,reg=region,it=iteration))
    match_ids = getMatchIDs(version, gamemode, region)

    clusters = getClusters(match_ids=match_ids,roles=json.loads(roles_data))

    for cluster, data in clusters.items():

        items = []

        for dataset in data:
            items += dataset['items']

        unique_items = set(items) - ITEMS_TO_IGNORE

        for item in unique_items:
            roles[cluster].append({item: float(items.count(item)) / float(len(items))})

    dataToWrite = json.dumps(roles, sort_keys=True, indent=4, separators=(',', ': '))
    writeAllToFile('./jsons/kmeans/{ver}/{gm}/{reg}/{it}.json'.format(ver=version,gm=gamemode,reg=region,it=iteration+1), dataToWrite)