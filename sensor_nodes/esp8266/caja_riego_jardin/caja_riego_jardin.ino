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
int pin_pasto = 13; 
int pin_jardinera = 12;
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
  server.send(200, "text/plain", responseString);           
  });

  server.on("/jardinera", riego_jardinera);
  server.on("/pasto", riego_pasto);
  server.on("/macetas", riego_macetas);
  server.on("/estado", estado);
  server.begin();

}

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
  delay(100);
  
}

void handle_root() {
  server.send(200, "text/plain", "Estacion de riego");
  delay(100);
}


void riego_jardinera() {
  String comando_arg = server.arg("command");
  String tiempo_arg = server.arg("tiempo");
    if(tiempo_arg==""){
    tiempo_arg= "60";
  }
  if(comando_arg=="turn_on") {
    digitalWrite(pin_jardinera, HIGH);
    tiempo_jardinera = 60*tiempo_arg.toInt()*1000;
    timer_jardinera = millis();
  }
  if(comando_arg == "turn_off") {
    digitalWrite(pin_jardinera, LOW);
  }
  String respuesta = "";
  server.send(200, "text/plain", respuesta);
}

void riego_macetas() {
  String comando_arg = server.arg("command");
  String tiempo_arg = server.arg("tiempo");
  if(tiempo_arg==""){
    tiempo_arg= "60";
  }
  if(comando_arg=="turn_on") {
    digitalWrite(pin_macetas, HIGH);
    tiempo_macetas = 60*tiempo_arg.toInt()*1000;
    timer_macetas = millis();
  }
  if(comando_arg == "turn_off") {
    digitalWrite(pin_macetas, LOW);
  }
  String respuesta = "";
  server.send(200, "text/plain", respuesta);

}
void riego_pasto() {
  String comando_arg = server.arg("command");
  String tiempo_arg = server.arg("tiempo");
  if(tiempo_arg==""){
    tiempo_arg= "60";
  }
  if(comando_arg=="turn_on") {
    digitalWrite(pin_pasto, HIGH);
    tiempo_pasto = 60*tiempo_arg.toInt()*1000;
    timer_pasto = millis();
  }
  if(comando_arg == "turn_off") {
    digitalWrite(pin_pasto, LOW);
  }
  String respuesta = "";
  server.send(200, "text/plain", respuesta);

}


void estado(){
  int jardinera = digitalRead(pin_jardinera);
  int macetas = digitalRead(pin_macetas);
  int pasto = digitalRead(pin_pasto);
  long actual = millis();
  long restante_jardinera;
  long restante_macetas;
  long restante_pasto;

  restante_jardinera = (actual - timer_jardinera)/(1000*60);
  restante_macetas = (actual - timer_macetas)/(1000*60);
  restante_pasto = (actual - timer_pasto)/(1000*60);
  String estado_str = "\{";
  estado_str += "\"jardinera\":";
  estado_str += "\{\"state\":";
  estado_str += String(jardinera);
  estado_str += "\}";
  estado_str += ",\"pasto\":";
  estado_str += "\{\"state\":";
  estado_str += String(pasto);
  estado_str += "\}";
  estado_str += ",\"macetas\":";
  estado_str += "\{\"state\":";
  estado_str += String(macetas);
  estado_str += "\}";
  estado_str += "\}";
  server.send(200, "text/plain", estado_str);
  
}

