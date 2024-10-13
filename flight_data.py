import os
import requests
import datetime
from dotenv import load_dotenv
from flight_search import FlightSearch

load_dotenv()



class FlightData:
    # This class is responsible for structuring the flight data.

    def __init__(self, price, origin_airport, destination_airport, out_date, return_date, stop):
        self.prices = price
        self.origin_airport = origin_airport
        self.destination_airport = destination_airport
        self.out_date = out_date
        self.return_date = return_date
        self.stops = stop


def find_cheapest_flights(data):
    if data is None or not data['data']:
        print('No flight Data')
        return FlightData(
            'N/A',
            'N/A',
            'N/A',
            'N/A',
            'N/A',
            'N/A'
        )

    # if destination has more than 1 segment then the first destination will become the new iata and we will
    # calculate from there until we reach ['itineraries'][-1], the last segment in the itineraries list

    first_flight = data['data'][0]
    lowest_price = float(first_flight['price']['grandTotal'])
    stops = len(first_flight['itineraries'][0]['segments']) - 1
    origin = first_flight['itineraries'][0]['segments'][0]['departure']['iataCode']
    destination = first_flight['itineraries'][0]['segments'][stops]['arrival']['iataCode']
    out_date = first_flight['itineraries'][0]['segments'][0]['departure']['at'].split('T')[0]
    return_date = first_flight['itineraries'][1]['segments'][0]['departure']['at'].split('T')[0]

    cheapest_flights = FlightData(lowest_price, origin, destination, out_date, return_date, stops)

    for flights in data['data']:
        price = float(flights['price']['grandTotal'])
        if price < lowest_price:
            origin = flights['itineraries'][0]['segments'][0]['departure']['iataCode']
            destination = flights['itineraries'][stops]['segments'][0]['arrival']['iataCode']
            out_date = flights['itineraries'][0]['segments'][0]['departure']['at'].split('T')[0]
            return_date = flights['itineraries'][1]['segments'][0]['departure']['at'].split('T')[0]
            cheapest_flights = FlightData(lowest_price, origin, destination, out_date, return_date, stops)

            print(f'Lowest price to {destination} is ${lowest_price}')

    return cheapest_flights



