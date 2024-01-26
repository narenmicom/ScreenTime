import time
import sys


time = time.localtime()
time = str(time.tm_hour) + ":" + str(time.tm_min) + ":" + str(time.tm_sec)

if(sys.argv[1] == 'start'):
	file = open("start.txt","a+")
	file.write(time+'\n')

if(sys.argv[1] == 'end'):
	file = open("end.txt","a+")
	file.write(time+'\n')
	
print("Time : "+time)


