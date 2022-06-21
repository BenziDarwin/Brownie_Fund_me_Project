//SPDX-License-Identifier: MIT

pragma solidity >=0.6.0 <0.9.0;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

//import "@chainlink/contracts/src/v0.8/vendor/SafeMathChainlink.sol";

contract FundMe {
    mapping(address => uint256) public addressToSender;
    address[] funders;
    address owner;
    AggregatorV3Interface priceFeed;

    constructor(address _priceFeed) public {
        owner = msg.sender;
        priceFeed = AggregatorV3Interface(_priceFeed);
    }

    function fundMe() public payable {
        uint256 minimumUSD = 50 * 10**18;
        require(
            getConversionRate(msg.value) >= minimumUSD,
            "You need to spend more ETH!"
        );
        addressToSender[msg.sender] = msg.value;
        funders.push(msg.sender);
    }

    function version() public view returns (uint256) {
        return priceFeed.version();
    }

    function getPrice() public view returns (uint256) {
        (, int256 answer, , , ) = priceFeed.latestRoundData();
        return uint256(answer * 10000000000);
    }

    function getConversionRate(uint256 _ethAmount)
        public
        view
        returns (uint256)
    {
        uint256 ethPrice = getPrice();
        uint256 ethToUsd = (ethPrice * _ethAmount) / 1000000000000000000;
        //return ethToUsd;
        // In Usd
        return ethToUsd;
        //0.0000111367029894
    }

    modifier OnlyOwner() {
        require(msg.sender == owner, "You are not the owner of this contract");
        _;
    }

    function withdraw() public payable OnlyOwner {
        // Only want the owner of the contract to withdraw all funds
        payable(msg.sender).transfer(address(this).balance);
        for (uint256 index; index < funders.length; index++) {
            addressToSender[funders[index]] = 0;
            funders = new address[](0);
        }
    }
}
