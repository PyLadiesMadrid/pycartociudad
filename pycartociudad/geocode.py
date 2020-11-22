"""Calls to Cartociudad geocoding API

Geolocation of Spanish addresses via Cartociudad API calls
"""
import requests
import urllib
import json


def geocode(full_address: str):
    """This function performs the geocoding of an address. It returns
    the details of the closest address in Spain.

    Parameters
    ----------
    full_address : str
        Character string providing the full address to be
        geolocated; e.g., "calle miguel servet 5, zaragoza".
        Adding the country may cause problems.

    Returns
    -------
    geolocation
        A dictionary consisting of location guess
        * id
        * province
        * comunidadAutonoma
        * muni
        * type
        * address
        * poblacion
        * geom
        * lat
        * lng
        * portalNumber
        * stateMsg
        * state
        * countryCode
    """
    # check & parse parameter
    if not full_address:
        return {}
    
    if not isinstance(full_address, str):
        full_address = str(full_address)

    full_address = urllib.parse.quote(full_address)

    # build url
    url = f'http://www.cartociudad.es/geocoder/api/geocoder/findJsonp?q={full_address}'

    # perform request
    r = requests.get(url)

    # format output
    result = r.text.replace('callback(', '')[:-1]
    result = json.loads(result)

    return result or {}
