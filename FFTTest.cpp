#include <fftw3.h>
#include <iostream>
#include <math.h>
#include "WAVFile.h"
#include <fann.h>
#include <fann_cpp.h>
#include <vector>

std::vector<float*> input_training;
std::vector<float*> output_training;

const int samples_per_segment = 1000;

void add_training_sound(WAVFile &input, WAVFile &output)
{
    double *in;
    fftw_complex *out;
    fftw_plan plan;

    int length = input.m_data_header.sub_chunk_2_size;
    in = (double*)fftw_malloc(sizeof(double)*samples_per_segment);
    out = (fftw_complex*)fftw_malloc(sizeof(fftw_complex)*samples_per_segment/2+1);

    plan = fftw_plan_dft_r2c_1d(samples_per_segment, in, out, FFTW_ESTIMATE);

    int sample_number = 0;
    while (sample_number < length/2) {
        for (int i = 0; i < samples_per_segment; i++) {
            if (sample_number+i >= length/2) {
                break;
            }
            in[i] = (double)input.m_data.PCM16[sample_number+i]/((double)(65536/2));
        }
        sample_number += samples_per_segment;

        fftw_execute(plan);

        float *input_train = (float*)malloc((sizeof(float)*samples_per_segment/2+1)*2);
        for (int i = 0; i < samples_per_segment/2+1; i++) {
            input_train[i] = out[0][i];
            input_train[i+samples_per_segment/2+1] = out[1][i];
        }
        input_training.push_back(input_train);
    }

    sample_number = 0;
    while (sample_number < length/2) {
        for (int i = 0; i < samples_per_segment; i++) {
            if (sample_number+i >= length/2) {
                break;
            }
            in[i] = (double)output.m_data.PCM16[sample_number+i]/((double)(65536/2));
        }
        sample_number += samples_per_segment;

        fftw_execute(plan);

        float *output_train = (float*)malloc((sizeof(float)*samples_per_segment/2+1)*2);
        for (int i = 0; i < samples_per_segment/2+1; i++) {
            output_train[i] = out[0][i];
            output_train[i+samples_per_segment/2+1] = out[1][i];
        }
        output_training.push_back(output_train);
    } fftw_destroy_plan(plan);
}
void translate_wav(WAVFile input)
{
    double *in;
    fftw_complex *out;
    fftw_complex *in_back;
    double *out_back;
    fftw_plan plan;
    fftw_plan plan_back;

    int length = input.m_data_header.sub_chunk_2_size;
    in = (double*)fftw_malloc(sizeof(double)*samples_per_segment);
    out = (fftw_complex*)fftw_malloc(sizeof(fftw_complex)*samples_per_segment/2+1);
    in_back = (fftw_complex*)fftw_malloc(sizeof(fftw_complex)*samples_per_segment/2+1);
    out_back = (double*)fftw_malloc(sizeof(double)*samples_per_segment+2);

    plan = fftw_plan_dft_r2c_1d(samples_per_segment, in, out, FFTW_ESTIMATE);
    plan_back = fftw_plan_dft_c2r_1d(samples_per_segment+1, in_back, out_back, FFTW_ESTIMATE);

    FANN::neural_net net;
    net.create_from_file("net.net");
    
    short outbuffer[(((length/2)/samples_per_segment)+1)*samples_per_segment];

    int sample_number = 0;
    while (sample_number < length/2) {
        for (int i = 0; i < samples_per_segment; i++) {
            if (sample_number+i >= length/2) {
                break;
            }
            in[i] = (double)input.m_data.PCM16[sample_number+i]/((double)(65536/2));
        }

        fftw_execute(plan);

        float *input_train = (float*)malloc(sizeof(float)*samples_per_segment/2+1);
        for (int i = 0; i < samples_per_segment/2+1; i++) {
            input_train[i] = out[0][i];
        }

        // Use neural net to translate voice
        std::cout << "outputting data\n";
        float *out_net = net.run(input_train);

        for (int i = 0; i < samples_per_segment/2+1; i++) {
            in_back[0][i] = out_net[i];
            in_back[1][i] = out_net[i+samples_per_segment/2+1];
            //in_back[0][i] = out[0][i];
            //in_back[1][i] = out[1][i];
        }

        memset(out_back, 0, sizeof(double)*samples_per_segment);
        fftw_execute(plan_back);

        for (int i = 0; i < samples_per_segment; i++) {
            outbuffer[sample_number+i] = ((out_back[i])/samples_per_segment)*(65536.f/2.f);
            //std::cout << ((out_back[i])/(float)samples_per_segment)*(65536.f/2.f)<<"\n";//outbuffer[sample_number+i] << "\n";
        }

        sample_number += samples_per_segment;
    }
    WAVFile output_wav(outbuffer, length, 16);
    output_wav.writeToFile("output.wav");
}

/*int main(int argc, char *argv[])
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
}*/

int main(int argc, char *argv[])
{
    if (argv[1][0] == 'r') {
        WAVFile inp(argv[2]);
        translate_wav(inp);
        return 0;
    }
    if (argc == 1 || argc % 2 != 1) {
        std::cout << "bad number of training examples\n";
        return -1;
    }

    int to_open = (argc - 1)/2;
    for (int i = 0; i < to_open; i++) {
        WAVFile inp(argv[2*i+1]);
        WAVFile out(argv[2*i+2]);
        add_training_sound(inp, out);
    }

    float *train_in[input_training.size()];
    float *train_out[output_training.size()];
    for (int i = 0; i < input_training.size(); i++) {
        train_in[i] = input_training[i];
        train_out[i] = output_training[i];
    }
    FANN::training_data training;
    training.set_train_data(input_training.size(), (samples_per_segment/2+1)*2,
            train_in, (samples_per_segment/2+1)*2, train_out);
    FANN::neural_net net; 
    const unsigned int layers[] = {(samples_per_segment/2+1)*2, (samples_per_segment/2+1)*2, (samples_per_segment/2+1)*2};
    net.create_standard_array(3, (unsigned int*)layers);
    net.set_activation_function_output(FANN::LINEAR);
    //net.set_activation_function_hidden(FANN::LINEAR);
    net.set_learning_rate(1.2f);
    net.train_on_data(training, 50000, 1, 3.0f);

    net.save("net.net");
}


