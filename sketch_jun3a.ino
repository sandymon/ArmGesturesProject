#include <Servo.h>;

#define numOfValsRec  6
#define digitsPerValRec 1

int valsRec[numOfValsRec];
int stringLength = numOfValsRec * digitsPerValRec + 1;
int counter = 0;
bool counterStart = false;
String receivedString;


Servo thumbServo;
Servo indexServo;
Servo middleServo;
Servo ringServo;
Servo pinkyServo;
Servo wristServo;


void setup() {
  // put your setup code here, to run once:
    Serial.begin(9600);

    //finger Servo pinsouts
    thumbServo.attach(9);
    indexServo.attach(8);
    middleServo.attach(7);
    ringServo.attach(6);
    pinkyServo.attach(5);
    wristServo.attach(4);
}

void receivedData(){
  while(Serial.available()){
    char c = Serial.read();
    
    if (c=='$'){
      counterStart = true;
    }
    if(counterStart){
      if(counter < stringLength){
        receivedString = String(receivedString+c);
        counter++;
      }
      if(counter >=stringLength){
        for(int i =0; i < numOfValsRec; i++){
          int num = (i*digitsPerValRec)+1;
          valsRec[i] = receivedString.substring(num, num + digitsPerValRec).toInt();
        }
        receivedString = "";
        counter = 0;
        counterStart = false;
      }
    }
  }
}

void loop() {
  // put your main code here, to run repeatedly:
  receivedData();

  if(valsRec[0]==1){thumbServo.write(170);}else{thumbServo.write(0);}
  if(valsRec[1]==1){indexServo.write(170);}else{indexServo.write(0);}
  if(valsRec[2]==1){middleServo.write(170);}else{middleServo.write(0);}
  if(valsRec[3]==1){ringServo.write(170);}else{ringServo.write(0);}
  if(valsRec[4]==1){pinkyServo.write(170);}else{pinkyServo.write(0);}
  if(valsRec[5]==1){wristServo.write(170);}else{wristServo.write(0);}
  

}
