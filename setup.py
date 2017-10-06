import json
from web3 import Web3, HTTPProvider, IPCProvider
from solc import compile_standard

web3 = Web3(HTTPProvider('http://localhost:8545'))

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

def check_example_for_victory(contract):
    print(contract.call().get())
    return contract.call().get() == 4

sources = {}
with open('challenges/example/vulnerable.sol', 'r') as f:
    sources['vulnerable.sol'] = {}
    sources['vulnerable.sol']['content'] = f.read()

contracts = compile_standard({
    'language': 'Solidity',
    'sources': sources
})['contracts']

contractFromSolc = contracts['vulnerable.sol']['Vulnerable']

deployed_contract = deploy_contract(contractFromSolc)

print(deployed_contract.call().getAddress())

deployed_contract.transact({'from': '0x1da7e787a1897046677e57e87177c4de88cc388a'}).set(2, "0x1da7e787a1897046677e57e87177c4de88cc388a")

print(check_example_for_victory(deployed_contract))
