import numpy as np
import pandas as pd
import random
import itertools
import librosa
import IPython.display as ipd
import matplotlib.pyplot as plt
import soundfile as sf
import os
import argparse

sound_path = './bg_noise/'

def sample(path):
    files = []
    for dirpath, __, filenames in os.walk(path):
        for file in filenames:
            files.append(dirpath + '/' + file)
    return np.random.choice(files, 1)[0]

def circle(data, N):
    n = len(data)
    if n >= N:
        return data[:N]
    return np.pad(data, (0, N - n), 'wrap')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parameters.')
    parser.add_argument('input', type=str, help='path to directory with input sounds')
    parser.add_argument('noise', type=str, help='path to directory with noises')
    parser.add_argument('power', type=float, help="power of noise, [0.01 : 0.2]")

    args = parser.parse_args()
    assert args.power >= 0.01, "argument \'power\' should be in range [0.01 : 0.2]"
    assert args.power <= 0.2, "argument \'power\' should be in range [0.01 : 0.2]"


    inputpath = args.input
    if inputpath[-1] == '/' or inputpath[-1] == '\'':
        inputpath = inputpath[:-1]
    outputpath = inputpath + '_noised'

    noisepath = sample(args.noise)
    noise_data, _ = sf.read(noisepath)

    for dirpath, dirnames, filenames in os.walk(inputpath):
        structure = outputpath + dirpath[len(inputpath):]
        if not os.path.isdir(structure):
            os.mkdir(structure, 0o777)
        for file in filenames:
            if file[-3:] != 'wav' and file[-4:] != 'flac':
                continue
            inputfile = dirpath + '/' + file
            outputfile = structure + '/' + file

            data, samplerate = sf.read(inputfile)

            noise_to_add = circle(noise_data.copy(), len(data))
            data += noise_to_add * args.power
            sf.write(outputfile, data, samplerate)