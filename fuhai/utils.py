from __future__ import print_function, division, absolute_import

import numpy as np
import scipy.io.wavfile

import fnmatch, os

def wavread(filename):
    fs, x = scipy.io.wavfile.read(filename)
    if np.issubdtype(x.dtype, np.integer):
        x = x / np.iinfo(x.dtype).max
    return x, fs


def wavwrite(filename, s, fs):
    if s.dtype != np.int16:
        s = np.array(s * 2**15, dtype=np.int16)
    scipy.io.wavfile.write(filename, fs, s)


def recursive_glob(treeroot, pattern):
    results = []
    for base, dirs, files in os.walk(treeroot):
        goodfiles = fnmatch.filter(files, pattern)
        results.extend(os.path.join(base, f) for f in goodfiles)
    return results


