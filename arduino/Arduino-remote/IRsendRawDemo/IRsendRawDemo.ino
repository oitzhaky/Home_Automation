/*
 * IRremote: IRsendRawDemo - demonstrates sending IR codes with sendRaw
 * An IR LED must be connected to Arduino PWM pin 3.
 * Version 0.1 July, 2009
 * Copyright 2009 Ken Shirriff
 * http://arcfn.com
 *
 * IRsendRawDemo - added by AnalysIR (via www.AnalysIR.com), 24 August 2015
 *
 * This example shows how to send a RAW signal using the IRremote library.
 * The example signal is actually a 32 bit NEC signal.
 * Remote Control button: LGTV Power On/Off. 
 * Hex Value: 0x20DF10EF, 32 bits
 * 
 * It is more efficient to use the sendNEC function to send NEC signals. 
 * Use of sendRaw here, serves only as an example of using the function.
 * 
 */


#include <IRremote.h>

IRsend irsend;
String incomingString;

void setup()
{

}

void loop() {
  
  int khz = 38; // 38kHz carrier frequency for the NEC protocol
unsigned int raw[100] = { 3650,1700,450,400,450,1300,450,400,450,400,450,400,450,400,500,400,450,400,450,400,450,400,450,400,450,400,500,400,450,1250,400,450,500,400,400,450,400,450,400,450,450,400,400,500,350,500,450,400,400,1300,400,500,400,450,400,450,400,450,400,450,400,450,400,500,400,450,400,1300,400,500,400,450,400,1300,400,500,400,450,400,1300,400,500,400,1300,400,450,400,500,400,1300,400,450,400,500,400,1300,400,1350,400, };

      irsend.sendRaw(raw, sizeof(raw) / sizeof(raw[0]), khz); //Note the approach used to automatically calculate the size of the array.
       Serial.println(" AC ON");

       delay(3000);

 /* 
  // see if there's incoming serial data:
  if (Serial.available() > 0) {
    // read the oldest byte in the serial buffer:
    incomingString = Serial.read();
    if (incomingString == "ON") {
    
    }
    if (incomingString == "LOW") {
  
    }
  }
*/
}

 



