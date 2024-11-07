import paho.mqtt.client as mqtt
import json

host = "mqtt.eclipseprojects.io"
port = 1883
clientId = "device_id_sell_sim_1"

connectData = {
  "deviceId": clientId,
}

mqttClient = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=clientId)


def onMessage(client, userdata, msg):
    if msg.topic == "run":
        print("Run")

def onConnect(client, userdata, flags, reason_code, properties):
    client.subscribe("connect")
    client.subscribe("run")
    mqttClient.publish("connect", json.dumps(connectData))

def onDisconnect():
    print("disconnect")

mqttClient.on_connect = onConnect
mqttClient.on_disconnect = onConnect
mqttClient.on_message = onMessage
mqttClient.connect(host, port)

mqttClient.loop_forever()
