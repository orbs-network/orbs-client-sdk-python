import io
from streams.types import FIELD_SIZES, FieldTypes, align_offset_to_type


class StreamReader:
    def __init__(self, stream: bytes) -> None:
        self.__reader = io.BytesIO(stream)
        self.__size = len(stream)
        self.__cursor = 0

    def get_size(self) -> int:
        return self.__size

    def get_stream_value(self) -> bytes:
        return self.__reader.getvalue()

    def done_reading(self) -> bool:
        return self.__size == self.__cursor

    def close(self) -> None:
        self.__size = 0
        self.__cursor = 0
        self.__reader.close()

    def read_uint8(self) -> int:
        self.__cursor = align_offset_to_type(self.__cursor, FieldTypes.TYPE_UINT8)
        self.__reader.seek(self.__cursor)
        if self.__cursor + FIELD_SIZES[FieldTypes.TYPE_UINT8] > self.get_size():
            raise RuntimeError(f'cannot read uint8 type, expected {FIELD_SIZES[FieldTypes.TYPE_UINT8]} bytes')
        uint8_bytes = self.__reader.read(FIELD_SIZES[FieldTypes.TYPE_UINT8])
        uint8_value = int.from_bytes(uint8_bytes, byteorder='little', signed=False)
        self.__cursor += FIELD_SIZES[FieldTypes.TYPE_UINT8]
        return uint8_value

    def read_uint16(self) -> int:
        self.__cursor = align_offset_to_type(self.__cursor, FieldTypes.TYPE_UINT16)
        self.__reader.seek(self.__cursor)
        if self.__cursor + FIELD_SIZES[FieldTypes.TYPE_UINT16] > self.get_size():
            raise RuntimeError(f'cannot read uint16 type, expected {FIELD_SIZES[FieldTypes.TYPE_UINT16]} bytes')
        uint16_bytes = self.__reader.read(FIELD_SIZES[FieldTypes.TYPE_UINT16])
        uint16_value = int.from_bytes(uint16_bytes, byteorder='little', signed=False)
        self.__cursor += FIELD_SIZES[FieldTypes.TYPE_UINT16]
        return uint16_value

    def read_uint32(self) -> int:
        self.__cursor = align_offset_to_type(self.__cursor, FieldTypes.TYPE_UINT32)
        self.__reader.seek(self.__cursor)
        if self.__cursor + FIELD_SIZES[FieldTypes.TYPE_UINT32] > self.get_size():
            raise RuntimeError(f'cannot read uint32 type, expected {FIELD_SIZES[FieldTypes.TYPE_UINT32]} bytes')
        uint32_bytes = self.__reader.read(FIELD_SIZES[FieldTypes.TYPE_UINT32])
        uint32_value = int.from_bytes(uint32_bytes, byteorder='little', signed=False)
        self.__cursor += FIELD_SIZES[FieldTypes.TYPE_UINT32]
        return uint32_value

    def read_uint64(self) -> int:
        self.__cursor = align_offset_to_type(self.__cursor, FieldTypes.TYPE_UINT64)
        self.__reader.seek(self.__cursor)
        if self.__cursor + FIELD_SIZES[FieldTypes.TYPE_UINT64] > self.get_size():
            raise RuntimeError(f'cannot read uint64 type, expected {FIELD_SIZES[FieldTypes.TYPE_UINT64]} bytes')
        uint64_bytes = self.__reader.read(FIELD_SIZES[FieldTypes.TYPE_UINT64])
        uint64_value = int.from_bytes(uint64_bytes, byteorder='little', signed=False)
        self.__cursor += FIELD_SIZES[FieldTypes.TYPE_UINT64]
        return uint64_value

    def read_bytes(self) -> bytes:
        self.__cursor = align_offset_to_type(self.__cursor, FieldTypes.TYPE_BYTES)
        self.__reader.seek(self.__cursor)
        bytes_length = self.read_uint32()
        if self.__cursor + bytes_length > self.__size:
            raise RuntimeError(f'bytes object has an invalid length {self.__size - self.__cursor}, expected {bytes_length}')
        bytes_value = self.__reader.read(bytes_length)
        self.__cursor += bytes_length
        return bytes_value

    def read_string(self) -> str:
        self.__cursor = align_offset_to_type(self.__cursor, FieldTypes.TYPE_STRING)
        self.__reader.seek(self.__cursor)
        str_length = self.read_uint32()
        if self.__cursor + str_length > self.__size:
            raise RuntimeError(f'str object has an invalid length {self.__size - self.__cursor}, expected {str_length}')
        str_bytes = self.__reader.read(str_length)
        str_value = str(str_bytes, 'utf-8')
        self.__cursor += str_length
        return str_value
