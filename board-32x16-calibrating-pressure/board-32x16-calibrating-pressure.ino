// Arduino Uno
// ! Analog signal (SIG_pin)
#define SIG_pin A0
#define s0 A4
#define s1 A3
#define s2 A2
#define s3 A1

// ! Output signal (OUT_pin)
// Top
#define OUT_top_pin 2
#define wt0 3
#define wt1 4
#define wt2 5
#define wt3 6

// Bottom
#define OUT_bottom_pin 9
#define wb0 10
#define wb1 11
#define wb2 12
#define wb3 13

#define ROW_SIZE 32
#define COL_SIZE 16
#define MAX_SIZE ROW_SIZE*COL_SIZE

const boolean muxChannel[16][4] = {
  {0, 0, 0, 0}, //channel 0
  {1, 0, 0, 0}, //channel 1
  {0, 1, 0, 0}, //channel 2
  {1, 1, 0, 0}, //channel 3
  {0, 0, 1, 0}, //channel 4
  {1, 0, 1, 0}, //channel 5
  {0, 1, 1, 0}, //channel 6
  {1, 1, 1, 0}, //channel 7
  {0, 0, 0, 1}, //channel 8
  {1, 0, 0, 1}, //channel 9
  {0, 1, 0, 1}, //channel 10
  {1, 1, 0, 1}, //channel 11
  {0, 0, 1, 1}, //channel 12
  {1, 0, 1, 1}, //channel 13
  {0, 1, 1, 1}, //channel 14
  {1, 1, 1, 1} //channel 15
};


//incoming serial byte
int inByte = 0;

int valor = 0;                                // Variable for sending bytes to processing
unsigned int calibra[ROW_SIZE][COL_SIZE];     // Calibration array for the min values of each od the {MAX_SIZE} sensors.
int minsensor = 254;                          // Variable for staring the min array
int multiplier = 254;

void setup() {

  pinMode(s0, OUTPUT);
  pinMode(s1, OUTPUT);
  pinMode(s2, OUTPUT);
  pinMode(s3, OUTPUT);

  pinMode(wt0, OUTPUT);
  pinMode(wt1, OUTPUT);
  pinMode(wt2, OUTPUT);
  pinMode(wt3, OUTPUT);

  pinMode(wb0, OUTPUT);
  pinMode(wb1, OUTPUT);
  pinMode(wb2, OUTPUT);
  pinMode(wb3, OUTPUT);

  pinMode(OUT_top_pin, OUTPUT);
  pinMode(OUT_bottom_pin, OUTPUT);


  digitalWrite(s0, LOW);
  digitalWrite(s1, LOW);
  digitalWrite(s2, LOW);
  digitalWrite(s3, LOW);

  digitalWrite(wt0, LOW);
  digitalWrite(wt1, LOW);
  digitalWrite(wt2, LOW);
  digitalWrite(wt3, LOW);

  digitalWrite(wb0, LOW);
  digitalWrite(wb1, LOW);
  digitalWrite(wb2, LOW);
  digitalWrite(wb3, LOW);

  digitalWrite(OUT_top_pin, HIGH);
  digitalWrite(OUT_bottom_pin, HIGH);


  Serial.begin(115200);

  Serial.println("\n....Calibrating...\n");

  // Full of 0's of initial matrix
  for (byte j = 0; j < ROW_SIZE; j ++) {
    if (j < ROW_SIZE / 2)
      writeTopMux(j);
    if (j >= ROW_SIZE / 2)
      writeBottomMux(j - 16);

    for (byte i = 0; i < COL_SIZE; i ++)
      calibra[j][i] = 0;
  }

  // Calibration
  int n_round = 250;
  for (byte k = 0; k < n_round; k++) {
    for (byte j = 0; j < ROW_SIZE; j ++) {
      if (j < ROW_SIZE / 2)
        writeTopMux(j);
      if (j >= ROW_SIZE / 2)
        writeBottomMux(j - 16);

      for (byte i = 0; i < COL_SIZE; i ++)
        calibra[j][i] = calibra[j][i] + readMux(i);
    }
//    Serial.print(".");
  }
  Serial.println();

  //Print averages
  for (byte j = 0; j < ROW_SIZE; j ++) {
    if (j < ROW_SIZE / 2)
      writeTopMux(j);
    if (j >= ROW_SIZE / 2)
      writeBottomMux(j - 16);

    for (byte i = 0; i < COL_SIZE; i ++) {
      calibra[j][i] = calibra[j][i] / n_round;
      if (calibra[j][i] < minsensor)
        minsensor = calibra[j][i];

      // Show calibrate value
      Serial.print(calibra[j][i]);
      Serial.print("\t");
    }
    Serial.println();
  }

  Serial.println();
  Serial.print("Minimum Value: ");
  Serial.println(minsensor);
  Serial.println();

  establishContact();

  //  digitalWrite(COL_pin, LOW);
}


