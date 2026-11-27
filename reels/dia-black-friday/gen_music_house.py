# Original upbeat electronic track (house / commercial EDM) for the Black Friday day reel.
# Synthesised here, no third-party audio. 130 BPM (same grid as the video cuts), major key
# (C – G – Am – F), four-on-the-floor kick, off-beat open hats, claps on 2 & 4, off-beat bass,
# bright saw chords with sidechain "pumping" and a happy pluck melody.
# Bar 1 (calendar hook) is a build-up (riser + snare roll); the beat drops on bar 2 with the slogan.
# Writes music.wav and mixes it with the reduced sfx.wav into audio.wav (≈ -13 LUFS).
import json
import subprocess
import wave
import numpy as np

SR = 48000
BPM = 130
BEAT = 60 / BPM
BAR = 4 * BEAT
DROP = BAR
rng = np.random.default_rng(5)
DUR = json.load(open("sfx-events.json"))["duration"]
N = int(DUR * SR)
mus = np.zeros((N, 2))


def ta(d):
    return np.arange(int(d * SR)) / SR


def add(sig, t0, g=1.0, pan=0.0):
    i = int(round(t0 * SR))
    if i >= N:
        return
    sig = sig[: N - i] * g
    mus[i:i + len(sig), 0] += sig * np.sqrt((1 - pan) / 2)
    mus[i:i + len(sig), 1] += sig * np.sqrt((1 + pan) / 2)


def hp(x, k=16):
    return x - np.convolve(x, np.ones(k) / k, mode="same")


def lp(x, k=6):
    return np.convolve(x, np.ones(k) / k, mode="same")


def midi(m):
    return 440 * 2 ** ((m - 69) / 12)


def saw(f, t, detune=0.0):
    ph = (f * (1 + detune) * t) % 1.0
    return 2 * ph - 1


# ---------------------------------------------------------------- instruments
def kick():
    d = 0.28; t = ta(d)
    f = 52 + 140 * np.exp(-t / 0.025)
    return np.tanh(1.8 * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.12)) * 0.9


def clap():
    d = 0.22; t = ta(d)
    env = np.exp(-t / 0.06)
    for off in (0.0, 0.011, 0.022):              # three quick bursts = clap
        env += 0.6 * np.exp(-np.maximum(t - off, 0) / 0.006) * (t >= off)
    return hp(rng.standard_normal(len(t)), 8) * env * 0.35


def hat(open_=False):
    d = 0.16 if open_ else 0.04; t = ta(d)
    return hp(hp(rng.standard_normal(len(t)), 4), 4) * np.exp(-t / (0.05 if open_ else 0.01)) * 0.4


def supersaw(notes, d):
    t = ta(d)
    s = sum(saw(midi(n), t, dt) for n in notes for dt in (-0.006, 0.0, 0.006))
    s = lp(s, 2) / (len(notes) * 3)
    env = np.clip(t / 0.01, 0, 1) * np.clip((d - t) / 0.05, 0, 1)
    return s * env


def bass(note, d):
    t = ta(d)
    s = lp(saw(midi(note), t), 10) + 0.6 * np.sin(2 * np.pi * midi(note) * t)
    return s * np.clip(t / 0.005, 0, 1) * np.exp(-t / 0.18) * 0.7


def pluck(note, d=0.22):
    t = ta(d)
    s = np.sin(2 * np.pi * midi(note) * t) + 0.4 * np.sin(4 * np.pi * midi(note) * t) + 0.45 * saw(midi(note), t)
    return s * np.exp(-t / 0.09) * 0.5


def riser(d):
    t = ta(d)
    return 0.3 * hp(rng.standard_normal(len(t)), 6) * (t / d) ** 2.5 + 0.12 * supersaw([60, 64, 67], d) * (t / d) ** 2


def crash(d=1.4):
    t = ta(d)
    return hp(rng.standard_normal(len(t)), 3) * np.exp(-t / 0.5) * 0.25


