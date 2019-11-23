#include <wiringPi.h>
#include <stdio.h>
#include <stdlib.h>

const int PWM_pin = 18;

int main (void)
{
    int intensity;
    if (wiringPiSetup() == -1)
    {
        exit(1);
    }
    pinMode(PWM_pin, PWM_OUTPUT);

    for (int i = 0; i < 5; i++)
    {
        for(intensity = 0; intensity < 1024; intensity++)
        {
            pwmWrite(PWM_pin, intensity);
            delay(1);
        }
        delay(1);
        for (intensity = 1023; intensity < 0; intensity--)
        {
            pwmWrite(PWM_pin, intensity);
            delay(1);
        }
        delay(1);
    }
}