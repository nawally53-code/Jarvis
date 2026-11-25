# Original background track for the reel (synthesised here, no third-party audio).
# Upbeat electronic, 120 BPM, A minor (Am–F–C–G). The beat "drops" at the first scene change
# (2.6 s) so every later scene change (6.6 s, 10.6 s) lands on a downbeat; the hook gets a riser.
# Writes music.wav, then mixes it quietly under sfx.wav (with ducking) into audio.wav.
import json
import wave
import numpy as np

SR = 48000
BPM = 120
BEAT = 60 / BPM
DROP = 2.6                     # first downbeat of the groove
rng = np.random.default_rng(3)
cues = json.load(open("sfx-events.json"))
DUR = cues["duration"]
N = int(DUR * SR)
music = np.zeros((N, 2))


def t_axis(d):
    return np.arange(int(d * SR)) / SR


def add(sig, t0, gain=1.0, pan=0.0):
    i = int(t0 * SR)
    if i >= N or i + len(sig) <= 0:
        return
    if i < 0:
        sig, i = sig[-i:], 0
    sig = sig[: N - i] * gain
    music[i:i + len(sig), 0] += sig * np.sqrt((1 - pan) / 2)
    music[i:i + len(sig), 1] += sig * np.sqrt((1 + pan) / 2)


def noise(d):
    return rng.standard_normal(int(d * SR))


def hp(x, k=0.97):               # crude one-pole high-pass
    y = np.empty_like(x); prev_x = prev_y = 0.0
    for i, v in enumerate(x):
        prev_y = k * (prev_y + v - prev_x); prev_x = v; y[i] = prev_y
    return y


def kick():
    d = 0.35; t = t_axis(d)
    f = 45 + 110 * np.exp(-t / 0.035)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.16)


def hat(open_=False):
    d = 0.18 if open_ else 0.05; t = t_axis(d)
    return hp(noise(d)) * np.exp(-t / (0.06 if open_ else 0.012))


def clap():
    d = 0.25; t = t_axis(d)
    env = np.exp(-t / 0.07) * (1 + 0.6 * (np.sin(2 * np.pi * 90 * t) > 0) * (t < 0.03))
    return hp(noise(d), 0.9) * env


def saw(f, d):
    t = t_axis(d)
    return sum(np.sin(2 * np.pi * f * k * t) / k for k in range(1, 9)) * 0.6


def note(f, d, attack=0.005, rel=0.08, kind="saw"):
    t = t_axis(d)
    w = saw(f, d) if kind == "saw" else np.sin(2 * np.pi * f * t) + 0.3 * np.sin(4 * np.pi * f * t)
    env = np.clip(t / attack, 0, 1) * np.clip((d - t) / rel, 0, 1)
    return w * env


def midi(m):
    return 440 * 2 ** ((m - 69) / 12)


# chords (root, third, fifth as MIDI), one per bar (2 s)
PROG = [(57, 60, 64), (53, 57, 60), (48, 52, 55), (55, 59, 62)]   # Am F C G
BAR = 4 * BEAT

# ---- hook: soft pad + rising noise sweep into the drop
add(sum(note(midi(m + 12), DROP, attack=0.8, rel=0.3) for m in PROG[0]) * 0.05, 0.0, pan=0.0)
t = t_axis(DROP)
riser = hp(noise(DROP), 0.95) * (t / DROP) ** 3
add(riser * 0.10, 0.0)

# ---- groove from the drop to the end
end = DUR - 0.2
bar = 0
tb = DROP
while tb < end:
    chord = PROG[bar % 4]
    # pad (stereo spread), bass on 8ths, arpeggio on 16ths
    for j, m in enumerate(chord):
        add(note(midi(m + 12), BAR, attack=0.05, rel=0.25) * 0.035, tb, pan=(j - 1) * 0.5)
    for k in range(8):
        bt = tb + k * BEAT / 2
        add(note(midi(chord[0] - 12), BEAT / 2 * 0.9, rel=0.03, kind="sine") * 0.32, bt)
    arp = [chord[0] + 24, chord[1] + 24, chord[2] + 24, chord[1] + 24]
    for k in range(16):
        add(note(midi(arp[k % 4]), BEAT / 4 * 0.8, rel=0.04, kind="sine") * 0.05, tb + k * BEAT / 4, pan=0.35 * (1 if k % 2 else -1))
    # drums
    for b in range(4):
        bt = tb + b * BEAT
        add(kick() * 0.55, bt)
        if b in (1, 3):
            add(clap() * 0.16, bt, pan=0.05)
        add(hat() * 0.05, bt + BEAT / 2, pan=0.25)
        add(hat(open_=b == 3) * 0.035, bt + BEAT / 4 * 3, pan=-0.25)
    tb += BAR
    bar += 1

# fade in after the hook build, fade out at the end
env = np.ones(N)
fo = int(2.5 * SR)
env[-fo:] = np.linspace(1, 0, fo) ** 1.5
music *= env[:, None]
music /= np.abs(music).max() + 1e-9


def write(path, x):
    with wave.open(path, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(x, -1, 1) * 32767).astype("<i2").tobytes())


write("music.wav", music * 0.9)

# ---- mix: music low under the SFX, ducked a little when an effect plays
with wave.open("sfx.wav") as w:
    sfx = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").astype(float).reshape(-1, 2) / 32767
sfx = np.pad(sfx, ((0, max(0, N - len(sfx))), (0, 0)))[:N]
level = np.abs(sfx).max(axis=1)
win = int(0.12 * SR)
level = np.convolve(level, np.ones(win) / win, mode="same")
duck = 1 - 0.45 * np.clip(level / 0.15, 0, 1)
MUSIC_GAIN = 0.22                                   # ≈ -13 dB under the effects
mix = sfx + music * MUSIC_GAIN * duck[:, None]
mix = np.tanh(mix * 1.3) / np.tanh(1.3)
mix *= 0.89 / (np.abs(mix).max() + 1e-9)
write("audio.wav", mix)
print(f"music.wav + audio.wav: {DUR}s, {bar} bars at {BPM} BPM from {DROP}s")
