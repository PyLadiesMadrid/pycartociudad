"""
Reverse geocoding of a location using cartociudad API
"""

import requests



def reverse_geocode(latitude, longitude):
    """This function performs reverse geocoding of a location. It returns
    the details of the closest address in Spain.

    Parameters
    ----------
    latitude : float
        Point latitude in geographical coordinates (e.g., 40.473219)

    longitude: float
        Point longitude in geographical coordinates (e.g., -3.7227241)

    Returns
    -------
    addrs_details :  dictionary with the following items:
        * tipo:         type of location
        * tipoVia:      road type
        * nombreVia:    road name
        * numVia:       road number
        * numViaId:     internal id of this address in cartociudad database
        * municipio:    town
        * provincia:    province
        * codPostal:    zip code
    """
    pass