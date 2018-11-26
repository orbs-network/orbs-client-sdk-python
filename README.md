# Orbs Client SDK Python

> Client SDK for the Orbs blockchain in Python

## Usage

1. Create a few end user accounts:

    ```python
    import orbs
    sender = orbs.create_account();
    receiver = orbs.create_account();
    ```
    
2. Create a client instance:

    ```python
    virtual_chain_Id = 42;
    client = orbs.client("http://node-endpoint.com", virtual_chain_Id, "TEST_NET");
    ```

3. Send a transaction:

    ```python
    payload, tx_id = client.create_send_transaction_payload(
      sender.public_key,
      sender.private_key,
      "BenchmarkToken",
      "transfer"
    );
    response = client.send_transaction(payload);
    ```
    
4. Check the transaction status:

    ```python
    payload = client.create_get_transaction_status_payload(tx_id);
    response = client.get_transaction_status(payload);
    ```
    
5. Call a smart contract method:

    ```python
    payload = client.create_call_method_payload(
      receiver.public_key,
      "BenchmarkToken",
      "getBalance"
    );
    response = client.call_method(payload);
    ```

## Installation

1. Install Gamma: https://github.com/orbs-network/orbs-contract-sdk
2. Install the package:

    ```sh
    pip install orbs
    ```
    
3. Import the client in your project:

    ```python
    import orbs
    ```

## Test

Coming soon
