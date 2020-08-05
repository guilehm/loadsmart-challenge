import csv
import logging
import os
import sys
from math import asin, cos, radians, sin, sqrt

EARTH_RADIUS = 6371


def haversine(origin_lat, origin_lng, destination_lat, destination_lng, earth_radius=EARTH_RADIUS):
    lat, lng, des_lat, des_lng = map(radians, map(float, [origin_lat, origin_lng, destination_lat, destination_lng]))
    distance_lat = des_lat - lat
    distance_lng = des_lng - lng

    a = sin(distance_lat / 2) ** 2 + cos(lat) * cos(des_lat) * sin(distance_lng / 2) ** 2
    c = 2 * asin(sqrt(a))

    km = earth_radius * c
    return km


def get_csv_reader(filename):
    with open(f'{os.getcwd()}/src/resources/{filename}.csv', 'r') as file:
        reader = csv.DictReader(file.read().splitlines())
    return reader


def get_logger():
    logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(message)s')
    return logging
