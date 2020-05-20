import requests
from bs4 import BeautifulSoup
import re
import os
import csv
import random as rd
import time
import sys


def check_for_csv(fieldnames,player_name):
    if os.path.isfile('dota_match_data_' + player_name + '.csv'):
        return True
    else:
        with open('dota_match_data_' + player_name + '.csv', 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
        return False


def get_soup(player_url, match_url=None):
    print('getting soup object...')
    if not match_url is None:  # this is an individual match link
        url = 'https://www.dotabuff.com' + match_url
    else:  # this is a matches page
        url = player_url + '/matches'
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                 'Chrome/81.0.4044.138 Safari/537.36 '
    headers = {'user-agent': user_agent}

    count = 0

    while True:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            break
        else:
            print('status code: {}'.format(response.status_code))
            print(response.headers)
            lag = rd.randint(600,620)
            print(f'sleeping for {lag} seconds')
            count += 1
            time.sleep(lag)
        if count == 3:
            print('too many failed attempts, exiting program and try again later')
            sys.exit(0)

    soup = BeautifulSoup(response.content, 'html.parser')

    return soup


def get_player_name(soup):
    name = soup.find('div', class_='header-content-title').text
    final_name = name.replace('Matches','')
    return final_name


def get_match_pages(soup, url):
    last_page_link = 'https://www.dotabuff.com' + soup.find('span', class_='last').find('a').attrs['href']
    subsequent = url + '/matches?enhance=overview&page='
    count = 2
    final_pages = [url + '/matches']

    while final_pages[-1] != last_page_link:
        final_pages.append(subsequent + str(count))
        count += 1
        if count > 6:
            break

    return final_pages


def get_match_links(profile_url):
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
    headers = {'user-agent': user_agent}

    count = 0

    while True:
        response = requests.get(profile_url, headers=headers)
        if response.status_code == 200:
            break
        else:
            print('status code: {}'.format(response.status_code))
            print(response.headers)
            lag = rd.randint(300, 600)
            print(f'sleeping for {lag} seconds')
            count += 1
            time.sleep(lag)
        if count == 3:
            print('too many failed attempts, exiting program and try again later')
            sys.exit(0)

    soup = BeautifulSoup(response.content, 'html.parser')
    reg_obj = re.compile('won|lost')
    links_tags = soup.find_all('a', class_=reg_obj, attrs={'href': re.compile(r'/matches/\d+')})

    links_results = {}

    for i in links_tags:
        links_results[i.attrs["href"]] = ''.join(i.attrs['class'])

    return links_results


def get_new_links(player_name, links):
    with open('dota_match_data_' + player_name + '.csv', 'r') as f:
        reader = csv.reader(f)
        full_list = list(reader)
        old_links = [x[0] for x in full_list][1:]  # omit the header 'link'

    final_new_links = [x for x in links if x not in old_links]
    if not final_new_links:
        print('no new links, exiting program')
        sys.exit(0)
    return final_new_links


def extract_match_data(soup):
    # get the match details

    match_data = soup.find('div', class_='header-content-secondary').find_all('dd')
    match_data_headers = ['skill_bracket', 'lobby_type', 'game_mode', 'region', 'duration', 'match_date']

    final_match_data = {}

    for i in range(len(match_data_headers)):
        final_match_data[match_data_headers[i]] = match_data[i].text
    return final_match_data


def extract_team_data(soup, player_id):
    # get own team stats

    my_team_regex = re.compile('.*' + player_id + '.*')
    my_team = soup.find('tr', class_=my_team_regex)
    my_team_table = my_team.find_parent('table')
    team_stat_headers = ['team_k', 'team_d', 'team_a', 'team_net', 'team_lh', 'team_dn', 'team_gpm', 'team_xpm',
                         'team_dmg', 'team_heal', 'team_bld', 'team_wards']
    my_team_stats = my_team_table.find('tfoot').find_all('td')

    final_team_data = {}
    count = 0

    for i in my_team_stats:
        if i.text != '':
            # because the longer strings (name, item timing) omitted
            if len(i.text) < 10:
                final_team_data[team_stat_headers[count]] = i.text
                count += 1

    # wards data only sometimes (TrueSight), loop through to check
    for header in team_stat_headers:
        if header not in final_team_data.keys():
            final_team_data[header] = 0

    return final_team_data


def extract_own_data(soup, player_id):
    # extract my own data from my row

    my_regex = re.compile('.*' + player_id + '.*')
    my_row = soup.find('tr', class_=my_regex)
    my_hero = my_row.find('img', class_=re.compile('image-hero.+')).attrs['title']
    my_data = my_row.find_all('td')
    my_name = my_row.find('td', class_='tf-pl single-lines').text
    own_stat_headers = ['hero', 'final_lvl', 'k', 'd', 'a', 'net', 'lh', 'dn', 'gpm', 'xpm', 'dmg', 'heal', 'bld',
                        'wards', 'final_items']

    final_own_data = {}
    count = 1
    final_own_data[own_stat_headers[0]] = my_hero

    for i in my_data:
        if i.text != '':
            if len(i.text) < 10 and i.text != my_name:
                final_own_data[own_stat_headers[count]] = i.text
                count += 1

    # wards data only sometimes (TrueSight), loop through to check
    for header in own_stat_headers:
        if header not in final_own_data.keys():
            final_own_data[header] = 0

    # get final items

    my_items_regex = re.compile(r'image-item.+')
    my_items = my_row.find_all('img', class_=my_items_regex)
    final_items = ''

    for i in my_items:
        if final_items == '':
            final_items = i.attrs['title']
        else:
            final_items = final_items + ',' + i.attrs['title']

    final_own_data['final_items'] = final_items

    return final_own_data


def write_to_csv(player_name, fieldnames, link, result, final_match_data, final_own_data, final_team_data):
    with open('dota_match_data_' + player_name + '.csv', 'a', newline='') as f:
        # combine into one single dictionary
        combined_data = {'link': link, 'result': result}
        combined_data.update(final_match_data)
        combined_data.update(final_own_data)
        combined_data.update(final_team_data)

        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writerow({k: combined_data[k] for k in fieldnames})


