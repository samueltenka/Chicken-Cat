// WAVEFile.cpp
// Simple hacky reader that may read a wav file
// Written by Ian Ewell

#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include "WAVFile.h"

WAVFile::WAVFile(const std::string file)
{
    m_data.PCM8 = nullptr;

    FILE *wav = fopen(file.c_str(), "rb");
    fread(&m_riff_header, 1, sizeof(RIFFHeader), wav);
    fread(&m_wav_header, 1, sizeof(WAVHeader), wav);
    fread(&m_data_header, 1, sizeof(DATAHeader), wav);

    if (m_riff_header.chunk_id[0] != 'R' ||
            m_riff_header.chunk_id[1] != 'I' ||
            m_riff_header.chunk_id[2] != 'F' ||
            m_riff_header.chunk_id[3] != 'F') {
        std::cout << "Error: Not a wav file\n";
    }

    m_data.PCM8 = new char[m_data_header.sub_chunk_2_size];
    fread(m_data.PCM8, 1, m_data_header.sub_chunk_2_size, wav);
    fclose(wav);
};

WAVFile::WAVFile(void *data, unsigned int length, unsigned short bits_per_sample)
{
    m_data.PCM8 = new char[length];
    memcpy(m_data.PCM8, data, length);

    // Construct headers
    m_riff_header.chunk_id[0] = 'R';
    m_riff_header.chunk_id[1] = 'I';
    m_riff_header.chunk_id[2] = 'F';
    m_riff_header.chunk_id[3] = 'F';
    m_riff_header.chunk_size = 36 + length;
    m_riff_header.format[0] = 'W';
    m_riff_header.format[1] = 'A';
    m_riff_header.format[2] = 'V';
    m_riff_header.format[3] = 'E';
    
    m_wav_header.sub_chunk_1_id[0] = 'f';
    m_wav_header.sub_chunk_1_id[1] = 'm';
    m_wav_header.sub_chunk_1_id[2] = 't';
    m_wav_header.sub_chunk_1_id[3] = ' ';
    m_wav_header.sub_chunk_1_size = 16;
    m_wav_header.audio_format = 1;
    m_wav_header.num_channels = 1;
    m_wav_header.sample_rate = 44100;
    m_wav_header.byte_rate = 44100 * bits_per_sample / 8;
    m_wav_header.block_align = bits_per_sample / 8;
    m_wav_header.bits_per_sample = bits_per_sample;

    m_data_header.sub_chunk_2_id[0] = 'd';
    m_data_header.sub_chunk_2_id[1] = 'a';
    m_data_header.sub_chunk_2_id[2] = 't';
    m_data_header.sub_chunk_2_id[3] = 'a';
    m_data_header.sub_chunk_2_size = length;
}

WAVFile::~WAVFile()
{
    if (m_data.PCM8 != nullptr) {
        delete[] m_data.PCM8;
    }
}

void WAVFile::writeToFile(const std::string file)
{
    FILE *wav = fopen(file.c_str(), "wb");
    fwrite(&m_riff_header, 1, sizeof(m_riff_header), wav);
    fwrite(&m_wav_header, 1, sizeof(m_wav_header), wav);
    fwrite(&m_data_header, 1, sizeof(m_data_header, wav), wav);
    fwrite(m_data.PCM8, 1, m_data_header.sub_chunk_2_size, wav);
    fclose(wav);
}
