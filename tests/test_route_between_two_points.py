#!/usr/bin/env python

"""Tests for `reverse_geocode` function."""


import unittest

from pycartociudad import route_between_two_points


class TestRouteBetweenTwoPoints(unittest.TestCase):
    """Tests for `reverse_geocode` function."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_001_route_between_two_points(self):
        """Test the route between two points using the distance,
            when is not using a vehicle"""

        lat_init, lon_init, lat_dest, lon_dest = 40.4166896, -3.7038101, 40.4113844, -3.7083022

        self.assertEqual(
                         route_between_two_points(lat_init=lat_init, lon_init=lon_init,
                                                  lat_dest=lat_dest, lon_dest=lon_dest,
                                                  vehicle=False)['distance'], 815.7369613261391)

    def test_002_route_between_two_points(self):
        """Test the route between two points using the distance,
            when using a vehicle"""

        lat_init, lon_init, lat_dest, lon_dest = 40.4166896, -3.7038101, 40.4113844, -3.7083022

        self.assertEqual(
                         route_between_two_points(lat_init=lat_init, lon_init=lon_init,
                                                  lat_dest=lat_dest, lon_dest=lon_dest,
                                                  vehicle=True)['distance'], 815.736961326139)

    def test_003_route_between_two_points(self):
        """Test correct args type"""
        self.assertEqual(route_between_two_points('lat1', 'lon1', 'lat2', 'lon2',
                                                  error='ignore'), {})

    def test_004_route_between_two_points(self):
        """Test correct args raising exception"""
        with self.assertRaises(SystemExit):
            route_between_two_points('lat1', 'lon1', 'lat2', 'lon2')

    def test_005_route_between_two_points(self):
        # Test coords not found
        self.assertEqual(route_between_two_points(40.4166896, -3.7038101, 0, 0,
                                                  error='ignore'), {})

    def test_006_route_between_two_points(self):
        # Test coords not found raising exception
        with self.assertRaises(SystemExit):
            route_between_two_points(40.4166896, -3.7038101, 0, 0)


if __name__ == '__main__':
    unittest.main()
