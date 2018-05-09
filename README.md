# mailman

This project sends a text message to notify me when the mail has arrived

## components
Particle Photon with a reed switch (available through Adafruit)
Some machine to run python program
  - need to pip install twilio and paho-mqtt
Twilio account to send an SMS message

### overview
The reed switch is installed in the mailbox. When the mailbox opens, this breaks the circuit and triggers the Photon to publish that the door is open to an MQTT topic. When the mailbox closes, the circuit is completed again and triggers the Photon to publish that the door is closed. My python program subscribes to the MQTT topic and looks for a the pattern of an OPEN followed by a CLOSED. Upon picking up this pattern, a message is sent through to Twilio server. The Twilio server sends an SMS to the list of cell phone numbers sent to it.
