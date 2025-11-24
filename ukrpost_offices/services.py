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
    with open("ukrpost_offices/offices.json", encoding="utf-8") as file:
        data = json.load(file)
        return data


def get_office_number_in_city(city_number: str) -> int:
    if "№" in city_number:
        city, number = city_number.split("№")
    elif "П-т" in city_number or "ВВ" in city_number:
        _, city, number = city_number.split()
    elif len(city_number.split()) == 1:
        return 1
    else:
        city, number, *_ = city_number.split()
    return int(number)



def convert_json_offices_format():
    data = []
    offices_json = read_offices_from_json()
    for office in offices_json:
        for city_title, offices_list in office.items():
            for office_item in offices_list:
                office_data = {
                    "city_id": cities_id_map[city_title],
                    "office_number": int(office_item["office_id"]),
                    "address": office_item["address"],
                    "number_in_city": get_office_number_in_city(office_item["po_short"])
                }
                data.append(office_data)
    return data


convert_json_offices_format()