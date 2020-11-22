#!/usr/bin/env python

"""Tests for `reverse_geocode` function."""


import unittest

from pycartociudad import reverse_geocode


class TestReverseGeocode(unittest.TestCase):
    """Tests for `reverse_geocode` function."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_001_reverse_geocode(self):
        """Test correct reverse geocoding
        with existing coords"""
        self.assertEqual(
                         reverse_geocode(40.4472476241486,
                                         -3.7076498426208833)['address'],
                         'REINA VICTORIA')

    def test_002_reverse_geocode(self):
        """Test correct reverse geocoding
        in a cadastral search
        with existing coords"""
        self.assertEqual(
                         reverse_geocode(40.4472476241486,
                                         -3.7076498426208833,
                                         cadastral=True)['address'],
                         '0079609VK4707G')

    def test_003_reverse_geocode(self):
        """Test correct args type"""
        self.assertEqual(reverse_geocode('a', 'b', error='ignore'), {})

    def test_004_reverse_geocode(self):
        """Test correct args raising exception"""
        with self.assertRaises(SystemExit):
            reverse_geocode('a', 'b')

    def test_005_reverse_geocode(self):
        """Test coords not found"""
        self.assertEqual(reverse_geocode(0, 0, error='ignore'), {})

    def test_006_reverse_geocode(self):
        """Test coords not found raising exception"""
        with self.assertRaises(SystemExit):
            reverse_geocode(0, 0)


if __name__ == '__main__':
    unittest.main()
