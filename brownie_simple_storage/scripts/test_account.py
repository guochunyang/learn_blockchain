from brownie import accounts, config
import os


def main():
    account = accounts.add(config["wallets"]["from_key"])
    print(account)
