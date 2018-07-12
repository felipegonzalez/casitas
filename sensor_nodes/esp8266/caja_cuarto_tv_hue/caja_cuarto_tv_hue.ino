#include <SimpleTimer.h>
#include <Wire.h>
#include <Adafruit_MCP9808.h>
#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>


Adafruit_MCP9808 tempsensor = Adafruit_MCP9808();

const char* ssid     = "Niebelheim5";
const char* password = "valquiria";
ESP8266WebServer server(80);
String responseString="";    
IPAddress ip(192, 168, 100, 157);  
IPAddress gateway(192, 168, 100, 201);  
IPAddress subnet(255, 255, 255, 0 ); 

#define pin_photo A0

int pin_switch = 12;
int pin_pir = 16;
int pin_ventilador = 14;

const char* host = "192.168.100.50";
const int port = 8090;

SimpleTimer timer_send;
SimpleTimer timer;

void setup() {
  Serial.begin(9600);
  pinMode(pin_switch, OUTPUT);
  digitalWrite(pin_switch, LOW);
  pinMode(pin_pir, INPUT);
  // check sensor
  if (!tempsensor.begin()) {
    Serial.println("Couldn't find MCP9808!");
  }
  // connect to wifi
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.mode(WIFI_STA);
  WiFi.config(ip, gateway, subnet); 
  delay(500);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");   
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP()); 

  //set timers
  timer_send.setInterval(10000, send_data);
  server.on("/switch", switch_a);
  server.on("/status", estado);
  server.begin();
}

void switch_a() {
  // receives light command
  String comando_arg = server.arg("command");
  if(comando_arg=="turn_on") {
    digitalWrite(pin_switch, HIGH);
  }
  if(comando_arg=="turn_off") {
    digitalWrite(pin_switch, LOW);
  }
  timer.setTimeout(200, estado);
  //String respuesta = "Comando recibido lampara";
  //server.send(200, "text/plain", respuesta);
}
void send_data(){
  Serial.println("Send data");
  int light_level = 0;
  float c_temp = tempsensor.readTempC();
  delay(5);
  light_level = analogRead(pin_photo);
  delay(5);
  light_level = analogRead(pin_photo);  
  WiFiClient client;
  if (!client.connect(host, port)) {
    Serial.println("connection failed");
    return;
  }
  // We now create a URI for the request
  String url_1 = "/send_event?event_type=temperature&value=";
  url_1 += String(c_temp);
  // This will send the request to the server
  client.print(String("GET ") + url_1 + " HTTP/1.1\r\n" +
               "Host: " + host + "\r\n" + 
               "Connection: close\r\n\r\n");
   if (!client.connect(host, port)) {
    Serial.println("connection failed");
    return;
  }            
  String url_2 = "/send_event?event_type=photo&value=";
  url_2 += String(light_level);               
  client.print(String("GET ") + url_2 + " HTTP/1.1\r\n" +
               "Host: " + host + "\r\n" + 
               "Connection: close\r\n\r\n");

}

void send_movement(){
  WiFiClient client;
  if (!client.connect(host, port)) {
    Serial.println("connection failed");
    return;
  }
  // We now create a URI for the request
  String url = "/send_event?event_type=motion&value=True";
  // This will send the request to the server
  client.print(String("GET ") + url + " HTTP/1.1\r\n" +
               "Host: " + host + "\r\n" + 
               "Connection: close\r\n\r\n");
            
}

void estado() {
  Serial.println("Status rquest");
  int switch_state = 0;
  switch_state = digitalRead(pin_switch);
  String estado_str = "\{";
  estado_str += "\"type\":\"status\",";
  estado_str += "\"values\":";
  estado_str += "\{";
  estado_str += "\"switch\":";
  estado_str += "\{\"state\":";
  estado_str += String(switch_state);
  estado_str += "\}\}\}";
  server.send(200, "text/plain", estado_str);
}

long last_motion = millis();
void loop() {
  server.handleClient();
  int movement_state = 0;
  int pir_state = 0;
  pir_state = digitalRead(pin_pir);
  if(pir_state == 1 && movement_state == 0){
    if((unsigned long)(millis() - last_motion ) > 6000){
      send_movement();
      //Serial.println("Movement");
      last_motion = millis();
    }
    movement_state = 1;
  } 
  if(pir_state == 0){
    //Serial.println("No movement");
    movement_state = 0;
  }
  timer_send.run();
}


