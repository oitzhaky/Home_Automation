// Open a serial connection and flash LED when input is received
char inByte;
#include <IRremote.h>

int RECV_PIN = 11;
IRrecv irrecv(RECV_PIN);
decode_results results;
//unsigned int info[500];
int count;

void setup(){
  // Open serial connection.
  Serial.begin(9600);
  pinMode(13, OUTPUT);
  Serial.write('1');
  irrecv.enableIRIn(); // Start the receiver
}

void dump(decode_results *results) {
  
  count = results->rawlen;
  Serial.print(count);

  delay(500);
  
  for (int i = 1; i < count; i++) {
   
    if ((i % 2) == 1) {
    Serial.print(results->rawbuf[i]*USECPERTICK,DEC);
    }else {
    Serial.print((int)results->rawbuf[i]*USECPERTICK,DEC);
    }
    delay(500);
  }
}



void loop(){ 
  if(Serial.available() > 0){      // if data present, blink
      inByte = Serial.read();
      switch (inByte){
      case 'r':
      //turn led on and off
        digitalWrite(13, HIGH);
        delay(500);            
        digitalWrite(13, LOW);
        delay(500); 
        digitalWrite(13, HIGH);
        delay(500);            
        digitalWrite(13, LOW);

        //Serial.write('1');

        Serial.flush();
        Serial.print("Please place the remote in front of the Arduino and press it");
        delay(3000);

        //wait for button press and send it over the serial
        while(1){
          if (irrecv.decode(&results)) {
            dump(&results);
            //delay(1000);
            //irrecv.resume();
           // Serial.write( (uint8_t*)info, sizeof(info) );
           break;
           // delay(5000);
          }
        }
        delay(5000);
        
        Serial.write('c');
        break;
     
        case 's':
          break;
        }
  }
}

