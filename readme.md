# ethereum-ctf
Ethereum-ctf is a framework for capture the flag competitions on the ethereum blockchain. It is a CTFd plugin (https://github.com/CTFd/CTFd). It runs a proof of authority blockchain and connects to a http web3 provider that it runs and allows for deploying and testing Ethereum contracts. 

## Usage
Just paste the solidity source and the test condition into the boxes provided when creating a contract of type "ethereum."
[TODO: screenshots and code snippets]

## Requirements
 - dill (pip install dill)
 - testrpc
 - puppeth
 - bootnode
 - geth
 - ports 30301 (UDP) & 30303 (TCP & UDP) open

## Installation
Clone it into the `CTFd/plugins/` directory.

## Bugs
 - Changing flags does not work, nor do multiple flags.
 - the geth instance doesn't stop and just runs in the background forever.
 - the geth instance is restarted and a new blockchain is created each time.  
 - geth command with domain in enode does not work; it needs an ip

## Todo 
 - Use the database that already exists instead of the filesystem.
 - Allow deploying of non-solidity contracts. (Directly paste in the evm code)
   - Could be in the same input box. Just check for a 0x in front?
   - Also need abi
 - Create requirements.txt
 - Create config.html
 - Check if a blockchain is already running and don't restart it if it is not necessary.
 - Load accounts with ethereum
 - Allow for starting contracts with ethereum
 - Provide accurate instructions for connecting to the blockchain with geth
   - Correct ip in enode
   - geth's enode, not bootstrap
   - provide genesis.json (currently named ethereumctf.json) and use:
     - `geth --datadir ~/.ethereum/ctf init genesis.json`
   - provide correct geth command to execute next
     - `geth --datadir ~/.ethereum/ctf --networkid 1337 --bootnodes "enode//bleh@ip:30303"`
