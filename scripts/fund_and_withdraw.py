from brownie import FundMe, accounts
from scripts.helpful_scripts import choose_account
from scripts.deploy import deploy_fund_me


def fund():
    account = choose_account()
    fund_me = deploy_fund_me()
    entrance_fee = fund_me.getEntranceFee()
    # Showing entrance fee
    print(entrance_fee)
    fund_me.fundMe({"from": account, "value": entrance_fee / 1000})


def withdraw():
    account = choose_account()
    fund_me = FundMe[0]
    fund_me.withdraw({"from": account})


def main():
    fund()
    withdraw()
