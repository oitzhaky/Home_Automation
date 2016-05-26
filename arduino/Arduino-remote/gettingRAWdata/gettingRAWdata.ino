// If one keypress results in multiple codes being output, then
// change in IRremoteInt.h:
// #define _GAP 50000

#include <IRremote.h>

int RECV_PIN = 11;
IRrecv irrecv(RECV_PIN);
decode_results results;

void setup()
{
  Serial.begin(9600);
  irrecv.enableIRIn(); // Start the receiver
}

int c = 1;

void dump(decode_results *results) {
  int count = results->rawlen;
  Serial.println(c);
  c++;
  Serial.println("For IR Scope: ");
  for (int i = 1; i < count; i++) {
   
	if ((i % 2) == 1) {
  	Serial.print("+");
  	Serial.print(results->rawbuf[i]*USECPERTICK, DEC);
	}
	else {
  	Serial.print(-(int)results->rawbuf[i]*USECPERTICK, DEC);
	}
	Serial.print(" ");
  }
  Serial.println("");
  Serial.println("For Arduino sketch: ");
  Serial.print("unsigned int raw[");
  Serial.print(count, DEC);
  Serial.print("] = {");
  for (int i = 1; i < count; i++) {
   
	if ((i % 2) == 1) {
  	Serial.print(results->rawbuf[i]*USECPERTICK, DEC);
	}
	else {
  	Serial.print((int)results->rawbuf[i]*USECPERTICK, DEC);
	}
	Serial.print(",");
  }
  Serial.print("};");
  Serial.println("");
  Serial.print("irsend.sendRaw(raw,");
  Serial.print(count, DEC);
  Serial.print(",38);");
  Serial.println("");
  Serial.println("");
}

void loop() {
  if (irrecv.decode(&results)) {
	dump(&results);
	irrecv.resume(); // Receive the next value
  }
}

