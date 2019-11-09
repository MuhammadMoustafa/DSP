
#include <SPI.h>
#include <SD.h>

 const int filterSelectBtn = 2;       // the number of the pushbutton pin 
 const int toggleBtn = 7;             // the second push button used to toggle the state

 File myFile;
 int MicFlag = 1 ;
 int SDFlag  = 0 ;
 int filterNumber = 0;
 int filterCounter = 0;
 int flagCounter = 0;
 
 float sensorPin = A0;    // select the input pin for the potentiometer
 float x[7] = {0,0,0,0,0,0,0};
 float y[7] = {0,0,0,0,0,0,0};
 
bool buttonState = 0;         // variable for reading the filterSelect button status
bool toggleState = 0;         // variable for reading the toggle button status

 
 float aL[4] = { 1 ,-1.76004188 , 1.18289326 ,-0.27805992 };
 float bL[4] = { 0.01809893 , 0.0542968 ,  0.0542968 ,  0.01809893 };
 
 float aH [4] ={ 1     ,   1.76004188 , 1.18289326,  0.27805992}; 
 float bH [4]= { 0.01809893 ,-0.0542968  , 0.0542968 , -0.01809893};


float aBP[7] = { 1 ,  -1.54663136 , 2.5732668 , -2.05722665 , 1.70653526, -0.65538675,  0.27805992};
float bBP[7] = {  0.01809893 , 0.    ,     -0.0542968  , 0.    ,      0.0542968  , 0., -0.01809893};



void applyFilter(float a[] , float b[],int sizeA)
{
  y[0]=0;
for (int i=0;i<sizeA ;i++)
{ y[0] += b[i]*x[i];  
}
for (int i=1;i<sizeA ;i++)
{y[0] -= a[i]*y[i];}

for(int i=sizeA-2;i>=0;i--){
  x[i+1]=x[i];
  y[i+1]=y[i];
  
}
}

void updateFlags()
{
  buttonState = digitalRead(filterSelectBtn) ;      // read the value of the filter select button 
  toggleState = digitalRead(toggleBtn) ;        // read the value of the toggle button
  
 if(toggleState == HIGH)
  {
    delay(200) ;
    flagCounter++;
  }
  if(flagCounter%2 == 0)
  {
    MicFlag =1 ;
    SDFlag = 0 ;
  }
  else if(flagCounter%2 == 1)
  {
    MicFlag = 0 ;
    SDFlag =1 ;
  }
  
  if (buttonState == HIGH)
  {
    delay(200) ;
    filterCounter++ ;
  }
  if (filterCounter%3 == 0){filterNumber = 0;}
  else if(filterCounter%3 == 1){filterNumber = 1;}
  else if(filterCounter%3 == 2){filterNumber = 2;}
}


void setup()
{
  Serial.begin(9600);
  pinMode(sensorPin,INPUT);
  while (!Serial) {
    ; 
  }
 // pinMode(10, OUTPUT);
}

void loop()
{
  
  //put here function to set flags from omar , updateFlags();
  updateFlags();
  
  if(SDFlag==1){
    if (!SD.begin(4)) {
    Serial.println("initialization failed!");
    return;
  }  
  myFile = SD.open("test.txt");
  if (myFile) {

      // read from the file until there's nothing else in it:
    while (myFile.available()) {
    
      x[0]=myFile.parseFloat();
      
      //put here any code you want
      updateFlags();
      if (SDFlag==0){
      break;}
      
      if(filterNumber ==0){
      applyFilter(aL,bL,4);}
      else if(filterNumber ==1){
      applyFilter(aH,bH,4);}
      else if (filterNumber == 2){
      applyFilter(aBP,bBP,7);}
      
      Serial.print(x[0]);
      Serial.print(',') ;
      Serial.println(y[0]);
     
       }
            Serial.println("Stop");

    // close the file:
    myFile.close();
   
  }
  else {
    // if the file didn't open, print an error:
    Serial.println("error opening test.txt");
  }

  }
  
  
  
  
  else if (MicFlag ==1){
       x[0]= analogRead(sensorPin);
      
      //put here any code you want
      if(filterNumber ==0){  
      applyFilter(aL,bL,4);}
      else if(filterNumber ==1){
      applyFilter(aH,bH,4);}
      else if (filterNumber == 2){
      applyFilter(aBP,bBP,7);}
      
      Serial.print(x[0]);
      Serial.print(',') ;
      Serial.println(y[0]);
  }
 
}


