#include <Adafruit_GFX.h>    // Core graphics library
#include <Adafruit_ST7789.h> // Hardware-specific library for ST7789
#include <SPI.h>

#if defined(ESP8266)
  #define TFT_CS         7
  #define TFT_RST        16                                            
  #define TFT_DC         5

#else
  // For the breakout board, you can use any 2 or 3 pins.
  // These pins will also work for the 1.8" TFT shield.
  #define TFT_CS        10
  #define TFT_RST        9 // Or set to -1 and connect to Arduino RESET pin
  #define TFT_DC         8
#endif

Adafruit_ST7789 tft = Adafruit_ST7789(TFT_CS, TFT_DC, TFT_RST);

const int joyH = 3;        // L/R Parallax Thumbstick
const int joyV = 4;        // U/D Parallax Thumbstick
const int deadZone = 23;
int hori = 0;
int vert = 0;
int16_t x1, y1;
uint16_t w, h;
int potPin = A2;
int switch_pin1 = 5;
int switch_pin2 = 6;
int sliderPin = A5;
int diamondButton = A1;
int squareButton = A0;
const char* terminator = 126;
String incomingByte = "null";

//240x135
void setup(void) {
  Serial.begin(9600);

  Serial.println("X:,Y:");
  pinMode(switch_pin1, INPUT);
  pinMode(switch_pin2, INPUT);
  
  tft.init(135, 240);
  tft.setSPISpeed(60000000);
  uint16_t time = millis();
  tft.fillScreen(ST77XX_BLACK);
  time = millis() - time;
  delay(500);
  tft.fillScreen(ST77XX_BLACK);
  testdrawtext((char *)"Initializing...",  ST77XX_WHITE);
  delay(1000);
  tft.fillScreen(ST77XX_BLACK);
}

void loop() {

  hori = analogRead(joyH)-493;
  vert = analogRead(joyV)-482;

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
   Serial.print("JOY ");
   Serial.print(hori/2.5);
   Serial.print(",");
   Serial.println(vert/2.5);
  Serial.print("~");
  incomingByte = Serial.readStringUntil(terminator);
  draw();
  delay(1);
}


void drawCenteredText(char *text, int x, int y,uint16_t color) {
  tft.setCursor(0, 0);
  tft.setTextColor(color);
  tft.setTextWrap(true);
  tft.getTextBounds(String(*text), x, y, &x1, &y1, &w, &h);
  tft.setCursor(x - w / 2, y);
  tft.print(text);
}


void testdrawtext(char *text, uint16_t color) {
  tft.setCursor(0, 0);
  tft.setTextColor(color);
  tft.setTextWrap(true);
  tft.print(text);
}


