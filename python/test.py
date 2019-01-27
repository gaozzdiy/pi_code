unsigned long startime;
int sampling=1;
unsigned long duration;
unsigned long lowpulseoccupancy=0;
unsigned long samplelasttime_ms=30*1000;
int pin=8;
float ratio=0.0;
float concentration=0.0;
const float pm25coef=0.00207916725464941;
unsigned long pm25val;


void setup()
{
  Serial.begin(9600);
  pinMode(pin,INPUT);
  startime=millis();
}

void loop()
{
  if(1==sampling)
  {
    duration=pulseIn(pin,LOW);
    lowpulseoccupancy=lowpulseoccupancy+duration;
    if(millis()-startime>samplelasttime_ms)
    {
      ratio=lowpulseoccupancy/(samplelasttime_ms*10.0);
      concentration=1.1*pow(ratio,3)-3.8*pow(ratio,2)+520*ratio+0.62;
      pm25val=pm25coef*concentration;
      
      Serial.print("ratio=");
      Serial.println(ratio);
      Serial.print("concentration=");
      Serial.println(concentration);
      Serial.print("PM2.5=");
      Serial.println(pm25val);
      
      startime=millis();
      lowpulseoccupancy=0;
    }
  }
}
