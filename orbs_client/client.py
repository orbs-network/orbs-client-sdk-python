from typing import List
from datetime import datetime
import requests
from codec.network_type import NetworkType
from codec.method_arguments import MethodArgument
from codec.op_send_transaction import encode_send_transaction_request, decode_send_transaction_response, SendTransactionRequest, SendTransactionResponse
from codec.op_call_method_request import encode_call_method_request, decode_call_method_response, CallMethodRequest, CallMethodResponse
from codec.op_get_transaction_status import encode_get_transaction_status_request, decode_get_transaction_status_response, GetTransactionStatusRequest, GetTransactionStatusResponse
from crypto.base58_encoding import Base58


class Client:
    __PROTOCOL_VERSION = 1
    __CONTENT_TYPE = 'application/octet-stream'
    __SEND_TRANSACTION_URL = '/api/v1/send-transaction'
    __CALL_METHOD_URL = '/api/v1/call-method'
    __GET_TRANSACTION_STATUS_URL = '/api/v1/get-transaction-status'

    def __init__(self, endpoint: str, virtual_chain_id: int, network_type: NetworkType):
        self.__endpoint = endpoint
        self.__virtual_chain_id = virtual_chain_id
        self.__network_type = network_type

    def create_send_transaction_payload(self, public_key: bytes, private_key: bytes, contract_name: str, method_name: str, input_arguments: List[MethodArgument]):
        req, tx_id = encode_send_transaction_request(SendTransactionRequest(
            protocol_version=self.__PROTOCOL_VERSION,
            virtual_chain_id=self.__virtual_chain_id,
            timestamp=datetime.utcnow(),
            network_type=self.__network_type,
            public_key=public_key,
            contract_name=contract_name,
            method_name=method_name,
            input_arguments=input_arguments), private_key)
        return req, Base58.encode(tx_id)

    def create_call_method_payload(self, public_key: bytes, contract_name: str, method_name: str, input_arguments: List[MethodArgument]) -> bytes:
        return encode_call_method_request(CallMethodRequest(
            protocol_version=self.__PROTOCOL_VERSION,
            virtual_chain_id=self.__virtual_chain_id,
            timestamp=datetime.utcnow(),
            network_type=self.__network_type,
            public_key=public_key,
            contract_name=contract_name,
            method_name=method_name,
            input_arguments=input_arguments))

    def create_get_transaction_status_payload(self, tx_id: str) -> bytes:
        raw_tx_id = Base58.decode(bytes(tx_id))
        return encode_get_transaction_status_request(GetTransactionStatusRequest(
            protocol_version=self.__PROTOCOL_VERSION,
            virtual_chain_id=self.__virtual_chain_id,
            tx_id=raw_tx_id))

    def send_transaction(self, payload: bytes) -> SendTransactionResponse:
        res = self.send_http_post(self.__SEND_TRANSACTION_URL, payload)
        return decode_send_transaction_response(res.content)

    def call_method(self, payload: bytes) -> CallMethodResponse:
        res = self.send_http_post(self.__CALL_METHOD_URL, payload)
        return decode_call_method_response(res.content)

    def get_transaction_status(self, payload: bytes) -> GetTransactionStatusResponse:
        res = self.send_http_post(self.__GET_TRANSACTION_STATUS_URL, payload)
        return decode_get_transaction_status_response(res.content)

    def send_http_post(self, relative_url: str, payload: bytes):
        if len(payload) == 0:
            raise ValueError('payload sent by https is empty')

        res = requests.post(url=self.__endpoint + relative_url, data=payload, headers={'Content-Type': self.__CONTENT_TYPE})
        if res.content is None:
            raise RuntimeError(f'no response data available, http status: {res.status_code}, {res.reason}')
        return res
