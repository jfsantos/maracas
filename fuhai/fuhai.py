import numpy as np
from scipy.signal import lfilter

def asl_meter(x, fs, nbits=16):
    '''Measure the Active Speech Level (ASR) of x following ITU-T P.56.
    If x is integer, it will be scaled to (-1, 1) according to nbits.
    '''

    if np.issubdtype(x.dtype, np.integer):
        x = x / 2**(nbits-1)

    # Constants
    MIN_LOG_OFFSET = 1e-20
    T = 0.03                # Time constant of smoothing in seconds
    g = np.exp(-1/(T*fs))
    H = 0.20                # Time of handover in seconds
    I = int(np.ceil(H*fs))
    M = 15.9                # Margin between threshold and ASL in dB

    a = np.zeros(nbits-1)                       # Activity count
    c = 0.5**np.arange(nbits-1, 0, step=-1)     # Threshold level
    h = np.ones(nbits)*I                        # Hangover count
    s = 0
    sq = 0
    p = 0
    q = 0
    asl = -100

    L = len(x)
    s = sum(abs(x))
    sq = sum(x**2)
    dclevel = s/np.arange(1, L+1)
    lond_term_level = 10*np.log10(sq/np.arange(1, L+1) + MIN_LOG_OFFSET)
    c_dB = 20*np.log10(c)

    for i in range(L):
        p = g * p + (1-g) * abs(x[i])
        q = g * q + (1-g) * p

        for j in range(nbits-1):
            if q >= c[j]:
                a[j] += 1
                h[j] = 0
            elif h[j] < I:
                a[j] += 1;
                h[j] += 1

    a_dB = -100 * np.ones(nbits-1)

    for i in range(nbits-1):
        if a[i] != 0:
            a_dB[i] = 10*np.log10(sq/a[i])

    delta = a_dB - c_dB
    idx = np.where(delta <= M)[0]

    if len(idx) != 0:
        idx = idx[0]
        if idx > 1:
            asl = bin_interp(a_dB[idx], a_dB[idx-1], c_dB[idx], c_dB[idx-1], M)
        else:
            asl = a_dB[idx]

    return asl

def bin_interp(upcount, lwcount, upthr, lwthr, margin, tol=0.1):
    n_iter = 1
    if abs(upcount - upthr - margin) < tol:
        midcount = upcount
    elif abs(lwcount - lwthr - margin) < tol:
        midcount = lwcount
    else:
        midcount = (upcount + lwcount)/2
        midthr = (upthr + lwthr)/2
        diff = midcount - midthr - margin
        while abs(diff) > tol:
            n_iter += 1
            if n_iter > 20:
                tol *= 1.1
            if diff > tol:
                midcount = (upcount + midcount)/2
                midthr = (upthr + midthr)/2
            elif diff < -tol:
                midcount = (lwcount + midcount)/2
                midthr = (lwthr + midthr)/2
            diff = midcount - midthr - margin
    return midcount

