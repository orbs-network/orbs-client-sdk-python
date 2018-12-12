import unittest
import json
import base64
from typing import List
from codec.date_time import utc_string_to_date, date_to_utc_string
from codec.method_arguments import MethodArgument, Uint32Arg, Uint64Arg, BytesArg, StringArg
from codec.op_get_transaction_status import encode_get_transaction_status_request, decode_get_transaction_status_response, GetTransactionStatusRequest
from codec.op_send_transaction import encode_send_transaction_request, decode_send_transaction_response, SendTransactionRequest
from codec.op_call_method_request import encode_call_method_request, decode_call_method_response, CallMethodRequest
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


def json_unmarshal_base64_bytes(json_str: str) -> bytes:
    return base64.b64decode(json_str)


def json_marshal_base64_bytes(buf: bytes) -> str:
    return base64.b64encode(buf).decode('utf-8')


def json_unmarshal_number(json_str: str) -> int:
    return int(json_str)


def json_unmarshal_method_arguments(args: List[str], arg_types: List[str]) -> List[MethodArgument]:
    if len(args) != len(arg_types):
        raise ValueError(f'number of args {len(args)} is different than number of argTypes {len(arg_types)}')

    res = list()
    for i in range(len(args)):
        arg = args[i]
        arg_type = arg_types[i]
        if arg_type == 'uint32':
            res.append(Uint32Arg(json_unmarshal_number(arg)))
        elif arg_type == 'uint64':
            res.append(Uint64Arg(json_unmarshal_number(arg)))
        elif arg_type == 'string':
            res.append(StringArg(arg))
        elif arg_type == 'bytes':
            res.append(BytesArg(json_unmarshal_base64_bytes(arg)))
        else:
            raise ValueError(f'unknown arg type {arg_type}')
    return res


def json_marshal_method_arguments(args: List[MethodArgument]) -> List[str]:
    res = list()
    for arg in args:
        if isinstance(arg, Uint32Arg):
            res.append(str(arg))
        elif isinstance(arg, Uint64Arg):
            res.append(str(arg))
        elif isinstance(arg, StringArg):
            res.append(arg)
        elif isinstance(arg, BytesArg):
            res.append(json_marshal_base64_bytes(arg))
        else:
            raise ValueError(f'unsupported type in json marshal of method arguments')
    return res


