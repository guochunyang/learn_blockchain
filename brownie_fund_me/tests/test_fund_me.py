from brownie import network, accounts

from scripts.deploy import get_account, deploy_fund_me


def test_can_fund():
    account = get_account()
    fund_me = deploy_fund_me()
    entrance_fee = fund_me.getEntranceFee() + 100
    tx = fund_me.fund({"from": account, "value": entrance_fee})
    tx.wait(1)
    # assert fund_me.addressToAmountFunded(account.address) == entrance_fee

