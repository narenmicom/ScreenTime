import time

time = time.localtime()
time = str(time.tm_hour) + ":" + str(time.tm_min) + ":" + str(time.tm_sec)

txt_file = open("start.txt","a+")
txt_file.write(time+'\n')
print("Start Time" + time)
