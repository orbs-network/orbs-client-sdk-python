from typing import NamedTuple, List
from datetime import datetime
from codec.execution_result import ExecutionResult, execution_result_decode
from codec.transaction_status import TransactionStatus, transaction_status_decode
from codec.request_status import RequestStatus, request_status_decode
from codec.method_arguments import MethodArgument, method_arguments_opaque_decode
from codec.date_time import unix_nano_to_date
from crypto.digest import Digest
from codec.stream_writer import StreamWriter
from codec.stream_reader import StreamReader


class GetTransactionStatusRequest(NamedTuple):
    protocol_version: int
    virtual_chain_id: int
    tx_id: bytes


class GetTransactionStatusResponse(NamedTuple):
    request_status: RequestStatus
    tx_hash: bytes
    execution_result: ExecutionResult
    output_arguments: List[MethodArgument]
    transaction_status: TransactionStatus
    block_height: int
    block_timestamp: datetime


def encode_get_transaction_status_request(req: GetTransactionStatusRequest) -> bytes:
    # validate input
    if len(req.tx_id) != Digest.TX_ID_SIZE_BYTES:
        raise ValueError(f'expected TxID length {Digest.TX_ID_SIZE_BYTES}, {len(req.tx_id)} given')

    # extract tx_id
    tx_hash, tx_timestamp = Digest.extract_tx_id(req.tx_id)

    # encode get transaction status request
    msg = StreamWriter()
    msg.write_uint32(req.protocol_version)
    msg.write_uint32(req.virtual_chain_id)
    msg.write_uint64(tx_timestamp)
    msg.write_bytes(tx_hash)
    res = msg.get_stream_value()
    msg.close()
    return res


def decode_get_transaction_status_response(buf: bytes) -> GetTransactionStatusResponse:
    get_transaction_status_response_msg = StreamReader(buf)
    if get_transaction_status_response_msg.get_size() == 0:
        raise RuntimeError(f'response is corrupt and cannot be decoded')

    # decode request status
    request_status = request_status_decode(get_transaction_status_response_msg.read_uint16())

    # read transaction receipt message
    transaction_receipt_msg = StreamReader(get_transaction_status_response_msg.read_bytes())

    # read tx hash
    tx_hash = transaction_receipt_msg.read_bytes()

    # decode execution result
    execution_result = execution_result_decode(transaction_receipt_msg.read_uint16())

    # decode method arguments
    output_arguments = method_arguments_opaque_decode(transaction_receipt_msg.read_bytes())

    # decode transaction status
    transaction_status = transaction_status_decode(get_transaction_status_response_msg.read_uint16())

    # read block height
    block_height = get_transaction_status_response_msg.read_uint64()

    # decode block timestamp
    block_timestamp = unix_nano_to_date(get_transaction_status_response_msg.read_uint64())

    return GetTransactionStatusResponse(request_status=request_status,
                                        tx_hash=tx_hash,
                                        execution_result=execution_result,
                                        output_arguments=output_arguments,
                                        transaction_status=transaction_status,
                                        block_height=block_height,
                                        block_timestamp=block_timestamp)
