"""
Obtain static image map of an address 
using cartociudad API
"""

import requests
import urllib
from PIL import Image
from math import radians, cos, sin, asin, sqrt
#import shutil

import geocode

def haversine(lon1: float, lat1: float, lon2: float, lat2: float) -> float:
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r

def get_bounding_box(lat: float, lon: float, radiusKm: float, aspectRatio: float) -> list:
    """
    Creates the bbox centered on a point with coords (lat,lon)

    Parameters
    ----------
    lat: float
        central point latitude

    lon: float
        central point longitude

    radiusKm: float
        area covered by the map (from center to the sides)

    aspectRatio: float
        height/width of the map

    Returns
    -------
    bbox: list of float
        list of coordinates in EPSG 4326 representation:
        [bottom lat, left long, upper lat, right long]

    """

    assert radiusKm > 0

    delta = 0.5 # This is sort of a magic number ?
    deltaLon = radiusKm * delta * haversine(lon, lat, lon+delta, lat) / 2000
    deltaLat = radiusKm * delta * haversine(lon, lat, lon, lat+delta) / 2000
    deltaLat = deltaLat * aspectRatio

    bbox = [lat - deltaLat, # bottom lat
            lon - deltaLon, # left lon
            lat + deltaLat, # upper lat
            lon + deltaLon] # right lon
            
    bbox = ['{:.12f}'.format(x) for x in bbox]

    return bbox

def get_layer_img(url: str, searchContent: str) -> Image.Image:
    qParams = urllib.parse.urlencode(searchContent)
    """Helper function to download the layer image
    """
    # perform request
    r = requests.get(url=url, params=qParams, stream=True)
    
    # Get image from the API response
    if r.status_code == 200:
        r.raw.decode_content = True
        layerImg = Image.open(r.raw)
        r.close()

    return layerImg


def get_map(center: tuple, radius: float, 
    height: float = 600, width: float = 800,
    censalLayer: bool = False, 
    postLayer: bool = False, 
    cadastralLayer: bool = False) -> Image.Image:
    """This function downloads a map from CartoCiudad API centered on
    a geographical point and returns it as a PIL image.

    Parameters
    ----------
    center : tuple of str
        (latitude, longitude) coordinates to center the map

    radius: float
        Map coverage in kilometers

    height: int
        Returned map height in pixels (default 600)

    width: int
        Returned map width in pixels (default 800)

    censalLayer: bool
        Option to add the limit of censal sections and districts to the
        base map; note that this layer may not be available at low zoom
        levels

    postLayer: bool
        Option to add the limit of zip code areas to the base map; note
        that this layer may not be available at low zoom levels

    cadastralLayer: bool
        Option to add cadastral information

    Returns
    -------
    image :  PIL image of height x width pixels
    """

    # build query content
    bbox = get_bounding_box(float(center[0]),
                            float(center[1]),
                            float(radius),
                            float(height)/width)

    url = 'http://www.ign.es/wms-inspire/ign-base'
    searchContent = {'service': 'WMS',
                     'version': '1.3.0',
                     'request': 'GetMap',
                     'format': 'image/png',
                     'transparent': 'true',
                     'layers': 'IGNBaseTodo',
                     'styles': 'default',
                     'exceptions': 'xml',
                     'srs': 'EPSG:4326',
                     'width': str(width),
                     'height': str(height),
                     'bbox': ','.join(bbox)
                    }
    bgLayerImg = get_layer_img(url, searchContent)

    if postLayer:
        url = 'http://www.ign.es/wms-inspire/ign-base'
        searchContent = {'service': 'WMS',
                         'version': '1.3.0',
                         'request': 'GetMap',
                         'format': 'image/png',
                         'transparent': 'true',
                         'layers': 'codigo-postal',
                         'styles': 'codigopostal',
                         'exceptions': 'xml',
                         'srs': 'EPSG:4326',
                         'width': str(width),
                         'height': str(height),
                         'bbox': ','.join(bbox)
                        }
        fgLayerImg = get_layer_img(url, searchContent)
        bgLayerImg.paste(fgLayerImg, (0,0), fgLayerImg.convert('RGBA'))


    ## Code to download image locally
    #r.raw.decode_content = True

    #with open('image_name.png', 'wb') as handler:
    #    shutil.copyfileobj(r.raw, handler)
    #del r

    return bgLayerImg

