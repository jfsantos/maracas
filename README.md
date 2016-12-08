[![Build Status](https://travis-ci.org/jfsantos/maracas.svg?branch=master)](https://travis-ci.org/jfsantos/maracas)

maracas is a library for corrupting audio files with additive and convolutive
noise. Its objective is to simplify reproducible dataset generation for speech processing (mainly enhancement and ASR).

The usage is really simple and based on the `maracas.dataset.Dataset` class. Here is a short example:

```python
from maracas.dataset import Dataset
import numpy as np

# Make sure this is reproducible
np.random.seed(42)

d = Dataset()

# All files can be added one by one or by folder. Adding a folder will add
# all speech files inside that folder recursively if recursive=True.
d.add_speech_files('/home/jfsantos/data/speech_files/', recursive=True)

# When adding noises, you can give a "nickname" to each noise file. If you do not
# give it a name, the name will be the file name without the '.wav' extension
d.add_noise_files('/home/jfsantos/data/multichannel_noises/restaurant_ch01.wav', name='restaurant')
d.add_noise_files('/home/jfsantos/data/multichannel_noises/cafeteria_ch01.wav', name='cafeteria')
d.add_noise_files('/home/jfsantos/data/multichannel_noises/traffic_ch01.wav', name='traffic')

# Adding reverb files works like adding noise files
d.add_reverb_files('/home/jfsantos/data/RIR_sim/rir_0.2_1.wav')
d.add_reverb_files('/home/jfsantos/data/RIR_sim/rir_0.8_1.wav')

# When generating a dataset, you can choose which SNRs will be used and how many
# files per condition you want to be generated. 
d.generate_dataset([-6, -3, 0, 3, 6], '/tmp/noise_plus_reverb_dataset', files_per_condition=5)
```
