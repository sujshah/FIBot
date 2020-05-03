import json
from functools import lru_cache
from typing import Generator, Dict, Set

import requests
from cache_to_disk import cache_to_disk
from bs4 import BeautifulSoup

from main import Player

url = 'https://www.premierleague.com/clubs'


def get_club_by_club_number() -> Dict[int, str]:
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    club_by_club_number = {}
    for i, tag in enumerate(soup.find_all('h4', class_='clubName')):
        club_by_club_number[i + 1] = tag.next
    return club_by_club_number


def get_players_from_club(club_num: int) -> Generator[Player, None, None]:
    page = requests.get(f'{url}/{club_num}/club/squad')
    soup = BeautifulSoup(page.text, 'html.parser')
    club = get_club_by_club_number()[club_num]
    for tag in soup.find_all('a', class_='playerOverviewCard active'):
        name, surname = None, None
        names = tag.find('h4', text=True).next.split(' ')
        if len(names) == 1:
            name = names[0]
        else:
            name, *surname = names
            if isinstance(surname, list):
                surname = ' '.join(surname)
        position = tag.find('span', class_='position').next
        number = tag.find('span', class_='number').next
        nationality = tag.find('span', class_='playerCountry').next
        yield Player(name=name,
                     surname=surname,
                     club=club,
                     nationality=nationality,
                     position=position,
                     number=number)


def get_premier_league_players() -> Set[Player]:
    result = set()
    for i in range(1, 21):
        for player in get_players_from_club(i):
            result.add(player)
    return result


if __name__ == '__main__':
    players = get_premier_league_players()
    with open('data.json', 'a+', encoding='utf-8') as f:
        json.dump(list(map(lambda player: player.__dict__, players)), f)



