import json

with open('v5.11_NORMAL_5V5_NA.json') as old_champs, open('v5.14_NORMAL_5V5_NA.json') as new_champs:
	old_champs = json.load(old_champs)
	new_champs = json.load(new_champs)
	for cnum in range(len(old_champs)):
		old_champ = old_champs[cnum]
		old_wins = old_champ['fields']['wins']
		new_champ = new_champs[cnum]
		new_wins = new_champ['fields']['wins']
		cname = old_champ['fields']['name']
		if (abs(old_wins-new_wins) > 300): #corresponds to an change in win rate >= 3%
			if (old_wins > new_wins):
				print cname + '\'s winrate dropped after the patch.'
			else:
				print cname + '\'s winrate increased after the patch.'
		#else:
			#print cname + '\'s winrate stayed relatively the same after the patch.'