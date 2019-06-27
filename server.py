from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import time
import argparse
import json
import schedule
from awslib import AwsLib
from bottle import route, run, template, request
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
AWS_SERVER = AwsLib(CONFIG_CLIENTID, CONFIG_HOST, CONFIG_PORT, CONFIG_ROOT, CONFIG_CERT, CONFIG_PKEY, CONFIG_MESSAGE)

# Refresh AWS pub-sub connection in 60 seconds
def check_pubsub() :
	AWS_SERVER.disconnect()
	AWS_SERVER.connect()
	AWS_SERVER.publish(CONFIG_TOPIC_MONITOR, "{\"status\":\"ok\"}")
	print('reconnect...')

def run_schedule():
	while True:
		schedule.run_pending()
		time.sleep(1)

# Check pubsub every 60 seconds
schedule.every(60).seconds.do(check_pubsub)
t = Thread(target=run_schedule)
t.daemon = True
t.start()

# (clientId, hostName, rootCert, certKey, privKey, port, topic, message)
AWS_SERVER.connect()

# ===============================================================================================
# CONTROLLER BOTTLE
# ===============================================================================================
@route('/publish', method='GET')
def index():
	AWS_SERVER.publish(CONFIG_TOPIC, 'hello world')
	return 'OK'

@route('/disconnect', method='GET')
def disconnect():
	AWS_SERVER.disconnect()
	return 'OK'

@route('/connect', method='GET')
def connect():
	AWS_SERVER.connect()
	return 'OK'

run(host='localhost', port=8080)