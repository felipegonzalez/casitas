//caja_9_estudiot.ino
#include "Adafruit_MCP9808.h"
#include "Wire.h"

 


Adafruit_MCP9808 tempsensor = Adafruit_MCP9808();

int pir_pin = 7;
int photo_pin = 0;
int reed_pin = 3;

int bloque_enviar = 0;
long tiempo_ultima;
long tiempo_pir;

int pir_read;
int door;
int door_anterior;

void setup()
{
  Serial.begin(9600);
  Serial.println("Empezando MCP");
  if (!tempsensor.begin()) {
     //Serial.println("Couldn't find MCP9808!");
    while (1);
  }
  //Serial.println("Empezando def pins");
  pinMode(pir_pin, INPUT);
  pinMode(reed_pin, INPUT);
  
  tiempo_ultima = millis();
  tiempo_pir = millis();
  door = digitalRead(reed_pin);
  door_anterior = digitalRead(reed_pin);
}

void loop() {
  
  long tiempo_actual = millis();
  int pir_read = digitalRead(pir_pin);
  int door  = digitalRead(reed_pin);
  if(pir_read == 1){
        if(tiempo_actual >= tiempo_pir + 3000){
          //Serial.println("Movimiento registrado");
          tiempo_pir = millis();
          //tiempo_ultima = millis();
          enviar_pir();
  		}
  		
  }
  if(door_anterior!=door){
      //Serial.println("Cambio de estado de puerta");
  		door_anterior = door;
  		tiempo_pir = millis();
      enviar_pir();
  	}


  
  if(tiempo_actual >= tiempo_ultima + 20000){
    registro_enviar();
    tiempo_ultima = millis();
    bloque_enviar = 1 - bloque_enviar;
  }
}

void enviar_pir(){
  int door  = digitalRead(reed_pin);
  int pir_read = digitalRead(pir_pin);
  Serial.print("pir,binary,1,");
  Serial.println(pir_read);
  Serial.print("puerta,binary,1,");
  Serial.println(door);
}
void registro_enviar(){
  delay(500);
  if(bloque_enviar==0){
    enviar_pir();
  } else {
    int photoread = analogRead(photo_pin);  
    float ctemp = tempsensor.readTempC();
    Serial.print("photo,analog,1,"); 
    Serial.println(photoread);  
    Serial.print("temperature,C,1,"); 
    Serial.println(ctemp);
  
  }
  
  //if(bloque_enviar==1){

  //} else {

  //}

  
}
  

