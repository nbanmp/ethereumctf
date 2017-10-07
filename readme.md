# ethereum-ctf

Ethereum-ctf is a framework for capture the flag competitions on the ethereum blockchain.

## What it does

Creates and runs a proof of authority blockchain

Will create vulnerable contracts and test it with calls itself.

Hosts a rest api to provide target addesses to users and check if solutions were right.

Stores shared challenges as an object to match addresses up with challenges.

## Expected Usage

### Set up challenges properly in the directory structure:

File names "vulnerable.sol" and "test.py" are required.
"vulnerable.sol" is the vulnerable contract. It must have a contract called "Vulnerable" 
"test.py" is the condition required to win that challenge. See example test.py.

```
Challenges
|
└───Challenge Name
│   │  vulnerable.sol
│   │  test.py
│
└───Challenge2 Name
│   │  vulnerable.sol
│   │  test.py
```

### Start
Run node start.js with the arguments you want.
