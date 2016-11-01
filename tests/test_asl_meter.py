from maracas import asl_meter
from maracas.utils import wavread

import numpy as np

def test_asl_meter():
    x, fs = wavread('tests/sp10.wav')
    assert np.isclose(asl_meter(x, fs), -25.631381743520010)

if __name__ == '__main__':
    test_asl_meter()

