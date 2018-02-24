import bitso
import csv
import json
from datetime import datetime

api= bitso.Api()


configFileName="../config/config.json"
config_data=open(configFileName,"r")

data = json.load(config_data)
config_data.close()

date=datetime.now().strftime('%Y-%m-%d %H:%M:%S')

for ecoin in data:
	print "Checking "+ecoin
	tick = api.ticker(data[ecoin]["BitsoTag"])
	price=tick.bid
	print "coin value "+str(price)
	print "oz money "+str(data[ecoin]["MoneyInvested"])
	
	past=data[ecoin]["Current"]
	latest=data[ecoin]["MoneyCurrency"]*float(price)
	data[ecoin]["Current"]=data[ecoin]["MoneyCurrency"]*float(price)
	
	if abs(latest-past) >=100:
		print "notify OZ"
	
	current=data[ecoin]["Current"]
	max=data[ecoin]["Max"]
	min=data[ecoin]["Min"]
	
	if current > max:
		data[ecoin]["Max"]=current
	
	if current < min:
		data[ecoin]["Min"]=current
		
	print "current "+str(current)
		
	#print date
	print "********************************"
	
jsonFile = open(configFileName, "w+")
json.dump(data,jsonFile,indent=4)
jsonFile.close()