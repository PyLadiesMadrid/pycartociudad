"""
Get the route between two points using cartociudad API
"""

import requests


def route_between_two_points(lat_init: float, lon_init: float, lat_dest: float,
                             lon_dest: float, vehicle: bool = False) -> dict:
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
     :  dictionary with the following items:

    """

    pass


