import vehicleParams
import paho.mqtt.subscribe as subscribe
import pickle

while True:
    msg = subscribe.simple("testtopic/single", hostname="broker.emqx.io")
    unserialized_q7 = pickle.loads(msg.payload)
    print("vehicle length %s and width %s" % \
          (unserialized_q7.length, unserialized_q7.width))
