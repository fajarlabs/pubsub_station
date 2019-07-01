from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import time
import argparse
import json
from json import dumps
import schedule
from awslib import AwsLib
from bottle import route, run, template, request, response
import schedule
from threading import Thread
from postgredb import myQuery

# ===============================================================================================
# AWS MQTT CONFIGURATION AND INITIALIZE
# ===============================================================================================

CONFIG_HOST = "a1gw4ay7j34fac-ats.iot.us-east-1.amazonaws.com"
CONFIG_ROOT = "account/root-CA.crt"
CONFIG_CERT = "account/device-98f44a5b-edf0-4a0b-8e89-c0e33a77847d.cert.pem"
CONFIG_PKEY = "account/device-98f44a5b-edf0-4a0b-8e89-c0e33a77847d.private.key" 
CONFIG_PORT = 443
CONFIG_CLIENTID = "SecureIOTPubSub"

# Check signal healt
CONFIG_TOPIC_MONITOR = "signal/healt/server"
CONFIG_TOPIC_DATA = "signal/device/data"
CONFIG_CHECK_RECONNECT = 1 # in seconds
CONFIG_CHECK_SUBSCRIBE = 1 # in seconds
# (clientId, hostName, rootCert, certKey, privKey, port, topic, message)	
AWS_SERVER = AwsLib(CONFIG_CLIENTID, CONFIG_HOST, CONFIG_PORT, CONFIG_ROOT, CONFIG_CERT, CONFIG_PKEY)

# Refresh AWS pub-sub connection in 60 seconds
def connection_check() :
	if (AWS_SERVER.getInfoStatus() == False) :
		AWS_SERVER.disconnect()
		print('MQTT Reconnecting...')
		AWS_SERVER.connect()
		AWS_SERVER.publish(CONFIG_TOPIC_MONITOR, "{\"message\":\"ok\"}")
		print('MQTT Connected...')

def _callback(client, userdata, message):
	data = ''
	topic = ''
	try :
		b = message.payload
		json_data = json.loads(b.decode('utf-8'))
		print(b.decode('utf-8')) # debug uncoment to show data
		data = json_data["message"]
	except Exception as e_payload :
		print(e_payload)

	try :
		topic = message.topic
	except Exception as e_topic :
		print(e_topic)

	myQuery("\
		INSERT INTO \"MQTT_DATA\" (\"MQTT_DEVICE_TOPIC\",\"MQTT_DEVICE_DATA\") \
		VALUES ('"+topic+"','"+data+"')")


def subscribe_check() :
	if AWS_SERVER.getInfoStatus() :
		AWS_SERVER.subscribe(CONFIG_TOPIC_MONITOR, _callback)
		devices = myQuery("SELECT \"MQTT_DEVICE_TOPIC\" FROM \"MQTT_DEVICE\" WHERE \"IS_SUBSCRIBE\" = 'Y' ","FETCHALL")
		if (len(devices) > 0) :
			for t in devices :
				AWS_SERVER.subscribe(t[0], _callback)
		else :
			print('No data devices found!')
	else :
		print('Subscribing is fail, because not connected to aws.')

def run_schedule():
	while True:
		schedule.run_pending()
		time.sleep(1)

# Check pubsub every 60 seconds
schedule.every(CONFIG_CHECK_RECONNECT).seconds.do(connection_check)
schedule.every(CONFIG_CHECK_SUBSCRIBE).seconds.do(subscribe_check)
t = Thread(target=run_schedule)
t.daemon = True
t.start()

# ===============================================================================================
# CONTROLLER BOTTLE
# ===============================================================================================
@route('/', method='GET')
def index():
	response.content_type = 'application/json'
	rv = { "status":"ok"}
	return dumps(rv)

@route('/publish', method='POST')
def publish():
	topic = request.forms.get('topic')
	message = request.forms.get('message')
	rv = None
	if (AWS_SERVER.getInfoStatus()) :
		transmit_json =  '{ "message":"'+message+'" }'
		AWS_SERVER.publish(topic, transmit_json)
		rv = { "status":"ok", "description":"Publish OK" }
	else :
		rv = { "status":"failed", "description":"MQTT reconnect to server" }

	response.content_type = 'application/json'
	return dumps(rv)

@route('/disconnect', method='GET')
def disconnect():
	rv = None
	if (AWS_SERVER.getInfoStatus()) :
		AWS_SERVER.disconnect()
		rv = { "status":"ok", "description":"Disconnect MQTT is OK" }
	else :
		rv = { "status":"failed", "description":"MQTT reconnect to server" }

	response.content_type = 'application/json'
	return dumps(rv)

@route('/connect', method='GET')
def connect():
	rv = None
	if AWS_SERVER.getInfoStatus() == False :
		AWS_SERVER.connect()
		rv = { "status":"ok", "description":"Connect MQTT is OK" }
	else :
		rv = { "status":"failed", "description":"MQTT reconnect to server" }

	response.content_type = 'application/json'
	return dumps(rv)

run(host='localhost', port=8080)