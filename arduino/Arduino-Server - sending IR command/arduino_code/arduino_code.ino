// Open a serial connection and flash LED when input is received
char inByte;
#include <IRremote.h>

int RECV_PIN = 11;
IRrecv irrecv(RECV_PIN);
decode_results results;
//unsigned int info[500];
int count;
IRsend irsend;

void setup(){
  // Open serial connection.
  Serial.begin(9600);
  pinMode(13, OUTPUT);
  Serial.write('1');
  irrecv.enableIRIn(); // Start the receiver
}

void dump(decode_results *results) {
  
  count = results->rawlen;
  Serial.println(count);

  delay(100);
 
  for (int i = 1; i < count; i++) {
   
    if ((i % 2) == 1) {
    Serial.println(results->rawbuf[i]*USECPERTICK,DEC);
    }else {
    Serial.println((int)results->rawbuf[i]*USECPERTICK,DEC);
    }
    delay(50);
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
        Serial.print("Please place the remote in front of the Arduino and press it\n");
        delay(3000);

        //wait for button press and send it over the serial
        while(1){
          if (irrecv.decode(&results)) {
            dump(&results);
            //irrecv.resume();
           // Serial.write( (uint8_t*)info, sizeof(info) );
           break;
          }
        }
        delay(1000);
  
        
        //Serial.write('c');
        break;
     
        case 's':
            Serial.write('1');
            delay(100);
            int size = Serial.parseInt();
            //Serial.println("Size is: ");
            //Serial.println(size);
            unsigned int data[size];
           //Serial.println(" { ");
           
            for(int i =0; i < size; i++){
              data[i] = Serial.parseInt();
              delay(50);
              Serial.println(data[i]);
            
            }
            //Serial.println(" } ");

            while (1){
               int khz = 38; // 38kHz carrier frequency for the NEC protocol
               irsend.sendRaw(data, sizeof(data) / sizeof(data[0]), khz); //Note the approach used to automatically calculate the size of the array.
               delay(1000);
            }
              break;
       
         }
  }
}

