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

# ===============================================================================================
# AWS MQTT CONFIGURATION AND INITIALIZE
# ===============================================================================================

CONFIG_HOST = "a1gw4ay7j34fac-ats.iot.us-east-1.amazonaws.com"
CONFIG_ROOT = "account/root-CA.crt"
CONFIG_CERT = "account/device-98f44a5b-edf0-4a0b-8e89-c0e33a77847d.cert.pem"
CONFIG_PKEY = "account/device-98f44a5b-edf0-4a0b-8e89-c0e33a77847d.private.key" 
CONFIG_PORT = 443
CONFIG_CLIENTID = "basicPubSub"
CONFIG_TOPIC = "topic/test/python"
CONFIG_MESSAGE = "HELLO WORLD!"

# Check signal healt
CONFIG_TOPIC_MONITOR = "signal/healt/server"
CONFIG_RECONNECT_INTERVAL = 60 # seconds
AWS_SERVER = AwsLib(CONFIG_CLIENTID, CONFIG_HOST, CONFIG_PORT, CONFIG_ROOT, CONFIG_CERT, CONFIG_PKEY, CONFIG_MESSAGE)

# Flag check if MQTT is connected
is_connect = False

# Refresh AWS pub-sub connection in 60 seconds
def check_pubsub() :
	global is_connect
	AWS_SERVER.disconnect()
	# Set is connect to False for disconnect
	is_connect = False
	# Connecting again..
	AWS_SERVER.connect()
	AWS_SERVER.publish(CONFIG_TOPIC_MONITOR, "{\"status\":\"ok\"}")
	# Set info is connected
	is_connect = True
	print('MQTT Connected...')

def run_schedule():
	while True:
		schedule.run_pending()
		time.sleep(1)

# Check pubsub every 60 seconds
schedule.every(CONFIG_RECONNECT_INTERVAL).seconds.do(check_pubsub)
t = Thread(target=run_schedule)
t.daemon = True
t.start()

# (clientId, hostName, rootCert, certKey, privKey, port, topic, message)
AWS_SERVER.connect()
is_connect = True

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
	global is_connect
	topic = request.forms.get('topic')
	message = request.forms.get('message')
	rv = None
	if (is_connect) :
		AWS_SERVER.publish(topic, message)
		rv = { "status":"ok", "description":"Publish OK" }
	else :
		rv = { "status":"failed", "description":"MQTT reconnect to server" }

	response.content_type = 'application/json'
	return dumps(rv)

@route('/disconnect', method='GET')
def disconnect():
	global is_connect
	rv = None
	if (is_connect) :
		AWS_SERVER.disconnect()
		rv = { "status":"ok", "description":"Disconnect MQTT is OK" }
	else :
		rv = { "status":"failed", "description":"MQTT reconnect to server" }

	response.content_type = 'application/json'
	return dumps(rv)

@route('/connect', method='GET')
def connect():
	global is_connect
	rv = None
	if (is_connect) :
		AWS_SERVER.connect()
		rv = { "status":"ok", "description":"Connect MQTT is OK" }
	else :
		rv = { "status":"failed", "description":"MQTT reconnect to server" }

	response.content_type = 'application/json'
	return dumps(rv)

run(host='localhost', port=8080)