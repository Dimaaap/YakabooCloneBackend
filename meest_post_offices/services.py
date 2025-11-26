import json

cities_id_map = {
    "Вінниця": 1,
    "Дніпро": 2,
    "Запоріжжя": 3,
    "Івано-Франківськ": 4,
    "Київ": 5,
    "Львів": 6,
    "Одеса": 7,
    "Полтава": 8,
    "Тернопіль": 9,
    "Харків": 10
}


def read_offices_from_json():
    with open("offices.json", encoding="utf-8") as f:
        data = json.load(f)
        return data


def convert_json_offices_format():
    data = []
    offices_json = read_offices_from_json()
    for office in offices_json:
        office_data = {
            "city_id": cities_id_map[office["city_title"]],
            "office_number": office["office_number"],
            "address": office["address"]
        }
        data.append(office_data)
    return data
