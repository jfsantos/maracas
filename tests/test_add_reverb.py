from maracas import add_reverb, asl_meter, rms_energy
from maracas.utils import wavread

import numpy as np

def test_add_reverb():
    x, fs = wavread('tests/sp10.wav')
    r, _ = wavread('tests/rir.wav')

    y = add_reverb(x, r, fs, speech_energy='P.56')

    y_ref, _ = wavread('tests/sp10_reverb_ref.wav')

    assert np.allclose(y, y_ref, atol=2e-3)


if __name__ == '__main__':
    test_add_reverb()