class TestCodecContract(unittest.TestCase):

    def test_codec_contract(self):
        try:
            with open('./contract/test/codec/input.json', 'r') as input_file:
                contract_input = json.loads(input_file.read())

            with open('./contract/test/codec/output.json', 'r') as output_file:
                contract_output = json.loads(output_file.read())
        except FileNotFoundError:
            print('Contract spec input.json and output.json not found in ROOT/contract/test/codec\n'
                  'These files are cloned from the reference implementation found at\n'
                  'https://github.com/orbs-network/orbs-client-sdk-go.git when using setup.py dev command')
            raise

        for i in range(len(contract_input)):
            input_scenario = contract_input[i]
            output_scenario = contract_output[i]
            with self.subTest(TestId=input_scenario['Test']):

                if 'SendTransactionRequest' in input_scenario:
                    send_transaction_request = input_scenario['SendTransactionRequest']
                    encoded, tx_id = encode_send_transaction_request(SendTransactionRequest(
                        protocol_version=json_unmarshal_number(send_transaction_request['ProtocolVersion']),
                        virtual_chain_id=json_unmarshal_number(send_transaction_request['VirtualChainId']),
                        timestamp=utc_string_to_date(send_transaction_request['Timestamp']),
                        network_type=send_transaction_request['NetworkType'],
                        public_key=json_unmarshal_base64_bytes(send_transaction_request['PublicKey']),
                        contract_name=send_transaction_request['ContractName'],
                        method_name=send_transaction_request['MethodName'],
                        input_arguments=json_unmarshal_method_arguments(send_transaction_request['InputArguments'], input_scenario['InputArgumentsTypes'])
                        ), json_unmarshal_base64_bytes(input_scenario['PrivateKey']))

                    expected = json_unmarshal_base64_bytes(output_scenario['SendTransactionRequest'])
                    self.assertEqual(encoded, expected)
                    expected_tx_id = json_unmarshal_base64_bytes(output_scenario['TxId'])
                    self.assertEqual(tx_id, expected_tx_id)
                    continue

                if 'CallMethodRequest' in input_scenario:
                    call_method_request = input_scenario['CallMethodRequest']
                    encoded = encode_call_method_request(CallMethodRequest(
                        protocol_version=json_unmarshal_number(call_method_request['ProtocolVersion']),
                        virtual_chain_id=json_unmarshal_number(call_method_request['VirtualChainId']),
                        timestamp=utc_string_to_date(call_method_request['Timestamp']),
                        network_type=call_method_request['NetworkType'],
                        public_key=json_unmarshal_base64_bytes(call_method_request['PublicKey']),
                        contract_name=call_method_request['ContractName'],
                        method_name=call_method_request['MethodName'],
                        input_arguments=json_unmarshal_method_arguments(call_method_request['InputArguments'], input_scenario['InputArgumentsTypes'])))

                    expected = json_unmarshal_base64_bytes(output_scenario['CallMethodRequest'])
                    self.assertEqual(encoded, expected)
                    continue

                if 'GetTransactionStatusRequest' in input_scenario:
                    get_transaction_status_request = input_scenario['GetTransactionStatusRequest']
                    encoded = encode_get_transaction_status_request(GetTransactionStatusRequest(
                        protocol_version=json_unmarshal_number(get_transaction_status_request['ProtocolVersion']),
                        virtual_chain_id=json_unmarshal_number(get_transaction_status_request['VirtualChainId']),
                        tx_id=json_unmarshal_base64_bytes(get_transaction_status_request['TxId'])
                    ))

                    expected = json_unmarshal_base64_bytes(output_scenario['GetTransactionStatusRequest'])
                    self.assertEqual(encoded, expected)
                    continue

                if 'SendTransactionResponse' in input_scenario:
                    send_transaction_response = input_scenario['SendTransactionResponse']

                    decoded = decode_send_transaction_response(json_unmarshal_base64_bytes(send_transaction_response))
                    res = {
                        'BlockHeight': str(decoded.block_height),
                        'OutputArguments': json_marshal_method_arguments(decoded.output_arguments),
                        'RequestStatus': decoded.request_status.value,
                        'ExecutionResult': decoded.execution_result.value,
                        'BlockTimestamp': date_to_utc_string(decoded.block_timestamp),
                        'TxHash': json_marshal_base64_bytes(decoded.tx_hash),
                        'TransactionStatus': decoded.transaction_status.value
                    }

                    expected = output_scenario['SendTransactionResponse']
                    self.assertEqual(res, expected)
                    continue

                if 'CallMethodResponse' in input_scenario:
                    call_method_response = input_scenario['CallMethodResponse']

                    decoded = decode_call_method_response(json_unmarshal_base64_bytes(call_method_response))
                    res = {
                        'BlockHeight': str(decoded.block_height),
                        'OutputArguments': json_marshal_method_arguments(decoded.output_arguments),
                        'RequestStatus': decoded.request_status.value,
                        'ExecutionResult': decoded.execution_result.value,
                        'BlockTimestamp': date_to_utc_string(decoded.block_timestamp),
                    }

                    expected = output_scenario['CallMethodResponse']
                    self.assertEqual(res, expected)
                    continue

                if 'GetTransactionStatusResponse' in input_scenario:
                    get_transaction_status_response = input_scenario['GetTransactionStatusResponse']

                    decoded = decode_get_transaction_status_response(json_unmarshal_base64_bytes(get_transaction_status_response))
                    res = {
                        'BlockHeight': str(decoded.block_height),
                        'OutputArguments': json_marshal_method_arguments(decoded.output_arguments),
                        'RequestStatus': decoded.request_status.value,
                        'ExecutionResult': decoded.execution_result.value,
                        'BlockTimestamp': date_to_utc_string(decoded.block_timestamp),
                        'TxHash': json_marshal_base64_bytes(decoded.tx_hash),
                        'TransactionStatus': decoded.transaction_status.value
                    }

                    expected = output_scenario['GetTransactionStatusResponse']
                    self.assertEqual(res, expected)
                    continue

                self.fail(f'unhandled input scenario:\n{input_scenario}')


if __name__ == '__main__':
    unittest.main()
