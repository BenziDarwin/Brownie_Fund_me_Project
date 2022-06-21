from brownie import network, config, accounts, MockV3Aggregator
from web3 import Web3

DECIMALS = 18
STARTING_PRICE = 2000


def choose_account():
    if network.show_active() == "development":
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def deploy_mocks(_account):
    print("Deploying mocks...")
    if len(MockV3Aggregator) <= 0:
        MockV3Aggregator.deploy(
            DECIMALS, Web3.toWei(STARTING_PRICE, "ether"), {"from": _account}
        )
    print("Mocks deployed...")
