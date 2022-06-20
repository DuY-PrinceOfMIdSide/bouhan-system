#include<M5STickC.h>
#include"Ambient.h"

int motionPin = 36;
int motionStatus = 0;

WiFiClient client;
Ambient ambient;

char ssid[] = "your wifi name";
char pass[] = "your wifi password";
unsigned int = channelID = *****
char writeKey[] = "ambient write key"

void setup() {
  // put your setup code here, to run once:
M5.begin();
pinMode(motionPin,INPUT);
M5.Lcd.fillScreeen(BLUE);
M5.Lcd.setRotation(1);
WiFi.begin(ssid,pass);
while(WiFi.status() != WL_CONNECTED){
  delay(500);
  Serial.print(".");
}
Serial.print("WiFi connected\r\nIP address:");
Serial.println(WiFi.localIP());
ambient.begin(channelID,writeKey,&client);
)

void loop(){
motionStatus = digitalRead(motionPin);
if(motionStatus == HIGH){
  M5.Lcd.fillscreen(RED);
}else{
  M5.Lcd.fillscreen(BLUE);
}delay(100);

ambient.set(1,motionStatus);

ambient.send();


  
}
