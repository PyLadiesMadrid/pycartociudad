"""
Reverse geocoding of a location using cartociudad API
"""

import requests
import urllib
import json


def reverse_geocode(latitude: float, longitude: float, cadastral: bool = False, error: str = 'raise') -> dict:
    """This function performs reverse geocoding of a location in Spain.
    It returns the closest address details (or cadastral details if)  a
    cadastral reverse geocode is done.

    Parameters
    ----------
    latitude : float
        Point latitude in geographical coordinates (e.g., 40.473219)

    longitude: float
        Point longitude in geographical coordinates (e.g., -3.7227241)

    cadastral: bool (optional) (default: False)
        Set to True if performing cadastral address reverse geocoding

    Returns
    -------
    addrs_details :  dictionary with the following items
    ** For non cadastral searches **:
        * id:                Ref identifier
        * province:          (if applicable) Province to which the
                             location belongs.
        * comunidadAutonoma: (if applicable) Autonomous community to
                             which the location belongs.
        * muni:              Municipality to which the location belongs
        * type:              Entity type
        * address:           Result name
        * postalCode:        Codigo postal (si corresponde)
        * poblacion:         Town to which the location belongs
        * geom:              GML geometry
        * tip_via:           Street (1) or road (2)
        * lat:               Latitude
        * lng:               Longitude
        * portalNumber:      Street/km number
        * stateMsg:          Geometry computation result
        * state:             Digit indicating the geometry computation
                             result:
            · 1: exact result
            · 2: even street number not found
            · 3: odd street number not found
            · 4: km number not found (closest is returned)
            · 5: street/km number not found
            · 6: Type does not match query
            · 10: no results found, higher entity returned
        * priority:          Priority (?)
        * countryCode:       Country code (default 011 for Spain)

    ** For cadastral searches **: Same fields but
        * address:           Address as registered in Cadastre
        * refCatastral:      Cadastral reference
    """

    # build query content
    searchContent = {'lat': latitude,
                     'lon': longitude}
    if cadastral:
        searchContent['type'] = 'refcatastral'

    qParams = urllib.parse.urlencode(searchContent)

    url = 'http://www.cartociudad.es/geocoder/api/geocoder/reverseGeocode'

    # perform request
    try:
        r = requests.get(url=url, params=qParams)
        if error == 'raise':
            r.raise_for_status()
        elif error == 'ignore':
            return {}
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)

    try:
        addrs_details = json.loads(r.text)
        if error == 'ignore':
            addrs_details = {}
    except json.JSONDecodeError as err:
        raise SystemExit(err)

    return addrs_details
