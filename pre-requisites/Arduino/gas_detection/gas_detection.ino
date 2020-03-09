#include <SoftwareSerial.h>
#include "SIM900.h"
#include "sms.h"
#include "MQ2.h"
#include "LiquidCrystal_I2C.h"

const int Analog_Input = A0, pinBuzzer = 7, ledReady = 8;
int lpg, co, smoke;
MQ2 mq2(Analog_Input);

SMSGSM sms;
LiquidCrystal_I2C LCD_DRVR(0x27, 16, 2); // Declare LCD Screen
SoftwareSerial wifiSerial(2, 3);         // RX, TX for ESP8266

bool DEBUG = true;     //show more logs
int responseTime = 10; //communication timeout

int device_id = 69;
String PostMessage = "";

int numdata;
boolean started = false;
char smsbuffer[160];
char n[20];

void setup()
{
  Serial.begin(115200);
  LCD_DRVR.begin();

  // Setup Pins
  pinMode(ledReady, OUTPUT);
  while (!Serial)
    ;

  LCD_DRVR.setCursor(0, 0);
  LCD_DRVR.print(F(" Gas Detection  "));
  LCD_DRVR.setCursor(0, 1);
  LCD_DRVR.print(F("  For CpEHacks  "));

  LCD_DRVR.noBacklight();
  LCD_DRVR.clear();
  delay(500);
  LCD_DRVR.backlight();

  //Start Wifi Module
  // Open serial communications and wait for port to open esp8266:
  wifiSerial.begin(115200);

  sendToWifi("AT+RST", responseTime, DEBUG);
  //Serial.println("AT+RST");

  sendToWifi("AT+CWJAP=\"RNHLD\",\"MotivationsPLS\"", responseTime, DEBUG);
  //Serial.println("AT+CWJAP=\"cabral\",\"17151613\"");
  delay(4000);

  sendToWifi("AT+CWJAP?", responseTime, DEBUG);
  //Serial.println("AT+CWJAP?");
  delay(4000);

  sendToWifi("AT+CIFSR", responseTime, DEBUG);
  //Serial.println("AT+CIFSR");
  delay(1000);

  sendToWifi("AT+CIPMUX=1", responseTime, DEBUG);
  //Serial.println("AT+CIPMUX=1");
  delay(4000);

  sendToUno("Wifi connection is running!", responseTime, DEBUG);
  //End Wifi Module

  //Start GSM Module
  if (gsm.begin(2400))
  {
    Serial.println("\nstatus=READY");
    started = true;
  }
  else
    Serial.println("\nstatus=IDLE");
  //End GSM Module

  //Start GSM Module
  if (gsm.begin(2400))
  {
    Serial.println("\nstatus=READY");
    started = true;
  }
  else
    Serial.println("\nstatus=IDLE");
  //End GSM Module

  digitalWrite(ledReady, HIGH);
}

//Text function
void text()
{
  if (started)
  {
    if (sms.SendSMS("09953148842", "Alert! Gas particle/s has been detected. Please check the web application for details."))
      Serial.println("\nSMS sent OK");
  }
}
//end text function

//post
void post(String gases, int smokePPM)
{
  String gas = gases;
  int smoke = smokePPM;

  PostMessage += "{\"device_id\":";
  PostMessage += "\"";
  PostMessage += device_id;
  PostMessage += "\"";
  PostMessage += ",\"gas\":";
  PostMessage += "\"";
  PostMessage += gas;
  PostMessage += "\"";
  PostMessage += ",\"reading\":";
  PostMessage += "\"";
  PostMessage += smoke;
  PostMessage += "\"";
  PostMessage += "}";

  unsigned int l = PostMessage.length();

  String JSON = "";

  JSON += "POST /post/notif HTTP/1.1\n";
  JSON += "Host:192.168.43.90:5000\n";

  JSON += "Content-Length:";
  JSON += l;
  JSON += "\n";

  JSON += "Content-Type:application/json\n\n";

  JSON += PostMessage;

  unsigned int i = JSON.length();

  sendToUno(JSON, responseTime, DEBUG);
  String len = "";
  len += i;
  sendToUno(len, responseTime, DEBUG);

  String startMsg = "";
  startMsg += "AT+CIPSTART=0,";
  startMsg += "\"TCP\",";
  startMsg += "\"192.168.43.90\",";
  startMsg += "5000";
  sendToWifi(startMsg, responseTime, DEBUG);
  startMsg = "";
  delay(4000);

  String cipMsg = "";
  cipMsg += "AT+CIPSEND=0,";
  cipMsg += i;
  sendToWifi(cipMsg, responseTime, DEBUG);
  cipMsg = "";
  delay(4000);

  sendToWifi(JSON, responseTime, DEBUG);

  String closeMsg = "";
  closeMsg += "AT+CIPCLOSE=0,";
  sendToWifi(closeMsg, responseTime, DEBUG);

  sendToUno("JSON Sent", responseTime, DEBUG);
  JSON = "";
  PostMessage = "";
}
//end post

