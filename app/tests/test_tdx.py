from app.services.tdx import transform
from unittest import TestCase


class TestTDX(TestCase):

    def test_transform_with_taipei_307(self):
        self.assertIsNotNone(
            transform([
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
