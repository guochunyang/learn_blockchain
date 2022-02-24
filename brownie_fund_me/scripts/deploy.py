from brownie import FundMe, config, accounts, network, MockV3Aggregator


def get_account():
    if network.show_active() == "development":
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def deploy_fund_me():
    account = get_account()

    if network.show_active() != "development":
        # 正式环境
        pass
    else:
        # 部署 mock
        account = get_account()
        mock_price_feed = MockV3Aggregator.deploy(8, 200000000000, {"from": account})
        print("Deploy mock ...")
        # return mock_price_feed

    fund_me = FundMe.deploy(
        "0x8A753747A1Fa494EC906cE90E9f37563A8AF630e", {"from": account}
    )
    print(f"contract deployd to {fund_me.address}")
    return fund_me


def main():
    deploy_fund_me()
