#include <MsTimer2.h>
#include <DHT11.h>


int temp = 2;
int led1 = 4;  //1층
int led2 = 3;  //2층
int led3 = 6; //외부
int cds = A0;
int fan = 5;

DHT11 dht11(temp);

int err;
String inputString = "";         // a String to hold incoming data
boolean stringComplete = false;  // whether the string is complete
int state = 0;
int TH_flag=0;

void flag_check()
{
    TH_flag=1;
}


void setup() {
  Serial.begin(9600);
  inputString.reserve(200);
  pinMode(led1,OUTPUT);
  pinMode(led2,OUTPUT);
  pinMode(led3,OUTPUT);
  pinMode(fan,OUTPUT);
  MsTimer2::set(3000, flag_check); // 3sec period
  MsTimer2::start();
  
//  MsTimer2::set(3000,flash);
//  MsTimer2::start();
  
}

void loop() {
  
  int cdsValue = analogRead(cds);
  float temp, humi;  

  if(TH_flag){
      if((err=dht11.read(humi,temp))==0){
        //Serial.print("t:");
        //Serial.print(temp);
        //Serial.print(" ℃");
        //Serial.print("\n");
//        Serial.print(humi);
//        Serial.print(" %");
        String q = "t:"+(String)temp+" ℃";
        Serial.print(q);
        q = "h:"+(String)humi+" %";
        Serial.print(q);
        //Serial.print("h:");
        //Serial.print(humi);
        //Serial.println();
     }
    else{
        Serial.println();
        Serial.println("e: ");
        Serial.print(err);
        Serial.println();
    }
    TH_flag=0;
  }
  
//  Serial.print("L: ");
//  Serial.print(cdsValue);
//  Serial.println();
  if(cdsValue<200){
//    digitalWrite(led1,HIGH);
//    digitalWrite(led2,HIGH);
    digitalWrite(led3,LOW);
//    Serial.print("31");
    //야외조명 꺼짐 켜짐 신호보내기
  }else{
//    digitalWrite(led1,LOW);
//    digitalWrite(led2,LOW);
    digitalWrite(led3,HIGH);
    //Serial.print("30");
  }
  if(temp > 30){
    digitalWrite(fan,HIGH);
  }else{
    digitalWrite(fan,LOW);
  }
   /* Received from Raspberry Pi */
  if (stringComplete) {    
       if(inputString == "L1Z"){  
            digitalWrite(led1, (state) ? HIGH : LOW);
            state = !state;     
       }
       else if(inputString == "L2Z"){  
            digitalWrite(led2, (state) ? HIGH : LOW);
            state = !state;     
       }
       inputString = "";
       stringComplete = false;
  }
  delay(500);  
}
void serialEvent() 
{
     int i;
     while (Serial.available()) {
          char inChar = (char)Serial.read();    
          inputString += inChar;
          Serial.print(inChar);
          if (inChar == 'Z') {
               stringComplete = true;
          }
     }
}
