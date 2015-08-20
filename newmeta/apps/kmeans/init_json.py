import json

roles = {}

roles['Marksman'] = [{"Infinity Edge": 1}, {"Phantom Dancer": 1}, {"Last Whisper": 1}, {"Blade of the Ruined King": 1}, {"Statikk Shiv": 1}, {"The Bloodthirster": 1}, {"Berserker's Greaves": 1}]
roles['Support'] = [{"Ruby Sightstone": 1}, {"Sightstone": 1}, {"Face of the Mountain": 1}, {"Talisman of Ascension": 1}, {"Frost Queen's Claim": 1}, {"Locket of the Iron Solari": 1}, {"Mikael's Crucible": 1}]
roles['Mage'] = [{"Rabadon's Deathcap": 1}, {"Zhonya's Hourglass": 1}, {"Luden's Echo": 1}, {"Rylai's Crystal Scepter": 1}, {"Void Staff": 1}, {"Morellonomicon": 1}, {"Athene's Unholy Grail": 1}]
roles['Tank'] = [{"Warmog's Armor": 1}, {"Randuin's Omen": 1}, {"Spirit Visage": 1}, {"Banshee's Veil": 1}, {"Thornmail": 1}, {"Sunfire Cape": 1}, {"Frozen Heart": 1}]
roles['Fighter'] = [{"Trinity Force": 1}, {"Blade of the Ruined King": 1}, {"The Black Cleaver": 1}, {"Youmuu's Ghostblade": 1}, {"Last Whisper": 1}, {"Ravenous Hydra": 1}, {"Hexdrinker": 1}]

print json.dumps(roles, sort_keys=True, indent=4, separators=(',', ': '))