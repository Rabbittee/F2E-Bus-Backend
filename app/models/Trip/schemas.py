from enum import IntEnum

from pydantic.main import BaseModel


class TripStatus(IntEnum):
    '''
    車輛狀態備註 : [0:'正常',1:'尚未發車',2:'交管不停靠',3:'末班車已過',4:'今日未營運']
    '''
    Default = 0
    NotDepart = 1
    Skipped = 2
    Terminate = 3
    Unscheduled = 4


class Trip(BaseModel):
    route_id: str
    station_id: str
    time_offset: int
    status: TripStatus
