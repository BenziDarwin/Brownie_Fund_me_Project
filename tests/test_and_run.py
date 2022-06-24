from brownie import FundMe, accounts, network, exceptions
from scripts.helpful_scripts import choose_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from scripts.deploy import deploy_fund_me
import pytest


def test_can_fund_and_withdraw():
    account = choose_account()
    fund_me = deploy_fund_me()
    entrance_fee = fund_me.getEntranceFee()

    # Fund
    txn = fund_me.fundMe({"from": account, "value": entrance_fee})
    txn.wait(1)
    assert fund_me.addressToSender(account.address) == (entrance_fee)

    # Withdraw
    txn2 = fund_me.withdraw({"from": account})
    txn2.wait(1)
    assert fund_me.addressToSender(account.address) == 0


def test_withdraw_only_owner():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only local envronments!")

    account = choose_account()
    account2 = accounts[1]
    fund_me = deploy_fund_me()
    # fund_me.withdraw({"from": account2})
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from": account2})
