import random as rd
import time
import scrape_func
import messages as msg
import re

fieldnames = ['link', 'result', 'skill_bracket', 'lobby_type', 'game_mode', 'region', 'duration', 'match_date',
              'hero', 'final_lvl', 'k', 'd', 'a', 'net', 'lh', 'dn', 'gpm', 'xpm', 'dmg',
              'heal', 'bld', 'wards', 'final_items',
              'team_k', 'team_d', 'team_a', 'team_net', 'team_lh', 'team_dn', 'team_gpm',
              'team_xpm', 'team_dmg', 'team_heal', 'team_bld', 'team_wards']


# todo error check
url = input(msg.ask_for_profile)
player_id_regex = re.compile('\d+')
player_id = re.search(player_id_regex, url).group()

# getting matches_pages to extract indiv match links from
# to get the last page number
first_page_soup = scrape_func.get_soup(url)
player_name = scrape_func.get_player_name(first_page_soup)
print(f'player name: {player_name}')
# returns a list of match pages to get all the indiv match urls
matches_pages_url = scrape_func.get_match_pages(first_page_soup, url)
print('you have {} match pages'.format(len(matches_pages_url)))

links_and_results = {}  # to contain all the match links in proper format
temp_new_links = []
for page in matches_pages_url:
    links_and_results.update(scrape_func.get_match_links(page))  # returns a dictionary

    # to compare against previous iteration of new links
    print(f'retrieved links from {page}')
    if scrape_func.check_for_csv(fieldnames, player_name):  # only check if there is a file existing
        new_links = scrape_func.get_new_links(player_name, list(links_and_results.keys()))  # already has a check that no new links, quit program
        if page == matches_pages_url[0] and len(new_links) < len(links_and_results):
            print('no new links after 1st page')
            break
        elif page.find('enhance') > 0 and temp_new_links == new_links:  # if 2nd page and no more new links
            print('no more new links')
            print('{} new link(s)'.format(len(new_links)))
            break
        else:
            temp_new_links = new_links

    break_time = rd.randint(60, 128)
    print(f'waiting for {break_time} seconds')
    time.sleep(break_time)

print(msg.check_for_file)

if scrape_func.check_for_csv(fieldnames, player_name):
    print(msg.check_file_yes)

    new_links_and_results = {}
    # noinspection PyUnboundLocalVariable
    for i in new_links:
        new_links_and_results[i] = links_and_results[i]

    # so that I can shorten the code and put the scraping outside the if statement
    links_and_results = new_links_and_results


else:
    print(msg.check_file_no)

length = len(links_and_results)
count = 0

for link, result in links_and_results.items():
    match_soup = scrape_func.get_soup(url, link)

    final_match_data = scrape_func.extract_match_data(match_soup)  # ok
    final_team_data = scrape_func.extract_team_data(match_soup, player_id)  # ok
    final_own_data = scrape_func.extract_own_data(match_soup, player_id)  # ok

    scrape_func.write_to_csv(player_name, fieldnames, link, result, final_match_data, final_own_data, final_team_data)

    count += 1
    print(f'{count} matches of {length} matches done')

    # don't sleep if last link already
    if link != list(links_and_results.keys())[-1]:
        break_time = rd.randint(120, 180)
        print(f'sleeping for {break_time} seconds')
        time.sleep(break_time)
    else:
        print('data download completed')
