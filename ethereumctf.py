import json
import time
from web3 import Web3, HTTPProvider, IPCProvider
from solc import compile_standard
from solc.exceptions import SolcError
import dill as pickle
from CTFd.plugins.ethereumctf import setup

address = '0x' + setup.setup()


web3 = Web3(HTTPProvider('http://localhost:8545'))

published_contracts = {}
contracts = {}
sources = {}
flags = {}
test_functions = {}
test_functions_sources = {}


try:
    with open('CTFd/saved_solidity.json', 'rb') as f:
        sources = pickle.loads(f.read())
except:
    sources = {}
    with open('CTFd/saved_solidity.json', 'wb') as f:
        f.write(pickle.dumps(sources))

try:
    with open('CTFd/saved_contracts.json', 'rb') as f:
        contracts = pickle.loads(f.read())
except:
    contracts = {}
    with open('CTFd/saved_contracts.json', 'wb') as f:
        f.write(pickle.dumps(contracts))

try:
    with open('CTFd/test_functions.json', 'rb') as f:
        test_functions = pickle.loads(f.read())
except:
    test_functions = {}
    with open('CTFd/test_functions.json', 'wb') as f:
        f.write(pickle.dumps(test_functions))

try:
    with open('CTFd/test_functions_sources.json', 'rb') as f:
        test_functions_sources = pickle.loads(f.read())
except:
    test_functions_source = {}
    with open('CTFd/test_functions_sources.json', 'wb') as f:
        f.write(pickle.dumps(test_functions_sources))

try:
    with open('CTFd/saved_flags.json', 'rb') as f:
        flags = pickle.loads(f.read())
except:
    flags = {}
    with open('CTFd/saved_flags.json', 'wb') as f:
        f.write(pickle.dumps(flags))

def compile_contracts(name, solidity_source, test_func_source, flag=None):
    global sources
    global contracts
    global flags
    global test_functions
    global test_functions_sources

    if flag == None:
        flag = flags[name]

    with open('CTFd/saved_solidity.json', 'rb') as f:
        sources = pickle.loads(f.read())

    backup_contracts = contracts

    # add to test_functions
    # TODO: Make better
    l = lambda contract: eval(test_func_source)
    test_functions[name] = l
    with open('CTFd/test_functions.json', 'wb') as f:
        f.write(pickle.dumps(test_functions))
    test_functions_sources[name] = test_func_source
    with open('CTFd/test_functions_sources.json', 'wb') as f:
        f.write(pickle.dumps(test_functions_sources))

    # Set solidity sources
    sources[name] = {}
    sources[name]['content'] = solidity_source

    # Add flag
    flags[name] = flag

    with open('CTFd/saved_flags.json', 'wb') as f:
        f.write(pickle.dumps(flags))

    # Compile Solidity
    try:
        contracts = compile_standard({
            'language': 'Solidity',
            'sources': sources
        })['contracts']

        # save stuffs
        with open('CTFd/saved_solidity.json', 'wb') as f:
            f.write(pickle.dumps(sources))
        with open('CTFd/saved_contracts.json', 'wb') as f:
            f.write(pickle.dumps(contracts))

        return True
    except Exception as e:
        return False

def deploy_contract(contractFromSolc):
    abi = contractFromSolc['abi']
    code = contractFromSolc['evm']['bytecode']['object']
    contract_factory = web3.eth.contract(abi, bytecode=code)

    contract_args = []
    trans_hash = contract_factory.deploy({
        'from': address,
        'value': 0,
        'gas': 1500000
    }, contract_args)
    time.sleep(10) # TODO: Do better. (Or just render a loading gif)
    txn_receipt = web3.eth.getTransactionReceipt(trans_hash)
    contract_address = txn_receipt['contractAddress']

    return contract_factory(address=contract_address)

# This is called when deploying for a normal person
def deploy_from_contracts(chal):
    global published_contracts
    global contracts
    global test_functions

    result = deploy_contract(contracts[chal]['Vulnerable'])
    published_contracts[result.address] = {}
    published_contracts[result.address]['contract'] = result
    published_contracts[result.address]['test_func'] = test_functions[chal]
    published_contracts[result.address]['flag'] = flags[chal]

    return result.address

def check_address_for_victory(address):
    global published_contracts
    try:
        if(published_contracts[address]['test_func'](published_contracts[address]['contract'])):
           return published_contracts[address]['flag']
        else:
           return False
    except KeyError as e:
        print("[DEBUG] Wrong address?")
        return "Try another address."

def check_example_for_victory(contract):
    print(contract.call().get())
    return contract.call().get() == 4

def deploy_new(challenge_name):
    if(challenge_name == "example"):
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

        return deployed_contract.address

if __name__ == "__main__":
    #compile_contracts('asdf', 'this should fail!')
    deployed_contract = published_contracts[deploy_new('example')]['contract']

    print(deployed_contract.call().getAddress())

    deployed_contract.transact({'from': address}).set(4, address)

    print(check_address_for_victory(deployed_contract.address))

    print(published_contracts)
