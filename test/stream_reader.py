import unittest
from os import sys, path
from streams.stream_reader import StreamReader
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


class TestStreamReader(unittest.TestCase):
    def test_read_uint8(self):
        stream = bytes([0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])
        reader = StreamReader(stream)
        expected = 255
        self.assertEqual(expected, reader.read_uint8())
        reader.close()

    def test_read_corrupt_uint8(self):
        stream = bytes()
        reader = StreamReader(stream)
        self.assertRaises(RuntimeError, reader.read_uint8)
        reader.close()

    def test_read_uint16(self):
        stream = bytes([0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])
        reader = StreamReader(stream)
        expected = 65535
        self.assertEqual(expected, reader.read_uint16())
        reader.close()

    def test_read_corrupt_uint16(self):
        stream = bytes([0xFF])
        reader = StreamReader(stream)
        self.assertRaises(RuntimeError, reader.read_uint16)
        reader.close()

    def test_read_uint32(self):
        stream = bytes([0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])
        reader = StreamReader(stream)
        expected = 4294967295
        self.assertEqual(expected, reader.read_uint32())
        reader.close()

    def test_read_corrupt_uint32(self):
        stream = bytes([0xFF, 0xFF, 0xFF])
        reader = StreamReader(stream)
        self.assertRaises(RuntimeError, reader.read_uint32)
        reader.close()

    def test_read_uint64(self):
        stream = bytes([0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])
        reader = StreamReader(stream)
        expected = 18446744073709551615
        self.assertEqual(expected, reader.read_uint64())
        reader.close()

    def test_read_corrupt_uint64(self):
        stream = bytes([0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])
        reader = StreamReader(stream)
        self.assertRaises(RuntimeError, reader.read_uint64)
        reader.close()

    def test_read_bytes(self):
        stream = bytes([0x03, 0x00, 0x00, 0x00, 0x01, 0x02, 0x03, 0x00, 0x05, 0x00, 0x00, 0x00, 0x01, 0x02, 0x03, 0x04, 0x05])
        reader = StreamReader(stream)
        expected1 = bytes([0x01, 0x02, 0x03])
        self.assertEqual(expected1, reader.read_bytes())
        expected2 = bytes([0x01, 0x02, 0x03, 0x04, 0x05])
        self.assertEqual(expected2, reader.read_bytes())
        reader.close()

    def test_read_corrupt_bytes(self):
        stream = bytes([0x03, 0x00, 0x00, 0x00, 0x01, 0x02])
        reader = StreamReader(stream)
        self.assertRaises(RuntimeError, reader.read_bytes)
        reader.close()

    def test_read_string(self):
        stream = bytes([0x05, 0x00, 0x00, 0x00, ord('h'), ord('e'), ord('l'), ord('l'), ord('o'), 0x00, 0x00, 0x00, 0x06, 0x00, 0x00, 0x00, ord('w'), ord('o'), ord('r'), ord('l'), ord('d'), ord('!')])
        reader = StreamReader(stream)
        expected1 = 'hello'
        self.assertEqual(expected1, reader.read_string())
        expected2 = 'world!'
        self.assertEqual(expected2, reader.read_string())
        reader.close()

    def test_read_corrupt_string(self):
        stream = bytes([0x05, 0x00, 0x00, 0x00, ord('h'), ord('e'), ord('l'), ord('l')])
        reader = StreamReader(stream)
        self.assertRaises(RuntimeError, reader.read_string)
        reader.close()
