from app.services.tdx import routes, stations
from unittest import TestCase


class TestTDX(TestCase):

    def test_transform_routes_with_taipei_307(self):
        self.assertIsNotNone(
            routes.transform([
                {
                    "RouteUID": "TPE16111",
                    "RouteID": "16111",
                    "HasSubRoutes": True,
                    "Operators": [
                        {
                            "OperatorID": "100",
                            "OperatorName": {
                                "Zh_tw": "臺北客運",
                                "En": "Taipei Bus Co., Ltd."
                            },
                            "OperatorCode": "TaipeiBus",
                            "OperatorNo": "1407"
                        },
                        {
                            "OperatorID": "200",
                            "OperatorName": {
                                "Zh_tw": "首都客運",
                                "En": "Capital Bus Co., Ltd."
                            },
                            "OperatorCode": "CapitalBus",
                            "OperatorNo": "0913"
                        }
                    ],
                    "AuthorityID": "004",
                    "ProviderID": "045",
                    "SubRoutes": [
                        {
                            "SubRouteUID": "TPE157462",
                            "SubRouteID": "157462",
                            "OperatorIDs": [
                                "100",
                                "200"
                            ],
                            "SubRouteName": {
                                "Zh_tw": "307莒光往板橋前站",
                                "En": "307"
                            },
                            "Direction": 1,
                            "FirstBusTime": "0500",
                            "LastBusTime": "2210",
                            "HolidayFirstBusTime": "0500",
                            "HolidayLastBusTime": "2210"
                        },
                        {
                            "SubRouteUID": "TPE157463",
                            "SubRouteID": "157463",
                            "OperatorIDs": [
                                "100",
                                "200"
                            ],
                            "SubRouteName": {
                                "Zh_tw": "307莒光往撫遠街",
                                "En": "307"
                            },
                            "Direction": 0,
                            "FirstBusTime": "0500",
                            "LastBusTime": "2210",
                            "HolidayFirstBusTime": "0500",
                            "HolidayLastBusTime": "2210"
                        },
                        {
                            "SubRouteUID": "TPE157685",
                            "SubRouteID": "157685",
                            "OperatorIDs": [
                                "100",
                                "200"
                            ],
                            "SubRouteName": {
                                "Zh_tw": "307西藏往板橋前站",
                                "En": "307"
                            },
                            "Direction": 1,
                            "FirstBusTime": "0500",
                            "LastBusTime": "2210",
                            "HolidayFirstBusTime": "0500",
                            "HolidayLastBusTime": "2210"
                        },
                        {
                            "SubRouteUID": "TPE159291",
                            "SubRouteID": "159291",
                            "OperatorIDs": [
                                "100",
                                "200"
                            ],
                            "SubRouteName": {
                                "Zh_tw": "307西藏往撫遠街",
                                "En": "307"
                            },
                            "Direction": 0,
                            "FirstBusTime": "0500",
                            "LastBusTime": "2210",
                            "HolidayFirstBusTime": "0500",
                            "HolidayLastBusTime": "2210"
                        }
                    ],
                    "BusRouteType": 11,
                    "RouteName": {
                        "Zh_tw": "307",
                        "En": "307"
                    },
                    "DepartureStopNameZh": "板橋",
                    "DepartureStopNameEn": "Banqiao",
                    "DestinationStopNameZh": "撫遠街",
                    "DestinationStopNameEn": "Fuyuan St.",
                    "TicketPriceDescriptionZh": "兩段票",
                    "TicketPriceDescriptionEn": "2 segments",
                    "FareBufferZoneDescriptionZh": "萬大國小-中和國稅局",
                    "FareBufferZoneDescriptionEn": "WanDa Elementary School-Zhonghe National Tax Administration",
                    "RouteMapImageUrl": "https://ebus.gov.taipei/MapOverview?nid=0100030700",
                    "City": "Taipei",
                    "CityCode": "TPE",
                    "UpdateTime": "2021-10-31T04:07:16+08:00",
                    "VersionID": 1292
                }
            ])
        )

    def test_transform_stations_with_TPE10(self):
        self.assertIsNotNone(
            stations.transform([
                {
                    "StationUID": "TPE10",
                    "StationID": "10",
                    "StationName": {
                        "Zh_tw": "八勢里"
                    },
                    "StationPosition": {
                        "PositionLon": 121.45952,
                        "PositionLat": 25.15123,
                        "GeoHash": "wsqr5fshe"
                    },
                    "StationAddress": "中正東路二段107號(向北)",
                    "Stops": [
                        {
                            "StopUID": "TPE56147",
                            "StopID": "56147",
                            "StopName": {
                                "Zh_tw": "八勢里",
                                "En": "Bashi Li"
                            },
                            "RouteUID": "TPE15151",
                            "RouteID": "15151",
                            "RouteName": {
                                "Zh_tw": "308",
                                "En": "308"
                            }
                        },
                        {
                            "StopUID": "TPE129931",
                            "StopID": "129931",
                            "StopName": {
                                "Zh_tw": "八勢里",
                                "En": "Bashi Village"
                            },
                            "RouteUID": "TPE16504",
                            "RouteID": "16504",
                            "RouteName": {
                                "Zh_tw": "756",
                                "En": "756"
                            }
                        },
                        {
                            "StopUID": "TPE151757",
                            "StopID": "151757",
                            "StopName": {
                                "Zh_tw": "八勢里",
                                "En": "Bashi Li"
                            },
                            "RouteUID": "TPE16707",
                            "RouteID": "16707",
                            "RouteName": {
                                "Zh_tw": "757",
                                "En": "757"
                            }
                        },
                        {
                            "StopUID": "TPE189101",
                            "StopID": "189101",
                            "StopName": {
                                "Zh_tw": "八勢里",
                                "En": "Bashi Li"
                            },
                            "RouteUID": "TPE17740",
                            "RouteID": "17740",
                            "RouteName": {
                                "Zh_tw": "957",
                                "En": "957"
                            }
                        }
                    ],
                    "LocationCityCode": "NWT",
                    "Bearing": "N",
                    "UpdateTime": "2021-10-31T04:07:16+08:00",
                    "VersionID": 1292
                }
            ])
        )
