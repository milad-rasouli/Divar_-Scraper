import requests
import urllib.parse
import os
from dotenv import load_dotenv

load_dotenv()

def send_text_etta(text, date=0, parse_mode='html', pin=0, view_count_for_delete=None):
    token = os.getenv('TOKEN')
    chat_id = os.getenv('CHAT_ID')

    base_url = f'https://eitaayar.ir/api/{token}/sendMessage'
    
    # encoded_text = urllib.parse.quote(text)
    
    params = {
        'chat_id': chat_id,
        'text': text,
        'date': date,
        'parse_mode': parse_mode,
        'pin': pin,
    }
    
    if view_count_for_delete is not None:
        params['viewCountForDelete'] = view_count_for_delete
    
    try:
        response = requests.get(base_url, params=params)
        
        # print("Original text:", text)
        # print("Encoded text:", encoded_text)
        # print("Response:", response.text)
        print('message has been sent!')
    except Exception as e:
        print(f"An error occurred while sending: {e}")

# if __name__ == "__main__":
#     text = 'an example from ettaqwqw wq' 
#     date = 0
#     parse_mode = 'html'
#     # pin = 'off'
#     # view_count_for_delete = None

#     send_text_etta(text, date, parse_mode, pin, view_count_for_delete)