void draw() {
  tft.setTextWrap(false);
  tft.setCursor(0, 0);
  delay(1);
  tft.setTextColor(ST77XX_WHITE);
  tft.setTextSize(0);
    tft.setCursor((tft.width()/4)-1, 0);
  tft.println("Hello World!");
  //tft.setCursor(0, 0);
  tft.setTextSize(1);
  //tft.setTextColor(ST77XX_WHITE);
  //tft.println("Sketch has been");
  //tft.println("running for: ");
  tft.setTextColor(ST77XX_WHITE,ST77XX_BLACK);
  tft.setCursor(7, 8);
  tft.print("Seconds Elapsed: ");
  tft.setTextColor(ST77XX_MAGENTA,ST77XX_BLACK);
  tft.println(millis() / 1000);
  tft.setCursor(11, 16);
  tft.setTextColor(ST77XX_WHITE,ST77XX_BLACK);
  tft.print("Packages Left: ");
  tft.setTextColor(ST77XX_MAGENTA,ST77XX_BLACK);

  //size_t found = str.find(str2);
    if (incomingByte != "null"){
    tft.println(incomingByte);
  }
  else{
    tft.println(5);
  }
    

  
  tft.setCursor(0, 35);
  tft.setTextColor(ST77XX_WHITE,ST77XX_BLACK);
  tft.println("Statuses: ");
  tft.setTextColor(ST77XX_WHITE,ST77XX_BLACK);
  tft.setCursor(0, 50);
  tft.print("Sketch Theme: ");
  tft.setTextColor(ST77XX_MAGENTA,ST77XX_BLACK);
  tft.println("Original");
  tft.setTextColor(ST77XX_WHITE,ST77XX_BLACK);
  tft.print("Time of Day: ");
  tft.setTextColor(ST77XX_MAGENTA,ST77XX_BLACK);
  tft.println("Noon");
   tft.setTextColor(ST77XX_WHITE,ST77XX_BLACK);
  tft.print("Heads Up Display: ");
  tft.setTextColor(ST77XX_MAGENTA,ST77XX_BLACK);
  if(digitalRead(switch_pin1) == LOW){
    tft.setTextColor(ST77XX_RED,ST77XX_BLACK);
    tft.println("OFF    ");
    Serial.println("HUD OFF");
  }
  else if(digitalRead(switch_pin1) == HIGH) {
    tft.setTextColor(ST77XX_GREEN,ST77XX_BLACK);
    tft.println("ON     ");
    Serial.println("HUD ON");
  }
    tft.setTextColor(ST77XX_WHITE,ST77XX_BLACK);
  tft.print("Manual Override: ");
  if(digitalRead(switch_pin2) == LOW){
    tft.setTextColor(ST77XX_RED,ST77XX_BLACK);
    tft.println("OFF     ");
    Serial.println("OVERRIDE OFF");
  }
  else if(digitalRead(switch_pin2) == HIGH){
    tft.setTextColor(ST77XX_GREEN,ST77XX_BLACK);
    tft.println("ON     ");
    Serial.println("OVERRIDE ON");
  }
  
  
  int temp = analogRead(squareButton);
 //analogRead(diamondButton)

  if ( temp > 90 && temp < 140){ 
    tft.fillCircle(19, 127, 5, ST77XX_WHITE);
    Serial.println("square TR");
  }
  else if ( temp >= 140 && temp < 200){ 
    tft.fillCircle(6, 127, 5, ST77XX_WHITE);
    Serial.println("square TL");  
    }
  else if ( temp >= 200 && temp < 300){
    tft.fillCircle(6, 140, 5, ST77XX_WHITE);
    Serial.println("square BL");
  }
  else if ( temp >= 300 && temp < 500){
    tft.fillCircle(19, 140, 5, ST77XX_WHITE);
    Serial.println("square BR");
  }
  else
  {
    tft.fillCircle(6, 127, 5, ST77XX_BLACK);
    tft.fillCircle(19, 127, 5, ST77XX_BLACK);
    tft.fillCircle(6, 140, 5, ST77XX_BLACK);
    tft.fillCircle(19, 140, 5, ST77XX_BLACK);
    Serial.println("square none");
   }
   
  tft.drawCircle(6, 127, 5, ST77XX_WHITE);
  tft.drawCircle(19, 127, 5, ST77XX_WHITE);
  tft.drawCircle(6, 140, 5, ST77XX_WHITE);
  tft.drawCircle(19, 140, 5, ST77XX_WHITE);

  
  


  
  int squareButton = A2;



  temp = analogRead(diamondButton);

  if ( temp > 90 && temp < 140){ 
    tft.fillCircle(tft.width()-18, 126, 5, ST77XX_WHITE);
    Serial.println("diag Left");
  }
  else if ( temp >= 140 && temp < 200){ 
    tft.fillCircle(tft.width()-26, 134, 5, ST77XX_WHITE);
    Serial.println("diag Down");
  }
  else if ( temp >= 200 && temp < 300){
    tft.fillCircle(tft.width()-18, 143, 5, ST77XX_WHITE);
    Serial.println("diag Right");
  }
  else if ( temp >= 300 && temp < 500){
    tft.fillCircle(tft.width()-10, 134, 5, ST77XX_WHITE);
    Serial.println("diag Up");
  }
  else
  {
    tft.fillCircle(tft.width()-18, 126, 5, ST77XX_BLACK);
    tft.fillCircle(tft.width()-10, 134, 5, ST77XX_BLACK);
    tft.fillCircle(tft.width()-18, 143, 5, ST77XX_BLACK);
    tft.fillCircle(tft.width()-26, 134, 5, ST77XX_BLACK);
    Serial.println("diag none");
   }

  tft.drawCircle(tft.width()-18, 126, 5, ST77XX_WHITE);
  tft.drawCircle(tft.width()-10, 134, 5, ST77XX_WHITE);
  tft.drawCircle(tft.width()-18, 143, 5, ST77XX_WHITE);
  tft.drawCircle(tft.width()-26, 134, 5, ST77XX_WHITE);



    
  tft.fillCircle(tft.width()/2+(hori/8), 194.5-(vert/8), 6, ST77XX_WHITE);
  tft.drawCircle(tft.width()/2, 189, 50, ST77XX_WHITE);
  tft.fillCircle(tft.width()/2, 189, 49.9, ST77XX_BLACK);

  int sliderTemp = 0.064*-analogRead(sliderPin);
  tft.fillRect(35, 126 , 64, 8, ST77XX_BLACK); //fillbar
  tft.fillRect(35, 126 , 64+sliderTemp, 8, ST77XX_MAGENTA); //fillbar
  tft.drawRect(35, 126 , 64, 8, ST77XX_WHITE);

  tft.fillRect(35, 115 , 20, 8, ST77XX_BLACK);
  if(digitalRead(switch_pin1) == LOW){
    tft.fillRect(35, 115 , 10, 8, ST77XX_RED);
  }
  if(digitalRead(switch_pin1) == HIGH){
    tft.fillRect(45, 115 , 10, 8, ST77XX_GREEN);
  }
  tft.drawRect(35, 115 , 20, 8, ST77XX_WHITE);
  
  tft.fillRect(79, 115 , 20, 8, ST77XX_BLACK);
  if(digitalRead(switch_pin2) == LOW){
    tft.fillRect(79, 115 , 10, 8, ST77XX_RED);
  }
  if(digitalRead(switch_pin2) == HIGH){
    tft.fillRect(89, 115 , 10, 8, ST77XX_GREEN);
  }
  tft.drawRect(79, 115 , 20, 8, ST77XX_WHITE);

  //int x = 5;  
  temp = analogRead(potPin); //max is 1000 for the analog and the max in 
  int x = 11-0.011*temp; 
  
  tft.fillTriangle(tft.width()/2,(tft.height()/2)+2,tft.width()/2-11,tft.height()/2-11,tft.width()/2+11,tft.height()/2-11,ST77XX_BLACK);
  tft.fillTriangle(tft.width()/2,(tft.height()/2)+2,tft.width()/2-x,tft.height()/2-x,tft.width()/2+x,tft.height()/2-x,ST77XX_MAGENTA);
  tft.drawTriangle(tft.width()/2,(tft.height()/2)+2,tft.width()/2-11,tft.height()/2-11,tft.width()/2+11,tft.height()/2-11,ST77XX_WHITE);
  
}
