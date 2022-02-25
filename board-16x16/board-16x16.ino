// Arduino Uno
#define SIG_pin A0
#define s0 A4
#define s1 A3
#define s2 A2
#define s3 A1

//#define OUT_pin 2
//#define w0 3
//#define w1 4
//#define w2 5
//#define w3 6

#define OUT_pin 9
#define w0 10
#define w1 11
#define w2 12
#define w3 13

//Mux control pins for analog signal (SIG_pin) default for arduino mini pro
//const byte s0 = D0;
//const byte s1 = D1;
//const byte s2 = D2;
//const byte s3 = D3;

//Mux control pins for Output signal (OUT_pin) default for arduino mini pro
//const byte w0 = D5; 
//const byte w1 = D6;
//const byte w2 = D7;
//const byte w3 = D8;

//Mux in "SIG" pin default for arduino mini pro 
//const byte SIG_pin = A0; 

//Mux out "SIG" pin default for arduino mini pro
//const byte OUT_pin = D4;

//Row and Column pins default for arduino mini pro
//const byte STATUS_pin = 3;
//const byte COL_pin = 2;

const boolean muxChannel[16][4]={
    {0,0,0,0}, //channel 0
    {1,0,0,0}, //channel 1
    {0,1,0,0}, //channel 2
    {1,1,0,0}, //channel 3
    {0,0,1,0}, //channel 4
    {1,0,1,0}, //channel 5
    {0,1,1,0}, //channel 6
    {1,1,1,0}, //channel 7
    {0,0,0,1}, //channel 8
    {1,0,0,1}, //channel 9
    {0,1,0,1}, //channel 10
    {1,1,0,1}, //channel 11
    {0,0,1,1}, //channel 12
    {1,0,1,1}, //channel 13
    {0,1,1,1}, //channel 14
    {1,1,1,1}  //channel 15
  };


//incoming serial byte
int inByte = 0;

int valor = 0;               //variable for sending bytes to processing
int calibra[16][16];         //Calibration array for the min values of each od the 225 sensors.
int minsensor=254;          //Variable for staring the min array
int multiplier = 254;
int pastmatrix[16][16];

void setup(){
    
  pinMode(s0, OUTPUT); 
  pinMode(s1, OUTPUT); 
  pinMode(s2, OUTPUT); 
  pinMode(s3, OUTPUT); 
  
  pinMode(w0, OUTPUT); 
  pinMode(w1, OUTPUT); 
  pinMode(w2, OUTPUT); 
  pinMode(w3, OUTPUT); 
  
  pinMode(OUT_pin, OUTPUT); 
  
//  pinMode(STATUS_pin, OUTPUT);
//  pinMode(COL_pin, OUTPUT);

  
  digitalWrite(s0, LOW);
  digitalWrite(s1, LOW);
  digitalWrite(s2, LOW);
  digitalWrite(s3, LOW);
  
  digitalWrite(w0, LOW);
  digitalWrite(w1, LOW);
  digitalWrite(w2, LOW);
  digitalWrite(w3, LOW);
  
  digitalWrite(OUT_pin, HIGH);
//  digitalWrite(STATUS_pin, HIGH);
//  digitalWrite(COL_pin, HIGH);
  
 
  
  Serial.begin(115200);
  
  Serial.println("\n....Calibratong...\n");
  
  // Full of 0's of initial matrix
  for(byte j = 0; j < 16; j ++){ 
    writeMux(j);
    for(byte i = 0; i < 16; i ++)
      calibra[j][i] = 0;
  }
  
  // Calibration
  for(byte k = 0; k < 50; k++){  
    for(byte j = 0; j < 16; j ++){ 
      writeMux(j);
      for(byte i = 0; i < 16; i ++)
        calibra[j][i] = calibra[j][i] + readMux(i);
    }
  }
  
  //Print averages
  for(byte j = 0; j < 16; j ++){ 
    writeMux(j);
    for(byte i = 0; i < 16; i ++){
      calibra[j][i] = calibra[j][i]/50;
      if(calibra[j][i] < minsensor)
        minsensor = calibra[j][i];
//      Serial.print(calibra[j][i]);
//      Serial.print("\t");
    }
//  Serial.println(); 
  }
  
//  Serial.println();
//  Serial.print("Minimum Value: ");
//  Serial.println(minsensor);
//  Serial.println();
  
  establishContact();
 
//  digitalWrite(COL_pin, LOW);
}


void loop(){
  //Loop through and read all 16 values
  //Reports back Value at channel 6 is: 346
  if (Serial.available() > 0){
    inByte = Serial.read();
    
    if(inByte == 'A'){
    
      for(int j = 15; j >= 0; j--){ 
        writeMux(j);
        
        for(int i = 0; i < 16; i++){
            
          valor = readMux(i);
          
          //Saturation sensors
          int limsup = 450;
          if(valor > limsup)
            valor = limsup;
            
          if(valor < calibra[j][i])
            valor = calibra[j][i];  
          
          valor = map(valor,minsensor, limsup,1,254); 
          
          if(valor < 150)
            valor = 0;
          if(valor > 254)
            valor = 254;

          Serial.print(valor);
          Serial.print("\t");
//          Serial.write(valor);
//          digitalWrite(COL_pin,!digitalRead(COL_pin));
        } 
//        Serial.println();
      }
//      Test Delay
//      delay(2000);
    }
        
  }
}


int readMux(byte channel){
  byte controlPin[] = {s0, s1, s2, s3};

  //loop through the 4 sig
  for(int i = 0; i < 4; i ++){
    digitalWrite(controlPin[i], muxChannel[channel][i]);
  }

  //read the value at the SIG pin
  int val = analogRead(SIG_pin);

  //return the value
  return val;
}

void writeMux(byte channel){
  byte controlPin[] = {w0, w1, w2, w3};

  //loop through the 4 sig
  for(byte i = 0; i < 4; i ++){
    digitalWrite(controlPin[i], muxChannel[channel][i]);
  }
}

void establishContact() {
  while (Serial.available() <= 0) {
    Serial.print('A');   // send a capital A
    delay(300);
  }
}
