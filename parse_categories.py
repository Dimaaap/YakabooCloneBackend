import requests
import json
from bs4 import BeautifulSoup
from slugify import slugify

def get_page():
    URL = "https://www.yakaboo.ua/ua/knigi/dobirki-yakaboo/premija-goodreads-choice-awards-2024.html"
    HEADERS = {"User-Agent": "Mozilla/5.0 (platform; rv:geckoversion) Gecko/geckotrail Firefox/firefoxversion"}

    response = requests.get(URL, headers=HEADERS)
    response.encoding = "utf-8"
    text = response.text
    return text

def parse_page(text):
    soup = BeautifulSoup(text, "lxml")
    subcategories_container = soup.find_all(class_="subcategory")
    subcategories = []
    for subcategory in subcategories_container:
        subcategory_images = subcategory.find_all("img")
        images = []
        for image in subcategory_images:
            images.append({"image_src": image.get("src")})
        subcategory_name = subcategory.find("span").get_text(strip=True)
        subcategories.append({
            "title": subcategory_name,
            "slug": slugify(subcategory_name),
            "images_src": images,
            "is_active": True,
            "subcategory_id": 167
        })
    with open("double_subcategories/subcategories.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(subcategories, indent=4, ensure_ascii=False))
        print("File created")


parse_page(get_page())