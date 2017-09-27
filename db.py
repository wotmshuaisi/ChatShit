#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from os import path
import json

def dbFile(): #获取用户数据路径
	dbFile = "./Db/Users.json" #用户数据路径
	if not path.exists(dbFile): #如果不存在就直接退出
		raise "Data File not exists!"
	return dbFile #返回用户数据路径

def dbRead(): #获取用户数据json
	tempDbFile = dbFile() #获取路径
	with open(tempDbFile,'r') as fileRead: #打开数据文件
		tempData = fileRead.read() #读出数据文件
		tempData = json.loads(tempData) #通过json loads成["PassWord": "", "UserName": "", "UserTempAddr": , "Status": }]
	return tempData #返回json loads后的数据

def dbReadUser(userName): #获取单ge的用户的信息
	tempData = dbRead() #获取全部用户数据
	for tempLine in tempData: #遍历list
		if tempLine['UserName'] == userName: #如果当前元素用户名为传入用户名，返回当前用户名的字典
			return tempLine

def dbWrite(tempData): #写入数据
	tempdbFile = dbFile() #获取数据文件路径
	tempData = json.dumps(tempData) #将传入的tempdata打包成json
	with open(tempdbFile,'w') as fileWrite: #写入tempdata到数据文件
		fileWrite.write(tempData)

def userOnline(userName,userAddr): #设置用户在线状态
	tempData = dbRead() #读取数据
	for tempUserInfo in tempData: #遍历数据
		if tempUserInfo['UserName'] == userName: #如果遍历到用户名等于传入的用户名 就把在线状态设置为1 把传入的ip和端口写入到json文件
			tempUserInfo['Status'] = 1
			tempUserInfo['UserTempAddr'] = userAddr
	dbWrite(tempData) #写入

def userOffline(userName): #设置用户下线
	tempData = dbRead() #读取数据
	for tempUserInfo in tempData:#遍历数据
		if tempUserInfo['UserName'] == userName:#如果遍历到用户名等于传入的用户名 就把在线状态设置为0
			tempUserInfo['Status'] = 0
	dbWrite(tempData)#写入

def userList(userName): #获取在线用户列表
	tempList = []
	tempData = dbRead() #获取json文件数据
	for tempUserInfo in tempData: #遍历
		if tempUserInfo['UserName'] == userName: #如果传入用户面等于当前遍历到的用户名就不加入列表（用户本身在线是肯定的 只需要看看别人是不是在线）
			continue
		if tempUserInfo['Status'] == 1: #把在线用户加入列表 username[online or offline]
			tempList.append("%s[Online]" %tempUserInfo['UserName'])
			continue
		tempList.append("%s[Offline]" %tempUserInfo['UserName']) #把不在线用户加入列表username[online or offline]
	return tempList

def transMsg(userName): #服务器获取转发目标用户的IP/port
	tempUserInfo = dbReadUser(userName) #通过dbreaduser函数获取传入username的字典
	tempUserInfo = tempUserInfo['UserTempAddr'] #获取目标用户ip/port
	tempUserInfo = tuple(tempUserInfo) #转为元组
	return tempUserInfo #返回