# ---------------------------------------------------------------- arrangement
PROG = [([60, 64, 67], 36), ([59, 62, 67], 43), ([57, 60, 64], 45), ([57, 60, 65], 41)]   # C G Am F (+ bass roots)
MEL = [76, None, 79, 76, 74, None, 72, 74, 76, None, 79, None, 81, 79, 76, None]           # 16ths, 1 bar, C major

# build: riser + snare roll (claps) accelerating, then drop
add(riser(DROP), 0.0, 0.9)
for k, rt in enumerate([0, 1, 2, 3, 4, 4.5, 5, 5.5, 6, 6.25, 6.5, 6.75, 7, 7.125, 7.25, 7.375, 7.5, 7.625, 7.75]):
    tt = rt * BEAT / 2
    if tt < DROP - 0.05:
        add(clap(), tt, 0.2 + 0.6 * tt / DROP)
add(crash(), DROP, 0.8)

pump_env = np.ones(N)                               # sidechain envelope driven by the kick
b = 0
t0 = DROP
while t0 < DUR:
    chord, root = PROG[b % 4]
    outro = t0 > DUR - 2 * BAR
    for beat in range(4):
        bt = t0 + beat * BEAT
        add(kick(), bt, 0.85)
        i = int(bt * SR)
        k = np.arange(min(int(0.3 * SR), N - i)) / SR
        pump_env[i:i + len(k)] = np.minimum(pump_env[i:i + len(k)], 1 - 0.75 * np.exp(-k / 0.11))
        add(hat(open_=True), bt + BEAT / 2, 1.1, pan=0.25)
        add(hat(), bt + BEAT / 4, 0.5, pan=-0.25)
        add(hat(), bt + 3 * BEAT / 4, 0.5, pan=-0.25)
        if beat in (1, 3):
            add(clap(), bt, 0.9)
        add(bass(root, BEAT / 2 * 0.9), bt + BEAT / 2, 0.8)           # off-beat house bass
    if not outro:
        for k, n in enumerate(MEL):
            if n is not None:
                add(pluck(n + (0 if b % 2 == 0 else (-3 if k > 11 else 0))), t0 + k * BEAT / 4, 0.45, pan=0.2 * (1 if k % 2 else -1))
    t0 += BAR
    b += 1

# chords as a separate pumped layer
pad = np.zeros(N)
b, t0 = 0, DROP
while t0 < DUR:
    chord, _ = PROG[b % 4]
    s = supersaw([n + 12 for n in chord] + [chord[0]], BAR)
    i = int(t0 * SR); s = s[: N - i]
    pad[i:i + len(s)] += s
    t0 += BAR; b += 1
pad *= pump_env * 0.55
mus[:, 0] += pad * 0.95; mus[:, 1] += np.roll(pad, int(0.012 * SR)) * 0.95   # tiny delay → wide stereo

fo = int(1.8 * SR)
mus[-fo:] *= np.linspace(1, 0, fo)[:, None] ** 1.3
mus = np.tanh(mus * 1.1)
mus /= np.abs(mus).max() + 1e-9


def write(path, x):
    with wave.open(path, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(x, -1, 1) * 32767).astype("<i2").tobytes())


write("music.wav", mus * 0.9)

with wave.open("sfx.wav") as w:
    sfx = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").astype(float).reshape(-1, 2) / 32767
sfx = np.pad(sfx, ((0, max(0, N - len(sfx))), (0, 0)))[:N]
lvl = np.convolve(np.abs(sfx).max(axis=1), np.ones(int(0.1 * SR)) / int(0.1 * SR), mode="same")
duck = 1 - 0.3 * np.clip(lvl / 0.2, 0, 1)
mix = 0.55 * sfx + 0.85 * mus * duck[:, None]
mix = np.tanh(mix * 1.1) / np.tanh(1.1)
mix *= 0.89 / (np.abs(mix).max() + 1e-9)
write("audio_raw.wav", mix)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "audio_raw.wav", "-af", "loudnorm=I=-13:TP=-1.5:LRA=9", "-ar", "48000", "audio.wav"], check=True)
print(f"music.wav + audio.wav: {DUR}s, house at {BPM} BPM, drop at {DROP:.3f}s")
