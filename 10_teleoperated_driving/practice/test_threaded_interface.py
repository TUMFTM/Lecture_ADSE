import paho.mqtt.client as mqtt

this_program_should_be_terminated = False

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("testtopic/single")

def on_message(client, userdata, msg):
    payload_text = msg.payload.decode("utf-8")
    print(msg.topic+" "+str(payload_text))
    finish_statement = "finish"
    if payload_text == finish_statement:
        global this_program_should_be_terminated
        this_program_should_be_terminated = True

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("broker.emqx.io", port=1883, keepalive=10)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.

client.loop_start()

import time
while True:
    time.sleep(5)
    print("Here, the main work is done")
    if this_program_should_be_terminated:
        print("program terminated")
        break