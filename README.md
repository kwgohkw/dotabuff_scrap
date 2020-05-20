# dotabuff_scrap
scraping your own (or other people's) DoTA match statistics for analysis

Using requests, bs4, and some standard python packages, pulls match data statistics into a CSV file which you can then use your data science know-how to squeeze some insights on your dota gameplay, or maybe just found out how addicted you are looking at your number of matches per day and time spent on the game.

Match data not formatted, ended up as objects instead of intended format (datetime, int, lists) but just format that before you do your analysis, might add in formatting in the future.

below are the column headers + examples of each entry 
link': /matches/4747505750
result': won
skill_bracket': normal
'lobby_type': all pick
'game_mode': turbbo
'region': SEA
'duration': 34:40
'match_date': 2020-05-20
hero': Sniper
'final_lvl': 25
'k': 5
'd': 2
'a': 15
'net': 1.5k
'lh': 100
'dn': 23
'gpm': 850
'xpm': 620
'dmg': 3.2k
'heal': 0
'bld': 153
'wards': 12/5
'final_items': ['Boots of Travel', 'Desolator','Black King Bar']
team_k': 6
'team_d': 20
'team_a': 50
'team_net': 6.5k
'team_lh': 500
'team_dn': 120
'team_gpm': 500
team_xpm': 600
'team_dmg': 8.5k
'team_heal': 200
'team_bld': 4.5k
'team_wards': 20/10
