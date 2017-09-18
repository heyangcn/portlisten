#!/usr/bin/python
#coding=utf-8
import commands
import sys
##########返回命令执行结果
def getComStr(comand):
	try:
		stat, proStr = commands.getstatusoutput(comand)
	except:
		print "command %s execute failed, exit" % comand
	#将字符串转化成列表
	#proList = proStr.split("\n")
	return proStr
##########获取系统服务名称和监听端口
def filterList(commands):
	tmpStr = getComStr(commands)
	tmpList = tmpStr.split("\n")
	#del tmpList[0:2]
	newList = []
	for i in tmpList:
		if i.startswith(('tcp','udp')):
			val = i.split()
			del val[0:3]
			if i.startswith('tcp'):
				del val[1:3]
			else:
				del val[1:2]
			#提取端口号
			valTmp = val[0].split(":")
			val[0] = valTmp[1]
			#提取服务名称
			valTmp = val[1].split("/")
			val[1] = valTmp[-1]
			if val[1] != '-' and val not in newList:
				newList.append(val)
	return newList
def main():
	com = "netstat -tpln"
	if len(sys.argv) != 2:
		print "arguments error"
		return 
	if sys.argv[1] == 'tcp':
		com = 'netstat -tpln'	
	elif sys.argv[1] == 'udp':
		com = "netstat -upln"
	else:
		print "arguments error"	
		return 
	netInfo = filterList(com)
	if 0 == len(netInfo):
		print 'no information  you need'
		return 
	#格式化成适合zabbix lld的json数据
	json_data = "{\n" + "\t" + '"data":[' + "\n"
	#print netInfo
	for net in netInfo:
		if net != netInfo[-1]:
			json_data = json_data + "\t\t" + "{" + "\n" + "\t\t\t" + '"{#TCP_PORT}":"' + str(net[0]) + "\",\n" + "\t\t\t" + '"{#PNAME}":"' + str(net[1]) + "\"},\n"
		else:
			json_data = json_data + "\t\t" + "{" + "\n" + "\t\t\t" + '"{#TCP_PORT}":"' + str(net[0]) + "\",\n" + "\t\t\t" + '"{#PNAME}":"' + str(net[1]) + "\"}]}"
	print json_data
if __name__ == "__main__":
	main()
