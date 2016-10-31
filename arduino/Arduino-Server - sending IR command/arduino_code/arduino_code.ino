/*
 * my.c
 *
 *  Created on: Jun 13, 2016
 *      Author: Omri
 */

// Open a serial connection and flash LED when input is received
#include <IRremote.h>
/////////////////////////////
//VARS
char inByte;
int first = 1;
//the time we give the sensor to calibrate (10-60 secs according to the datasheet)
int calibrationTime = 30;

//the time when the sensor outputs a low impulse
long unsigned int lowIn;

//the amount of milliseconds the sensor has to be low 
//before we assume all motion has stopped
long unsigned int pause = 5000;

int pirPin = 7;    //the digital pin connected to the PIR sensor's output
int ledPin = 8;

int RECV_PIN = 11;
IRrecv irrecv( RECV_PIN);
decode_results results;
int count;
IRsend irsend;
/////////////////////////////

void setup() {
  // Open serial connection.
  Serial.begin(9600);
  pinMode(13, OUTPUT);
  irrecv.enableIRIn(); // Start the receiver

  pinMode(pirPin, INPUT);
  pinMode(ledPin, OUTPUT);
  digitalWrite(pirPin, LOW);

  //give the sensor some time to calibrate
  //Serial.print("calibrating sensor ");
  for (int i = 0; i < calibrationTime; i++) {
    //Serial.print(".");
    delay(1000);
  }
  //Serial.println(" done");
  //Serial.println("SENSOR ACTIVE");
  delay(50);
  Serial.write('1'); //Tell the server the Arduino is ready
}

void dump(decode_results *results) {

  count = results->rawlen;
  Serial.println(count);

  delay(100);

  for (int i = 1; i < count; i++) {

    if ((i % 2) == 1) {
      Serial.println(results->rawbuf[i] * USECPERTICK, DEC);
    } else {
      Serial.println((int) results->rawbuf[i] * USECPERTICK, DEC);
    }
    delay(50);
  }

}

void loop() {
  if (Serial.available() > 0) {      // if data present, blink
    inByte = Serial.read();
    switch (inByte) {
    case 'r': //Recieve IR-code
    {
      //turn led on and off
      digitalWrite(13, HIGH);
      delay(500);
      digitalWrite(13, LOW);
      delay(500);
      digitalWrite(13, HIGH);
      delay(500);
      digitalWrite(13, LOW);

      // Serial.flush();
      Serial.print(
          "Please place the remote in front of the Arduino and press it");
      delay(3000);

      if (!first) {
        irrecv.resume();
      }

      //wait for button press and send it over the serial
      while (1) {
        if (irrecv.decode(&results)) {
          dump(&results);
          first = 0;
          //irrecv.resume();
          // Serial.write( (uint8_t*)info, sizeof(info) );
        }
      }
      break;
    }
      //delay(1000);

      //Serial.write('c');
      //break;

    case 's': //Send IR-code
    {
      delay(100);
      int size = Serial.parseInt();
      //Serial.println("Size is: ");
      Serial.println(size);
      unsigned int data[size];
      //Serial.println(" { ");

      for (int i = 0; i < size; i++) {
        data[i] = Serial.parseInt();
        delay(50);
        Serial.println(data[i]);

      }

      for (int j = 0; j < 2; j++) {
        int khz = 38; // 38kHz carrier frequency for the NEC protocol
        irsend.sendRaw(data, sizeof(data) / sizeof(data[0]), khz); //Note the approach used to automatically calculate the size of the array.
        delay(1000);
      }
      break;
    }

    case 'm': {
      while(1){
        if (digitalRead(pirPin) == HIGH) {
          digitalWrite(ledPin, HIGH); //the led visualizes the sensors output pin state
          delay(1000);
          digitalWrite(ledPin, LOW); //the led visualizes the sensors output pin state
          Serial.println("Intruder");
          break;
        }
      }
    }
    }
  }
}


