import subprocess
from subprocess import PIPE
import re
import os
import time
import socket

password = 'password'


def setup():
    # TODO: CHECK IF GETH IS ALREADY RUNNING

    os.system('pkill geth')

    password = 'password'

    p = subprocess.Popen('geth account list --datadir ~/.ethereum/ethereumctf'.split(), stdout=PIPE, stdin=PIPE, stderr=PIPE)
    sout, serr = p.communicate(bytes(password + '\n' + password + '\n', 'utf8'))
    match = re.search('{(.*)}', str(sout))
    if match:
        address = match.group(1)
    else:
        p = subprocess.Popen('geth account new --datadir ~/.ethereum/ethereumctf'.split(), stdout=PIPE, stdin=PIPE, stderr=PIPE)
        sout, serr = p.communicate(bytes(password + '\n' + password + '\n', 'utf8'))
        address = re.search('{(.*)}', str(sout)).group(1)

    print("Address: " + address)

    # http://blog.enuma.io/update/2017/08/29/proof-of-authority-ethereum-networks.html
    p = subprocess.Popen('puppeth', stdout=PIPE, stdin=PIPE, stderr=PIPE)
    sout, serr = p.communicate(bytes('ethereumctf\n2\n2\n5\n' + address + '\n\n' + address + '\n\n1337\nethereumctf poa blockchain\n2\nethereumctf.json\n', 'utf8'))

    # Initialize chain with genisis block
    p = subprocess.Popen('geth --networkid 1337 --datadir ~/.ethereum/ethereumctf init ethereumctf.json'.split(), stdout=PIPE, stdin=PIPE, stderr=PIPE)
    sout, serr = p.communicate()

    with open('password_file', 'w') as f:
        f.write(password)

    # Get enode.
    enode_uri = None
    while not enode_uri:
        try:
            p = subprocess.Popen(('geth --networkid 1337 --datadir ~/.ethereum/ethereumctf --ipcdisable').split(), stdout=PIPE, stderr=PIPE)
            time.sleep(5)
            os.system('kill ' + str(p.pid))
            sout, serr = p.communicate()
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            enode_uri = re.search('enode\S+$', str(serr), re.MULTILINE).group(0)[:-3].replace('[::]', ip)
        except:
            print("[DEBUG] Trying to get enode_uri again.")
            pass

    # Run the chain
    # geth --nodiscover --datadir ~/.ethereum/ethereumctf --unlock address --mine --rpcaddr 127.0.0.1 --rpcapi eth,net,web3,personal
    # This runs in the background
    subprocess.Popen(('geth --networkid 1337 --datadir ~/.ethereum/ethereumctf --unlock 0x' + address + ' --password password_file --mine --rpc --rpcaddr 127.0.0.1 --rpcapi admin,debug,miner,rpc,txpool,eth,net,web3,personal').split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(7)

    command_to_connect_to_our_node = 'geth --datadir ~/.ethereum/ctf --networkid 1337 --bootnodes "' + enode_uri + '"'

    print('[ETHEREUMCTF] Connect to our blockchain with this command:\n' + command_to_connect_to_our_node)

    os.remove('password_file')
    #os.remove('bootnodekey.key')

    #read genesis json
    with open('ethereumctf.json', 'r') as f:
        genesis_json = f.read()

    return address, command_to_connect_to_our_node, genesis_json

if __name__ == '__main__':
    setup()


