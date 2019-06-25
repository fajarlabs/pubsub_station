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

TEST_HOST = "a1gw4ay7j34fac-ats.iot.us-east-1.amazonaws.com"
TEST_ROOT = "account/root-CA.crt"
TEST_CERT = "account/device-98f44a5b-edf0-4a0b-8e89-c0e33a77847d.cert.pem"
TEST_PKEY = "account/device-98f44a5b-edf0-4a0b-8e89-c0e33a77847d.private.key" 
TEST_PORT = 443
TEST_CLIENTID = "basicPubSub"
TEST_TOPIC = "topic/test/python"
TEST_MESSAGE = "HELLO WORLD!"
TEST_MODE = "subscribe"

# TEST_HOST2 = "a1gw4ay7j34fac-ats.iot.us-east-1.amazonaws.com"
# TEST_ROOT2 = "device-2/root-CA.crt"
# TEST_CERT2 = "device-2/device-6e5c4b13-357f-4a56-abb9-a22a23f2e505.cert.pem"
# TEST_PKEY2 = "device-2/device-6e5c4b13-357f-4a56-abb9-a22a23f2e505.private.key" 
# TEST_PORT2 = 443
# TEST_CLIENTID2 = "basicPubSub"
# TEST_TOPIC2 = "topic2/test/python"
# TEST_MESSAGE2 = "HELLO WORLD2!"
# TEST_MODE2 = "subscribe"

# (clientId, hostName, rootCert, certKey, privKey, port, topic, message)
aws = AwsLib(TEST_CLIENTID, TEST_HOST, TEST_PORT, TEST_ROOT, TEST_CERT, TEST_PKEY, TEST_MESSAGE)
aws.connect()

schedule.every(1).seconds.do(aws.publish, "topic1/test/python", "topic1")
schedule.every(1).seconds.do(aws.publish, "topic2/test/python", "topic2")
schedule.every(1).seconds.do(aws.subscribe, "topic2/test/python")

while True:
    schedule.run_pending()
    time.sleep(1)