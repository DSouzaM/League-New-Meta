from iterate import *
from kmeans import *
from pull import *

def download():

    getMatchData(5.11, 'RANKED_SOLO', 'NA')
    getMatchData(5.14, 'RANKED_SOLO', 'NA')

    getChampions(5.11, 'RANKED_SOLO', 'NA')
    getChampions(5.14, 'RANKED_SOLO', 'NA')

    getIteration(8, 5.11, 'RANKED_SOLO', 'NA')
    getIteration(8, 5.14, 'RANKED_SOLO', 'NA')

    # count_champ_normal_5x5(5.11, 'NA')
    # count_champ_normal_5x5(5.14, 'NA')