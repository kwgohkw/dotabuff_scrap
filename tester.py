import random as rd
import time
import scrape_func
import messages as msg

links_and_results = {'/matches/5411779904': 'won', '/matches/5410674269': 'won', '/matches/5408915928': 'won',
         '/matches/5408859764': 'won', '/matches/5409053516': 'won'}

url = 'https://www.dotabuff.com/players/350519205'
player_id = '350519205'

if scrape_func.check_for_csv():
    pass

else:
    print(msg.check_file_no)

for link, result in links_and_results.items():
    match_soup = scrape_func.get_soup(url,link)

    final_match_data = scrape_func.extract_match_data(match_soup)  # ok
    final_team_data = scrape_func.extract_team_data(match_soup,player_id)  # ok
    final_own_data = scrape_func.extract_own_data(match_soup,player_id)  # ok

    scrape_func.write_to_csv(link, result, final_match_data, final_own_data, final_team_data)

    break_time = rd.randint(60, 128)
    time.sleep(break_time)