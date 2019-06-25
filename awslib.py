from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time

class AwsLib :
    clientId = None
    hostName = None
    rootCert = None
    certKey = None
    privKey = None
    topic = None
    message = None
    port = None
    myAWSIoTMQTTClient = None

    def __init__(self, clientId, hostName, port, rootCert, certKey, privKey, message) :
        self.clientId = clientId
        self.hostName = hostName
        self.rootCert = rootCert
        self.certKey = certKey
        self.privKey = privKey
        self.port = port
        self.message = message

    def connect(self) :
        try :
            # Init AWSIoTMQTTClient
            self.myAWSIoTMQTTClient = AWSIoTMQTTClient(self.clientId)
            self.myAWSIoTMQTTClient.configureEndpoint(self.hostName, self.port)
            self.myAWSIoTMQTTClient.configureCredentials(self.rootCert, self.privKey, self.certKey)
            # AWSIoTMQTTClient connection configuration
            self.myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
            self.myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
            self.myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
            self.myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
            self.myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
            self.myAWSIoTMQTTClient.connect()
        except Exception as e :
            print(e)

    def subscribe(self, topic) :
        try :
            self.myAWSIoTMQTTClient.subscribe(topic, 1, self.receiveCallback)
            # save to DB here
        except Exception as e :
            print(e)

    def publish(self, topic, message) :
        try :
            self.myAWSIoTMQTTClient.publish(topic, message, 1)
        except Exception as e :
            print(e)

    # Custom MQTT message callback
    def receiveCallback(self, client, userdata, message):
        print("Received a new message: ")
        print(message.payload)
        print("from topic: ")
        print(message.topic)
        print("--------------\n\n")