#include <fftw3.h>
#include <iostream>
#include <math.h>
#include "WAVFile.h"

const int samples_per_segment = 1000;

int main(int argc, char *argv[])
{
    double *in;
    fftw_complex *out;
    fftw_plan plan;

    if (argc != 2) {
        return -1;
    }

    WAVFile wave(argv[1]);
    int length = wave.m_data_header.sub_chunk_2_size;
    in = (double*)fftw_malloc(sizeof(double)*samples_per_segment);
    out = (fftw_complex*)fftw_malloc(sizeof(fftw_complex)*samples_per_segment/2+1);

    plan = fftw_plan_dft_r2c_1d(samples_per_segment, in, out, FFTW_ESTIMATE);

    int sample_number = 0;
    while (sample_number < length/2) {

        for (int i = 0; i < samples_per_segment; i++) {
            if (sample_number+i >= length/2) {
                break;
            }
            in[i] = (double)wave.m_data.PCM16[sample_number+i]/((double)(65536/2));
        }
        sample_number += samples_per_segment;

        fftw_execute(plan);

        for (int i = 0; i < length/4+1; i++) {
            //std::cout << out[i][0] << " " << out[i][1] << "\n";
        }
    
        // correction
        int m = 0;
        double correction = (double)44100/(double)(length/2);
        for (int i = 0; i < (samples_per_segment/2)+1; i++) {
            double absval = sqrt(out[i][0] * out[i][0]);
            double cc = (double)m * correction;
            std::cout << cc << "," << absval << "\n";
            m++;
        }
        std::cout << "\n";
    }
    
   fftw_destroy_plan(plan);
}
