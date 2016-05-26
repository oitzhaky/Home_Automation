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
unsigned int low21[101] = {3100,2950,1000,850,1050,950,1000,1800,2000,900,1050,900,1050,900,1000,900,1050,850,1050,1800,2050,1800,1100,850,2000,950,1000,900,1000,900,1050,900,1050,900,1000,850,1100,850,1050,850,1100,900,1000,900,1000,900,1000,1000,950,900,1000,950,1000,950,1000,850,1100,900,950,1950,1900,950,3000,2850,1050,950,950,950,1000,1850,2000,900,1050,850,1050,900,1050,850,1050,900,1000,1850,2000,1850,1100,850,2000,900,1050,850,1050,900,1050,850,1050,900,1050,850,1050,900,};
unsigned int high21[101] = {3100,2800,1100,900,1000,850,1100,1800,1050,900,1050,850,2000,950,1000,900,1050,850,1050,1850,2000,1850,1100,800,2000,950,1000,900,1000,1000,1000,850,1050,850,1100,850,1000,950,1000,900,1000,1000,950,950,950,950,1050,850,1000,950,1000,950,1000,850,1100,850,1050,850,1100,1800,2000,900,3000,2900,1000,1000,1000,850,1050,1800,1100,850,1100,850,2000,850,1100,850,1000,950,1000,1850,2000,1900,1000,850,2050,850,1100,850,1050,850,1050,950,950,950,1000,950,1000,850,};

      irsend.sendRaw(low21, sizeof(low21) / sizeof(low21[0]), khz); //Note the approach used to automatically calculate the size of the array.
       Serial.println(" AC ON");

       delay(3000);
       
      irsend.sendRaw(high21, sizeof(high21) / sizeof(high21[0]), khz); //Note the approach used to automatically calculate the size of the array.
      Serial.println("AC low fan");   
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

 



