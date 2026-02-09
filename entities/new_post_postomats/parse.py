import json

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from entities.new_post_postomats.services import get_postomat_number, get_postomat_address

city_title_slug_map = {
    "kyiv-1": "Київ",
    "ternopil-21985": "Тернопіль",
    "kharkiv-23043": "Харків",
    "lviv-13614": "Львів",
    "dnipro-3643": "Дніпро",
    "odesa-16453": "Одеса",
    "zaporizhzhia-8719": "Запоріжжя",
    "vinnytsia-1053": "Вінниця",
    "ivano-frankivsk-9672": "Івано-Франківськ",
    "poltava-17628": "Полтава"
}

city_max_pages = {
    "Київ": 311,
    "Тернопіль": 24,
    "Харків": 66,
    "Львів": 127,
    "Дніпро": 107,
    "Одеса": 66,
    "Запоріжжя": 41,
    "Вінниця": 47,
    "Івано-Франківськ": 15,
    "Полтава": 19
}

HEADERS = {"User-Agent": UserAgent().random}


def parse_postomats():
    result = []

    for city_id, city_title in city_title_slug_map.items():
        start_page = 1
        city_pages_count = city_max_pages[city_title]

        while start_page <= city_pages_count:
            print(f"Getting the {start_page} page for city {city_title}")
            try:
                response = requests.get(f"https://delengine.com/en/{city_id}/novaposhta?department_type_id=5&page={start_page}")
                response.raise_for_status()
                text = response.text
                soup = BeautifulSoup(text, "lxml")
                cards_content = soup.find_all("div", class_="row gx-2")
                for content in cards_content:
                    title = content.find("div", class_="h4 mb-0").text
                    address = content.find("div", class_="d-flex flex-wrap").text
                    postomat_dict = {
                        "city_title": city_title,
                        "number": get_postomat_number(title),
                        "address": get_postomat_address(address)
                    }
                    print(postomat_dict)
                    result.append(postomat_dict)
            except requests.exceptions.HTTPError:
                break
            except requests.RequestException as e:
                print(f"Error while getting office for {city_id}: {e}")
            start_page += 1
    return result


def save_postomats_in_file():
    offices = parse_postomats()
    with open("postomats.json", "w", encoding="utf-8") as f:
        json.dump(offices, f, ensure_ascii=False, indent=2)


def main():
    save_postomats_in_file()


if __name__ == "__main__":
    main()