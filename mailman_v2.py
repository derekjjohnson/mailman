import mailman_param
import paho.mqtt.client as mqtt
from twilio.rest import Client
import datetime
import time
now = datetime.datetime.now()

# Your list of numbers to send an SMS notification
call_list = ['+14436918085']




def send_sms(client):
    counter = 0
    for cell_number in call_list:
        counter = counter + 1
        my_text = 'You\'ve got mail #' + str(counter)
        message = client._sms_client.messages.create(
            to=cell_number,
            from_=client._mailman.twilio_number,
            body= my_text)
        print(message.sid)
    to_return = 'TEXT SENT TO ' + str(counter) + ' NUMBER(S)'
    return to_return


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print('Connected with result code ' + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(client._mailman.mqtt_queue)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    mailStatus = str(msg.payload)[2:-1]
    if mailStatus != client._last_mailStatus:
        print(mailStatus, ' new value')
        log(mailStatus + ' new value')
        #client._last_mailStatus = mailStatus
        if mailStatus.upper() == 'CLOSED' and client._last_mailStatus == 'OPEN':
            cindy = send_sms(client)
            log(cindy)
            # client.publish(client._mailman.mqtt_queue+"/lastmail",)
        client._last_mailStatus = mailStatus


def log(msg):
    log_file=open('mailman_log.txt', 'a')
    log_file.write(str(datetime.datetime.now()) + ', ' + msg + '\n')
    log_file.close()
    pass


def menu():
    to_return = ''

    return to_return


def main():
    log('STARTUP')
    bob = mailman_param.Mailman()
    my_url = bob.url_string
    # print(my_url)
    # print(bob.twilio_acct_sid)
    # print(bob.twilio_auth_token)
    sms_client = Client(bob.twilio_acct_sid, bob.twilio_auth_token)

    mqtt_client = mqtt.Client()
    mqtt_client._mailman = bob
    mqtt_client._sms_client = sms_client
    mqtt_client._last_mailStatus = ''
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    mqtt_client.connect(bob.mqtt_url, 1883, 60)

    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a
    # manual interface.
    mqtt_client.loop_start()
    control_string = input('Enter Q to quit: ').upper()
    if control_string == 'Q':
        log('quit command sent, closing program')
        mqtt_client.loop_stop()
    return None


if __name__ == '__main__':
    main()