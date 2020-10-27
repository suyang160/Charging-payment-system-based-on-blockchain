import serial
import time
import rsa
import random
import json
import web3
from gpiozero import *
from time import strftime,asctime,ctime,gmtime,mktime
from time import sleep
from web3 import Web3
from web3.contract import ConciseContract

HC05_Port = serial.Serial("/dev/ttyUSB0",9600)
HC05_EN = OutputDevice(4)                     #if this pin sets high,enable the bluetooth,otherwise disable
HC05_EN.off()                             	  #default disable bluetooth
button = Button(2)                            #if the button has been pressed long for 2 seconds,enable the bluetooth
HC05_State = InputDevice(17)                  #if the bluetooth is connected, the pin is high.
button27 = Button(27)                         #simulate the action of putting on the gun
button10 = Button(10)                         #simulate the action of putting off the gun
LED22 =  OutputDevice(22)                     #simulate the process of charging
LED22.off()
HC05_State_flag = 0
lasttime_state = 0
HC05_EN_flag = 0

w3 = Web3(Web3.HTTPProvider("http://192.168.1.156:8042"))
w3.eth.defaultAccount = w3.eth.accounts[1]
w3.personal.unlockAccount(w3.eth.accounts[1],'199628')
chargingfee = w3.eth.contract(
    address='0x325804dA67A1d008c2F12d9b1C79B28eD1Da9618',
    abi=[{'constant': True, 'inputs': [], 'name': 'value', 'outputs': [{'name': '', 'type': 'uint256'}], 'payable': False, 'stateMutability': 'view', 'type': 'function'}, {'constant': False, 'inputs': [], 'name': 'Withdraw_fund', 'outputs': [], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'function'}, {'constant': False, 'inputs': [], 'name': 'payDeposit', 'outputs': [], 'payable': True, 'stateMutability': 'payable', 'type': 'function'}, {'constant': True, 'inputs': [], 'name': 'car_owner', 'outputs': [{'name': '', 'type': 'address'}], 'payable': False, 'stateMutability': 'view', 'type': 'function'}, {'constant': True, 'inputs': [], 'name': 'charger_owner', 'outputs': [{'name': '', 'type': 'address'}], 'payable': False, 'stateMutability': 'view', 'type': 'function'}, {'constant': False, 'inputs': [{'name': 'to', 'type': 'address'}, {'name': 'return_fee', 'type': 'uint256'}], 'name': 'Finishcharging', 'outputs': [], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'constructor'}]
)


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

def receive_data_not_encode():
	sleep(2)
	count = HC05_Port.inWaiting()
	if count!=0:
		recv = HC05_Port.read(count)
		return recv
	else:
		return None	

def send_data(str,delay=1):
	sleep(delay)
	HC05_Port.flushOutput()
	HC05_Port.write(str.encode())
	return

def send_data_raw(str,delay=1):
	sleep(delay)
	HC05_Port.flushOutput()
	HC05_Port.write(str)
	return


while True:
	if button.is_pressed:
		sleep(0.5)	
		if button.is_pressed:
			print(timestamp("The button has been Pressed, this button simulate the geomagnetic sensor's signal"))
			while button.is_pressed:
				pass
			HC05_EN.on()
			HC05_EN_flag = 1
	if HC05_EN_flag == 1:
		if HC05_State.value == 0:
			if lasttime_state == 1:
				print(timestamp("The bluetooth has not been connected"))
				lasttime_state = 0 
				HC05_State_flag = 0
		else:
			if lasttime_state == 0:
				print(timestamp("The bluetooth has been connected"))
				lasttime_state = 1
				HC05_State_flag = 1
	if HC05_State_flag == 1:
		HC05_Port.write('Request_public_key'.encode())
#			WaitACK()
		HC05_Port.flushInput()
		sleep(1)
		count = HC05_Port.inWaiting()
		if count != 0:
			recv = HC05_Port.read(count).decode()
			print(timestamp("Have received the public key"))
