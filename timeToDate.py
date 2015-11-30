#coding=utf-8
import time
import sys

def tranceTime(inputTime):
	if isinstance(inputTime, int) == False:
		inputTime = int(inputTime)
	timeTuple = time.localtime(inputTime)
	print(time.strftime('%Y-%m-%d %H:%M:%S', timeTuple)+'\n')

def doInput():
	inputTime = input('请手动输入时间戳:\n')
	tranceTime(inputTime)
	doInput()
	
if len(sys.argv)>1:
	tranceTime(sys.argv[1])
else:
	doInput();