void loop() {
  //Loop through and read all 16 values
  //Reports back Value at channel 6 is: 346
  if (Serial.available() > 0) {
    inByte = Serial.read();

    if (inByte == 'A') {

      // *NOTE* ส่งไปยัง python เก็บ 2 Sets:
      // (1) Fisrt Data : ไม่มีการปรับค่า
      Serial.print(1);
      Serial.print("\t");
      for (int j = 0; j < ROW_SIZE; j++) {
        if (j < ROW_SIZE / 2)
          writeTopMux(j);
        if (j >= ROW_SIZE / 2)
          writeBottomMux(j - 16);

        for (int i = 0; i < COL_SIZE; i++) {

          valor = readMux(i);

          if (valor < calibra[j][i])
            valor = calibra[j][i];

          Serial.print(valor);
          Serial.print("\t");

        }
        // Serial.println();
      }
      delay(5000);

      // (2) Second Data : มีการปรับค่า ตาม สเกล
//      Serial.print(2);
//      Serial.print("\t");
//      for (int j = 0; j < ROW_SIZE; j++) {
//        if (j < ROW_SIZE / 2)
//          writeTopMux(j);
//        if (j >= ROW_SIZE / 2)
//          writeBottomMux(j - 16);
//
//        for (int i = 0; i < COL_SIZE; i++) {
//
//          valor = readMux(i);
//
//          // Saturation sensors
//          int limsup = 1024;
//          if (valor > limsup)
//            valor = limsup;
//
//          if (valor < calibra[j][i])
//            valor = calibra[j][i];
//
//          valor = map(valor, minsensor, limsup, 1, 254);
//
//          //          if(valor < 150)
//          //            valor = 0;
//          //          if(valor > 254)
//          //            valor = 254;
//
//          Serial.print(valor);
//          Serial.print("\t");
//
//        }
//        // Serial.println();
//      }
//
//
//      // Test Delay
//      delay(5000);
    }

  }
}


int readMux(byte channel) {
  byte controlPin[] = {s0, s1, s2, s3};

  //loop through the 4 sig
  for (int i = 0; i < 4; i ++) {
    digitalWrite(controlPin[i], muxChannel[channel][i]);
  }

  //read the value at the SIG pin
  int val = analogRead(SIG_pin);

  //return the value
  return val;
}

void writeTopMux(byte channel) {
  byte controlPin[] = {wt0, wt1, wt2, wt3};

  //loop through the 4 sig
  for (byte i = 0; i < 4; i ++) {
    digitalWrite(controlPin[i], muxChannel[channel][i]);
  }
}

void writeBottomMux(byte channel) {
  byte controlPin[] = {wb0, wb1, wb2, wb3};

  //loop through the 4 sig
  for (byte i = 0; i < 4; i ++) {
    digitalWrite(controlPin[i], muxChannel[channel][i]);
  }
}

void establishContact() {
  while (Serial.available() <= 0) {
    Serial.print('A');   // send a capital A
    delay(1000);
  }
}
