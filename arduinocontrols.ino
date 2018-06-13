#include <Stepper.h>


int Angle;
const int stepsPerRevolution = 850;
const int stepsToGo = 1;
Stepper myStepper(stepsPerRevolution, 2, 3);

void setup() {
  Serial.begin(9600);
  Serial.println("TOP");
  Angle = 300;

   //Steering LA
  pinMode(9, OUTPUT); // pot 1 gnd
  digitalWrite(9, LOW);
  pinMode(8, OUTPUT); //pot 1 5V
  digitalWrite(8, HIGH);
  pinMode(A2, INPUT); //pot 1 sig
  
  //Steering Relay
  pinMode(50, OUTPUT);
  pinMode(51, OUTPUT);
  digitalWrite(50, LOW);
  digitalWrite(51, HIGH);
  delay(3000);
  digitalWrite(50, HIGH);
  Serial.println(analogRead(A2));

  //Scoop Relay
  pinMode(48, OUTPUT);
  pinMode(49, OUTPUT);
  digitalWrite(48, LOW);
  digitalWrite(49, HIGH);
  delay(3000);
  digitalWrite(48, HIGH);
  
  //Door Relay
  pinMode(46, OUTPUT);
  pinMode(47, OUTPUT);
  digitalWrite(46, HIGH);
  digitalWrite(47, LOW);
  delay(3000);
  digitalWrite(47, HIGH);
  
  //Throttle
  myStepper.setSpeed(60);
  myStepper.step(-stepsPerRevolution);
  delay(100);

//limitswitch
  pinMode(45, INPUT);
}


void steer(int ang)
{
  int current_pos = analogRead(A2);
  if (current_pos < (ang + 10)&& current_pos >(ang - 10)) {
    digitalWrite(50, HIGH);
    digitalWrite(51, HIGH);
  // Serial.println("I'm stopped");
  }
  else if (current_pos+10 > ang)
  {
    digitalWrite(51, HIGH);
    digitalWrite(50, LOW);
   // Serial.println("Left");

  }
  else if (current_pos-10 < ang)
  {
    digitalWrite(50, HIGH);
    digitalWrite(51, LOW);
   //Serial.println("Right");
  }
  else
  {
    digitalWrite(50, HIGH);
    digitalWrite(51, HIGH);
    //Serial.println("I'm stopped");
  }

}

void pickup(){
  digitalWrite(48, HIGH);
  digitalWrite(49, LOW);
  delay(2000); //lift off ground
  
  digitalWrite(48, HIGH);
  digitalWrite(49, HIGH);
  delay(400); //pause to get weight reading

  while(digitalRead(45) == LOW){ //get to top
    digitalWrite(48, HIGH);
    digitalWrite(49, LOW);
  }
  delay(200); 

  digitalWrite(48, LOW);//lower scoop
  digitalWrite(49, HIGH);
  delay(5000);
  
  digitalWrite(48, HIGH); //scoop returned to idle position
  digitalWrite(49, HIGH);  

}

void harvest(){ 
  digitalWrite(46, LOW); //extend
  digitalWrite(47, HIGH);
  delay(4000);

  digitalWrite(46, HIGH); //retract
  digitalWrite(47, LOW);
  delay(4000);

  digitalWrite(48, HIGH); //door returned to idle position
  digitalWrite(49, HIGH);  
  
}


int Speed;
String num;
void loop() {
  Serial.flush();
  if (Serial.available())
  {
    char in = Serial.read();
    switch (in)
    {
      case 'E': Angle = analogRead(A2); break; // emergency stop?
      case 'W': num = Serial.readString();
                Angle = num.toInt(); break; //enter # degrees
      case 'L': Angle = 0; break;
      case 'M': Angle = 400; break;
      case 'R': Angle = 965; break;
      case 'S': num = Serial.readString();
                myStepper.step(num.toInt()); break; //enter # of steps 
      case 'P': pickup(); break;
      case 'H': harvest(); break;
                

      default: break;
    }
  }
  steer(Angle);

}
