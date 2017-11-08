#include "LPD8806.h"
#include "SPI.h" 

long tiempo_actual;
long tiempo_pir;
long tiempo_enviar;


int nLEDs = 160;
int data_pin  = 2;
int clock_pin = 3;
int pir_pin = 7;
LPD8806 strip = LPD8806(nLEDs, data_pin, clock_pin);
int estado_leds = 0;

void setup() {
  Serial.begin(9600);
  strip.begin();
  strip.show();
  estado_leds = 0;
  tiempo_actual = millis();
  tiempo_pir = millis();
  tiempo_enviar = millis();
  

}

void loop() {
  tiempo_actual = millis();
  int pir_read = digitalRead(pir_pin);
  //if(estado_leds == 1){
  // if(tiempo_actual >= tiempo_pir + 120000){
  //   apagar_leds();
  //    estado_leds = 0;
   // }
  //}
  if(pir_read > 0) {
    if(tiempo_actual >= tiempo_pir + 5000){
      tiempo_pir = millis();
      tiempo_enviar = millis();
      registro_enviar();
    }
  //  if(estado_leds==0){
  //    aleatorio();
  //    estado_leds = 1;
  //  }
  }
  if(tiempo_actual >= tiempo_enviar + 10000){
    tiempo_enviar = millis();
    registro_enviar();
  }
  
  if(Serial.available() > 0){
    char leer = Serial.read();
    if(leer=='1'){
      aleatorio();
    }
    if(leer=='0'){
      apagar_leds();
    }
   }
}

void registro_enviar(){
    int pir_read = digitalRead(pir_pin);
    Serial.print("pir,binary,1,");
    Serial.println(pir_read);
 }
  
void aleatorio() {
  //Serial.println("Prenderleds");
  for(int i=0; i<strip.numPixels(); i++) strip.setPixelColor(i, 0);
  for(int i=0; i < strip.numPixels(); i++){
    int r = random(100)+1;
    int g = random(100)+1;
    int b = random(100)+1;
    if(i%3 == 0){
      strip.setPixelColor(i, strip.Color(r, g, b));
      }
  }
  strip.show();
  delay(2000);
}

void apagar_leds() {
  //Serial.println("Apagar leds");
  for(int i=0; i<strip.numPixels(); i++) strip.setPixelColor(i, 0);
  strip.show();
  delay(2000); 
}


