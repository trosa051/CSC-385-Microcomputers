//https://www.instructables.com/Arduino-2-Servos-Thumbstick-joystick/

const int joyH = 3;        // L/R Parallax Thumbstick
const int joyV = 4;        // U/D Parallax Thumbstick
const int deadZone = 25;

void setup() {

  // Inizialize Serial
  Serial.begin(9600);
  Serial.println("X:,Y:");
}


void loop(){
   int hori = analogRead(joyH)-493;
   int vert = analogRead(joyV)-482;

  if ((-deadZone < analogRead(joyH)-493) && (analogRead(joyH)-493) < deadZone){
    hori = 0;
    }
  else{
    hori = analogRead(joyH)-493;
    }

  if ((analogRead(joyV)-493) > 10){
    vert = 1.85 * (analogRead(joyV)-482);
    }
  else if ((-deadZone <= analogRead(joyV)-482) && (deadZone >= analogRead(joyV)-482)){
    vert = 0;
    }
  else if ((analogRead(joyV)-482) < 10){
    vert = (analogRead(joyV)-482)/1.35;
   }

   Serial.print(hori/2.5);
   Serial.print(",");
   Serial.println(vert/2.5);
   delay(1);        

    //240x135 Color TFT Breakout LCD Display Testing next
}
