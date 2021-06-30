import math 
import requests
from pathlib import Path
from bs4 import BeautifulSoup


GOOGLE_IMAGES = "https://www.google.com/search?gbv=2&sxsrf=ALeKk013-aPRFAbl1W6dz8feGoIr_KxFjA:1624952066702&source=lnms&tbm=isch&sa=X&ved=2ahUKEwi3r9mVqrzxAhX8zzgGHSTFAPwQ_AUoAXoECAEQAw&biw=778&bih=625"
USER_AGENT = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3",
    "Accept-Encoding": "none",
    "Accept-Language": "en-US,en;q=0.8",
    "Connection": "keep-alive",
}

def save_image(link, i, what, where, ext = "jpg"):
    response = requests.get(link)
    image_name = f"{where}/{what}-{i}.{ext}"
    with open(image_name, 'wb') as file:
        file.write(response.content)


def download_images(what, how_many=20, where=""):
    if not where: where = what
    Path(where).mkdir(parents=True, exist_ok=True)

    images_per_page = 20
    iterations = math.ceil(how_many / images_per_page)


    for i in range(iterations):
        url = f"{GOOGLE_IMAGES}&q={what}&start={i*images_per_page}"

        response = requests.get(url, headers=USER_AGENT)
        html = response.text

        soup = BeautifulSoup(html, 'html.parser')
        limit = (how_many - i*images_per_page) if i == iterations-1 else images_per_page
        image_tags = soup.findAll('img', {'class': 't0fcAb'}, limit=limit)
        
        for j, image_tag in enumerate(image_tags):
            image_link = image_tag.get_attribute_list("src")[0]
            save_image(image_link, ((i*images_per_page) + j+1), what, where)


def main():
    download_images("cats", 35, "data/cats")

if __name__ == '__main__':
    main()