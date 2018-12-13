# Orbs Client SDK Python

> Client SDK for the Orbs blockchain in Python

## Installation
1. Clone this repo to a directory in your computer

2. Install the package:

    ```sh
    python setup.py install
    ```
3. The package will be built in `./build/lib/orbs_client`
    
4. Import the client-sdk in your project:

    ```python
    import orbs_client as orbs
    ```

## Usage

1. Create a few end user accounts:

    ```python
    import orbs_client as orbs
    sender = orbs.create_account()
    receiver = orbs.create_account()
    ```
    
2. Create a client instance:

    ```python
    virtual_chain_Id = 42
    client = orbs.Client("http://node-endpoint.com", virtual_chain_Id, "TEST_NET")
    ```

3. Send a transaction:

    ```python
    payload, tx_id = client.create_send_transaction_payload(
      sender.public_key,
      sender.private_key,
      "BenchmarkToken",
      "transfer",
      [codec.Uint64Arg(10), codec.BytesArg(receiver.raw_address)])
    )
    response = client.send_transaction(payload)
    ```
    
4. Check the transaction status:

    ```python
    payload = client.create_get_transaction_status_payload(tx_id)
    response = client.get_transaction_status(payload)
    ```
    
5. Call a smart contract method:

    ```python
    payload = client.create_call_method_payload(
      receiver.public_key,
      "BenchmarkToken",
      "getBalance"
    )
    response = client.call_method(payload)
    ```

## Test

#### All tests (including Codec Contract test) 
To make sure the client implementation is compliant to the Orbs protocol specifications, there are several compliance tests, named codec contract tests.
The codec contract test requires an input and output JSON files which are located in https://github.com/orbs-network/orbs-client-sdk-go.git.

To execute all tests, run the setup package with the test flag:
```sh
python setup.py test
```

#### End-to-End test with Gamma server
Gamma server is a local development server for the Orbs network that can run on your own machine and be used for testing. This server can process smart contract deployments and transactions. The server is accessed via HTTP (just like a regular node) which makes it excellent for testing clients.

1. Install the Gamma server (https://github.com/orbs-network/orbs-contract-sdk)
    
    ```sh
    brew install orbs-network/devtools/gamma-cli
    ```
    
2. Run the end to end test script:
    
    ```sh
    python setup.py test_e2e
    ```
    
## Requirements    
The client SDK requires Python 3.7 and above
