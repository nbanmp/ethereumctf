# ethereum-ctf
Ethereum-ctf is a framework for capture the flag competitions on the ethereum blockchain. It is a CTFd plugin (https://github.com/CTFd/CTFd). It currently connects to a http web3 provider and allows for deploying and testing Ethereum contracts (It will run it itself soon). 
## Usage
Just paste the solidity source and the test condition into the boxes provided when creating a contract of type "ethereum."
[TODO: screenshots and code snippets]
## Requirements
 - dill (pip install dill)
 - testrpc

## Installation
Place it in the `CTFd/plugins/` directory.

## Bugs
 - If the server stops, active addresses stop working and new ones must be requested.
 - Changing flags does not work, nor do multiple flags.
 - A testrpc instance needs to be running and an unsecured address must manually be pasted into the code. [FIX ME NEXT]

## Todo 
 - Run a proof of authority blockhain and connect to it itself. [FIX ME NEXT]
 - Use the database that already exists instead of the filesystem.
 - Allow deploying of non-solidity contracts. (Directly paste in the evm code)
   - Could be in the same input box. Just check for a 0x in front?
 - Create requirements.txt
