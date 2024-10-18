import time
import sys
import hashlib
import requests
import os
from bs4 import BeautifulSoup
from d import fetch_description
from etta import send_text_etta,send_picture_etta

cards= set()

def fetch_and_parse(url):
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0"
    }
    response = requests.get(url, headers=headers)
    # response = requests.get(url)
    new = False
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        items = soup.find_all('article', class_='kt-post-card')
        base_url = "https://divar.ir"
        for item in reversed(items):
            link_tag = item.find('a', href=True)
            item_url = base_url + link_tag['href'] if link_tag else 'No URL found'

            title = item.find('h2', class_='kt-post-card__title')
            title_text = title.get_text(strip=True) if title else 'No title found'
            descriptions = item.find_all('div', class_='kt-post-card__description')
            mileage = descriptions[0].get_text(strip=True) if len(descriptions) > 0 else 'No mileage info'
            price = descriptions[1].get_text(strip=True) if len(descriptions) > 1 else 'No price info'
            time_location = item.find('span', class_='kt-post-card__bottom-description')
            time_location_text = time_location.get('title', 'No time/location info') if time_location else 'No time/location info'
            # img_tag = item.find('img', class_='kt-image-block__image')
            # img_url = img_tag['src'] if img_tag else 'No image found'
            location_text = str
            time_text = str
            if "در" in time_location_text:
                tl = str(time_location_text).split("در")
                location_text = tl[-1]
                time_text = tl[0]
            else:
                location_text = "Location not found"
                time_text = "Time not found"
            
            key = f"{title_text}{mileage}{price}{location_text}"
            hash_item = hashlib.md5(key.encode('utf-8')).hexdigest()
            global cards 
            if hash_item not in cards:
                cards.add(hash_item)
                if len(cards)>100:
                    cards.pop()
                print(f"Title: {title_text}")
                print(f"Mileage: {mileage}")
                print(f"Price: {price}")
                print(f"Location: {location_text}")
                print(f"Time: {time_text}")
                # do for the decription
                c,d,ip = fetch_description(item_url)
                print(f"Description: {d}")
                print(f"Color: {c}")
                print(f"URL: {item_url}")
                # print(f"Image URL: {img_url}")
                cap = f'{title_text}\n{mileage}\n{price}\n{location_text}\n{time_text}\n{c}\n{d}\n{item_url}'
                if ip != None:
                    send_picture_etta(cap,' ',ip)
                    os.remove(ip)
                else:
                    send_text_etta(cap)
                print('-' * 50)
                new = True
            # else:
            #     print(hash_item, " is already in the set.")
            

    else:
        print(f"Failed to retrieve page, status code: {response.status_code}")

    return new

interval = float(sys.argv[1])
# url = "https://divar.ir/s/mashhad/car?q=%D9%BE%D8%B1%D8%A7%DB%8C%D8%AF&motor_status=healthy&usage=-130000&price=200000000-300000000&body_status=intact"
url = "https://divar.ir/s/mashhad/car?q=%D8%AA%DB%8C%D8%A8%D8%A7&business-type=all&usage=-200000&price=-300000000&motor_status=healthy&has-photo=true&chassis_status=both-healthy&body_status=intact%2Csome-scratches"
print("Request for ",url)
try:
    while True:
        # i = i+1
        # print('request times: ', i)
        is_new = fetch_and_parse(url)
        if is_new == True:
            file = "mixkit-small-door-bell-589.wav"
            os.system("smplayer -close-at-end -minigui " + file)
        time.sleep(interval) # 30    
except KeyboardInterrupt:
    print("Exiting loop!")





# ll = ['dfgdf','sdfsdf','ddd','ddd']

# for x in ll:
#     print(x)
#     hash_item = hashlib.md5(x.encode('utf-8')).hexdigest()
#     print(hash_item)
#     if hash_item not in items:
#         items.add(hash_item)
#     else:
#         print(hash_item, " is already in the set.")
