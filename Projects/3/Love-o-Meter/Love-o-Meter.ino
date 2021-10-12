const int sensorPin =A0;
const float baselineTemp = 100.0;

void setup() {

Serial.begin(9600);

for(int pinNumber = 2; pinNumber<5; pinNumber++){
  pinMode(pinNumber, OUTPUT);
  digitalWrite(pinNumber, LOW);
  }

}

void loop() {
  int sensorVal = analogRead(sensorPin);
  Serial.print("Sensor Value: ");
  Serial.print(sensorVal);
  
  //convert the ADC reading to voltage
  float voltage = (sensorVal/1024.0)* 5.0;

  Serial.print(", Volts:");
  Serial.print(voltage);

  Serial.print(", degrees C: ");  
  //convert the voltage to temperature in degrees
  float temperature = voltage * 100;
  Serial.println(temperature);

  if(temperature < baselineTemp+50){
    digitalWrite(2,LOW);
    digitalWrite(3,LOW);
    digitalWrite(4,LOW);
  }
  else if(temperature >= baselineTemp+50 && temperature < baselineTemp+200){
    digitalWrite(2,HIGH);
    digitalWrite(3,LOW);
    digitalWrite(4,LOW);
  }
  else if(temperature >= baselineTemp+200 && temperature < baselineTemp+300){
    digitalWrite(2,HIGH);
    digitalWrite(3,HIGH);
    digitalWrite(4,LOW);
  }
  else if(temperature >= baselineTemp+300){
    digitalWrite(2,HIGH);
    digitalWrite(3,HIGH);
    digitalWrite(4,HIGH);
  }
  delay(1);
}
