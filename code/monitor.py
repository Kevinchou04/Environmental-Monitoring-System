import time
import RPi.GPIO as gpio

chanel = 13
def getvalue(chanel):
	j = 0
	data=[]
	gpio.setmode(gpio.BOARD)
	gpio.setwarnings(False)


	gpio.setup(chanel,gpio.OUT)
	gpio.output(chanel,gpio.HIGH)
	time.sleep(1)
	gpio.output(chanel,gpio.LOW)
	time.sleep(0.02)
	gpio.output(chanel,gpio.HIGH)

	#wait to response
	gpio.setup(chanel,gpio.IN)

	while gpio.input(chanel)==gpio.HIGH:
		continue

	while gpio.input(chanel)==gpio.LOW:
		continue

	while gpio.input(chanel)==gpio.HIGH:
		continue

	# get data
	while j<40:
		k=0
		while gpio.input(chanel)==gpio.LOW:
			pass
		while gpio.input(chanel)==gpio.HIGH:
			k+=1
			if k>100:
				break
		if k<3:
			data.append(0)
		else:
			data.append(1)
		j+=1
	# print('working')
	# print(data)
	return data

def getresult(chanel):
	# get temperature,humidity
	for i in range(10):
		data=getvalue(chanel)
		humidity_bit=data[0:8]
		humidity_point_bit=data[8:16]
		temperature_bit=data[16:24]
		temperature_point_bit=data[24:32]
		check_bit=data[32:40]

		humidity=0
		humidity_point=0
		temperature=0
		temperature_point=0
		check=0


		for i in range(8):
		    humidity+=humidity_bit[i]*2**(7-i)
		    humidity_point+=humidity_point_bit[i]*2**(7-i)
		    temperature+=temperature_bit[i]*2**(7-i)
		    temperature_point+=temperature_point_bit[i]*2**(7-i)
		    check+=check_bit[i]*2**(7-i)
 
		tmp=humidity+humidity_point+temperature+temperature_point
		if check==tmp:
		    print ("temperature is ", temperature,"wet is ",humidity,"%")
		else:
			continue
		    # print ("something is wrong .humidity:",humidity,"humidity_point:",humidity_point,"temperature:",temperature,"temperature_point:",temperature_point,"check:",check,"tmp:",tmp)
while (1):
	getresult(chanel)
gpio.cleanup()