from __future__ import absolute_import
import json
from solcx import compile_standard, install_solc
from web3 import Web3

install_solc("0.6.0")

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()


compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.6.0",
)

# 将编译好的数据保存在磁盘上
with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get abi
abi = json.loads(
    compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["metadata"]
)["output"]["abi"]


w3 = Web3(Web3.HTTPProvider("http://0.0.0.0:8545"))
chain_id = 1337
my_address = "0x199DCdA4A025EE5d7802Cb87f01235fa1911B0D3"  # todo
private_key = "0x7b3351b7f355088e834e7d1f57bfa32cbcbcb88af77ef2054e5eb2a06d217795"

# 创建 SimpleStorage 合约对象
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
# 貌似以太坊中的 nonce 是以账户的 txn 数量来生成的
nonce = w3.eth.getTransactionCount(my_address)
print(f"Current nonce: {nonce}")
# 构建一个交易，来部署合约
transaction = SimpleStorage.constructor().buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce,
    }
)
# 使用私钥进行解密
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
print("Deploying Contract!")
# Send it!
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
# Wait for the transaction to be mined, and get the transaction receipt
print("Waiting for transaction to finish...")
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(f"Done! Contract deployed to {tx_receipt.contractAddress}")


# Working with deployed Contracts
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
print(f"Initial Stored Value {simple_storage.functions.retrieve().call()}")

# 调用合约中的 store
greeting_transaction = simple_storage.functions.store(15).buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce + 1,
    }
)
signed_greeting_txn = w3.eth.account.sign_transaction(
    greeting_transaction, private_key=private_key
)
tx_greeting_hash = w3.eth.send_raw_transaction(signed_greeting_txn.rawTransaction)
print("Updating stored Value...")
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_greeting_hash)

print(
    f"After updating Value, Stored Value {simple_storage.functions.retrieve().call()}"
)
