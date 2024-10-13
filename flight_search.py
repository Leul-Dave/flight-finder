import os
import requests
from dotenv import load_dotenv

load_dotenv()

token_endpoint = os.getenv('TOKEN_ENDPOINT')
iata_endpoint = os.getenv('IATA_ENDPOINT')
flight_endpoint = os.getenv('FLIGHT_ENDPOINT')


class FlightSearch:
    # This class is responsible for talking to the Flight Search API.

    def __init__(self):
        self.amadeus_api_key = os.getenv('amadeus_api_key')
        self.amadeus_api_secret = os.getenv('amadeus_api_secret')
        self.token = self._get_new_token()

    def _get_new_token(self):
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        body = {
            'grant_type': 'client_credentials',
            'client_id': self.amadeus_api_key,
            'client_secret': self.amadeus_api_secret
        }
        response = requests.post(url=token_endpoint, headers=headers, data=body)
        response.raise_for_status()
        return response.json()['access_token']

    def get_destination_code(self, city_name):
        headers = {
            "Authorization": f'Bearer {self.token}'
        }

        parameters = {
            'keyword': city_name,
            'max': '2',
            'include': 'AIRPORTS'
        }

        iata_response = requests.get(url=iata_endpoint, headers=headers, params=parameters)
        try:
            iata_code = iata_response.json()['data'][0]['iataCode']
        except IndexError:
            print(f'Did not find the code for {city_name}')
            return 'N/A'
        except KeyError:
            print(f'Did not find the code for {city_name}')
            return 'None found'

        return iata_code

    def check_flights(self, origin_city_code, destination_city_code, from_time, to_time, is_direct=True):
        headers = {
            "Authorization": f'Bearer {self.token}'
        }
        parameters = {
            'originLocationCode': origin_city_code,
            'destinationLocationCode': destination_city_code,
            'departureDate': from_time.strftime('%Y-%m-%d'),
            'returnDate': to_time.strftime('%Y-%m-%d'),
            'adults': 1,
            'currencyCode': 'GBP',
            'nonStop': 'true' if is_direct else 'false',
            'max': '10'

        }
        flights_response = requests.get(
            url=flight_endpoint,
            params=parameters,
            headers=headers
        )
        if flights_response.status_code != 200:
            print(f'check_flights() response code: {flights_response.status_code}')
            return None

        return flights_response.json()