#				AnswerACK()         
			with open('public.pem',encoding='utf-8') as publickfile:
				p = publickfile.read()
			if recv == p:
				print(timestamp("The public key has been registered"))
				HC05_Port.flushOutput()
				HC05_Port.write("The public key has been registered".encode())
				WaitACK()
				nonce = random.randint(1,1000000000)
				print(timestamp("Have generated the nonce "+str(nonce)))
				HC05_Port.write(str(nonce).encode("utf-8"))
				recv = receive_data_not_encode()
				if recv != None:
					print(timestamp("Have received the signature"))
					AnswerACK()
					pubkey = rsa.PublicKey.load_pkcs1(p)
				try:
					rsa.verify(str(nonce).encode("utf-8"), recv, pubkey)
				except rsa.pkcs1.VerificationError:
					print(timestamp("The signature has been authenticated failurely"))
				else:
					print(timestamp("The signature has authenticated successfully"))
					print(timestamp("Waiting for the charging pile plug"))
					button27_flag = True
					while button27_flag == True:
						if button27.is_pressed:
							sleep(0.5)	
							if button27.is_pressed:
								print(timestamp("Start the charging process"))
								send_data("Start the charging process")
								WaitACK()
								startchaging = time.time()
								LED22.on()
								button27_flag = False

					button10_flag = True	
					while button10_flag == True:
						if button10.is_pressed:
							sleep(0.5)	
							if button10.is_pressed:
								print(timestamp("End the charging process"))
								send_data("End the charging process")
								WaitACK()
								endchaging = time.time()
								LED22.off()
								button10_flag = False

				charging_durition = endchaging - startchaging
				print(timestamp("The duration of charging is "+str(charging_durition)))	
				HC05_State_flag = 0

			else:
				print(timestamp(" The public key hasn't been registered, then will trigger the smart contract"))
				HC05_Port.flushOutput()
				HC05_Port.write("The public key has not been registered".encode())
				WaitACK()
				HC05_Port.write("0x325804dA67A1d008c2F12d9b1C79B28eD1Da9618".encode())
				print(timestamp("Have sent the contract address"))
				WaitACK()
				HC05_Port.write("10".encode())
				print(timestamp("Have sent the value of deposit"))
				WaitACK()

				tx_hash = receive_data_not_encode()
				print(timestamp("The car has generated a tx hash"))
				AnswerACK()
				if w3.eth.getTransaction(tx_hash).value == Web3.toWei(10, 'ether'):
					print(timestamp("The transaction has pay the right deposit value"))
				else:
					print(timestamp("The transaction has not pay the right deposit value"))
				while w3.eth.getTransaction(tx_hash).blockNumber==0:
					pass
				print(timestamp("The transaction has been mined"))
				print(timestamp("Waiting for the charging pile plug"))
				button27_flag = True
				while button27_flag == True:
					if button27.is_pressed:
						sleep(0.5)	
						if button27.is_pressed:
							print(timestamp("Start the charging process"))
							send_data("Start the charging process")
							WaitACK()							
							startchaging = time.time()
							LED22.on()
							button27_flag = False

				button10_flag = True	
				while button10_flag == True:
					if button10.is_pressed:
						sleep(0.5)	
						if button10.is_pressed:
							print(timestamp("End the charging process"))
							send_data("End the charging process")
							WaitACK()						
							endchaging = time.time()
							LED22.off()
							button10_flag = False
				charging_durition = endchaging - startchaging
				print(timestamp("The duration of charging is "+str(charging_durition)))
				fee_need = charging_durition*100000000000000000
				print(timestamp("The fee of charging is "+str(fee_need)+" Wei"))
				return_fee = 10*1000000000000000000 - fee_need
				tx_hash = chargingfee.functions.Finishcharging(w3.eth.accounts[2],Web3.toWei(int(return_fee), 'wei')).transact()
				print(timestamp("Have generated the fee deduction transaction"))
				AnswerACK()     #position1
				send_data_raw(tx_hash)
				# print(w3.eth.getTransaction(tx_hash))
				charger_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
				print(timestamp("Have received the fee deduction transaction receipt"))
				# print(charger_receipt)
				HC05_State_flag = 0

		

    
	
	              

