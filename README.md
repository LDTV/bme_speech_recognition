# Speech recognition project for Biomedical Engineering

[Classical approach to speech recognition code here](https://github.com/LDTV/bme_speech_recognition/blob/master/classical_approach.ipynb)

The project uses:
* [DTW for python](https://github.com/pierre-rouanet/dtw)
* [SciPy](https://www.scipy.org/)
* [LibROSA](https://librosa.github.io/librosa/)

Envelope code based on:
* [Jarne, Cecilia. "Simple empirical algorithm to obtain signal envelope in three steps." arXiv preprint arXiv:1703.06812 (2017).](https://arxiv.org/pdf/1703.06812.pdf)

## Installation

Install conda, then run:
```
conda create -n bme_speech_recognition jupyter scipy librosa -c conda-forge
```
Activate the source, run:
```
python -m pip install dtw
```
and you are ready to run the project notebooks.
