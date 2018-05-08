// This #include statement was automatically added by the Particle IDE.
#include <MQTT.h>

int sensorPin = A1;
int sensorPower = D5;
int sensorData = 0;
int doorStatus = -1;
int ledPin = D0;

void callback(char* topic, byte* payload, unsigned int length);
MQTT client("broker.hivemq.com", 1883, callback);
// recieve message
void callback(char* topic, byte* payload, unsigned int length) {
    char p[length + 1];
    memcpy(p, payload, length);
    p[length] = NULL;

}

void setup() {
  pinMode(sensorPin,INPUT_PULLUP);
  pinMode(sensorPower,OUTPUT);
  digitalWrite(sensorPower,HIGH);
  pinMode(ledPin,OUTPUT);
  digitalWrite(ledPin,LOW);
  
  Particle.variable("mailbox", &doorStatus, INT);
  
  Serial.begin(9600);
  delay(5000);
  Serial.print("Startup door: ");
  Serial.println(analogRead(sensorPin));
  
  
  // connect to the server
  client.connect("sparkclient");

  // publish/subscribe
  if (client.isConnected()) {
      client.publish("djmailman","hello world");
      client.subscribe("djmailman");
  }
  
}

void loop() {
    if (client.isConnected()){
        client.loop();
    }
    sensorData = analogRead(sensorPin);
    if (sensorData > 3500){
        if ( doorStatus != 1){
            doorStatus = 1;
            Serial.println("Latch Closed");
            Particle.publish("temp", "CLOSED", PRIVATE);
            client.publish("djmailman","CLOSED");
            digitalWrite(ledPin,LOW);
        }
    }
    else {
        if ( doorStatus != 0 ){
            doorStatus = 0;
            Serial.println("Latch Open");
            Particle.publish("temp", "OPEN", PRIVATE);
            client.publish("djmailman","OPEN");
            digitalWrite(ledPin,HIGH);
        }
    }
}