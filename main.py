import paho.mqtt.client as mqtt
import json
import time
from gpiozero import Button, LED

# Action
isInit = True
button = Button(2)
inputMotor1 = LED(23)
inputMotor2 = LED(24)
stepTime = 0.95

def stopProgress():
    global isInit
    inputMotor1.off()
    inputMotor2.off()
    isInit = True

def startProgress():
    global isInit
    if isInit:
        inputMotor1.on()
        inputMotor2.off()
        time.sleep(stepTime)
        stopProgress()
        time.sleep(0.5)
        inputMotor1.off()
        inputMotor2.on()
        time.sleep(stepTime + 0.3)
        stopProgress()


# Mqtt
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
        startProgress()

def onConnect(client, userdata, flags, reason_code, properties):
    print("Connected")
    client.subscribe("connect")
    client.subscribe("run")
    mqttClient.publish("connect", json.dumps(connectData))

def onDisconnect():
    print("disconnect")

mqttClient.on_connect = onConnect
mqttClient.on_disconnect = onDisconnect
mqttClient.on_message = onMessage
mqttClient.connect(host, port)

button.when_pressed = stopProgress

mqttClient.loop_forever()
