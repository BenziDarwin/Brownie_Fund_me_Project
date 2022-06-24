from brownie import FundMe, MockV3Aggregator, network, config
from scripts.helpful_scripts import (
    choose_account,
    deploy_mocks,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)


def deploy_fund_me():
    # Setting up and creating contract
    account = choose_account()
    print("Deploying contract...")

    # Pass the priceFeed address into the deploy function
    # If on persisent network deploy as below,
    # Otherwise deploy mocks

    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        print(f"The active network is {network.show_active()}")
        deploy_mocks(account)
        price_feed_address = MockV3Aggregator[-1].address

    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()]["verify"],
    )
    print("Contract deployed!")

    # Show version
    print("Getting version of aggregatorInterface... \n")
    version = fund_me.version()
    print(version)

    # Get price
    eth_price = fund_me.getPrice()
    print(eth_price)
    return fund_me


def main():
    deploy_fund_me()
