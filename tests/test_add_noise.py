from fuhai import add_noise, asl_meter, rms_energy
from scipy.io.wavfile import read as wavread
import numpy as np

def test_add_noise_rms():
    fs, x = wavread('tests/sp10.wav')
    _, n = wavread('tests/ssn.wav')

    x = x / 2.0**15
    n = n / 2.0**15

    y, n_scaled = add_noise(x, n, fs, 5.0)
    snr = 20*np.log10(np.linalg.norm(x)/np.linalg.norm(n_scaled))

    assert np.isclose(snr, 5.0)


def test_add_noise_p56():
    fs, x = wavread('tests/sp10.wav')
    _, n = wavread('tests/ssn.wav')

    x = x / 2.0**15
    n = n / 2.0**15

    y, n_scaled = add_noise(x, n, fs, 5.0, speech_energy='P.56')
    snr = asl_meter(x, fs) - rms_energy(n_scaled)

    assert np.isclose(snr, 5.0)


if __name__ == '__main__':
    test_add_noise_rms()
    test_add_noise_p56()

