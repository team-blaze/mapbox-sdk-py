import pytest
import responses

import mapbox
from mapbox import errors
import collections

@pytest.fixture
def coordinates():
    return [
            (-117.1728265285492,32.71204416018209),
            (-117.17288821935652,32.712258556224),
            (-117.17293113470076,32.712443613445814),
            (-117.17292040586472,32.71256999376694),
            (-117.17298477888109,32.712603845608285),
            (-117.17314302921294,32.71259933203019),
            (-117.17334151268004,32.71254065549407)
           ]

def test_class_attrs():
    """Get expected class attr values"""
    serv = mapbox.MapMatcher()
    assert serv.api_name == 'matching'
    assert serv.api_version == 'v5'

@responses.activate
def test_matching(coordinates):

    body = '{"matchings":[{"confidence":0.9559977809133028,"geometry":"gatfEfidjUk@Lc@@Y?E??L?\\\\Hh@","legs":[{"summary":"","weight":2.7,"duration":2.7,"steps":[],"distance":25},{"summary":"","weight":2.4,"duration":2.4,"steps":[],"distance":21},{"summary":"","weight":1.6,"duration":1.6,"steps":[],"distance":14},{"summary":"","weight":40.5,"duration":9.7,"steps":[],"distance":9.1},{"summary":"","weight":10.7,"duration":10.6,"steps":[],"distance":14.8},{"summary":"","weight":14.4,"duration":14.4,"steps":[],"distance":20}],"weight_name":"routability","weight":72.30000000000001,"duration":41.4,"distance":103.89999999999999}],"tracepoints":[{"alternatives_count":0,"waypoint_index":0,"matchings_index":0,"name":"North Harbor Drive","location":[-117.172836,32.712041]},{"alternatives_count":0,"waypoint_index":1,"matchings_index":0,"name":"North Harbor Drive","location":[-117.17291,32.712256]},{"alternatives_count":0,"waypoint_index":2,"matchings_index":0,"name":"North Harbor Drive","location":[-117.17292,32.712444]},{"alternatives_count":0,"waypoint_index":3,"matchings_index":0,"name":"North Harbor Drive","location":[-117.172922,32.71257]},{"alternatives_count":0,"waypoint_index":4,"matchings_index":0,"name":"West G Street","location":[-117.172985,32.7126]},{"alternatives_count":0,"waypoint_index":5,"matchings_index":0,"name":"West G Street","location":[-117.173143,32.712597]},{"alternatives_count":1,"waypoint_index":6,"matchings_index":0,"name":"West G Street","location":[-117.173345,32.712546]}],"code":"Ok"}'

    responses.add(
        responses.GET,
        'https://api.mapbox.com/matching/v5/mapbox/driving/-117.172826528549,32.712044160182;-117.172888219357,32.712258556224;-117.172931134701,32.712443613446;-117.172920405865,32.712569993767;-117.172984778881,32.712603845608;-117.173143029213,32.712599332030;-117.173341512680,32.712540655494?access_token=pk.test',
        match_querystring=True,
        body=body, status=200,
        content_type='application/json')

    service = mapbox.MapMatcher(access_token='pk.test')
    res = service.match(coordinates, profile='mapbox/driving')
    assert res.status_code == 200
    assert res.json() == res.geojson()

