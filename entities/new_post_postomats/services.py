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


def get_postomat_number(number: str):
    post_number = number.split()[2]
    return post_number


def get_office_weight_to(number: str):
    if "up to" in number:
        return int(number.split()[5])
    return None


def get_postomat_address(address: str):
    address = address.strip()
    street = " ".join(address.split()[2:])
    return street


def read_postomats_from_json():
    with open("postomats.json", encoding="utf-8") as f:
        data = json.load(f)
        return data


def read_offices_from_json():
    with open("../new_post_offices/offices.json", encoding="utf-8") as f:
        data = json.load(f)
        return data


def convert_json_postomats_format():
    data = []
    postomats_json = read_postomats_from_json()
    for postomat in postomats_json:
        postomat_data = {
            "city_id": cities_id_map[postomat["city_title"]],
            "number": int(postomat["number"]),
            "address": postomat["address"]
        }
        data.append(postomat_data)

    return data


def convert_json_offices_format():
    data = []
    offices_json = read_offices_from_json()
    for office in offices_json:
        office_data = {
            "city_id": cities_id_map[office["city_title"]],
            "number": int(office["number"]),
            "address": office["address"],
            "weight_to": office["weight_to"]
        }
        data.append(office_data)
    return data


def format_office_address(address: str):
    if "ункт" in address:
        address = address.lstrip("")
        address = address.split()[2:]
        return "пункт " + " ".join(address)
    return " ".join(address.split()[1:])