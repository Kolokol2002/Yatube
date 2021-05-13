from pprint import pprint
import os
from dotenv import load_dotenv
import requests
# https://oauth.vk.com/authorize?client_id=XXXXXX&scope=friends&response_type=token&v=5.92

load_dotenv()
token = os.getenv('Token')


result = requests.get(f"https://api.vk.com/method/users.get?user_id=210700286&v=5.92&access_token={token}")
vk = result.json()

def get_friends(user_id):
    data = {
        'user_id': user_id,
        'v': '5.92',
        'access_token': token,
    }
    friends_list = requests.post('https://api.vk.com/method/friends.get??user_id=&v=&access_token=', data) # ваш код здесь
    return friends_list.json()['response']

print(get_friends(531301803))

