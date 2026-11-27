# Original high-energy track for the Black Friday day reel (synthesised here, no third-party audio).
# Dark trap/phonk feel like the reference: 130 BPM, E minor, heavy distorted 808 + punchy kick,
# snare on 2 & 4, 16th hats with rolls, cowbell riff. Bar 1 (the calendar hook) is a build-up with
# an accelerating snare roll + riser; the beat drops on bar 2, exactly when "Multi Friday" lights up.
# Writes music.wav and mixes it with the (reduced) sfx.wav into audio.wav.
import json
import wave
import numpy as np

SR = 48000
BPM = 130
BEAT = 60 / BPM
BAR = 4 * BEAT
DROP = BAR                                       # 1.846 s
rng = np.random.default_rng(11)
cues = json.load(open("sfx-events.json"))
DUR = cues["duration"]
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


def hp(x, a=0.95):                                   # cheap high-pass: subtract a short moving average
    return x - np.convolve(x, np.ones(16) / 16, mode="same") * a


def midi(m):
    return 440 * 2 ** ((m - 69) / 12)


# ---------------------------------------------------------------- instruments
def kick():
    d = 0.32; t = ta(d)
    f = 48 + 160 * np.exp(-t / 0.03)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.13)
    click = rng.standard_normal(len(t)) * np.exp(-t / 0.002) * 0.4
    return np.tanh(2.2 * (body + click)) * 0.9


def b808(note, d, slide_from=None):
    t = ta(d)
    f0 = midi(note)
    f = np.full_like(t, f0)
    if slide_from is not None:
        f = f0 + (midi(slide_from) - f0) * np.exp(-t / 0.06)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR)
    env = np.clip(t / 0.004, 0, 1) * np.exp(-t / 0.55) * np.clip((d - t) / 0.03, 0, 1)
    return np.tanh(3.0 * s * env) * 0.8                 # saturation → audible on phone speakers


def snare():
    d = 0.28; t = ta(d)
    n = hp(rng.standard_normal(len(t))) * np.exp(-t / 0.07)
    tone = np.sin(2 * np.pi * 190 * t) * np.exp(-t / 0.04)
    return np.tanh(1.8 * (0.8 * n + 0.6 * tone)) * 0.7


def hat(d=0.04, dec=0.012):
    t = ta(d)
    return hp(hp(rng.standard_normal(len(t)))) * np.exp(-t / dec) * 0.5


def cowbell(note, d=0.18):
    t = ta(d)
    f = midi(note)
    sq = lambda fr: np.sign(np.sin(2 * np.pi * fr * t))
    s = (sq(f) + sq(f * 1.48)) * 0.5
    s = s - np.convolve(s, np.ones(40) / 40, mode="same")   # thin it out (band-pass-ish)
    return s * np.exp(-t / 0.06) * 0.5


def riser(d):
    t = ta(d)
    n = hp(rng.standard_normal(len(t))) * (t / d) ** 2.5
    sweep = np.sin(2 * np.pi * np.cumsum(200 * (8 ** (t / d))) / SR) * (t / d) ** 2
    return 0.35 * n + 0.15 * sweep


def boom(d=1.6):
    t = ta(d)
    f = 30 + 70 * np.exp(-t / 0.15)
    return np.tanh(2 * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.5)) * 0.9


# ---------------------------------------------------------------- arrangement
# bar 0: build (snare roll accelerating + riser), short gap, then DROP
add(riser(DROP), 0.0, 0.8)
roll = []
for k in range(4): roll.append(k * BEAT)                       # quarters
for k in range(4): roll.append(BAR / 2 + k * BEAT / 2 * 0.5)   # 8ths (first half of beat 3)
for k in range(8): roll.append(BAR * 0.625 + k * BEAT / 4 * 0.75)
for i, rt in enumerate(roll):
    if rt < DROP - 0.06:
        add(snare(), rt, 0.25 + 0.6 * rt / DROP)
add(boom(), DROP, 0.9)

# E minor riff for the 808 (eighths: note or None), 2-bar loop, MIDI numbers (E1 = 28)
BASS = [(0, 28, None), (3, 28, None), (6, 31, 28), (8, 28, None), (11, 26, None), (14, 23, 26)]
COW = [76, None, 79, 76, None, 74, 76, None, 79, None, 81, 79, 76, None, 74, None]   # 16ths, 1 bar
last_bar = int((DUR - DROP) / BAR) + 1
for b in range(last_bar):
    t0 = DROP + b * BAR
    outro = t0 > DUR - 2 * BAR                       # thin the arrangement on the closing card
    # drums
    for beat in range(4):
        bt = t0 + beat * BEAT
        if beat in (0, 2) or (beat == 1 and b % 2 == 1):
            add(kick(), bt, 0.75)
        if beat in (1, 3):
            add(snare(), bt, 0.9)
        for s16 in range(4):
            add(hat(), bt + s16 * BEAT / 4, 0.32 if s16 % 2 else 0.45, pan=0.2)
    add(kick(), t0 + 2.5 * BEAT, 0.7)
    if b % 2 == 1:                                    # hat triplet roll at the end of every 2nd bar
        for k in range(6):
            add(hat(0.03, 0.008), t0 + 3.5 * BEAT + k * BEAT / 12, 0.35, pan=-0.2)
    # 808
    for e8, note, slide in BASS:
        tt = t0 + (e8 % 8) * BEAT / 2 if (e8 // 8) == b % 2 else None
        if tt is not None:
            add(b808(note, BEAT * 1.4, slide), tt, 0.5)
    # cowbell riff (not on the outro)
    if not outro:
        for k, n in enumerate(COW):
            if n is not None:
                add(cowbell(n - (2 if b % 4 == 3 else 0)), t0 + k * BEAT / 4, 0.85, pan=0.15 * (1 if k % 2 else -1))

# fade the tail
fo = int(1.8 * SR)
mus[-fo:] *= np.linspace(1, 0, fo)[:, None] ** 1.3
mus = np.tanh(mus * 1.2)
mus /= np.abs(mus).max() + 1e-9


def write(path, x):
    with wave.open(path, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(x, -1, 1) * 32767).astype("<i2").tobytes())


write("music.wav", mus * 0.9)

# ---------------------------------------------------------------- mix with the reduced SFX
with wave.open("sfx.wav") as w:
    sfx = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").astype(float).reshape(-1, 2) / 32767
sfx = np.pad(sfx, ((0, max(0, N - len(sfx))), (0, 0)))[:N]
lvl = np.convolve(np.abs(sfx).max(axis=1), np.ones(int(0.1 * SR)) / int(0.1 * SR), mode="same")
duck = 1 - 0.3 * np.clip(lvl / 0.2, 0, 1)
MUSIC_GAIN = 0.85                                     # the track leads; effects only accent key moments
SFX_GAIN = 0.55
mix = SFX_GAIN * sfx + MUSIC_GAIN * mus * duck[:, None]
mix = np.tanh(mix * 1.1) / np.tanh(1.1)
mix *= 0.89 / (np.abs(mix).max() + 1e-9)
write("audio_raw.wav", mix)
import subprocess                                    # loudness-normalise for Instagram/TikTok (≈ -13 LUFS, -1.5 dBTP)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "audio_raw.wav", "-af", "loudnorm=I=-13:TP=-1.5:LRA=9", "-ar", "48000", "audio.wav"], check=True)
print(f"music.wav + audio.wav: {DUR}s at {BPM} BPM, drop at {DROP:.3f}s")
