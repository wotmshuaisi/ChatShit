#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = "CharlAnders"
__date__ = "5/10/2017"

import socket,json
import threading
from datetime import datetime

def printMsg(tempMsg):
	print(tempMsg.center(50, "-"))

def unPackData(tempData):
	tempData = json.loads(tempData[0].decode("utf-8"))
	return tempData

def packData(tempData):
	tempData = json.dumps(tempData).encode("utf-8")
	return tempData
def sendData(tempData):
	tempData = packData(tempData)
	udpClient.sendto(tempData,serverAdd)

def Auth():
	while True:
		tempData = dataFormat
		tempData['dataType'] = "Auth"
		userName = input("username:")
		userPass = input("password:")
		if not userName or not userPass:continue
		tempData['dataFrom'] = userName
		tempData['dataContents'] = userPass
		sendData(tempData)
		authRes = unPackData(udpClient.recvfrom(2000))
		if authRes['dataContents'] != 'True':continue
		break
	return userName

def GetMsg():
	global OnlineList
	while True:
		if threadLock:
			tempMsg = udpClient.recvfrom(2000)
			tempMsg = unPackData(tempMsg)
			if tempMsg['dataType'] == 'List':
				OnlineList = tempMsg['dataContents']
				print("\n")
				for i in OnlineList:
					print(i)
			if tempMsg['dataType'] == 'HList':OnlineList = tempMsg['dataContents']
			if tempMsg['dataType'] == 'Msg':print("\n\033[36m%s - %s :\033[0m\n\033[34m%s\033[0m\n" \
			%(tempMsg['dataFrom'],tempMsg['dataTime'],tempMsg['dataContents']))

def getOnlineList(userName,lType=True):
	tempData = dataFormat
	tempData['dataType'] = "List"
	if not lType:tempData['dataType'] = "HList"
	tempData['dataFrom'] = userName
	sendData(tempData)

def setUser(userName):
	for tempItem in OnlineList:
		if userName in tempItem and "Online" in tempItem:
			return True
	return False

def logoutUser(userName):
	tempData = dataFormat
	tempData['dataType'] = "Offline"
	tempData['dataFrom'] = userName
	sendData(tempData)






dataFormat = { #数据报字典
	"dataType" : "", #数据类型，包含auth(账户密码验证消息)、List（获取在线用户）、Msg（普通聊天消息）、Offline（退出用户）
	"dataContents" : "", #数据内容
	"dataSendTo" : "", #数据接收用户
	"dataFrom" : "", #数据发送用户
	"dataTime" : "" #数据发送时间
}
udpClient = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
serverAdd = ("127.0.0.1",10444) 

threadLock = True




printMsg("ChatShit! - bullshit chat soft ")
userName = Auth()
print("Welcome , %s" %userName)

t = threading.Thread(target=GetMsg)
t.setDaemon(True)
t.start()

OnlineList = []

print('''\n1. [ls] Get Online UserList
2. [set (username)] Set Chat User
3. [/q] Exit\n''')
while True:
	tempCmd = input("%s >" %userName)
	if tempCmd == "ls":getOnlineList(userName)
	if tempCmd == "/q":
		logoutUser(userName)
		print("bye bye , %s" %userName)
		break
	if tempCmd.startswith('set') :
		tempCmd = tempCmd.split(" ")
		if len(tempCmd) >= 2:
			setQuery = setUser(tempCmd[1])
		if not setQuery:
			print("user not exists or user is offline!")
			continue
		printMsg("Chat With %s , Exit with [/q]"%tempCmd[1])
		while True:
			tempData = dataFormat
			tempData['dataType'] = "Msg"
			tempData['dataSendTo'] = tempCmd[1]
			tempData['dataFrom'] = userName
			sendMsg = input()
			if not sendMsg:continue
			if sendMsg == "/q":break
			tempData['dataContents'] = sendMsg
			tempData['dataTime'] = datetime.now().strftime("%H:%M:%S")
			sendData(tempData)