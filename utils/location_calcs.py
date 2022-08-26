import math

from aiogram import types

R = 6378.1


def calc_distance(my_lat, my_long, barber_lat, barber_long):
    my_lat = math.radians(my_lat)
    my_long = math.radians(my_long)
    barber_lat = math.radians(barber_lat)
    barber_long = math.radians(barber_long)

    dlon = barber_long - my_long
    dlat = barber_lat - my_lat

    a = math.sin(dlat / 2) ** 2 + math.cos(my_lat) * math.cos(barber_lat) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c

    return distance


def choose_shortest(lat, long, barbers):
    distances = list()

    for barber in barbers:
        distances.append((
            barber[0],
            calc_distance(
                lat, long,
                barber[5], barber[4]
            )
        ))

    return sorted(distances, key=lambda x: x[1])
