// SPDX-License-Identifier: MIT

pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";

contract FundMe {
    using SafeMathChainlink for uint256;

    // 谁向合约付了多少钱
    mapping(address => uint256) public addressToAmountFunded;

    // 所有付款者的地址
    address[] public funders;
    // 合约创建者的 token
    address public owner;

    constructor() public {
        owner = msg.sender;
    }

    function fund() public payable {
        // 设置一个付款最低值
        uint256 minUSD = 5 * 10**18;
        require(
            getConversionRate(msg.value) >= minUSD,
            "you need to spend more ETH!!!"
        );

        addressToAmountFunded[msg.sender] += msg.value;
        funders.push(msg.sender);
    }

    function getVersion() public view returns (uint256) {
        // address https://docs.chain.link/docs/ethereum-addresses/#Rinkeby%20Testnet
        AggregatorV3Interface priceFeed = AggregatorV3Interface(
            0x8A753747A1Fa494EC906cE90E9f37563A8AF630e
        );
        return priceFeed.version();
    }

    function getPrice() public view returns (uint256) {
        AggregatorV3Interface priceFeed = AggregatorV3Interface(
            0x8A753747A1Fa494EC906cE90E9f37563A8AF630e
        );

        (, int256 answer, , , ) = priceFeed.latestRoundData();
        // 252987782319 -> 2529877823190000000000
        // 2529877823190000000000
        // decimals() 方法代表返回值中小数点个数，这意味着 252987782319 的实际值为 2529.87782319
        // 因为 ETH 到 wei 为 10**18 所以这里需要补齐 (18-8) = 10 个10
        // 为什么不直接除掉 10**8 猜测是为了保留精度又不使用浮点数
        return uint256(answer * 10000000000);
    }

    function getConversionRate(uint256 ethAmount)
        public
        view
        returns (uint256)
    {
        uint256 ethPrice = getPrice();
        uint256 ethAmountInUsd = (ethPrice * ethAmount) / 1000000000000000000;
        // 最终结果为 1ether代表多少USD
        // input 1 , output: 2529
        return ethAmountInUsd;
    }

    function getEntranceFee() public view returns (uint256) {
        // minimumUSD
        uint256 minimumUSD = 50 * 10**18;
        uint256 price = getPrice();
        uint256 precision = 1 * 10**18;
        // 最后的单位是 wei 还是 gWei ?
        // return (minimumUSD * precision) / price;
        // We fixed a rounding error found in the video by adding one!
        return ((minimumUSD * precision) / price) + 1;
    }

    modifier onlyOwner() {
        //is the message sender owner of the contract?
        require(msg.sender == owner, "you are not owner");

        _;
    }

    function withdraw() public payable onlyOwner {
        // 归还所有的 eth
        msg.sender.transfer(address(this).balance);

        for (
            uint256 funderIndex = 0;
            funderIndex < funders.length;
            funderIndex++
        ) {
            address funder = funders[funderIndex];
            addressToAmountFunded[funder] = 0;
        }

        // 清空数据
        funders = new address[](0);
    }
}
