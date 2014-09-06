// Test read a wav file
#include "WAVFile.h"
#include <iostream>

int main(int argc, char* argv[])
{
    WAVFile wav("apple.wav");
    for (int i = 0; i <= wav.m_data_header.sub_chunk_2_size/2; i++) {
        std::cout << (float)wav.m_data.PCM16[i]/(float)(65536/2) << "\n";
    }
}
