# https://stackoverflow.com/questions/12965203/how-to-get-json-from-webpage-into-python-script
import paho.mqtt.client as mqtt

import aiy.audio
#import aiy.cloudspeech
#import aiy.voicehat

import requests
import json
import pprint
import time
#my_url = 'https://api.thingspeak.com/channels/455616/feeds.json?api_key=I8OQ2ZN5KG1BAX2H&results=2'

# This URL lets me get a Particle.variable value
my_url = "https://api.particle.io/v1/devices/39002b000351353530373132/mailbox?access_token=926a1bf46e765af31593d70e6e218bbfe6428962"


from twilio.rest import Client

# Your Account SID from twilio.com/console
# account_sid = "AC300f12fd88f375037dbef7f3a6ff4627"
account_sid = "AC228a1e33755c942a720518f79bf6e9d2"
# Your Auth Token from twilio.com/console
# auth_token = "ca2ff797bb1a1d4be3cc6685cd36a53f"
auth_token  = "b2aa3d60a3f78ece350ea14fae26a10f"

twilio_number = "+16672136285"

client = Client(account_sid, auth_token)

call_list = ["+14436918085"]

def send_sms():
    counter = 1
    for cell_number in call_list:
        my_text = "You've got mail #" + str(counter)
        message = client.messages.create(
            to=cell_number,
            from_=twilio_number,
            body= my_text)
        counter = counter + 1
        print(message.sid)
    return "TEXT SENT"


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("djmailman/#")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    print(str(msg.payload)[2:-1])
    mailStatus = str(msg.payload)
    if mailStatus != client._last_mailStatus:
        print(mailStatus, " new value")
        client._last_mailStatus = mailStatus
        #bob = send.sms()
        #print(bob)
        to_repeat = "hi derek, the mailbox is "+str(msg.payload)[2:-1]
        print(to_repeat)
        aiy.audio.say(to_repeat)



client = mqtt.Client()
client._last_mailStatus = ''
client.on_connect = on_connect
client.on_message = on_message




client.connect("broker.hivemq.com", 1883, 60)


# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()