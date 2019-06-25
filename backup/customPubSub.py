'''
/*
 * Copyright 2010-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License").
 * You may not use this file except in compliance with the License.
 * A copy of the License is located at
 *
 *  http://aws.amazon.com/apache2.0
 *
 * or in the "license" file accompanying this file. This file is distributed
 * on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
 * express or implied. See the License for the specific language governing
 * permissions and limitations under the License.
 */
 '''

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import time
import argparse
import json
import schedule

# Configure logging
logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

DEFAULT_HOST = "a1gw4ay7j34fac-ats.iot.us-east-1.amazonaws.com"
DEFAULT_ROOT = "root-CA.crt"
DEFAULT_CERT = "device-98f44a5b-edf0-4a0b-8e89-c0e33a77847d.cert.pem"
DEFAULT_PKEY = "device-98f44a5b-edf0-4a0b-8e89-c0e33a77847d.private.key" 
DEFAULT_PORT = 443
DEFAULT_CLIENTID = "basicPubSub"
DEFAULT_TOPIC = "topic/test/python"
DEFAULT_MESSAGE = "HELLO WORLD!"
DEFAULT_MODE = "subscribe"

# Custom MQTT message callback
def customCallback(client, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")

# Init AWSIoTMQTTClient
myAWSIoTMQTTClient = None
myAWSIoTMQTTClient = AWSIoTMQTTClient(DEFAULT_CLIENTID)
myAWSIoTMQTTClient.configureEndpoint(DEFAULT_HOST, DEFAULT_PORT)
myAWSIoTMQTTClient.configureCredentials(DEFAULT_ROOT, DEFAULT_PKEY, DEFAULT_CERT)
# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
# Connect and subscribe to AWS IoT
myAWSIoTMQTTClient.connect()
# send topic first 
myAWSIoTMQTTClient.subscribe(DEFAULT_TOPIC, 1, customCallback)
time.sleep(2) # waiting

def publish_job() :
    message = {}
    message['message'] = "hello publish"
    messageJson = json.dumps(message)
    myAWSIoTMQTTClient.publish(DEFAULT_TOPIC, messageJson, 1)
    print('Published topic %s: %s\n' % (DEFAULT_TOPIC, messageJson))

schedule.every(1).seconds.do(publish_job)

while True:
    schedule.run_pending()
    time.sleep(1)