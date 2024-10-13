import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
load_dotenv()




class DataManager:
    # This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.sheety_api = os.getenv('SHEETY_PRICES_API')
        self.sheety_users_api = os.getenv('SHEETY_USERS_API')
        self._user = os.getenv('sheety_name')
        self._password = os.getenv('sheety_password')
        self.authorization = HTTPBasicAuth(self._user, self._password)
        self.sheety_header = {
            "Authorization": 'Basic bG91X2RhdmU6YmFuYW5hX2JhbmQ='
        }
        self.destination_data = {}
        self.user_data = {}

    def get_destination_data(self):
        response = requests.get(url=self.sheety_api, headers=self.sheety_header)
        data = response.json()
        self.destination_data = data['prices']
        return self.destination_data

    def update(self):
        for city in self.destination_data:
            data_to_update = {
                'price': {
                    'iataCode': city['iataCode']
                }
            }
            response1 = requests.put(url=f'{self.sheety_api}/{city['id']}', json=data_to_update, headers=self.sheety_header)
            print(response1.text)


    def get_customer_emails(self):
        customer_response = requests.get(url=self.sheety_users_api, headers=self.sheety_header)
        data = customer_response.json()
        self.user_data = data['users']
        return self.user_data
