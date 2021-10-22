"""Unit tests for bluesky.models.fires"""

__author__ = "Joel Dubowy"

from bluesky.models import fires
from bluesky.fuelmoisture import fill_in_defaults, MOISTURE_PROFILES

class TestFillInDefaults(object):

    def test_wildfire_no_fm(self):
        f = fires.Fire({
            "type": "wildfire",
            "activity": [
                {
                    "active_areas": [
                        {
                            "start": "2018-11-07T17:00:00",
                            "end": "2018-11-08T17:00:00",
                            "ecoregion": "western",
                            "utc_offset": "-07:00",
                            "specified_points": [
                                {
                                    "area": 500,
                                    "lng": -121.73434,
                                    "lat": 46.7905
                                }
                            ]
                        }
                    ]
                }
            ]
        })

        loc = f['activity'][0]['active_areas'][0]['specified_points'][0]
        fill_in_defaults(f, loc)

        assert loc['fuelmoisture'] == MOISTURE_PROFILES['dry']

    def test_wildfire_no_some_fm_defined(self):
        f = fires.Fire({
            "type": "wildfire",
            "activity": [
                {
                    "active_areas": [
                        {
                            "start": "2018-11-07T17:00:00",
                            "end": "2018-11-08T17:00:00",
                            "ecoregion": "western",
                            "utc_offset": "-07:00",
                            "specified_points": [
                                {
                                    "area": 500,
                                    "lng": -121.73434,
                                    "lat": 46.7905,
                                    "fuelmoisture": {
                                        "10_hr": 11.234,
                                        "1_hr": 9.865,
                                    },
                                }
                            ]
                        }
                    ]
                }
            ]
        })

        loc = f['activity'][0]['active_areas'][0]['specified_points'][0]
        fill_in_defaults(f, loc)

        expected = dict(MOISTURE_PROFILES['dry'],
            **{'10_hr': 11.234, '1_hr': 9.865})
        assert loc['fuelmoisture'] == expected

    def test_rx_no_fm(self):
        f = fires.Fire({
            "type": "rx",
            "activity": [
                {
                    "active_areas": [
                        {
                            "start": "2018-11-07T17:00:00",
                            "end": "2018-11-08T17:00:00",
                            "ecoregion": "western",
                            "utc_offset": "-07:00",
                            "specified_points": [
                                {
                                    "area": 500,
                                    "lng": -121.73434,
                                    "lat": 46.7905
                                }
                            ]
                        }
                    ]
                }
            ]
        })

        loc = f['activity'][0]['active_areas'][0]['specified_points'][0]
        fill_in_defaults(f, loc)

        assert loc['fuelmoisture'] == MOISTURE_PROFILES['moist']

    def test_rx_no_some_fm_defined(self):
        f = fires.Fire({
            "type": "rx",
            "activity": [
                {
                    "active_areas": [
                        {
                            "start": "2018-11-07T17:00:00",
                            "end": "2018-11-08T17:00:00",
                            "ecoregion": "western",
                            "utc_offset": "-07:00",
                            "specified_points": [
                                {
                                    "area": 500,
                                    "lng": -121.73434,
                                    "lat": 46.7905,
                                    "fuelmoisture": {
                                        "10_hr": 20.32,
                                        "1_hr": 21.46,
                                    },
                                }
                            ]
                        }
                    ]
                }
            ]
        })

        loc = f['activity'][0]['active_areas'][0]['specified_points'][0]
        fill_in_defaults(f, loc)

        expected = dict(MOISTURE_PROFILES['moist'],
            **{'10_hr': 20.32, '1_hr': 21.46})
        assert loc['fuelmoisture'] == expected


    def test_unknown_no_fm(self):
        f = fires.Fire({
            "type": "unknown",
            "activity": [
                {
                    "active_areas": [
                        {
                            "start": "2018-11-07T17:00:00",
                            "end": "2018-11-08T17:00:00",
                            "ecoregion": "western",
                            "utc_offset": "-07:00",
                            "specified_points": [
                                {
                                    "area": 500,
                                    "lng": -121.73434,
                                    "lat": 46.7905
                                }
                            ]
                        }
                    ]
                }
            ]
        })

        loc = f['activity'][0]['active_areas'][0]['specified_points'][0]
        fill_in_defaults(f, loc)

        assert loc['fuelmoisture'] == MOISTURE_PROFILES['moist']

    def test_unknown_no_some_fm_defined(self):
        f = fires.Fire({
            "type": "unknown",
            "activity": [
                {
                    "active_areas": [
                        {
                            "start": "2018-11-07T17:00:00",
                            "end": "2018-11-08T17:00:00",
                            "ecoregion": "western",
                            "utc_offset": "-07:00",
                            "specified_points": [
                                {
                                    "area": 500,
                                    "lng": -121.73434,
                                    "lat": 46.7905,
                                    "fuelmoisture": {
                                        "10_hr": 19.32,
                                        "1_hr": 43.46,
                                    },
                                }
                            ]
                        }
                    ]
                }
            ]
        })

        loc = f['activity'][0]['active_areas'][0]['specified_points'][0]
        fill_in_defaults(f, loc)

        expected = dict(MOISTURE_PROFILES['moist'],
            **{'10_hr': 19.32, '1_hr': 43.46})
        assert loc['fuelmoisture'] == expected

