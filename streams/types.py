from enum import Enum
from math import floor


class FieldTypes(Enum):
    TYPE_MESSAGE = 1
    TYPE_BYTES = 2
    TYPE_STRING = 3
    TYPE_UINT8 = 11
    TYPE_UINT16 = 12
    TYPE_UINT32 = 13
    TYPE_UINT64 = 14


FIELD_SIZES = dict([(FieldTypes.TYPE_MESSAGE, 4),
                    (FieldTypes.TYPE_BYTES, 4),
                    (FieldTypes.TYPE_STRING, 4),
                    (FieldTypes.TYPE_UINT8, 1),
                    (FieldTypes.TYPE_UINT16, 2),
                    (FieldTypes.TYPE_UINT32, 4),
                    (FieldTypes.TYPE_UINT64, 8)])


FIELD_ALIGNMENT = dict([(FieldTypes.TYPE_MESSAGE, 4),
                        (FieldTypes.TYPE_BYTES, 4),
                        (FieldTypes.TYPE_STRING, 4),
                        (FieldTypes.TYPE_UINT8, 1),
                        (FieldTypes.TYPE_UINT16, 2),
                        (FieldTypes.TYPE_UINT32, 4),
                        (FieldTypes.TYPE_UINT64, 4)])


def align_offset_to_type(offset: int, field_type: FieldTypes) -> int:
    field_size = FIELD_ALIGNMENT[field_type]
    result = floor((offset + field_size - 1) / field_size) * field_size
    return result
