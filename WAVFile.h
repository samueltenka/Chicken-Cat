// WAVEFile.h
// Simple hacky reader that may read a wav file
// Written by Ian Ewell

#include <string>

class WAVFile
{
    public:
        struct RIFFHeader
        {
            char chunk_id[4]; // "RIFF"
            unsigned int chunk_size;
            char format[4];
        };
        RIFFHeader m_riff_header;

        struct WAVHeader
        {
            char sub_chunk_1_id[4]; // "fmt "
            unsigned int sub_chunk_1_size; // Should be 16
            unsigned short audio_format; // 1 is PCM
            unsigned short num_channels; // 1 is mono
            unsigned int sample_rate;
            unsigned int byte_rate;
            unsigned short block_align;
            unsigned short bits_per_sample; // 8 = 8 bits, 16 = 16 bits
        };
        WAVHeader m_wav_header;

        struct DATAHeader
        {
            char sub_chunk_2_id[4]; // "data"
            unsigned int sub_chunk_2_size;
        };
        DATAHeader m_data_header;

        union DATA
        {
            char *PCM8;
            short *PCM16;
            int *PCM32;
        };
        DATA m_data;

        WAVFile(const std::string file);
        ~WAVFile();
};