void gas()
{
  float *values = mq2.read(false); //set it false if you don't want to print the values in the Serial
  //lpg = values[0];
  lpg = mq2.readLPG();
  //co = values[1];
  co = mq2.readCO();
  //smoke = values[2];
  smoke = mq2.readSmoke();

  if (lpg == 0 && co == 0)
  {
    //put lcd display of normal
    post("Normal", smoke);
    sendToUno("Normal Reading", responseTime, DEBUG);
    delay(30000);
  }
  else if (lpg > 0 && co == 0)
  {
    //put lcd alert
    post("LPG", smoke);
    text();
  }
  else if (co > 0 && lpg == 0)
  {
    //put lcd alert
    post("CO", smoke);
    text();
  }
  else if (co > 0 && lpg > 0)
  {
    //put lcd alert
    post("CO and LPG", smoke);
    text();
  }
}

void loop()
{
  // LCD_DRVR.setCursor(0, 0);

  // String gas = "";

  // lpg = mq2.readLPG();
  // co = mq2.readCO();
  // smoke = mq2.readSmoke();

  if (lpg == 0 && co == 0)
  {
    //put lcd display of normal
    // digitalWrite(pinBuzzer, LOW);
    // LCD_DRVR.print(F("Status |> Normal"));
    post("Normal", smoke);
  }
  else if (lpg > 0 && co == 0)
  {
    //put lcd alert
    //post("LPG", smoke);
    //text();
    // digitalWrite(pinBuzzer, HIGH);
    // LCD_DRVR.print(F("High LPG Dtcted!"));
    post("LPG", smoke);
  }
  else if (co > 0 && lpg == 0)
  {
    //put lcd alert
    //post("CO", smoke);
    //text();
    // digitalWrite(pinBuzzer, HIGH);
    // LCD_DRVR.print(F("High CO Dtcted! "));
    post("CO", smoke);
  }
  else if (co > 0 && lpg > 0)
  {
    //put lcd alert
    //post("CO and LPG", smoke);
    //text();
    // digitalWrite(pinBuzzer, HIGH);
    // LCD_DRVR.print(F("High CO and LPG!"));
    post("CO and LPG", smoke);
  }
}

/*
* Name: sendData
* Description: Function used to send string to tcp client using cipsend
* Params:
* Returns: void
*/
void sendData(String str)
{
  String len = "";
  len += str.length();
  sendToWifi("AT+CIPSEND=0," + len, responseTime, DEBUG);
  delay(100);
  sendToWifi(str, responseTime, DEBUG);
  delay(100);
  sendToWifi("AT+CIPCLOSE=5", responseTime, DEBUG);
}

/*
* Name: find
* Description: Function used to match two string
* Params:
* Returns: true if match else false
*/
boolean find(String string, String value)
{
  return string.indexOf(value) >= 0;
}

/*
* Name: readSerialMessage
* Description: Function used to read data from Arduino Serial.
* Params:
* Returns: The response from the Arduino (if there is a reponse)
*/
String readSerialMessage()
{
  char value[100];
  int index_count = 0;
  while (Serial.available() > 0)
  {
    value[index_count] = Serial.read();
    index_count++;
    value[index_count] = '\0'; // Null terminate the string
  }
  String str(value);
  str.trim();
  return str;
}

/*
* Name: readWifiSerialMessage
* Description: Function used to read data from ESP8266 Serial.
* Params:
* Returns: The response from the esp8266 (if there is a reponse)
*/
String readWifiSerialMessage()
{
  char value[100];
  int index_count = 0;
  while (wifiSerial.available() > 0)
  {
    value[index_count] = wifiSerial.read();
    index_count++;
    value[index_count] = '\0'; // Null terminate the string
  }
  String str(value);
  str.trim();
  return str;
}

/*
* Name: sendToWifi
* Description: Function used to send data to ESP8266.
* Params: command - the data/command to send; timeout - the time to wait for a response; debug - print to Serial window?(true = yes, false = no)
* Returns: The response from the esp8266 (if there is a reponse)
*/
String sendToWifi(String command, const int timeout, boolean debug)
{
  String response = "";
  wifiSerial.println(command); // send the read character to the esp8266
  long int time = millis();
  while ((time + timeout) > millis())
  {
    while (wifiSerial.available())
    {
      // The esp has data so display its output to the serial window
      char c = wifiSerial.read(); // read the next character.
      response += c;
    }
  }
  if (debug)
  {
    Serial.println(response);
  }
  return response;
}

/*
* Name: sendToUno
* Description: Function used to send data to Arduino.
* Params: command - the data/command to send; timeout - the time to wait for a response; debug - print to Serial window?(true = yes, false = no)
* Returns: The response from the esp8266 (if there is a reponse)
*/
String sendToUno(String command, const int timeout, boolean debug)
{
  String response = "";
  Serial.println(command); // send the read character to the esp8266
  long int time = millis();
  while ((time + timeout) > millis())
  {
    while (Serial.available())
    {
      // The esp has data so display its output to the serial window
      char c = Serial.read(); // read the next character.
      response += c;
    }
  }
  if (debug)
  {
    Serial.println(response);
  }
  return response;
}
