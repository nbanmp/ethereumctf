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
Place it in the `CTFd/plugins/` directory.

## Bugs
 - Changing flags does not work, nor do multiple flags.
 - the geth instance doesn't stop and just runs in the background forever.
 - the geth instance is restarted and a new blockchain is created each time.  

## Todo 
 - Use the database that already exists instead of the filesystem.
 - Allow deploying of non-solidity contracts. (Directly paste in the evm code)
   - Could be in the same input box. Just check for a 0x in front?
   - Also need abi
 - Create requirements.txt
 - Check if a blockchain is already running and dont restart it if it is not necessary.
