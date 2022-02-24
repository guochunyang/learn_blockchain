from brownie import FundMe, config, accounts, network


def get_account():
    if network.show_active() == "development":
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def deploy_fund_me():
    account = get_account()
    fund_me = FundMe.deploy({"from": account})
    print(f"contract deployd to {fund_me.address}")
    return fund_me


def main():
    deploy_fund_me()
