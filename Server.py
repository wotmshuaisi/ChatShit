#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = "CharlAnders"
__date__ = "5/10/2017"

import socketserver
import db
import json

class UDPServer(socketserver.BaseRequestHandler):
	dataFormat = { 
	"dataType" : "", 
	"dataContents" : "", 
	"dataSendTo" : "", 
	"dataFrom" : "", 
	"dataTime" : "" 
	}

	def unpackData(self):
		self.transferMsg = json.loads(self.request[0].decode("utf-8"))

	def packData(self):
		self.transferMsg = json.dumps(self.transferMsg).encode("utf-8")

	def getOnlineUser(self,lType = True): 
		tempList = self.dataFormat
		tempList["dataType"] =  "List"
		if not lType:tempList["dataType"] =  "HList"
		tempList["dataContents"] = db.userList(self.transferMsg['dataFrom']) 
		tempList = json.dumps(tempList).encode("utf-8")
		return tempList 

	def transMsg(self): 
		print("%s -> %s - %s : %s" %(self.transferMsg['dataFrom'],self.transferMsg['dataSendTo'],self.transferMsg['dataTime'],self.transferMsg['dataContents']) ) 
		sendToAddr = db.transMsg(self.transferMsg['dataSendTo']) 
		self.packData()	 
		self.request[1].sendto(self.transferMsg,sendToAddr) 

	def offlineUser(self): 
		db.userOffline(self.transferMsg['dataFrom']) 

	def userAuth(self): 
		tempData = self.dataFormat
		tempData['dataType'] = "Auth"
		tempUserInfo = db.dbReadUser(self.transferMsg['dataFrom']) 
		if tempUserInfo and self.transferMsg['dataContents'] == tempUserInfo['PassWord'] and tempUserInfo['Status'] != 1: 
			db.userOnline(self.transferMsg['dataFrom'],self.transferAdd) 
			tempData['dataContents'] = "True"
		else:
			tempData['dataContents'] = "False"
		tempData = json.dumps(tempData).encode("utf-8")
		return tempData

	def handle(self):
		self.unpackData() 
		self.transferAdd = self.client_address 
		print("User - %s \t Action - %s" %(self.transferMsg['dataFrom'],self.transferMsg['dataType']))
		if self.transferMsg['dataType'] == 'Auth': 
			self.request[1].sendto(self.userAuth(),self.transferAdd) 
		if self.transferMsg['dataType'] == 'List': 
			self.request[1].sendto(self.getOnlineUser(),self.transferAdd) 
		if self.transferMsg['dataType'] == "Offline": 
			self.offlineUser() 
		if self.transferMsg['dataType'] == "Msg": 
			self.transMsg() 

if __name__ == "__main__":
	print("ChatShit Server".center(50,"*"))
	serverAdd = ("127.0.0.1",10444) 
	Server = socketserver.ThreadingUDPServer(serverAdd,UDPServer)
	Server.serve_forever()