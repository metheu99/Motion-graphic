"""Synthesized 30 s futuristic BGM, 120 BPM. Deterministic."""
import numpy as np, wave, sys
SR = 44100; DUR = 30.0; BPM = 120; beat = 60 / BPM
t = np.arange(int(SR * DUR)) / SR
out = np.zeros((len(t), 2))
rng = np.random.default_rng(7)

def env(n, a=0.005, d=0.3):
    x = np.arange(n) / SR
    return np.minimum(x / a, 1) * np.exp(-x / d)

def add(sig, start, gain=1.0, pan=0.0):
    i = int(start * SR); j = min(len(t), i + len(sig)); sig = sig[: j - i] * gain
    out[i:j, 0] += sig * (1 - pan) ; out[i:j, 1] += sig * (1 + pan)

# pad: Dm9 chord, slow swell, detuned saws (approx with sines + harmonics)
chords = [[146.83, 220.0, 261.63, 329.63], [116.54, 174.61, 233.08, 293.66],
          [130.81, 196.0, 261.63, 311.13], [110.0, 164.81, 220.0, 277.18]]
for k in range(8):
    st = k * 4 * beat * 1.0 * 1.0 * 1.0 * 1.0  # 2 s per chord? 4 beats = 2s
    st = k * 4 * beat * 2 / 2 * 1.875  # 3.75 s per chord -> 8 chords = 30 s
    n = int(3.9 * SR); x = np.arange(n) / SR
    sig = np.zeros(n)
    for f in chords[k % 4]:
        for det in (-0.6, 0.6):
            sig += np.sin(2 * np.pi * (f + det) * x) + 0.3 * np.sin(4 * np.pi * (f + det) * x)
    e = np.minimum(x / 1.2, 1) * np.minimum((3.9 - x) / 0.8, 1)
    add(sig * e, st, 0.018)

# kick + sub pulse from 4 s, drop at 15 s doubles energy
for b in range(int(DUR / beat)):
    s = b * beat
    if s < 3.75 or s > 27.5: continue
    n = int(0.35 * SR); x = np.arange(n) / SR
    f = 50 + 120 * np.exp(-x * 30)
    kick = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.002, 0.18)
    add(kick, s, 0.55 if s >= 15 else 0.35)
    # offbeat hat
    if s >= 7.5:
        hn = int(0.06 * SR); hat = rng.standard_normal(hn) * env(hn, 0.001, 0.015)
        hat = np.diff(np.concatenate([[0], hat]))
        add(hat, s + beat / 2, 0.25 if s >= 15 else 0.15, pan=0.3)
    # pulsing bass 16ths
    root = chords[int(s // 3.75) % 4][0] / 2
    for q in range(4):
        bn = int(beat / 4 * SR * 0.9); x = np.arange(bn) / SR
        bass = np.tanh(2.5 * np.sin(2 * np.pi * root * x)) * env(bn, 0.003, 0.07)
        add(bass, s + q * beat / 4, 0.12 if s >= 15 else 0.07)

# arp from 15 s
notes = [587.33, 880, 698.46, 1046.5, 880, 698.46]
for i in range(int((27.5 - 15) / (beat / 4))):
    s = 15 + i * beat / 4; f = notes[i % len(notes)]
    n = int(0.12 * SR); x = np.arange(n) / SR
    add(np.sign(np.sin(2 * np.pi * f * x)) * 0.5 * env(n, 0.002, 0.05), s, 0.035, pan=0.5 * np.sin(i))

# risers before 15 s and 27.5 s
for end, ln in ((15.0, 3.0), (27.5, 2.0)):
    n = int(ln * SR); x = np.arange(n) / SR
    noise = rng.standard_normal(n); sweep = np.sin(2 * np.pi * np.cumsum(200 + 1800 * (x / ln) ** 2) / SR)
    add((noise * 0.3 + sweep * 0.5) * (x / ln) ** 2, end - ln, 0.12)

# impacts
for s, g in ((0.0, 0.5), (15.0, 0.8), (27.5, 0.9)):
    n = int(2.5 * SR); x = np.arange(n) / SR
    f = 40 + 60 * np.exp(-x * 8)
    boom = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.002, 0.9) + rng.standard_normal(n) * env(n, 0.001, 0.08) * 0.4
    add(boom, s, g)

# final tail fade
fade = np.ones(len(t)); fi = int(28.8 * SR); fade[fi:] = np.linspace(1, 0, len(t) - fi)
out *= fade[:, None]
out /= np.max(np.abs(out)) * 1.12
pcm = (out * 32767).astype(np.int16)
with wave.open(sys.argv[1], "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print("ok")
