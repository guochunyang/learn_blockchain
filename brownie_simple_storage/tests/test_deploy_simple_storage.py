from brownie import SimpleStorage, accounts


def test_deploy():
    # 如果不指定 rpc，brownie 就默认本地启动一个网络
    # 所以这里不用担心 accounts 为空数组
    account = accounts[0]
    simple_storage = SimpleStorage.deploy({"from": account})
    starting_value = simple_storage.retrieve()
    expected = 0
    assert starting_value == 0


def test_updating_storage():
    account = accounts[0]
    simple_storage = SimpleStorage.deploy({"from": account})
    expected = 1334
    txn = simple_storage.store(expected, {"from": account})
    txn.wait(1)
    assert expected == simple_storage.retrieve()
