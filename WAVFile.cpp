// WAVEFile.cpp
// Simple hacky reader that may read a wav file
// Written by Ian Ewell

#include <stdio.h>
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
}

WAVFile::~WAVFile()
{
    if (m_data.PCM8 != nullptr) {
        delete[] m_data.PCM8;
    }
}
