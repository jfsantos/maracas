from __future__ import print_function, division, absolute_import

import os, itertools
from tqdm import tqdm
from glob import glob
import numpy as np

from maracas.utils import wavread, wavwrite, recursive_glob
from maracas import add_noise, add_reverb

class Dataset(object):
    '''Defines a corrupted speech dataset. Contains information about speech
    material, additive and convolutive noise sources, and how to store output.
    '''

    def __init__(self, speech_energy='P.56'):
        self.speech = list()
        self.noise = dict()
        self.reverb = dict()
        self.speech_energy = speech_energy


    def add_speech_files(self, path, recursive=False):
        '''Adds speech files to the dataset. If the path is for a file, adds a single
        file. Otherwise, adds WAV files in the specified folder. If recursive=True,
        adds all WAV files in the path recursively.
        '''
        if os.path.isfile(path):
            self.speech.append(path)
        elif os.path.isdir(path):
            if recursive:
                files = recursive_glob(path, '*.wav') + recursive_glob(path, '*.WAV')
            else:
                files = glob(os.path.join(path, '*.wav')) + glob(os.path.join(path, '*.WAV'))
            self.speech.extend(files)
        else:
            raise ValueError('Path needs to point to an existing file/folder')


    def _add_distortion_files(self, path, distortion_dict, name=None):
        '''Adds noise files to the dataset. path can be either for a single file or
        for a folder. name will replace the file name as a key in the noise file dict.
        '''
        if os.path.isfile(path):
            if name is None:
                name = os.path.splitext(os.path.basename(path))[0]
            distortion_dict[name] = path
        elif os.path.isdir(path):
            files = glob(os.path.join(path, '*.wav')) + glob(os.path.join(path, '*.WAV'))

            if name is not None:
                if type(name) != list or type(name) != tuple:
                    raise ValueError('When path is a folder, name has to be a list or tuple with the same length as the number of distortion files in the folder.')
                elif len(name) != len(files):
                    raise ValueError('len(name) needs to be equal to len(files)')
            else:
                name = [os.path.splitext(os.path.basename(f))[0] for f in files]

            for n, f in zip(name, files):
                distortion_dict[n] = f
        else:
            raise ValueError('Path needs to point to an existing file/folder')


    def add_noise_files(self, path, name=None):
        self._add_distortion_files(path, self.noise, name=name)


    def add_reverb_files(self, path, name=None):
        self._add_distortion_files(path, self.reverb, name=name)


    def generate_condition(self, snrs, noise, output_dir, reverb=None, files_per_condition=None):
        if noise not in self.noise.keys():
            raise ValueError('noise not in dataset')

        if type(snrs) is not list:
            snrs = [snrs]

        n, nfs = wavread(self.noise[noise])

        if reverb is not None:
            r, rfs = wavread(self.reverb[reverb])
            condition_name = '{}_{}'.format(reverb, noise)
        else:
            condition_name = noise

        if not os.path.isdir(output_dir):
            os.mkdir(output_dir)

        # FIXME: avoid overwriting an existing folder?
        try:
            for snr in snrs:
                os.mkdir(os.path.join(output_dir, '{}_{}dB'.format(condition_name, snr)))
        except OSError:
            print('Condition folder already exists!')

        for snr in snrs:
            if files_per_condition is not None:
                speech_files = np.random.choice(self.speech, files_per_condition, replace=False).tolist()
            else:
                speech_files = self.speech

            for f in tqdm(speech_files, desc='{}dB'.format(snr)):
                x, fs = wavread(f)
                if fs != nfs:
                    raise ValueError('Speech file and noise file have different fs!')
                if reverb is not None:
                    if fs != rfs:
                        raise ValueError('Speech file and reverb file have different fs!')
                    x = add_reverb(x, r, fs, speech_energy=self.speech_energy)
                y = add_noise(x, n, fs, snr, speech_energy=self.speech_energy)[0]
                wavwrite(os.path.join(output_dir, '{}_{}dB'.format(condition_name, snr),
                    os.path.basename(f)), y, fs)


    def generate_dataset(self, snrs, output_dir, files_per_condition=None):
        if type(snrs) is not list:
            snrs = [snrs]

        if len(self.reverb) > 0:
            for reverb, noise in itertools.product(self.reverb.keys(), self.noise.keys()):
                self.generate_condition(snrs, noise, output_dir,
                        reverb=reverb,
                        files_per_condition=files_per_condition)
        else:
            for noise in self.noise.keys():
                self.generate_condition(snrs, noise, output_dir,
                    reverb=None,
                    files_per_condition=files_per_condition)




