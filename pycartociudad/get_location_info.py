"""
Get extra information of a location using official spanish web map services
"""

from typing import List
import requests
import xml.etree.ElementTree as ET
from pycartociudad import reverse_geocode


def get_location_info(latitude: float, longitude: float, sources: List[str] = None):
    """Retrieves info from the given location and specified sources. Allowed sources are cadastre, census and geocoding.

    Parameters
    ----------
    latitude: float
        Point latitude in geographical coordinates (e.g., 40.473219)

    longitude: float
        Point longitude in geographical coordinates (e.g., -3.7227241)

    sources: list of str
        List of sources to retrieve the data from (e.g. ["cadastre", "census"]).
        Allowed values are ["cadastre", "census", "geocoding"].
        Default value is None and will retrieve the data from all the sources.

            * "cadastre": retrieves from the spanish cadastre API the cadastral reference of the location
            * "census": retrieves from the spanish statistics institute API the census section and district codes
            * "geocoding": retrieves from cartociudad API the geocoding data (same as using the
              function ``pycartociudad.reverse_geocode``)

    Returns
    -------
    location_information: a dict with the following elements:

        * cadastral_ref: the cadastral reference. Only if cadastre source is selected.
        * census_section: the census section. Only if census source is selected.
        * district_code: the district code. Only if census source is selected.
        * tipo, tipoVia, ... and rest of the fields from ``pycartociudad.reverse_geocode``: the geocoding data.
          Only if "geocoding" is selected.
    """
    # Check the parameters
    cadastre_source = "cadastre"
    census_source = "census"
    geocoding_source = "geocoding"
    all_sources = [cadastre_source, census_source, geocoding_source]

    if sources is None:
        sources = all_sources

    invalid_sources = set(sources) - set(all_sources)
    if invalid_sources:
        raise ValueError(f"Invalid sources: {', '.join(invalid_sources)}")

    # Retrieve the information from the specified sources
    result = {}
    if cadastre_source in sources:
        result["cadastral_ref"] = get_cadastral_reference(latitude, longitude)
    if census_source in sources:
        census_data = get_census_info(latitude, longitude)
        result["census_section"] = census_data.get("census_section")
        result["district_code"] = census_data.get("district_code")
    if geocoding_source in sources:
        geocoding_data = reverse_geocode(latitude, longitude, cadastral=False) or {}
        result = {**result, **geocoding_data}

    return result


def get_cadastral_reference(latitude: float, longitude: float, srs: str = "EPSG:4326"):
    """Performs a request to the spanish cadastre web API. It returns the cadastral reference of the given location.

    Parameters
    ----------
    latitude: float
        Point latitude in geographical coordinates (e.g., 40.473219)

    longitude: float
        Point longitude in geographical coordinates (e.g., -3.7227241)

    srs: str
        Spatial reference system code (e.g. "EPSG:4230"). Default value is "EPSG:4326" (i.e. WGS 80)

    Returns
    -------
    cadastral_reference: a string with the cadastral reference, or None if not found
    """
    # Make the API requests
    url = "https://ovc.catastro.meh.es/ovcservweb/OVCSWLocalizacionRC/OVCCoordenadas.asmx/Consulta_RCCOOR"
    params = {"SRS": srs, "Coordenada_X": longitude, "Coordenada_Y": latitude}
    response = requests.get(url, params)

    # Parse the XML response
    root = ET.fromstring(response.text)
    ns = "{http://www.catastro.meh.es/}"  # the namespace of the xml elements
    xml_ref = root.find(f"{ns}coordenadas/{ns}coord/{ns}pc")
    if xml_ref is not None:
        # The reference is splitted in pc1 and pc2 elements
        xml_pc1 = xml_ref.find(f"{ns}pc1")
        xml_pc2 = xml_ref.find(f"{ns}pc2")
        cadastral_ref = f"{xml_pc1.text}{xml_pc2.text}" if xml_pc1 is not None and xml_pc2 is not None else None
    else:
        cadastral_ref = None

    return cadastral_ref


def get_census_info(latitude: float, longitude: float):
    """
    Performs a request to the spanish national institute of statistics map web services. It returns the census section
    and district codes

    Parameters
    ----------
    latitude: float
        Point latitude in geographical coordinates (e.g., 40.473219)

    longitude: float
        Point longitude in geographical coordinates (e.g., -3.7227241)

    Returns
    -------
    census_information: a dict with two elements, census_section and district_code. Or an empty dict if no results were
    found.
    """
    # Build the request parameters
    # TODO - parametrize year, automatically select the most recent one?
    bbox = [latitude, longitude, latitude + 1e-5, longitude + 1e-5]
    str_bbox = ",".join([str(point) for point in bbox])
    layers = ["Secciones2020", "Distritos2020"]
    params = {
        "bbox": str_bbox,
        "layers": str_bbox,
        "query_layers": ",".join(layers),
        "width": 1,
        "height": 1,
        "version": "1.3.0",
        "version": "1.3.0",
        "format": "text/xml",
        "info_format": "text/xml",
        "service": "WMS",
        "request": "GetFeatureInfo",
        "styles": "",
        "crs": "EPSG:4326",
    }

    # Make the request
    url = "http://servicios.internet.ine.es/WMS/WMS_INE_SECCIONES_G01/MapServer/WMSServer"
    response = requests.get(url, params)

    # Parse the XML response
    result = {}
    root = ET.fromstring(response.text)
    section_xml = root.find(".//*[@CUSEC]")
    district_xml = root.find(".//*[@CUDIS]")
    if section_xml is not None:
        result["census_section"] = section_xml.attrib.get("CUSEC")
    if district_xml is not None:
        result["district_code"] = district_xml.attrib.get("CUDIS")

    return result
