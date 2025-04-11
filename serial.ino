#include <Servo.h>  // Include the Servo library
#include <AFMotor.h>

// Define the servo motor pins
Servo leftServo;
Servo rightServo;

AF_DCMotor motor1(1); // Left motor
AF_DCMotor motor2(2); // Right motor
AF_DCMotor motor3(3); // Right motor
AF_DCMotor motor4(4); // Right motor


// Pin for the microphone (ZN-15E)
int micPin = A0;  // Microphone connected to A0 pin
int soundLevel = 0;  // Variable to store the sound level

void setup() {
  Serial.begin(9600);  // Start serial communication for debugging


    motor1.setSpeed(255); // Set speed
    motor2.setSpeed(255); // Set speed
    motor3.setSpeed(255); // Set speed
    motor4.setSpeed(255); // Set speed

  
  // Attach servos to pins
  leftServo.attach(9);  // Attach left servo to pin 9
  rightServo.attach(10); // Attach right servo to pin 10
  leftServo.write(0);
  rightServo.write(0);
}

void loop() 
{
  soundLevel = analogRead(micPin);  // Read the microphone input
  Serial.println(soundLevel);  // Print the sound level to the Serial Monitor
  
  // If sound level exceeds a threshold, trigger action
  if (soundLevel > 40) {  // You can adjust this threshold based on your testing
    Serial.println("Sound level high enough, triggering action...");
    delay(500);  // Delay to allow for the voice command trigger

    if (Serial.available() > 0){
      String command = Serial.readString();

      command.trim();

      if (command == "hello"){
        Serial.println("Hello command received.");
        leftServo.write(180);
        delay(1000);
        leftServo.write(90);
      }
      if (command == "goodbye"){
        Serial.println("goodbye command received.");
        leftServo.write(180);
        delay(1000);
        leftServo.write(90);
      }
      if (command == "dance"){
        dance();
        delay(1000);
      } 

      if (command == "front"){
        moveForward();
        delay(1000);
      }

      if (command == "back"){
        moveBackward();
        delay(1000);
      }
    }
  }
}


void moveForward() {
    motor1.run(FORWARD); // Move forward
    motor2.run(FORWARD);
    motor3.run(FORWARD);
    motor4.run(FORWARD);
    delay(2000); // Turn duration
    motor1.run(RELEASE); // Stop motors
    motor2.run(RELEASE);
    motor3.run(RELEASE);
    motor4.run(RELEASE);
    
}

void moveBackward() {
    motor1.run(BACKWARD); // Move backward
    motor2.run(BACKWARD);
    motor3.run(BACKWARD);
    motor4.run(BACKWARD);
    delay(2000); // Turn duration
    motor1.run(RELEASE); // Stop motors
    motor2.run(RELEASE);
    motor3.run(RELEASE);
    motor4.run(RELEASE);
}

void dance(){
    for (int i = 0; i <=2; i++) {
        leftServo.write(90);
        rightServo.write(90);
        delay(100);
        leftServo.write(0);
        rightServo.write(0);
        delay(100);
        }
}

