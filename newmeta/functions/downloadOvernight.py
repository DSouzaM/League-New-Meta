from iterate import *
from kmeans import *
from pull import *

def download():

    getMatchData(5.11, 'NORMAL_5x5', 'NA')
    getMatchData(5.14, 'NORMAL_5x5', 'NA')

    getChampions(5.11, 'NORMAL_5x5', 'NA')
    getChampions(5.14, 'NORMAL_5x5', 'NA')

    getIteration(8, 5.11, 'NORMAL_5x5', 'NA')
    getIteration(8, 5.14, 'NORMAL_5x5', 'NA')

    count_champ_normal_5x5(5.11, 'NA')
    count_champ_normal_5x5(5.14, 'NA')