from apps.main.models import *
from functions.util import *
import json

#######################################################
#                        VARS                         #
#######################################################

ITEMS_TO_IGNORE = set([]) # We will ignore items such as trinkets & potions
MATCH_IDS = [1852548676, 1852558827, 1852559208, 1852560871, 1852561073, 1852561268, 1852561502, 1852561581, 1852561687, 1852561785, 1852561946, 1852562005, 1852562088, 1852562166, 1852562277, 1852562346, 1852562389, 1852562408, 1852562571, 1852562781, 1852562894, 1852563071, 1852563141, 1852563215, 1852563267, 1852563364, 1852563477, 1852563546, 1852563597, 1852563619, 1852563644, 1852563683, 1852563694, 1852563798, 1852563886, 1852563912, 1852563915, 1852563921, 1852563958, 1852563971, 1852563976, 1852563999, 1852564006, 1852564053, 1852564058, 1852564072, 1852564083, 1852564130, 1852564155, 1852564164, 1852564167, 1852564184, 1852564192, 1852564230, 1852564248, 1852564270, 1852564554, 1852564610, 1852564762, 1852564767, 1852564814, 1852564823, 1852564838, 1852564927, 1852564954, 1852564972, 1852565037, 1852565072, 1852565094, 1852565233, 1852565294, 1852565306, 1852565378, 1852565385, 1852565408, 1852565420, 1852565518, 1852565615, 1852565667, 1852565696, 1852565715, 1852565766, 1852565847, 1852565907, 1852565927, 1852566104, 1852566168, 1852566213, 1852566330, 1852566377, 1852566405, 1852566581, 1852566600, 1852566755, 1852566937, 1852566971, 1852567098, 1852567111, 1852567147, 1852567158]



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


def generateNextIteration(iteration):

    roles = {'marksman': [], 'support': [], 'mage': [], 'tank': [], 'fighter': []}

    roles_data = readEntireFile('/home/gary/League-New-Meta/newmeta/jsons/kmeans/role_data_{i}.json'.format(i=iteration))
    clusters = getClusters(match_ids=MATCH_IDS,roles=json.loads(roles_data))

    for cluster, data in clusters.items():

        items = []

        for dataset in data:
            items += dataset['items']

        unique_items = set(items) - ITEMS_TO_IGNORE

        for item in unique_items:
            roles[cluster].append({item: float(items.count(item)) / float(len(items))})

    writeAllToFile('/home/gary/League-New-Meta/newmeta/jsons/kmeans/role_data_{i}.json'.format(i=iteration+1), json.dumps(roles))