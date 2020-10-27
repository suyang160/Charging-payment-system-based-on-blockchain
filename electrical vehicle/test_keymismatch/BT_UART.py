import serial
import time
import rsa
import json
import web3
from time import strftime,asctime,ctime,gmtime,mktime
from time import sleep
from web3 import Web3
from web3.contract import ConciseContract
from gpiozero import *

w3 = Web3(Web3.HTTPProvider("http://192.168.1.156:8042"))
w3.eth.defaultAccount = w3.eth.accounts[2]
w3.personal.unlockAccount(w3.eth.accounts[2],'199628')
chargingfee = w3.eth.contract(
    address='0x325804dA67A1d008c2F12d9b1C79B28eD1Da9618',
    abi=[{'constant': True, 'inputs': [], 'name': 'value', 'outputs': [{'name': '', 'type': 'uint256'}], 'payable': False, 'stateMutability': 'view', 'type': 'function'}, {'constant': False, 'inputs': [], 'name': 'Withdraw_fund', 'outputs': [], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'function'}, {'constant': False, 'inputs': [], 'name': 'payDeposit', 'outputs': [], 'payable': True, 'stateMutability': 'payable', 'type': 'function'}, {'constant': True, 'inputs': [], 'name': 'car_owner', 'outputs': [{'name': '', 'type': 'address'}], 'payable': False, 'stateMutability': 'view', 'type': 'function'}, {'constant': True, 'inputs': [], 'name': 'charger_owner', 'outputs': [{'name': '', 'type': 'address'}], 'payable': False, 'stateMutability': 'view', 'type': 'function'}, {'constant': False, 'inputs': [{'name': 'to', 'type': 'address'}, {'name': 'return_fee', 'type': 'uint256'}], 'name': 'Finishcharging', 'outputs': [], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'constructor'}]
)

HC05_Port = serial.Serial("/dev/ttyUSB0",9600)
HC05_State = InputDevice(17)                  #if the bluetooth is connected, the pin is high.
lasttime_state = 0
def WaitACK():
	WaitAck_flag = True
	while WaitAck_flag:
		HC05_Port.flushInput()
		sleep(1)
		count = HC05_Port.inWaiting()
		if count !=0:
			recv = HC05_Port.read(count)
			if recv.decode() == "Have received the data":
				WaitAck_flag = False
			else:
				pass

def AnswerACK():
	HC05_Port.flushOutput()
	HC05_Port.write("Have received the data".encode())
	return
    
def timestamp(str1):
	now_time = strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
	return now_time+" "+str1

def receive_data(delay=1):
	sleep(delay)
	count = HC05_Port.inWaiting()
	if count!=0:
		recv = HC05_Port.read(count)
		return recv.decode()
	else:
		return None

def receive_data_raw(delay=1):
	sleep(delay)
	count = HC05_Port.inWaiting()
	if count!=0:
		recv = HC05_Port.read(count)
		return recv
	else:
		return None

while True:
	count = HC05_Port.inWaiting()
	if HC05_State.value == 0:
		if lasttime_state == 1:
			print(timestamp("The bluetooth has not been connected"))
			lasttime_state = 0 
	else:
		if lasttime_state == 0:
			print(timestamp("The bluetooth has been connected"))
			lasttime_state = 1
	if count !=0:
		sleep(0.1)
		count = HC05_Port.inWaiting()
		recv = str(HC05_Port.read(count).decode())
		if recv == 'Request_public_key':
			print(timestamp("Have got the request of public key successfully"))
#			AnswerACK()
			# HC05_Port.flushInput()
			# HC05_Port.write("ACK")
			# sleep(1)
			with open('public.pem') as publickfile:
				p = publickfile.read()
				HC05_Port.flushOutput()
				HC05_Port.write(p.encode())
				print(timestamp("Have sent the public key successfully"))
#				WaitACK()
			HC05_Port.flushInput()
			sleep(1)
			count = HC05_Port.inWaiting()
			if count != 0:
				recv = HC05_Port.read(count).decode()
				AnswerACK()
				if recv == "The public key has been registered":
					data = receive_data()
					if data != None:
						print(timestamp("Have received the nonce"))
						with open('private.pem',encoding='utf-8') as privatefile:
							p = privatefile.read()
							privkey = rsa.PrivateKey.load_pkcs1(p)
							signature = rsa.sign(data.encode(), privkey, 'SHA-1')
							HC05_Port.write(signature)
							WaitACK()
						print(timestamp("Have generated the signature and sent the signature"))
						data = None
						while data != "End the charging process":
							data = receive_data()
							if data == "Start the charging process":
								print(timestamp("Have started the charging process"))
								AnswerACK()
							elif data == "End the charging process":
								print(timestamp("Have ended the charging process"))
								AnswerACK()

						

					pass
				else:
					print(timestamp("The public key has not been registered"))
					contract_address = receive_data()
					print(timestamp("Have received the contract's address: "+contract_address))
					AnswerACK()
					Deposit_value = receive_data()
					print(timestamp("Have received the value of the deposit"+Deposit_value))
					AnswerACK()
					print(timestamp("Prepare to pay the deposit"))
					tx_hash = chargingfee.functions.payDeposit().transact({'value': Web3.toWei(int(Deposit_value), 'ether')})
					print(timestamp("The transaction hash has been generated "))
					sleep(1)
					HC05_Port.write(tx_hash)
					WaitACK()
					car_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
					print(timestamp("Have received the car deposit transaction receipt"))
					data = None
					while data != "End the charging process":
						data = receive_data()
						if data == "Start the charging process":
							print(timestamp("Have started the charging process"))
							AnswerACK()
						elif data == "End the charging process":
							print(timestamp("Have ended the charging process"))
							AnswerACK()
					WaitACK()     #position1
					tx_hash = receive_data_raw(2)
					print(timestamp("Have received the charging end fee deduction transaction hash"))
					# print(w3.eth.getTransaction(tx_hash))
					charger_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
					print(timestamp("Have received the charging end fee deduction transaction receipt"))
					# print(charger_receipt)
		else:
			print(timestamp("Have not got the request of public key successfully"))




