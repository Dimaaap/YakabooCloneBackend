import requests
import xmltodict
from fake_useragent import UserAgent
import pprint
import json

city_title_id_map = {
    29713: "Київ",
    1057: "Вінниця",
    3641: "Дніпро",
    8698: "Запоріжжя",
    9826: "Івано-Франківськ",
    14288: "Львів",
    17069: "Одеса",
    19234: "Полтава",
    22662: "Тернопіль",
    24550: "Харків"
}

BASE_URL = "https://www.ukrposhta.ua/address-classifier/get_postoffices_postdistricts_web"
HEADERS = {"User-Agent": UserAgent().random}


def parse_offices():
    result = []

    for city_id, city_title in city_title_id_map.items():
        city_office = []
        offices = {city_title: city_office}

        city_offices = requests.get(f"{BASE_URL}?pdCityId={city_id}", headers=HEADERS)
        if city_offices.status_code != 200:
            continue
        xml_text = city_offices.text
        data = xmltodict.parse(xml_text, process_namespaces=False)
        entries = data.get("Entries", {}).get("Entry", [])

        if isinstance(entries, dict):
            entries = [entries]


        for office in entries:
            street = office.get("STREET_UA")
            house = office.get("HOUSENUMBER")
            po_short = office.get("PO_SHORT")
            office_id = office.get("ID")

            address = f"{street}, {house}" if street and house else street or None

            city_office.append({
                "office_id": office_id,
                "address": address,
                "po_short": po_short,
            })
        result.append(offices)
    return result


def save_offices_in_file():
    offices = parse_offices()
    with open("offices.json", "w", encoding="utf-8") as f:
        json.dump(offices, f, ensure_ascii=False, indent=2)


def main():
    save_offices_in_file()


if __name__ == '__main__':
    main()