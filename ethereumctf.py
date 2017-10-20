import json
import time
from web3 import Web3, HTTPProvider, IPCProvider
from solc import compile_standard
from solc.exceptions import SolcError
import dill as pickle
from CTFd.plugins.ethereumctf.setup import setup

#challenges = {}
#challenges[challenge]['solidity']['compiled'] = a string == contracts[chalid]
#challenges[challenge]['solidity']['source'] = a string == contracts[chalid]
#challenges[challenge]['python_check'] = a string
#challenges[challenge]['deployed'] = []
#challenges[challenge]['flag']

def load_challenges():
    try:
        with open('CTFd/saved_challenges.pickle', 'rb') as f:
            challenges = pickle.loads(f.read())
    except:
        challenges = {}
    return challenges

address, connect_to_geth_command = setup()
address = '0x' + address
web3 = Web3(HTTPProvider('http://localhost:8545'))
challenges = load_challenges()

def save_challenges():
    with open('CTFd/saved_challenges.pickle', 'wb') as f:
        f.write(pickle.dumps(challenges))

def compile_contract(chalid, solidity_source, test_func_source, flag=None):
    # add flag
    if flag == None:
        flag = challenges[chalid]['flag']
    else:
        challenges[chalid] = {}
        challenges[chalid]['flag'] = flag

    # add test function
    # TODO: Make better
    challenges[chalid]['python_check'] = test_func_source
    # To use: lambda contract: eval(challenges[chalid]['python_check'])
    # Set solidity sources
    challenges[chalid]['solidity'] = {}
    challenges[chalid]['solidity']['source'] = solidity_source

    try:
        # Compile Solidity
        contracts = compile_standard({
            'language': 'Solidity',
            'sources': { chalid: {'content': challenges[chalid]['solidity']['source'] } }
        })['contracts']

        challenges[chalid]['solidity']['compiled'] = contracts[chalid]

        save_challenges()
        return True
    except Exception as e:
        return False

# This is called when deploying for a normal person
def deploy_from_chalid(chalid):
    r = deploy_contract(challenges[chalid]['solidity']['compiled']['Vulnerable'])
    if not 'deployed' in challenges[chalid]:
        challenges[chalid]['deployed'] = []
    challenges[chalid]['deployed'].append(r.address)

    save_challenges()
    return r.address

def deploy_contract(compiled_contract, contract_args=[]):
    abi = compiled_contract['abi']
    code = compiled_contract['evm']['bytecode']['object']
    contract_factory = web3.eth.contract(abi, bytecode=code)

    trans_hash = contract_factory.deploy({
        'from': address,
        'value': 0,
        'gas': 1500000
    }, contract_args)
    time.sleep(10) # TODO: Do better. (Or just render a loading gif and pretend we're good.)
    txn_receipt = web3.eth.getTransactionReceipt(trans_hash)
    contract_address = txn_receipt['contractAddress']

    return contract_factory(address=contract_address)

def check_address_for_victory(chalid, address):
    if address in challenges[chalid]['deployed']:
        contract = web3.eth.contract(address=address, abi=challenges[chalid]['solidity']['compiled']['Vulnerable']['abi'])
        print(challenges[chalid]['python_check'])
        if( (lambda contract: eval(challenges[chalid]['python_check']))(contract) ):
            return challenges[chalid]['flag']
        else:
           return False
        #dostuff
        pass
    else:
        return "Try another address."


if __name__ == '__main__':
    pass
