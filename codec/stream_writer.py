import io
from codec.types import FIELD_SIZES, FieldTypes, align_offset_to_type


class StreamWriter:
    def __init__(self) -> None:
        self.__size = 0
        self.__writer = io.BytesIO()

    def reset(self) -> None:
        self.__size = 0
        self.__writer.truncate(0)

    def close(self) -> None:
        self.__size = 0
        self.__writer.close()

    def get_size(self) -> int:
        return self.__size

    def get_stream_value(self) -> bytes:
        return self.__writer.getvalue()

    def write_uint8(self, value: int) -> None:
        self.__size = align_offset_to_type(self.__size, FieldTypes.TYPE_UINT8)
        self.__writer.seek(self.__size)
        formatted_uint8 = value.to_bytes(1, byteorder='little', signed=False)
        self.__writer.write(formatted_uint8)
        self.__size += FIELD_SIZES[FieldTypes.TYPE_UINT8]

    def write_uint16(self, value: int) -> None:
        self.__size = align_offset_to_type(self.__size, FieldTypes.TYPE_UINT16)
        self.__writer.seek(self.__size)
        formatted_uint16 = value.to_bytes(2, byteorder='little', signed=False)
        self.__writer.write(formatted_uint16)
        self.__size += FIELD_SIZES[FieldTypes.TYPE_UINT16]

    def write_uint32(self, value: int) -> None:
        self.__size = align_offset_to_type(self.__size, FieldTypes.TYPE_UINT32)
        self.__writer.seek(self.__size)
        formatted_uint32 = value.to_bytes(4, byteorder='little', signed=False)
        self.__writer.write(formatted_uint32)
        self.__size += FIELD_SIZES[FieldTypes.TYPE_UINT32]

    def write_uint64(self, value: int) -> None:
        self.__size = align_offset_to_type(self.__size, FieldTypes.TYPE_UINT64)
        self.__writer.seek(self.__size)
        formatted_uint64 = value.to_bytes(8, byteorder='little', signed=False)
        self.__writer.write(formatted_uint64)
        self.__size += FIELD_SIZES[FieldTypes.TYPE_UINT64]

    def write_bytes(self, value: bytes) -> None:
        self.__size = align_offset_to_type(self.__size, FieldTypes.TYPE_BYTES)
        self.__writer.seek(self.__size)
        bytes_size = len(value)
        self.write_uint32(bytes_size)
        self.__writer.write(value)
        self.__size += bytes_size

    def write_string(self, value: str) -> None:
        self.__size = align_offset_to_type(self.__size, FieldTypes.TYPE_STRING)
        self.__writer.seek(self.__size)
        str_size = len(value)
        self.write_uint32(str_size)
        self.__writer.write(bytes(value, 'utf-8'))
        self.__size += str_size

