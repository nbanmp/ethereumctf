pragma solidity ^0.4.0;

contract Vulnerable {
    uint storedData; // This is never supposed to be 4

    function set(uint x, address adr) public {
        require(adr == msg.sender);
        storedData = x;
    }

    function get() public constant returns (uint) {
        return storedData;
    }

    function getAddress() public constant returns (address) {
        return this;
    }
}

