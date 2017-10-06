pragma solidity ^0.4.0;

contract Vulnerable {
    uint storedData; // This is never supposed to be 42

    function set(uint x, address adr) public {
        storedData = x;
    }

    function get() public constant returns (uint) {
        return storedData;
    }

    function getAddress() public constant returns (address) {
        return this;
    }
}

