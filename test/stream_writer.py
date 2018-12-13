import unittest
from os import sys, path
from streams.stream_writer import StreamWriter
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


class TestStreamWriter(unittest.TestCase):
    def test_write_uint8(self):
        sw = StreamWriter()
        value = 0x17
        sw.write_uint8(value)
        self.assertEqual(1, sw.get_size())
        expected = bytes([0x17])
        self.assertEqual(expected, sw.get_stream_value())
        sw.close()

    def test_write_uint16(self):
        sw = StreamWriter()
        value = 0x17
        sw.write_uint16(value)
        self.assertEqual(2, sw.get_size())
        expected = bytes([0x17, 0x00])
        self.assertEqual(expected, sw.get_stream_value())
        sw.close()

    def test_write_uint32(self):
        sw = StreamWriter()
        value = 0x17
        sw.write_uint32(value)
        self.assertEqual(4, sw.get_size())
        expected = bytes([0x17, 0x00, 0x00, 0x00])
        self.assertEqual(expected, sw.get_stream_value())
        sw.close()

    def test_write_uint64(self):
        sw = StreamWriter()
        value = 0x17
        sw.write_uint64(value)
        self.assertEqual(8, sw.get_size())
        expected = bytes([0x17, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
        self.assertEqual(expected, sw.get_stream_value())
        sw.close()

    def test_write_bytes(self):
        sw = StreamWriter()
        value = bytes([0x01, 0x02, 0x03])
        sw.write_bytes(value)
        expected = bytes([0x03, 0x00, 0x00, 0x00, 0x01, 0x02, 0x03])
        self.assertEqual(7, sw.get_size())
        self.assertEqual(expected, sw.get_stream_value())
        sw.write_bytes(value)
        expected = bytes([0x03, 0x00, 0x00, 0x00, 0x01, 0x02, 0x03, 0x00, 0x03, 0x00, 0x00, 0x00, 0x01, 0x02, 0x03])
        self.assertEqual(15, sw.get_size())
        self.assertEqual(expected, sw.get_stream_value())
        sw.close()

    def test_write_string(self):
        sw = StreamWriter()
        value = 'hello'
        sw.write_string(value)
        expected = bytes([0x05, 0x00, 0x00, 0x00, ord('h'), ord('e'), ord('l'), ord('l'), ord('o')])
        self.assertEqual(9, sw.get_size())
        self.assertEqual(expected, sw.get_stream_value())
        sw.write_string(value)
        expected = bytes([0x05, 0x00, 0x00, 0x00, ord('h'), ord('e'), ord('l'), ord('l'), ord('o'), 0x00, 0x00, 0x00, 0x05, 0x00, 0x00, 0x00, ord('h'), ord('e'), ord('l'), ord('l'), ord('o')])
        self.assertEqual(21, sw.get_size())
        self.assertEqual(expected, sw.get_stream_value())
        sw.close()

    def test_reset(self):
        sw = StreamWriter()
        value = 0x17
        sw.write_uint64(value)
        sw.write_uint64(value)
        sw.reset()
        expected = b''
        self.assertEqual(expected, sw.get_stream_value())
        self.assertEqual(0, sw.get_size())
        sw.close()


if __name__ == '__main__':
    unittest.main()
