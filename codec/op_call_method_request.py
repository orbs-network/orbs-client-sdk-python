from typing import NamedTuple, List
from datetime import datetime
from codec.network_type import NetworkType, network_type_encode
from codec.method_arguments import MethodArgument, method_arguments_opaque_encode, method_arguments_opaque_decode
from codec.request_status import RequestStatus, request_status_decode
from codec.execution_result import ExecutionResult, execution_result_decode
from codec.date_time import date_to_unix_nano, unix_nano_to_date
from streams.stream_writer import StreamWriter
from streams.stream_reader import StreamReader
from crypto.keys import Keys


class CallMethodRequest(NamedTuple):
    protocol_version: int
    virtual_chain_id: int
    timestamp: datetime
    network_type: NetworkType
    public_key: bytes
    contract_name: str
    method_name: str
    input_arguments: List[MethodArgument]


class CallMethodResponse(NamedTuple):
    request_status: RequestStatus
    execution_result: ExecutionResult
    output_arguments: List[MethodArgument]
    block_height: int
    block_timestamp: datetime


def encode_call_method_request(req: CallMethodRequest) -> bytes:
    # validate inputs
    if req.protocol_version != 1:
        raise ValueError(f'expected ProtocolVersion 1, {req.protocol_version} given')
    if len(req.public_key) != Keys.ED25519_PUBLIC_KEY_SIZE_BYTES:
        raise ValueError(f'expected PublicKey length {Keys.ED25519_PUBLIC_KEY_SIZE_BYTES}, {len(req.public_key)} given')

    # encode method arguments
    input_arguments_bytes = method_arguments_opaque_encode(req.input_arguments)

    # encode network type
    network_type = network_type_encode(req.network_type)

    # encode timestamp
    timestamp_nano = date_to_unix_nano(req.timestamp)

    # encode eddsa signer
    eddsa_signer = StreamWriter()
    eddsa_signer.write_uint16(network_type)
    eddsa_signer.write_bytes(req.public_key)
    signer = StreamWriter()
    signer.write_uint16(0)  # eddsa signer
    signer.write_bytes(eddsa_signer.get_stream_value())

    # encode transaction details
    transaction = StreamWriter()
    transaction.write_uint32(req.protocol_version)
    transaction.write_uint32(req.virtual_chain_id)
    transaction.write_uint64(timestamp_nano)
    transaction.write_bytes(signer.get_stream_value())
    transaction.write_string(req.contract_name)
    transaction.write_string(req.method_name)
    transaction.write_bytes(input_arguments_bytes)

    # encode call method message
    msg = StreamWriter()
    msg.write_bytes(transaction.get_stream_value())
    res = msg.get_stream_value()

    eddsa_signer.close()
    signer.close()
    transaction.close()
    msg.close()
    return res


def decode_call_method_response(buf: bytes) -> CallMethodResponse:
    call_method_response_msg = StreamReader(buf)
    if call_method_response_msg.get_size() == 0:
        raise RuntimeError(f'response is corrupt and cannot be decoded')

    # decode request status
    request_status = request_status_decode(call_method_response_msg.read_uint16())

    # decode method arguments
    output_arguments = method_arguments_opaque_decode(call_method_response_msg.read_bytes())

    # decode execution result
    execution_result = execution_result_decode(call_method_response_msg.read_uint16())

    # read block height
    block_height = call_method_response_msg.read_uint64()

    # decode block timestamp
    block_timestamp = unix_nano_to_date(call_method_response_msg.read_uint64())

    return CallMethodResponse(request_status=request_status,
                              execution_result=execution_result,
                              output_arguments=output_arguments,
                              block_height=block_height,
                              block_timestamp=block_timestamp)
