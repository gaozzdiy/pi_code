#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <errno.h>
#include <string.h>
#include <time.h>
#include <wiringPi.h>
#include <lcd.h>

int xio;

void send_command(int comm)
{
        // Send bit7-4 firstly
        int buf;
        buf = comm & 0xF0;
        buf |= 0x04;               // RS = 0, RW = 0, EN = 1

        wiringPiI2CWrite(xio,buf);
        usleep(2000);
        buf &= 0xFB;               // Make EN = 0
        wiringPiI2CWrite(xio,buf);

        // Send bit3-0 secondly
        buf = (comm & 0x0F) << 4;
        buf |= 0x04;               // RS = 0, RW = 0, EN = 1
        wiringPiI2CWrite(xio,buf);
        usleep(2000);
        buf &= 0xFB;               // Make EN = 0
        wiringPiI2CWrite(xio,buf);
}


void send_data(data)
{
        // Send bit7-4 firstly
        int buf;
        buf = data & 0xF0;
        buf |= 0x05;//               # RS = 1, RW = 0, EN = 1
        wiringPiI2CWrite(xio,buf);
        usleep(2000);
        buf &= 0xFB;//               # Make EN = 0
        wiringPiI2CWrite(xio,buf);
        
        // Send bit3-0 secondly
        buf = (data & 0x0F) << 4;
        buf |= 0x05;//               # RS = 1, RW = 0, EN = 1
        wiringPiI2CWrite(xio,buf);
        usleep(2000);
        buf &= 0xFB;//               # Make EN = 0
        wiringPiI2CWrite(xio,buf);
}

void init_lcd(void)
{
                send_command(0x33);// # Must initialize to 8-line mode at first
                usleep(5000);
                send_command(0x32);// # Then initialize to 4-line mode
                usleep(5000);
                send_command(0x28);// # 2 Lines & 5*7 dots
                usleep(5000);
                send_command(0x0C);// # Enable display without cursor
                usleep(5000);
                send_command(0x01);// # Clear Screen
}
                
                
void print_lcd(int x, int y, char* str)
{
        int addr;
        
        if( x < 0)
                x = 0;
        if(x > 15)
                x = 15;
        if(y <0)
                y = 0;
        if(y > 1)
                y = 1;

        //# Move cursor
        addr = 0x80 + 0x40 * y + x;
        send_command(addr);
        
        while(*str)
                send_data(*str++);
}
                
int main (void)
{
  struct tm *t ;
  time_t tim ;

  char buf [32] ;
  
  printf ("Raspberry Pi LCD test program\n") ;

  xio = wiringPiI2CSetup (0x3F);
  if (xio < 0){
    fprintf (stderr, "xio: Unable to initialise I2C: %s\n", strerror (errno));
    return 1;
  }
  wiringPiI2CWriteReg8 (xio, 0x0a, 0x84) ;  // IOCON - set BANK bit
  wiringPiI2CWriteReg8 (xio, 0x05, 0x84) ;  // IOCON - set ODR in bank 0
  wiringPiI2CWriteReg8 (xio, 0x00, 0x00) ;  // Port A -> Outputs

  init_lcd();
        

  while(1)
        {
    tim = time (NULL) ;
    t = localtime (&tim) ;
    sprintf (buf, "    %02d:%02d:%02d    ", t->tm_hour, t->tm_min, t->tm_sec) ;

        print_lcd(0, 0, "testing");
    print_lcd (0, 1, buf) ;
        }
        
  return 0;
}

