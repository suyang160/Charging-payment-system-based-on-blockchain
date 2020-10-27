import json
import web3

from web3 import Web3
from solc import compile_source
from web3.contract import ConciseContract

# Solidity source code
contract_source_code ='''

pragma solidity ^0.4.21;

contract Chargingfee {
    uint public value;
    address public charger_owner;
    address public car_owner;

    function Chargingfee() public{
        charger_owner = msg.sender;
    }

    modifier onlycharger_owner() {
        require(msg.sender == charger_owner);
        _;
    }

    function payDeposit()
        public
        payable
    {
        car_owner = msg.sender;
    }

    function Finishcharging(address to,uint return_fee)
        onlycharger_owner()
    {
        to.transfer(return_fee);
    }

    function Withdraw_fund()
        onlycharger_owner()
    {
        charger_owner.transfer(this.balance);
    }
}'''


compiled_sol = compile_source(contract_source_code) # Compiled source code
contract_interface = compiled_sol['<stdin>:Chargingfee']

# web3.py instance
w3 = Web3(Web3.HTTPProvider("http://192.168.1.156:8042"))

# set pre-funded account as senderimport 
w3.eth.defaultAccount = w3.eth.accounts[1]
w3.personal.unlockAccount(w3.eth.accounts[1],'199628')

# Instantiate and deploy contract
Greeter = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])

# Submit the transaction that deploys the contract
tx_hash = Greeter.constructor().transact()

# Wait for the transaction to be mined, and get the transaction receipt
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

print('tx_receipt is',tx_receipt)
print('address is',tx_receipt.contractAddress)
# Create the contract instance with the newly-deployed address
greeter = w3.eth.contract(
    address=tx_receipt.contractAddress,
    abi=contract_interface['abi'],
)

print('abi is',contract_interface['abi'])


