from datetime import datetime, timezone


def date_to_unix_nano(date: datetime) -> int:
    timestamp = int(date.replace(tzinfo=timezone.utc).timestamp()) * 1000000000
    return timestamp


def unix_nano_to_date(timestamp: int) -> datetime:
    date = datetime.utcfromtimestamp(int(timestamp / 1000000000))
    return date


def utc_string_to_date(utc_time: str, fmt='%Y-%m-%dT%H:%M:%S.%fZ') -> datetime:
    return datetime.strptime(utc_time, fmt)


def date_to_utc_string(date: datetime, fmt='%Y-%m-%dT%H:%M:%S.%f') -> str:
    # formatting the time to utc string in milliseconds
    dt, micro = date.strftime(fmt).split('.')
    dt = '%s.%03d' % (dt, int(micro) / 1000)
    return dt + 'Z'
