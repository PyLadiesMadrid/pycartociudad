"""Calls to Cartociudad geocoding API

Geolocation of Spanish addresses via Cartociudad API calls
"""

import requests


def geocode(full_address):
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
    pass
