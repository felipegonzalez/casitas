/*
 *  Simple HTTP get webclient test
 */

#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>



const char* ssid     = "Niebelheim5";
const char* password = "valquiria";
ESP8266WebServer server(80);
String responseString="";    
IPAddress ip(192, 168, 100, 154);  
IPAddress gateway(192, 168, 100, 201);  
IPAddress subnet(255, 255, 255, 255); 

int canal_pasto = 0;
int canal_jardinera = 0;
int canal_macetas = 0;
int pin_pasto = 12;
int pin_jardinera = 13;
int pin_macetas = 14;
long timer_pasto;
long timer_jardinera;
long timer_macetas;
long actual;
long tiempo_jardinera = 0;
long tiempo_pasto = 0;
long tiempo_macetas = 0;




void setup() {
  Serial.begin(115200);
  delay(100);
  pinMode(pin_pasto, OUTPUT);
  pinMode(pin_jardinera, OUTPUT);
  pinMode(pin_macetas, OUTPUT);
  digitalWrite(pin_pasto, LOW);
  digitalWrite(pin_jardinera, LOW);
  digitalWrite(pin_macetas, LOW);
  

  Serial.println();
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.config(ip, gateway, subnet); 
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");  
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  server.on("/", handle_root);
  server.on("/hello", [](){  
  responseString = "Hello friend";
  server.send(200, "text/plain", responseString);            // send to someones browser when asked
  });

  server.on("/encender", comenzar_riego);
  server.on("/apagar", detener_riego);
  
  server.begin();

}

int value = 0;

void loop() {
  server.handleClient();
  actual = millis();
  // apagar cuando el tiempo expira
  if(actual - timer_jardinera > tiempo_jardinera){
    digitalWrite(pin_jardinera, LOW);
  }
   if(actual - timer_pasto > tiempo_pasto){
    digitalWrite(pin_pasto, LOW);
  }
    if(actual - timer_macetas > tiempo_macetas){
    digitalWrite(pin_macetas, LOW);
  }
  
}

void handle_root() {
  server.send(200, "text/plain", "Estacion de riego");
  delay(100);
}

void comenzar_riego() {
  String zona_arg = server.arg("zona");
  String tiempo_arg = server.arg("tiempo");
  
  if(zona_arg!=""){
    if(tiempo_arg!=""){
      int zona_valor = 99;
        if(zona_arg == "jardinera") zona_valor=0;
        if(zona_arg == "macetas") zona_valor=1;
        if(zona_arg == "pasto") zona_valor=2; 
      switch(zona_valor){
          case 0:
            digitalWrite(pin_jardinera, HIGH);
            tiempo_jardinera = 60*tiempo_arg.toInt()*1000;
            timer_jardinera = millis();
            break;
          case 1:
            digitalWrite(pin_macetas, HIGH);
            tiempo_macetas = 60*tiempo_arg.toInt()*1000;
            timer_macetas = millis();
            break;
          case 2:
             digitalWrite(pin_pasto, HIGH);
            tiempo_pasto = 60*tiempo_arg.toInt()*1000;
            timer_pasto = millis();
            break;
          default:
            break;
          
      }     
    }
  }
  responseString = "Encendido ";
  responseString += server.arg("zona");
  responseString += " durante ";
  responseString += server.arg("tiempo");
  responseString += " minutos";
  server.send(200, "text/plain", responseString);
}

void detener_riego() {
  String zona_arg = server.arg("zona");
  String tiempo_arg = server.arg("tiempo");
  int pin_encender = 0;
  int zona_valor = 99;
  if(zona_arg == "jardinera") zona_valor=0;
  if(zona_arg == "macetas") zona_valor=1;
  if(zona_arg == "pasto") zona_valor=2;
  if(zona_arg!=""){
    if(tiempo_arg!=""){
      switch(zona_valor){
          case 0:
            digitalWrite(pin_jardinera, LOW);
            break;
          case 1:
            digitalWrite(pin_macetas, LOW);
            break;
          case 2:
             digitalWrite(pin_pasto, LOW);
            break;
          default:
            break;
          
      }     
    }
  }
  responseString = "Apagar ";
  responseString += server.arg("zona");
  server.send(200, "text/plain", responseString);
}
void estado(){
  
}

