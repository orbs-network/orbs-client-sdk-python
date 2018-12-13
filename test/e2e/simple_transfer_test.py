import unittest
from os import sys, path
import orbs_client as orbs
import codec
import test.e2e.harness as harness
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


class TestSimpleTransfer(unittest.TestCase):

    __GAMMA_PORT = '8092'
    __GAMMA_ENDPOINT = 'localhost'
    __VIRTUAL_CHAIN_ID = 42  # gamma-cli config default

    def test_create_account(self):
        try:
            # start the gamma server
            harness.start_gamma_server(self.__GAMMA_PORT)

            # create sender and receiver accounts
            sender = orbs.create_account()
            receiver = orbs.create_account()

            # create client
            endpoint = f'http://{self.__GAMMA_ENDPOINT}:{self.__GAMMA_PORT}'
            client = orbs.Client(endpoint=endpoint,
                                 virtual_chain_id=self.__VIRTUAL_CHAIN_ID,
                                 network_type=codec.NetworkType.NETWORK_TYPE_TEST_NET.value)

            # create transfer transaction payload
            payload, tx_id = client.create_send_transaction_payload(public_key=sender.public_key,
                                                                    private_key=sender.private_key,
                                                                    contract_name='BenchmarkToken',
                                                                    method_name='transfer',
                                                                    input_arguments=[codec.Uint64Arg(10), codec.BytesArg(receiver.raw_address)])

            # send the payload
            transaction_response = client.send_transaction(payload)
            self.assertEqual(transaction_response.request_status.value, codec.RequestStatus.REQUEST_STATUS_COMPLETED.value)
            self.assertEqual(transaction_response.execution_result.value, codec.ExecutionResult.EXECUTION_RESULT_SUCCESS.value)
            self.assertEqual(transaction_response.transaction_status.value, codec.TransactionStatus.TRANSACTION_STATUS_COMMITTED.value)

            # create get status payload
            payload = client.create_get_transaction_status_payload(tx_id=tx_id)

            # send the payload
            status_response = client.get_transaction_status(payload)
            self.assertEqual(status_response.request_status.value, codec.RequestStatus.REQUEST_STATUS_COMPLETED.value)
            self.assertEqual(status_response.execution_result.value, codec.ExecutionResult.EXECUTION_RESULT_SUCCESS.value)
            self.assertEqual(status_response.transaction_status.value, codec.TransactionStatus.TRANSACTION_STATUS_COMMITTED.value)

            # create balance method call payload
            payload = client.create_call_method_payload(public_key=receiver.public_key,
                                                        contract_name='BenchmarkToken',
                                                        method_name='getBalance',
                                                        input_arguments=[codec.BytesArg(receiver.raw_address)])

            # send the call method payload
            balance_response = client.call_method(payload)
            self.assertEqual(balance_response.request_status.value, codec.RequestStatus.REQUEST_STATUS_COMPLETED.value)
            self.assertEqual(balance_response.execution_result.value, codec.ExecutionResult.EXECUTION_RESULT_SUCCESS.value)
            self.assertEqual(balance_response.output_arguments[0], codec.Uint64Arg(10))

        except Exception as e:
            print(f'Exception occurred: {e.args}')

        finally:
            # stop the gamma server
            harness.stop_gamma_server()
