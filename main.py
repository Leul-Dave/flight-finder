import time
import datetime
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import find_cheapest_flights
from notification_manager import NotificationManager
from pprint import pprint

tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
six_months_later = datetime.datetime.now() + datetime.timedelta(days=180)
origin_city_code = 'LON'

# This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.

data_manager = DataManager()
sheet_data = data_manager.get_destination_data()
user_data = data_manager.get_customer_emails()
flight_search = FlightSearch()
notification = NotificationManager()

for row in sheet_data:
    if row['iataCode'] == '':
        row['iataCode'] = flight_search.get_destination_code(row['city'])
        time.sleep(2)

# print(f'{sheet_data}')
data_manager.destination_data = sheet_data
data_manager.update()


email_list = [row['email'] for row in user_data]


for row in sheet_data:
    print('Finding direct flights')
    flights = flight_search.check_flights(
        origin_city_code,
        row['iataCode'],
        tomorrow,
        six_months_later
    )
    cheapest_flight = find_cheapest_flights(flights)
    print(f'{row['city']}: ${cheapest_flight.prices}')
    time.sleep(2)

    if cheapest_flight.prices == 'N/A':
        print(f'No direct flights to {row['city']}')
        stopOver_flights = flight_search.check_flights(
            origin_city_code,
            row['iataCode'],
            tomorrow,
            six_months_later,
            is_direct=False
        )
        cheapest_flight = find_cheapest_flights(stopOver_flights)
        print(f'Cheapest indirect flight price ${cheapest_flight.prices}')
    body = f'Low price alert! Only GBP{cheapest_flight.prices} to fly from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, on {cheapest_flight.out_date} until {cheapest_flight.return_date}.'

    if cheapest_flight.prices != 'N/A' and cheapest_flight.prices < row['lowestPrice']:
        if cheapest_flight.stops == 0:
            notification.send_mail(body, ','.join(email_list))

    # if cheapest_flight.prices != 'N/A' and cheapest_flight.prices < row['lowestPrice']:
    #     notification.send_message(body=f'Low price alert! Only ${cheapest_flight.prices} to fly '
    #                                    f'from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, '
    #                                    f'on {cheapest_flight.out_date} until {cheapest_flight.return_date}.')
    # time.sleep(2)
