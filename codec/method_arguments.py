from streams.stream_writer import StreamWriter
from streams.stream_reader import StreamReader
from typing import Union, List


class Uint32Arg(int):
    pass


class Uint64Arg(int):
    pass


class StringArg(str):
    pass


class BytesArg(bytes):
    pass


MethodArgument = Union[Uint32Arg, Uint64Arg, StringArg, BytesArg]


def method_arguments_opaque_encode(args: List[MethodArgument]) -> bytes:
    msg = StreamWriter()
    for arg in args:
        method_arg = StreamWriter()
        if isinstance(arg, Uint32Arg):
            method_arg.write_bytes(b'uint32')
            method_arg.write_uint16(0)
            method_arg.write_uint32(arg)
        elif isinstance(arg, Uint64Arg):
            method_arg.write_bytes(b'uint64')
            method_arg.write_uint16(1)
            method_arg.write_uint64(arg)
        elif isinstance(arg, StringArg):
            method_arg.write_bytes(b'string')
            method_arg.write_uint16(2)
            method_arg.write_string(arg)
        elif isinstance(arg, BytesArg):
            method_arg.write_bytes(b'bytes')
            method_arg.write_uint16(3)
            method_arg.write_bytes(arg)
        else:
            raise ValueError(f'unsupported MethodArgument type: {type(arg)}')
        msg.write_bytes(method_arg.get_stream_value())
        method_arg.close()

    res = msg.get_stream_value()
    msg.close()
    return res


def method_arguments_opaque_decode(buf: bytes) -> List[MethodArgument]:
    args = list()
    method_args_reader = StreamReader(buf)

    while not method_args_reader.done_reading():
        arg = StreamReader(method_args_reader.read_bytes())
        name = arg.read_bytes()  # not using the arg name
        arg_type = arg.read_uint16()

        if arg_type == 0:
            val = arg.read_uint32()
            args.append(Uint32Arg(val))
        elif arg_type == 1:
            val = arg.read_uint64()
            args.append(Uint64Arg(val))
        elif arg_type == 2:
            val = arg.read_string()
            args.append(StringArg(val))
        elif arg_type == 3:
            val = arg.read_bytes()
            args.append(BytesArg(val))
        else:
            raise ValueError(f'received MethodArgument {name} has an unknown type: {arg_type}')

    return args
