import json
import collections

from uritemplate import URITemplate

from mapbox import errors
from mapbox.services.base import Service

class MapMatcher(Service):
    """Access to the Map Matching API V5"""

    api_name = 'matching'
    api_version = 'v5'
    valid_profiles = ['mapbox/driving', 'mapbox/driving-traffic', 'mapbox/walking', 'mapbox/cycling']

    def _validate_profile(self, profile):
        if profile not in self.valid_profiles:
            raise errors.InvalidProfileError(
                "{0} is not a valid profile".format(profile))
        return profile

    @staticmethod
    def _validate_single_option(value, option):
        if isinstance(value, list):
            raise errors.InvalidParameterError('Was expecting a single parameter for option {} but got a list'.format(option))

    @staticmethod
    def _join_list_or_single_option(value, separator):
        if isinstance(value, list):
            return separator.join(value)
        else:
            return value

    def _format_options(self, options):
        # Build query parameters from the options dictionary.
        # No validation is done - options are passed through to the API
        if options is None:
            return None

        formatted_options = collections.OrderedDict()
        for (option, original_value) in options.items():
            if option == 'annotations':
                formatted_value = self._join_list_or_single_option(original_value, ',')
            elif option == 'approaches':
                formatted_value = ';'.join(original_value)
            elif option == 'radiuses':
                formatted_value = ';'.join(original_value)
            elif option == 'waypoints':
                formatted_value = ';'.join(original_value)
            elif option == 'waypoint_names':
                formatted_value = ';'.join(original_value)
            elif option == 'timestamps':
                formatted_value = ';'.join([map(str, val) for val in original_value])
            else:
                # By default, pass through a single option
                MapMatcher._validate_single_option(original_value, option)
                formatted_value = original_value

            formatted_options[option] = formatted_value

        return formatted_options

    def _format_coordinates(self, coordinates):
        # Coordinates are a list of tuples - format them as a
        # Semicolon-separated list of  {longitude},{latitude} coordinate pairs to visit in order

        # Pick an output precision so we can more easily match URLs in our unit tests
        string_coordinates = [tuple('{:.12f}'.format(flt) for flt in coordinate) for coordinate in coordinates]

        formatted_coordinates = ';'.join([','.join(coordinate) for coordinate in string_coordinates])
        
        return formatted_coordinates

    def match(self, coordinates, profile, options=None):
        """Match features to OpenStreetMap data."""
        profile = self._validate_profile(profile)

        formatted_options = self._format_options(options)
        formatted_coordinates = self._format_coordinates(coordinates)

        path = '/{profile}/{coordinates}'.format(profile=profile, coordinates=formatted_coordinates)
        uri = URITemplate(self.baseuri + path)

        res = self.session.get(uri, params=formatted_options)
        self.handle_http_error(res)

        def geojson():
            return res.json()

        res.geojson = geojson
        return res
