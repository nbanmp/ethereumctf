import json
from web3 import Web3, HTTPProvider, IPCProvider
from solc import compile_standard

web3 = Web3(HTTPProvider('http://localhost:8545'))

published_contracts = {}

def deploy_contract(contractFromSolc):
    abi = contractFromSolc['abi']
    code = contractFromSolc['evm']['bytecode']['object']
    contract_factory = web3.eth.contract(abi, bytecode=code)

    contract_args = []
    trans_hash = contract_factory.deploy({
        'from': '0x1da7e787a1897046677e57e87177c4de88cc388a',
        'value': 0,
        'gas': 1500000
    }, contract_args)
    txn_receipt = web3.eth.getTransactionReceipt(trans_hash)
    contract_address = txn_receipt['contractAddress']

    return contract_factory(address=contract_address)


def check_address_for_victory(address):
    global published_contracts
    try:
        return published_contracts[address]['test_func'](published_contracts[address]['contract'])
    except KeyError as e:
        return False

def check_example_for_victory(contract):
    print(contract.call().get())
    return contract.call().get() == 4

# Read solidity sources
sources = {}
with open('challenges/example/vulnerable.sol', 'r') as f:
    sources['vulnerable.sol'] = {}
    sources['vulnerable.sol']['content'] = f.read()

# Compile Solidity
contracts = compile_standard({
    'language': 'Solidity',
    'sources': sources
})['contracts']

# THIS IS THE PROCESS FOR DEPLOYING A CONTRACT AND ADDING IT TO THE published_contracts DICT:
# Select the contract
contractFromSolc = contracts['vulnerable.sol']['Vulnerable']
# Deploy the contract
deployed_contract = deploy_contract(contractFromSolc)
# Give it its own spot in published_contracts
published_contracts[deployed_contract.address] = {}
published_contracts[deployed_contract.address]['contract'] = deployed_contract
# Add a function to test to see if it has been solved
published_contracts[deployed_contract.address]['test_func'] = check_example_for_victory

if __name__ == "__main__":
    print(deployed_contract.call().getAddress())

    deployed_contract.transact({'from': '0x1da7e787a1897046677e57e87177c4de88cc388a'}).set(4, "0x1da7e787a1897046677e57e87177c4de88cc388a")

    print(check_address_for_victory(deployed_contract.address))

    print(published_contracts)
