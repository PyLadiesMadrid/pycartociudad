"""
Get the route between two points using cartociudad API
"""

import json
import requests


def route_between_two_points(lat_init: float, lon_init: float, lat_dest: float,
                             lon_dest: float, vehicle: bool = False) -> list:
    """This function get the route between two points.

    Parameters
    ----------
    lat_init : float
        Initial point latitude in geographical coordinates (e.g., 40.4166896)
    lon_init : float
        Initial point longitude in geographical coordinates (e.g., -3.7038101)
    lat_dest : float
        Final point latitude in geographical coordinates (e.g., 40.4113844)
    lon_dest : float
        Final point longitude in geographical coordinates (e.g., -3.7083022)

    vehicle: bool
        If True, uses vehicle, if False walking

    Returns
    -------
     :  List with the instructions to follow

    """

    # base url:
    base_url = f'http://www.cartociudad.es/services/api/route'\

    request_url = f'{base_url}?orig={lat_init},{lon_init}&dest={lat_init},{lon_dest}' \
                  f'&locale=es&vehicle={"CAR" if vehicle else "WALK"}'

    request_result = requests.get(request_url)

    if request_result.status_code != 200:
        return []

    instructions_raw = json.loads(request_result.text)['instructionsData']['instruction']

    instructions_list = [f'{item["description"]} {item["distance"]}.'
                         for item in instructions_raw]

    return instructions_list

