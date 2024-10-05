import paho.mqtt.client as mqtt
from paho.mqtt.client import connack_string
import configparser
from mediola import Mediola

class Mediola_mqtt:
    _mqtt = {}
    def __init__(self):
        self._client = mqtt.Client()
        self._client.on_connect = self.on_connect
        self._client.on_disconnect = self.on_disconnect
        self._client.on_message = self.on_message

    def config(self, filep):
        config = configparser.ConfigParser()
        config.read_file(filep)
        mediola_host = config['mediola']['host']
        self._mediola = Mediola(mediola_host)

        self._mqtt['topic'] = config['mqtt']['topic']
        self._mqtt['host'] = config['mqtt']['host']
        self._mqtt['port'] = int(config['mqtt']['port'])

    def run(self):
        self._client.connect(self._mqtt['host'], self._mqtt['port'], 60)
        self._client.loop_forever()

    def on_connect(self, client, userdata, flags, rc):
        print("Connection returned result: "+connack_string(rc))
        client.subscribe(self._mqtt['topic']+'/#')
        client.message_callback_add(self._mqtt['topic']+'/IT/#', self.on_message_IT)
        client.message_callback_add(self._mqtt['topic']+'/SM/#', self.on_message_SM)
        client.message_callback_add(self._mqtt['topic']+'/WA/#', self.on_message_WA)
        client.message_callback_add(self._mqtt['topic']+'/Send2/#', self.on_message_Send2)

    def on_disconnect(self, client, userdata, rc):
        if rc != 0:
            print("Unexpected disconnection.")

    def on_message(self, client, userdata, message):
        print("Received message '" + str(message.payload) + "' on topic '"
            + message.topic + "' with QoS " + str(message.qos))

    def on_message_IT(self, client, userdata, message):
        device = message.topic.split('/')[-1]
        action = message.payload.decode()
        self._mediola.send_intertechno(device, action)

    def on_message_SM(self, client, userdata, message):
        device = message.topic.split('/')[-1]
        action = message.payload.decode()
        self._mediola.send_somfy(device, action)

    def on_message_WA(self, client, userdata, message):
        device = message.topic.split('/')[-1]
        action = message.payload.decode()
        self._mediola.send_warema(device, action)

    def on_message_Send2(self, client, userdata, message):
        code = message.payload.decode()
        self._mediola.send_send2(code)


if __name__ == '__main__':
    # Add commandline arguments
    import argparse
    parser = argparse.ArgumentParser(description='SMA Modbus MQTT Bridge')
    parser.add_argument('-c', '--config', type=argparse.FileType('r'),
            help='INI file with the configuration', required=True)
    args = parser.parse_args()

    mm = Mediola_mqtt()

    mm.config(args.config)
    args.config.close()

    mm.run()
