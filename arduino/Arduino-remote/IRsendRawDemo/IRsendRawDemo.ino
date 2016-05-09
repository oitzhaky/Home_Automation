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
unsigned int deg26[74] = {8900,4450,650,1650,650,550,650,550,650,1600,650,550,650,1650,650,550,650,550,650,500,700,1600,650,550,650,1650,650,550,650,550,600,550,650,550,650,550,650,550,650,550,650,550,650,550,650,1600,700,1600,700,500,650,1650,650,500,700,500,700,500,650,1650,650,550,650,1600,700,500,650,550,650,1650,650,550,650,};
unsigned int deg25[74] = {8900,4450,700,1600,650,550,650,550,650,1600,700,500,700,1600,650,550,650,550,650,1600,700,500,700,500,700,1600,650,550,650,550,650,550,650,500,700,500,650,550,700,500,650,550,650,550,650,1650,650,1600,700,500,700,1600,650,550,650,550,650,550,600,1650,700,500,700,1600,650,550,650,550,650,1600,700,500,700,};

  // see if there's incoming serial data:
  if (Serial.available() > 0) {
    // read the oldest byte in the serial buffer:
    incomingString = Serial.read();
    if (incomingString == "26 degrees") {
       irsend.sendRaw(deg26, sizeof(deg26) / sizeof(deg26[0]), khz); //Note the approach used to automatically calculate the size of the array.
       Serial.println("changing AC to 26 degrees");
    }
    if (incomingString == "25 degrees") {
      irsend.sendRaw(deg25, sizeof(deg25) / sizeof(deg25[0]), khz); //Note the approach used to automatically calculate the size of the array.
      Serial.println("changing AC to 25 degrees");
    }
  }

}

 



