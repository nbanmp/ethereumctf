pragma solidity ^0.4.4;

import "vulnerable.sol";

contract Test {

    Vulnerable target;

    // Constructor
    function Test(address _target) public {
        target = Vulnerable(_target);
    }

    function validate() public constant returns (bool) {
        require(target.get() == 42);
        return true;
    }

    function getAddress() public constant returns (address) {
        return this;
    }
}

