"""
Get the route between two points using cartociudad API
"""

import re
import json
import requests


def route_between_two_points(lat_init: float, lon_init: float, lat_dest: float,
                             lon_dest: float, vehicle: bool = False,
                             error: str = 'raise') -> dict:
    """This function get the route between two points.

    Parameters
    ----------
    :param lat_init : float
        Initial point latitude in geographical coordinates (e.g., 40.4166896)
    :param lon_init : float
        Initial point longitude in geographical coordinates (e.g., -3.7038101)
    :param lat_dest : float
        Final point latitude in geographical coordinates (e.g., 40.4113844)
    :param lon_dest : float
        Final point longitude in geographical coordinates (e.g., -3.7083022)
    :param vehicle: bool
        If True, uses vehicle, if False walking
    :param error: str
        if 'raise', an error would be raise, if 'ignore, just return an
        empty list.
    Returns
    -------
     :  dict with the following info:
        * 'bbox': list of four points of the bbox
        * 'distance': (float) distance in meters
        * 'found': bool if result is found
        * 'from': str with the two starting points given by the user
        * 'geom': hash
        * 'info': dist with info
        * 'instructionsData: dict with the instructions
        * 'time': time that takes (float)
        * 'to': final destination point given by user

    """

    # base url:
    base_url = f'http://www.cartociudad.es/services/api/route'
    request_url = f'{base_url}?orig={lat_init},{lon_init}&dest={lat_dest},{lon_dest}' \
                  f'&locale=es&vehicle={"CAR" if vehicle else "WALK"}'

    # perform request
    try:
        request_result = requests.get(request_url)
        if error == 'raise':
            request_result.raise_for_status()
        elif error == 'ignore':
            return {}
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)

    # load results
    try:
        instructions_raw = json.loads(request_result.text)
        if error == 'ignore':
            request_result = {}
    except json.JSONDecodeError as err:
        raise SystemExit(err)

    if instructions_raw['found'] == 'false':
        # Can not find the route
        if error == 'raise':
            raise SystemExit()
        elif error == 'ignore':
            return {}

    # parse to float
    instructions_raw['distance'] = float(instructions_raw['distance'])
    instructions_raw['time'] = float(instructions_raw['time'])

    # parse to float in each instruction:
    re_pattern = r"(\d+) m"
    for item in instructions_raw['instructionsData']['instruction']:
        distance_item = item['distance']
        distance_found = re.findall(re_pattern, distance_item)

        if distance_found and len(distance_found) == 1:
            item['distance'] = float(distance_found[0])

    return instructions_raw

