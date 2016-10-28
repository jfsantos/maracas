from fuhai import asl_meter
from scipy.io.wavfile import read as wavread
import numpy as np

def test_asl_meter():
    fs, x = wavread('tests/test.wav')
    assert np.isclose(asl_meter(x, fs), -25.904213588612738)

if __name__ == '__main__':
    test_asl_meter()

