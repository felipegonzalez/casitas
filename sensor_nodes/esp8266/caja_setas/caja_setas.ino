#include <DHT.h>
#include <DHT_U.h>

#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>




const char* ssid     = "COM-818";
const char* password = "valquiria";
ESP8266WebServer server(80);
String responseString="";    
IPAddress ip(192, 168, 100, 155);  
IPAddress gateway(192, 168, 100, 201);  
IPAddress subnet(255, 255, 255, 255); 

int pin_ventilador = 13; 
int pin_dht = 2;
int ventilador_state;
int tiempo_ventilador = 0;
long timer_ventilador = 0;
long time_read;
long actual;
DHT_Unified dht(pin_dht, DHT22);
sensors_event_t event;

float h= 0;
float t=0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  delay(100);
  // wait for serial monitor to open
  while(! Serial);
 
  // initialize dht22
  dht.begin();
  pinMode(pin_ventilador, OUTPUT);
  digitalWrite(pin_ventilador, LOW);
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
  server.on("/status", estado);
  server.on("/ventilador", ventilador);
  server.begin();
  time_read = 0;
}

void loop() {
  // put your main code here, to run repeatedly:
  server.handleClient();
  long now_time = millis();
  if(now_time - time_read > 3000){
      h = dht.humidity().getEvent(&event);
      h = event.relative_humidity;
      // Read temperature as Celsius (the default)
    dht.temperature().getEvent(&event);
    t = event.temperature;
    time_read = millis();
    Serial.println(h);
    Serial.println(t);
    ventilador_state = digitalRead(pin_ventilador);
    if(now_time - timer_ventilador > tiempo_ventilador){
      digitalWrite(pin_ventilador, LOW);
    }
  }
}
void estado(){
  int ventilador_state;
  ventilador_state = digitalRead(pin_ventilador);
  String estado_str = "\{";
  estado_str += "\"type\":\"status\",";
  estado_str += "\"values\":";
  estado_str += "\{";
  estado_str += "\"environment\":";
  estado_str += "\{";
  estado_str += "\"temperature\":";
  estado_str += String(t);
  estado_str += ",\"humidity\":";
  estado_str += String(h);
  estado_str += "\}";
  estado_str += ",\"ventilador\":";
  estado_str += "\{";
  estado_str += "\"status\":";
  estado_str += String(ventilador_state);
  estado_str += "\}";
  estado_str += "\}";
  estado_str += "\}";
  server.send(200, "text/plain", estado_str); 
}
void ventilador(){
  String comando_arg = server.arg("command");
  String tiempo_arg = server.arg("tiempo");
  if(tiempo_arg==""){
    tiempo_arg= "30";
  }
  if(comando_arg=="turn_on"){
    digitalWrite(pin_ventilador, HIGH);
    tiempo_ventilador = 60*tiempo_arg.toInt()*1000;
    timer_ventilador = millis();
  }
   if(comando_arg == "turn_off") {
    digitalWrite(pin_ventilador, LOW);
  }
  server.send(200, "text/plain", "Comando recibido"); 
  }



