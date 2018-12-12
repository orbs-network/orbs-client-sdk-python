from enum import Enum


class RequestStatus(Enum):
    REQUEST_STATUS_COMPLETED = 'COMPLETED'
    REQUEST_STATUS_IN_PROCESS = 'IN_PROCESS'
    REQUEST_STATUS_NOT_FOUND = 'NOT_FOUND'
    REQUEST_STATUS_REJECTED = 'REJECTED'
    REQUEST_STATUS_CONGESTION = 'CONGESTION'
    REQUEST_STATUS_SYSTEM_ERROR = 'SYSTEM_ERROR'


def request_status_decode(request_status: int) -> RequestStatus:
    if request_status == 0:
        raise ValueError('reserved RequestStatus received')
    elif request_status == 1:
        return RequestStatus.REQUEST_STATUS_COMPLETED
    elif request_status == 2:
        return RequestStatus.REQUEST_STATUS_IN_PROCESS
    elif request_status == 3:
        return RequestStatus.REQUEST_STATUS_NOT_FOUND
    elif request_status == 4:
        return RequestStatus.REQUEST_STATUS_REJECTED
    elif request_status == 5:
        return RequestStatus.REQUEST_STATUS_CONGESTION
    elif request_status == 6:
        return RequestStatus.REQUEST_STATUS_SYSTEM_ERROR
    else:
        raise ValueError(f'unsupported RequestStatus received: {request_status}')
