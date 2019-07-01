from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import time
import argparse
import json
import schedule
from awslib import AwsLib

# Configure logging
logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

# Configuration AWS MQTT
CONFIG_HOST = "a1gw4ay7j34fac-ats.iot.us-east-1.amazonaws.com"
CONFIG_ROOT = "account/root-CA.crt"
CONFIG_CERT = "account/device-98f44a5b-edf0-4a0b-8e89-c0e33a77847d.cert.pem"
CONFIG_PKEY = "account/device-98f44a5b-edf0-4a0b-8e89-c0e33a77847d.private.key" 
CONFIG_PORT = 443
CONFIG_CLIENTID = "basicPubSub"
CONFIG_TOPIC = "topic/test/python"
CONFIG_MESSAGE = "HELLO WORLD!"

# (clientId, hostName, rootCert, certKey, privKey, port, topic, message)
aws = AwsLib(CONFIG_CLIENTID, CONFIG_HOST, CONFIG_PORT, CONFIG_ROOT, CONFIG_CERT, CONFIG_PKEY)
aws.connect()

schedule.every(1).seconds.do(aws.publish, "signal/device/temperature01", "topic1")
#schedule.every(1).seconds.do(aws.publish, "signal/humidity/device2", "topic2").tag('a')
#schedule.every(1).seconds.do(aws.subscribe, "signal/humidity/device3").tag('b')
while True:
    schedule.run_pending()
    time.sleep(1)