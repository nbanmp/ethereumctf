import subprocess
from subprocess import PIPE
import re
import os
import time


password = 'password'


def setup():
    # TODO: CHECK IF GETH IS ALREADY RUNNING (Perhaps not in this func?)
    # TODO: CHECK IF ACCOUNTS ALREADY EXIST

    os.system('rm -r ~/.ethereum/ethereumctf')
    os.system('pkill geth')

    password = 'password'
    p = subprocess.Popen('geth account new --datadir ~/.ethereum/ethereumctf'.split(), stdout=PIPE, stdin=PIPE, stderr=PIPE)
    sout, serr = p.communicate(bytes(password + '\n' + password + '\n', 'utf8'))
    address = re.search('{(.*)}', str(sout)).group(1)
    print("Address: " + address)

    # http://blog.enuma.io/update/2017/08/29/proof-of-authority-ethereum-networks.html
    p = subprocess.Popen('puppeth', stdout=PIPE, stdin=PIPE, stderr=PIPE)
    sout, serr = p.communicate(bytes('ethereumctf\n2\n2\n5\n' + address + '\n\n' + address + '\n\n\nethereumctf poa blockchain\n2\nethereumctf.json\n', 'utf8'))

    # Initialize chain with genisis block
    p = subprocess.Popen('geth --nodiscover --datadir ~/.ethereum/ethereumctf init ethereumctf.json'.split(), stdout=PIPE, stdin=PIPE, stderr=PIPE)
    sout, serr = p.communicate()

    with open('password_file', 'w') as f:
        f.write(password)

    # Run the chain
    # geth --nodiscover --datadir ~/.ethereum/ethereumctf --unlock address --mine --rpcaddr 127.0.0.1 --rpcapi eth,net,web3,personal
    # This runs in the background
    subprocess.Popen(('geth --nodiscover --datadir ~/.ethereum/ethereumctf --unlock 0x' + address + ' --password password_file --mine --rpc --rpcaddr 127.0.0.1 --rpcapi eth,net,web3,personal').split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    time.sleep(7)

    os.remove('password_file')

    return address

if __name__ == '__main__':
    setup()


