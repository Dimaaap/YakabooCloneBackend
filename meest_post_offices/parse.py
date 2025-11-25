import requests
from fake_useragent import UserAgent
import json

city_title_id_map = {
    "5cb61671-749b-11df-b112-00215aee3ebe": "Київ",
    "87162365-749b-11df-b112-00215aee3ebe": "Харків",
    "62c3d54a-749b-11df-b112-00215aee3ebe": "Львів",
    "50c5951b-749b-11df-b112-00215aee3ebe": "Дніпро",
    "6ed81d37-749b-11df-b112-00215aee3ebe": "Одеса",
    "56bdd4c6-749b-11df-b112-00215aee3ebe": "Запоріжжя",
    "4aba3d28-749b-11df-b112-00215aee3ebe": "Вінниця",
    "80f55c6a-749b-11df-b112-00215aee3ebe": "Тернопіль",
    "56bdd87c-749b-11df-b112-00215aee3ebe": "Івано-Франківськ",
    "74dc4d38-749b-11df-b112-00215aee3ebe": "Полтава"
}

BASE_URL = "https://geo.meest.com/api/v1/branch/all?from=0&city_id="
HEADERS = {"User-Agent": UserAgent().random}


def parse_offices():
    result = []

    for city_id, city_title in city_title_id_map.items():
        try:
            response = requests.get(f"{BASE_URL}{city_id}", headers=HEADERS)
            response.raise_for_status()
            json_data = response.json()
        except requests.RequestException as e:
            print(f"Error while getting office for {city_title} : {e}")
            continue

        city_offices = json_data.get("result", {}).get("data", {})

        for office in city_offices:
            result.append({
                "city_title": city_title,
                "office_number": office.get("local_branch_number"),
                "address": f"{office.get("street_name_ua", "")}, {office.get("house")}",
            })
    return result


def save_offices_in_file():
    offices = parse_offices()
    with open("offices.json", "w", encoding="utf-8") as f:
        json.dump(offices, f, ensure_ascii=False, indent=2)


def main():
    save_offices_in_file()


if __name__ == "__main__":
    main()
