// Test generate a sine wave
#include "WAVFile.h"
#include <math.h>

int main(int argc, char* argv[])
{
    int length = 44100 * 5;
    short sound_buffer[length];
    float incr = 0.f;
    for (int i = 0; i < length; i++) {
        sound_buffer[i] = (int)(sinf(incr)*(65536/2));
        incr += 0.1f;
    }

    WAVFile wav(sound_buffer, length*2, 16);
    wav.writeToFile("sin.wav");
}
