 #define USB_CONTROL_PIN 5     // Digital pin 5 drives your relay/MOSFET
#define ON_TIME  (60UL * 60UL * 1000UL)   // 60 minutes
#define OFF_TIME (15UL * 60UL * 1000UL)   // 15 minutes

unsigned long timer = 0;
bool usbOn = true;

void setup() {
  pinMode(USB_CONTROL_PIN, OUTPUT);
  digitalWrite(USB_CONTROL_PIN, HIGH); // Start with USB (or LED) ON
  timer = millis();
}

void loop() {
  unsigned long now = millis();

  if (usbOn && now - timer >= ON_TIME) {
    digitalWrite(USB_CONTROL_PIN, LOW);   // Turn OFF
    usbOn = false;
    timer = now;
  }
  else if (!usbOn && now - timer >= OFF_TIME) {
    digitalWrite(USB_CONTROL_PIN, HIGH);  // Turn ON
    usbOn = true;
    timer = now;
  }
}
