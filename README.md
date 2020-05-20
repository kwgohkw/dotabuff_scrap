# dotabuff_scrap
scraping your own (or other people's) DoTA match statistics for analysis

Using requests, bs4, and some standard python packages, pulls match data statistics into a CSV file which you can then use your data science know-how to squeeze some insights on your dota gameplay, or maybe just found out how addicted you are looking at your number of matches per day and time spent on the game.

Match data not formatted, ended up as objects instead of intended format (datetime, int, lists) but just format that before you do your analysis, might add in formatting in the future.

below are the column headers + examples of each entry 
'link': /matches/4747505750<br />
'result': won<br />
'skill_bracket': normal<br />
'lobby_type': all pick<br />
'game_mode': turbbo<br />
'region': SEA<br />
'duration': 34:30<br />
'match_date': 2020-05-20<br />
hero': Sniper<br />
'final_lvl': 25<br />
'k': 5<br />
'd': 2<br />
'a': 15<br />
'net': 1.5k<br />
'lh': 100<br />
'dn': 23<br />
'gpm': 850<br />
'xpm': 620<br />
'dmg': 3.2k<br />
'heal': 0<br />
'bld': 153<br />
'wards': 12/5<br />
'final_items': ['Boots of Travel', 'Desolator','Black King Bar']<br />
team_k': 6<br />
'team_d': 20<br />
'team_a': 50<br />
'team_net': 6.5k<br />
'team_lh': 500<br />
'team_dn': 120<br />
'team_gpm': 500<br />
team_xpm': 600<br />
'team_dmg': 8.5k<br />
'team_heal': 200<br />
'team_bld': 4.5k<br />
'team_wards': 20/10<br />
