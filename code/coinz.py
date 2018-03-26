import bitso
import json
from datetime import datetime
import tweepy


def notify(message,coin,value,timestamp,max,min):
	tweet_api.update_status(message+" "+coin+" "+value+" "+"max "+max+" min "+min+" "+timestamp)
	
api= bitso.Api()

#Loading App configuration file
configFileName="../config/config.json"
config_data=open(configFileName,"r")
data = json.load(config_data)
config_data.close()

date=datetime.now().strftime('%Y-%m-%d %H:%M:%S')

#Loading keys to for tweet updates
tweetFileName="../config/twitterKeys.json"
tweet_data=open(tweetFileName,"r")
tweet= json.load(tweet_data)
tweet_data.close()

#handling twitter authentication
auth = tweepy.OAuthHandler(tweet["twitter"]["CONSUMER_KEY"],tweet["twitter"]["CONSUMER_SECRET"])
auth.set_access_token(tweet["twitter"]["ACCESS_KEY"], tweet["twitter"]["ACCESS_SECRET"])
tweet_api = tweepy.API(auth)

#Main
for ecoin in data:
	print "Checking "+ecoin
	tick = api.ticker(data[ecoin]["BitsoTag"])
	price=tick.bid
	print "coin value "+str(price)
	print "oz money "+str(data[ecoin]["MoneyInvested"])
	
	data[ecoin]["Current"]=data[ecoin]["MoneyCurrency"]*float(price)
	current=data[ecoin]["Current"]
	max=data[ecoin]["Max"]
	min=data[ecoin]["Min"]
	
	if current-data[ecoin]["Notify"] >= data[ecoin]["Increment"]:
		print "<<<Notify Increment>>>"
		notify("Incremento",ecoin,str(current),date,str(max),str(min))
		data[ecoin]["Notify"]+=data[ecoin]["Increment"]
		
	elif current-data[ecoin]["Notify"] < -100 :
		print "<<<Notify Decrement>>>"
		notify("Decremento",ecoin,str(current),date,str(max),str(min))
		data[ecoin]["Notify"]-=data[ecoin]["Increment"]
		
		
	if current > max:
		data[ecoin]["Max"]=current
	
	if current < min:
		data[ecoin]["Min"]=current
		
	print "current "+ecoin+" "+str(current)
	print "Max "+str(data[ecoin]["Max"])
	print "Min "+str(data[ecoin]["Min"])
	
	print "********************************"

#update json config file	
jsonFile = open(configFileName, "w+")
json.dump(data,jsonFile,indent=4)
jsonFile.close()