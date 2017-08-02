#define relay_pin 7
#define ring_pin 6

int ring;
int push_delay = 500;

void setup() {
  pinMode(relay_pin, OUTPUT);
  pinMode(ring_pin, INPUT);
  digitalWrite(relay_pin, LOW);
  Serial.begin(9600);
}

void loop() {
  digitalWrite(relay_pin, LOW);
  ring = digitalRead(ring_pin);
  if(ring==1){
    enviar_ring();
  }
  if(Serial.available() > 0){
    char leer = Serial.read();
    if(leer=='g'){
      digitalWrite(relay_pin, HIGH);
      delay(push_delay);
      digitalWrite(relay_pin, LOW);
    }
    if(leer=='1'){
      push_delay = 500;
    }
    if(leer=='2'){
      push_delay = 1000;
    }
   }
}

void enviar_ring() {
  Serial.println("timbre,binary,1,1");
  delay(3000);
}


