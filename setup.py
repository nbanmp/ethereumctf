import json
from web3 import Web3, HTTPProvider, IPCProvider
from solc import compile_standard

web3 = Web3(HTTPProvider('http://localhost:8545'))
sources = {}
with open('challenges/example/vulnerable.sol', 'r') as f:
    sources['vulnerable.sol'] = {}
    sources['vulnerable.sol']['content'] = f.read()

contracts = compile_standard({
    'language': 'Solidity',
    'sources': sources
})['contracts']

contractFromSolc = contracts['vulnerable.sol']['Vulnerable']

abi = contractFromSolc['abi']
code = contractFromSolc['evm']['bytecode']['object']
MyContract = web3.eth.contract(abi, bytecode=code)

contract_args = []
trans_hash = MyContract.deploy({
    'from': '0x1da7e787a1897046677e57e87177c4de88cc388a',
    'value': 0,
    'gas': 1500000
}, contract_args)
txn_receipt = web3.eth.getTransactionReceipt(trans_hash)
contract_address = txn_receipt['contractAddress']

deployed_contract = MyContract(address=contract_address)

print(deployed_contract.call().getAddress())
