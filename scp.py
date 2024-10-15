import time
import sys
import hashlib
import requests
import playsound
from bs4 import BeautifulSoup

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
        
        for item in items:
            title = item.find('h2', class_='kt-post-card__title')
            title_text = title.get_text(strip=True) if title else 'No title found'
            descriptions = item.find_all('div', class_='kt-post-card__description')
            mileage = descriptions[0].get_text(strip=True) if len(descriptions) > 0 else 'No mileage info'
            price = descriptions[1].get_text(strip=True) if len(descriptions) > 1 else 'No price info'
            time_location = item.find('span', class_='kt-post-card__bottom-description')
            time_location_text = time_location.get('title', 'No time/location info') if time_location else 'No time/location info'
            # img_tag = item.find('img', class_='kt-image-block__image')
            # img_url = img_tag['src'] if img_tag else 'No image found'
            
            tip = f"{title_text}{mileage}{price}{time_location_text}"
            hash_item = hashlib.md5(tip.encode('utf-8')).hexdigest()
            global cards 
            if hash_item not in cards:
                cards.add(hash_item)
                print(f"Title: {title_text}")
                print(f"Mileage: {mileage}")
                print(f"Price: {price}")
                print(f"Time/Location: {time_location_text}")
                # print(f"Image URL: {img_url}")
                print('-' * 50)
                new = True
            # else:
            #     print(hash_item, " is already in the set.")
            

    else:
        print(f"Failed to retrieve page, status code: {response.status_code}")

    return new

# url = "https://divar.ir/s/mashhad/car?q=%D9%BE%D8%A7%D8%B1%D8%B3&body_status=intact&usage=-130000&price=200000000-300000000"
interval = float(sys.argv[1])
url = "https://divar.ir/s/mashhad/car?q=%D9%BE%D8%B1%D8%A7%DB%8C%D8%AF&motor_status=healthy&usage=-130000&price=200000000-300000000&body_status=intact"
print("Request for ",url)
try:
    while True:
        # i = i+1
        # print('request times: ', i)
        is_new = fetch_and_parse(url)
        if is_new == True:
            playsound.playsound("mixkit-small-door-bell-589.wav")
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