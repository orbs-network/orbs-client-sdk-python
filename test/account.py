import unittest
from os import sys, path
from orbs_client.account import Account
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


class TestAccount(unittest.TestCase):

    def test_create_account(self):
        sender = Account.create_account()
        receiver = Account.create_account()
        self.assertNotEqual(sender.private_key, receiver.private_key)
        self.assertNotEqual(sender.raw_address, receiver.raw_address)


if __name__ == '__main__':
    unittest.main()
