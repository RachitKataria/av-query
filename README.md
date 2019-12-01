# av-query

***Notes for consistency:

• For each clip, compare A/V every 2 frames

• Sliding window step = 300 frames

• Make sure all step sizes are hyperparameters


***Audio:***
To try out various audio inputs, add your sample .wav to the `query` folder, then test it by modifying `fingerprint_wav.py` accordingly!

Example test with `harden.wav`:
`songs = djv.recognize(FileRecognizer, "query/harden.wav");`

