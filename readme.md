# ethereum-ctf

Ethereum-ctf is a framework for capture the flag competitions on the ethereum blockchain.

## What it does

Creates and runs a proof of authority blockchain

Will create vulnerable contracts and test it with calls itself.


## Expected Usage

### Set up challenges properly in the directory structure:

File names "vulnerable.sol" and "test.py" are required.
"vulnerable.sol" is the vulnerable contract. There are no requirements to how it may be designed.
"test.js" is the condition required to win that challenge. See example test.js.

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
