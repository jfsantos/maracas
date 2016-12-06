from maracas import add_noise, asl_meter, rms_energy
from maracas.utils import wavread

import numpy as np

def test_add_noise_rms():
    x, fs = wavread('tests/sp10.wav')
    n, _ = wavread('tests/ssn.wav')

    y, n_scaled = add_noise(x, n, fs, 5.0)
    snr = rms_energy(x) - rms_energy(n_scaled)

    assert np.isclose(snr, 5.0)


def test_add_noise_p56():
    x, fs = wavread('tests/sp10.wav')
    n, _ = wavread('tests/ssn.wav')

    y, n_scaled = add_noise(x, n, fs, 5.0, speech_energy='P.56')
    snr = asl_meter(x, fs) - rms_energy(n_scaled)

    assert np.isclose(snr, 5.0)


if __name__ == '__main__':
    test_add_noise_rms()
    test_add_noise_p56()

