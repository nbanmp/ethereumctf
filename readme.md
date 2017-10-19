# ethereum-ctf
Ethereum-ctf is a framework for capture the flag competitions on the ethereum blockchain. It is a CTFd plugin (https://github.com/CTFd/CTFd). It runs a proof of authority blockchain and connects to a http web3 provider that it runs and allows for deploying and testing Ethereum contracts. 
## Usage
Just paste the solidity source and the test condition into the boxes provided when creating a contract of type "ethereum."
[TODO: screenshots and code snippets]
## Requirements
 - dill (pip install dill)
 - testrpc
 - puppeth
 - geth
 - port 30301 open

## Installation
Place it in the `CTFd/plugins/` directory.

## Bugs
 - Changing flags does not work, nor do multiple flags.
 - the geth instance doesn't stop and just runs in the background forever.

## Todo 
 - Use the database that already exists instead of the filesystem.
 - Allow deploying of non-solidity contracts. (Directly paste in the evm code)
   - Could be in the same input box. Just check for a 0x in front?
   - Also need abi
 - Create requirements.txt
 - Provide access to the running blockchain to teams and admins. Provide a simple geth command to connect to it.
   - https://github.com/ethereum/go-ethereum/wiki/Setting-up-private-network-or-local-cluster#private-network
   - Also need to run geth so it is available on a port
   - Just run a bootnode and provide the right url
   - STATUS: Bootnode runs, now integrate with CTFd.
