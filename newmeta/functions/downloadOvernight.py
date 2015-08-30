from iterate import *
from kmeans import *
from pull import *
from export import *

def download():
    #regions = ['BR', 'EUNE', 'EUW', 'KR', 'LAN']
    #regions = ['NA', 'LAS', 'OCE', 'RU', 'TR']
    regions = ['NA', 'LAS']
    queues = ['NORMAL_5X5', 'RANKED_SOLO']
    versions = [5.11, 5.14]

    for region in regions:
        for queue in queues:
            for version in versions:

                #getMatchData(version, queue, region)
                #getChampions(version, queue, region)
                #getIteration(8, version, queue, region)
                generateChampionRoles(version, queue, region)
                #count_champ(version, queue, region)
            
            exportChampions(queue, region)