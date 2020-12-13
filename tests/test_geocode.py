#!/usr/bin/env python

"""Tests for `geocode` package."""


import unittest

from pycartociudad import geocode

class TestGeocode(unittest.TestCase):
    """Tests for `geocode` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_001_geocode_portal(self):
        """Test that geocode or portal level"""
        input_text = "Plaza mayor 1, Madrid"
        expected_output = {
            'province': 'Madrid', 
            'comunidadAutonoma': 'Comunidad de Madrid', 
            'muni': 'Madrid', 
            'type': 'portal', 
            'address': 'MAYOR', 
            'postalCode': '28012', 
            'poblacion': 'Madrid', 
            'tip_via': 'PLAZA', 
            'portalNumber': 1, 
            'state': 1, 
            'countryCode': '011'
        }
        
        output = geocode(input_text)
        self.assertDictContainsSubset(expected_output, output)
        
    def test_002_geocode_street(self):
        """Test geocode on street level"""
        input_text = "Calle Alcalá"
        expected_output = {
            'type':'callejero', 
            'address': 'ALCALA', 
            'tip_via': 'CALLE', 
            'state': 1, 
            'countryCode': '011'
        }
        
        output = geocode(input_text)
        self.assertDictContainsSubset(expected_output, output)
        
        # check that geometry is a line
        self.assertTrue(output['geom'].startswith('MULTILINESTRING'))
        
        # check that coordinates are not null
        self.assertIsNotNone(output['lat'])
        self.assertIsNotNone(output['lng'])
        
    def test_003_geocode_type_town(self):
        """Test geocode in town level"""
        input_text = "Logroño"
        expected_output = {
            'province':'La Rioja',
            'comunidadAutonoma':'La Rioja',
            'muni':'Logroño',
            'type':'Municipio',
            'address':'Logroño',
            'postalCode':None,
            'poblacion':None,
            'tip_via':None,
            'portalNumber':0,
            'state':1,
            'countryCode':'011',
        }
        
        output = geocode(input_text)
        self.assertDictContainsSubset(expected_output, output)
        
    def test_004_geocode_type_province(self):
        """Test geocode in province level"""
        input_text = "alava"
        expected_output = {
            'province':'Araba/Álava',
            'comunidadAutonoma':'País Vasco/Euskadi',
            'muni':None,
            'type':'provincia',
            'address':None,
            'postalCode':None,
            'poblacion':None,
            'tip_via':None,
            'portalNumber':0,
            'state':1,
            'countryCode':'011',
        }
        
        output = geocode(input_text)
        self.assertDictContainsSubset(expected_output, output)
        
    def test_005_geocode_type_region(self):
        """Test geocode in region level"""
        input_text = "La Rioja"
        expected_output = {
            'id':'17',
            'province':None,
            'comunidadAutonoma':'La Rioja',
            'muni':None,
            'type':'comunidad autonoma',
            'address':None,
            'postalCode':None,
            'poblacion':None,
        }
        
        output = geocode(input_text)
        self.assertDictContainsSubset(expected_output, output)
    
    def test_006_geocode_no_existing_address(self):
        """Test geocode with no existing address"""
        input_text = "gadfsdfwerewsfczx"
        
        output = geocode(input_text)
        self.assertEqual({}, output)
        
    def test_007_geocode_special_characters(self):
        """Test geocode with text with special characters"""
        self.assertEqual({}, geocode(True))
        self.assertNotEqual({}, geocode(101))
        self.assertNotEqual({}, geocode('Castilla & León'))
        
        
if __name__ == "__main__":
    unittest.main()
    