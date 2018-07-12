// caja_cocina.ino
#include "DHT.h"
#include <SPI.h>
#include <LPD8806.h>

#define dht_type DHT22
#define pin_dht 8

int photo_pin = 0;
int pir_pin = 7;
int gas_pin = 1;
int enviar_gas = 1;
int data_led_pin  = 12;
int clock_led_pin = 13;
LPD8806 strip = LPD8806(74 , data_led_pin, clock_led_pin);
DHT dht(pin_dht, dht_type);
long tiempo_ultima;
long tiempo_actual;
long tiempo_pir;

void setup() {
  strip.begin();
  strip.show();
  Serial.begin(9600);
  dht.begin();
  pinMode(pir_pin, INPUT);
  delay(5000);
  encender_luces();

  tiempo_ultima = millis();
  tiempo_actual = millis();
  tiempo_pir = millis();
}

void loop() {
  tiempo_actual = millis();

  int pir_read = digitalRead(pir_pin);
  if (pir_read > 0) {
    if (tiempo_actual >= tiempo_pir + 2000) {
      tiempo_pir = millis();
      tiempo_ultima = millis();
      registro_enviar();
    }
  }
  if (tiempo_actual >= tiempo_ultima +  15000) {
    registro_enviar();
    tiempo_ultima = millis();
  }
  if(Serial.available() > 0){
    char leer = Serial.read();
    if(leer=='1'){
      encender_luces();
    }
    if(leer=='0'){
      apagar_luces();
    }
   }
}

void encender_luces(){
  int i;
  for(i=3; i < 45; i=i+1){
    strip.setPixelColor(i, strip.Color(127,70,10));
  }
  strip.show();
}

void apagar_luces(){
  int i;
  for(i=0; i < 45; i=i+1){
    strip.setPixelColor(i, 0);
  }
  strip.show();
}
void registro_enviar() {

  if (enviar_gas == 1) {
    float humid = dht.readHumidity();
    float temp  = dht.readTemperature();
    int gas_read = analogRead(gas_pin);
    int pir_read = digitalRead(pir_pin);
    Serial.print("pir,binary,1,");
    Serial.println(pir_read);
    Serial.print("gaslpg,analog,1,");
    Serial.println(gas_read);
    Serial.print("humidity,pc,1,");
    Serial.println(humid);
    Serial.print("temperature,C,1,");
    Serial.println(temp);

  } else {
    int photo_read = analogRead(photo_pin);
    delay(10);
    photo_read = analogRead(photo_pin);
    int pir_read = digitalRead(pir_pin);

    Serial.print("photo,analog,1,");
    Serial.println(photo_read);
    Serial.print("pir,binary,1,");
    Serial.println(pir_read);
  }
  enviar_gas = 1 - enviar_gas;


}
