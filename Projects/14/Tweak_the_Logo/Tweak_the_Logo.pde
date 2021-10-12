import processing.serial.*;
Serial myPort;

PImage logo;

int bgcolor = 0;

void setup(){
size(1,1);
surface.setResizable(true);
colorMode(HSB,255);

logo = loadImage("https://tjarosar.io/media/groovin.gif");
surface.setSize(logo.width, logo.height);

println("Available serial ports: ");
println(Serial.list());

myPort = new Serial(this, Serial.list()[0], 9600);

}

void draw() {
  if (myPort.available()>0){
  bgcolor = myPort.read();
  println(bgcolor);
  }
  else{
  print("waiting?");
  }
  scale(3,3);
  tint(bgcolor,255,255);
  image(logo, 0, 0);
}
