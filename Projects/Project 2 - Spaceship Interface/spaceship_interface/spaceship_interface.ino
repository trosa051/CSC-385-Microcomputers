int switchState = 0;
void setup(){
    pinMode(3, OUTPUT);
    pinMode(4, OUTPUT);
    pinMode(5, OUTPUT);
    pinMode(2, INPUT);
}
void loop(){
    switchState = digitalRead(2);
    if (switchState == LOW){  //the button is not pressed
        digitalWrite(3,HIGH); // Grn LED
        digitalWrite(4,LOW);  // Red LED
        digitalWrite(5,LOW);  // Red LED
    }
    else{                     // The button has been pressed
        delay(250);
        digitalWrite(3,LOW); // Grn LED
        digitalWrite(4,LOW);  // Red LED
        digitalWrite(5,HIGH);  // Red LED

    delay(250); //250 is a quarter of a second
    // Toggle LEDs
    digitalWrite(4,HIGH); 
    digitalWrite(5,LOW);
    }
}
