from maracas import asl_meter
from scipy.io.wavfile import read as wavread
import numpy as np

def test_asl_meter():
    fs, x = wavread('tests/sp10.wav')
    assert np.isclose(asl_meter(x, fs), -25.631646819880210)

if __name__ == '__main__':
    test_asl_meter()