@responses.activate
def test_matching_with_options(coordinates):

    body = '{"matchings":[{"confidence":0.9559977809133028,"geometry":{"coordinates":[[-117.172836,32.712041],[-117.17291,32.712256],[-117.17292,32.712444],[-117.172922,32.71257],[-117.172922,32.712599],[-117.172985,32.7126],[-117.173145,32.712597],[-117.173345,32.712546]],"type":"LineString"},"legs":[{"annotation":{"distance":[12.342621171879989,6.298035886320184,6.329103172183789],"duration":[1.4,0.7,0.6]},"summary":"North Harbor Drive","weight":2.7,"duration":2.7,"steps":[{"intersections":[{"out":0,"entry":[true],"bearings":[340],"location":[-117.172836,32.712041]}],"driving_side":"right","geometry":{"coordinates":[[-117.172836,32.712041],[-117.172882,32.712145],[-117.172898,32.7122],[-117.17291,32.712256]],"type":"LineString"},"mode":"driving","maneuver":{"bearing_after":340,"bearing_before":0,"location":[-117.172836,32.712041],"type":"depart","instruction":"Head north on North Harbor Drive"},"weight":2.7,"duration":2.7,"name":"North Harbor Drive","distance":25},{"intersections":[{"in":0,"entry":[true],"bearings":[170],"location":[-117.17291,32.712256]}],"driving_side":"right","geometry":{"coordinates":[[-117.17291,32.712256],[-117.17291,32.712256]],"type":"LineString"},"mode":"driving","maneuver":{"bearing_after":0,"bearing_before":350,"location":[-117.17291,32.712256],"type":"arrive","instruction":"You have arrived at your 1st destination"},"weight":0,"duration":0,"name":"North Harbor Drive","distance":0}],"distance":25},{"annotation":{"distance":[1.347775405679008,7.932477316926939,4.337825700171268,6.006220199692893,1.3347155996172997],"duration":[0.2,0.9,0.5,0.7,0.1]},"summary":"North Harbor Drive","weight":2.4,"duration":2.4,"steps":[{"intersections":[{"out":0,"entry":[true],"bearings":[352],"location":[-117.17291,32.712256]}],"driving_side":"right","geometry":{"coordinates":[[-117.17291,32.712256],[-117.172912,32.712268],[-117.17292,32.712339],[-117.17292,32.712378],[-117.17292,32.712432],[-117.17292,32.712444]],"type":"LineString"},"mode":"driving","maneuver":{"bearing_after":352,"bearing_before":0,"location":[-117.17291,32.712256],"type":"depart","instruction":"Head north on North Harbor Drive"},"weight":2.4,"duration":2.4,"name":"North Harbor Drive","distance":21},{"intersections":[{"in":0,"entry":[true],"bearings":[180],"location":[-117.17292,32.712444]}],"driving_side":"right","geometry":{"coordinates":[[-117.17292,32.712444],[-117.17292,32.712444]],"type":"LineString"},"mode":"driving","maneuver":{"bearing_after":0,"bearing_before":0,"location":[-117.17292,32.712444],"type":"arrive","instruction":"You have arrived at your 2nd destination"},"weight":0,"duration":0,"name":"North Harbor Drive","distance":0}],"distance":21},{"annotation":{"distance":[7.786403421535881,6.229375811022434],"duration":[0.9,0.7]},"summary":"North Harbor Drive","weight":1.6,"duration":1.6,"steps":[{"intersections":[{"out":0,"entry":[true],"bearings":[359],"location":[-117.17292,32.712444]},{"out":0,"in":1,"entry":[true,false,false],"bearings":[0,180,270],"location":[-117.172921,32.712514]}],"driving_side":"right","geometry":{"coordinates":[[-117.17292,32.712444],[-117.172921,32.712514],[-117.172922,32.71257]],"type":"LineString"},"mode":"driving","maneuver":{"bearing_after":359,"bearing_before":0,"location":[-117.17292,32.712444],"type":"depart","instruction":"Head north on North Harbor Drive"},"weight":1.6,"duration":1.6,"name":"North Harbor Drive","distance":14},{"intersections":[{"in":0,"entry":[true],"bearings":[179],"location":[-117.172922,32.71257]}],"driving_side":"right","geometry":{"coordinates":[[-117.172922,32.71257],[-117.172922,32.71257]],"type":"LineString"},"mode":"driving","maneuver":{"bearing_after":0,"bearing_before":359,"location":[-117.172922,32.71257],"type":"arrive","instruction":"You have arrived at your 3rd destination"},"weight":0,"duration":0,"name":"North Harbor Drive","distance":0}],"distance":14},{"annotation":{"distance":[3.225562700018504,5.896898687141375],"duration":[0.4,4.2]},"summary":"North Harbor Drive, West G Street","weight":40.5,"duration":9.7,"steps":[{"intersections":[{"out":0,"entry":[true],"bearings":[0],"location":[-117.172922,32.71257]}],"driving_side":"right","geometry":{"coordinates":[[-117.172922,32.71257],[-117.172922,32.712599]],"type":"LineString"},"mode":"driving","maneuver":{"bearing_after":0,"bearing_before":0,"location":[-117.172922,32.71257],"type":"depart","instruction":"Head north on North Harbor Drive"},"weight":36.3,"duration":5.5,"name":"North Harbor Drive","distance":3.2},{"intersections":[{"out":2,"in":1,"entry":[true,false,true],"bearings":[0,180,270],"location":[-117.172922,32.712599]}],"driving_side":"right","geometry":{"coordinates":[[-117.172922,32.712599],[-117.172985,32.7126]],"type":"LineString"},"mode":"driving","maneuver":{"bearing_after":271,"bearing_before":358,"location":[-117.172922,32.712599],"modifier":"left","type":"turn","instruction":"Turn left onto West G Street"},"weight":4.2,"duration":4.2,"name":"West G Street","distance":5.9},{"intersections":[{"in":0,"entry":[true],"bearings":[91],"location":[-117.172985,32.7126]}],"driving_side":"right","geometry":{"coordinates":[[-117.172985,32.7126],[-117.172985,32.7126]],"type":"LineString"},"mode":"driving","maneuver":{"bearing_after":0,"bearing_before":271,"location":[-117.172985,32.7126],"type":"arrive","instruction":"You have arrived at your 4th destination"},"weight":0,"duration":0,"name":"West G Street","distance":0}],"distance":9.1},{"annotation":{"distance":[2.435748605452301,12.361217921620122],"duration":[1.8,8.8]},"summary":"West G Street","weight":10.7,"duration":10.6,"steps":[{"intersections":[{"out":0,"entry":[true],"bearings":[273],"location":[-117.172985,32.7126]},{"out":3,"in":1,"entry":[false,false,true,true],"bearings":[0,90,180,270],"location":[-117.173011,32.712601]}],"driving_side":"right","geometry":{"coordinates":[[-117.172985,32.7126],[-117.173011,32.712601],[-117.173143,32.712597]],"type":"LineString"},"mode":"driving","maneuver":{"bearing_after":273,"bearing_before":0,"location":[-117.172985,32.7126],"type":"depart","instruction":"Head west on West G Street"},"weight":10.700000000000001,"duration":10.600000000000001,"name":"West G Street","distance":14.8},{"intersections":[{"in":0,"entry":[true],"bearings":[88],"location":[-117.173143,32.712597]}],"driving_side":"right","geometry":{"coordinates":[[-117.173143,32.712597],[-117.173143,32.712597]],"type":"LineString"},"mode":"driving","maneuver":{"bearing_after":0,"bearing_before":268,"location":[-117.173143,32.712597],"type":"arrive","instruction":"You have arrived at your 5th destination"},"weight":0,"duration":0,"name":"West G Street","distance":0}],"distance":14.8},{"annotation":{"distance":[6.703844707900315,7.298824281308416,5.768085032759241],"duration":[4.8,5.3,4.1]},"summary":"West G Street","weight":14.4,"duration":14.4,"steps":[{"intersections":[{"out":0,"entry":[true],"bearings":[262],"location":[-117.173143,32.712597]}],"driving_side":"right","geometry":{"coordinates":[[-117.173145,32.712597],[-117.173216,32.712589],[-117.173291,32.712571],[-117.173345,32.712546]],"type":"LineString"},"mode":"driving","maneuver":{"bearing_after":262,"bearing_before":0,"location":[-117.173143,32.712597],"type":"depart","instruction":"Head west on West G Street"},"weight":14.4,"duration":14.4,"name":"West G Street","distance":20},{"intersections":[{"in":0,"entry":[true],"bearings":[61],"location":[-117.173345,32.712546]}],"driving_side":"right","geometry":{"coordinates":[[-117.173345,32.712546],[-117.173345,32.712546]],"type":"LineString"},"mode":"driving","maneuver":{"bearing_after":0,"bearing_before":241,"location":[-117.173345,32.712546],"type":"arrive","instruction":"You have arrived at your destination"},"weight":0,"duration":0,"name":"West G Street","distance":0}],"distance":20}],"weight_name":"routability","weight":72.30000000000001,"duration":41.4,"distance":103.89999999999999}],"tracepoints":[{"alternatives_count":0,"waypoint_index":0,"matchings_index":0,"name":"North Harbor Drive","location":[-117.172836,32.712041]},{"alternatives_count":0,"waypoint_index":1,"matchings_index":0,"name":"North Harbor Drive","location":[-117.17291,32.712256]},{"alternatives_count":0,"waypoint_index":2,"matchings_index":0,"name":"North Harbor Drive","location":[-117.17292,32.712444]},{"alternatives_count":0,"waypoint_index":3,"matchings_index":0,"name":"North Harbor Drive","location":[-117.172922,32.71257]},{"alternatives_count":0,"waypoint_index":4,"matchings_index":0,"name":"West G Street","location":[-117.172985,32.7126]},{"alternatives_count":0,"waypoint_index":5,"matchings_index":0,"name":"West G Street","location":[-117.173143,32.712597]},{"alternatives_count":1,"waypoint_index":6,"matchings_index":0,"name":"West G Street","location":[-117.173345,32.712546]}],"code":"Ok"}'

    responses.add(
        responses.GET,
        'https://api.mapbox.com/matching/v5/mapbox/driving/-117.172826528549,32.712044160182;-117.172888219357,32.712258556224;-117.172931134701,32.712443613446;-117.172920405865,32.712569993767;-117.172984778881,32.712603845608;-117.173143029213,32.712599332030;-117.173341512680,32.712540655494?access_token=pk.test&annotations=duration%2Cdistance&approaches=curb%3Bcurb%3Bcurb%3Bcurb%3Bcurb%3Bcurb%3Bcurb&geometries=geojson&steps=true',
        match_querystring=True,
        body=body, status=200,
        content_type='application/json')

    service = mapbox.MapMatcher(access_token='pk.test')
    options = collections.OrderedDict()
    options['annotations'] = ['duration','distance']
    options['approaches'] = ['curb','curb', 'curb', 'curb', 'curb', 'curb', 'curb']
    options['geometries'] = 'geojson'
    options['steps'] = 'true'

    res = service.match(coordinates, profile='mapbox/driving', options=options)
    assert res.status_code == 200
    assert res.json() == res.geojson()

def test_invalid_profile(coordinates):
    service = mapbox.MapMatcher(access_token='pk.test')
    with pytest.raises(ValueError):
        service.match(coordinates, profile='mapbox.driving') # Note, this is a dot not a slash

def test_invalid_single_options(coordinates):
    service = mapbox.MapMatcher(access_token='pk.test')

    # The following options must be non-list items
    with pytest.raises(errors.InvalidParameterError):
        service.match(coordinates, profile='mapbox/driving', options={'geometries': ['value not checked']})

    with pytest.raises(errors.InvalidParameterError):
        service.match(coordinates, profile='mapbox/driving', options={'language': ['value not checked']})

    with pytest.raises(errors.InvalidParameterError):
        service.match(coordinates, profile='mapbox/driving', options={'overview': ['value not checked']})

    with pytest.raises(errors.InvalidParameterError):
        service.match(coordinates, profile='mapbox/driving', options={'steps': ['value not checked']})

    with pytest.raises(errors.InvalidParameterError):
        service.match(coordinates, profile='mapbox/driving', options={'tidy': ['value not checked']})
