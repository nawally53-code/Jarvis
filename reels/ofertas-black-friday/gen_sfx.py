# Synthesises the reel's sound effects (all generated here, no third-party audio)
# from the cue list written by `node render.js --events` (sfx-events.json) into sfx.wav.
#   key    – keyboard typing          click  – mouse click (press + release)
#   pop    – chat bubble appears      pop2   – reply chip appears
#   whoosh – slide / scene transition chime  – offer revealed
#   ticks  – counter rolling up       neon   – neon sign flickering on
#   impact – closing hit
import json
import wave
import numpy as np

SR = 48000
rng = np.random.default_rng(7)


def t_axis(dur):
    return np.arange(int(dur * SR)) / SR


def band_noise(dur, lo, hi):
    n = int(dur * SR)
    spec = np.fft.rfft(rng.standard_normal(n))
    f = np.fft.rfftfreq(n, 1 / SR)
    spec[(f < lo) | (f > hi)] = 0
    x = np.fft.irfft(spec, n)
    return x / (np.abs(x).max() + 1e-9)


def env(dur, attack, tau):
    t = t_axis(dur)
    a = np.clip(t / max(attack, 1e-4), 0, 1)
    return a * np.exp(-np.maximum(t - attack, 0) / tau)


def sweep(dur, f0, f1):
    t = t_axis(dur)
    f = f0 * (f1 / f0) ** (t / dur)
    return np.sin(2 * np.pi * np.cumsum(f) / SR)


# ---------------------------------------------------------------- voices
def key():
    d = 0.06
    g = rng.uniform(0.32, 0.45)
    hi = band_noise(d, 2500, 8000) * env(d, 0.0008, 0.006)
    thock = np.sin(2 * np.pi * rng.uniform(160, 230) * t_axis(d)) * env(d, 0.001, 0.012)
    return g * (0.8 * hi + 0.5 * thock), rng.uniform(-0.25, 0.25)


def click():
    d = 0.16
    out = np.zeros(int(d * SR))
    for off, g in ((0.0, 0.95), (0.075, 0.55)):        # press, release
        dd = 0.03
        s = band_noise(dd, 2500, 9500) * env(dd, 0.0003, 0.0028)
        s += 0.6 * np.sin(2 * np.pi * 2300 * t_axis(dd)) * env(dd, 0.0003, 0.003)
        s += 0.4 * np.sin(2 * np.pi * 320 * t_axis(dd)) * env(dd, 0.0005, 0.006)
        i = int(off * SR)
        out[i:i + len(s)] += g * s
    return out, 0.1


def pop(f0=320, f1=920):
    d = 0.16
    return 0.32 * sweep(d, f0, f1) * env(d, 0.004, 0.045), 0.0


def whoosh():
    d = 0.5
    t = t_axis(d)
    n = band_noise(d, 250, 5000) * 0.7 + band_noise(d, 1200, 9000) * 0.3
    rise = np.clip(t / 0.36, 0, 1) ** 2.2
    fall = np.clip((d - t) / 0.14, 0, 1)
    return 0.2 * n * rise * fall, None                 # None → pan sweep L→R


def chime():
    d = 0.9
    out = np.zeros(int(d * SR))
    for off, f, g in ((0.0, 1318.5, 1.0), (0.07, 1975.5, 0.8)):
        dd = d - off
        tt = t_axis(dd)
        s = (np.sin(2 * np.pi * f * tt) + 0.35 * np.sin(2 * np.pi * 2 * f * tt) + 0.12 * np.sin(2 * np.pi * 3.01 * f * tt))
        s *= env(dd, 0.003, 0.28)
        i = int(off * SR)
        out[i:] += g * s[: len(out) - i]
    return 0.09 * out, 0.0


def ticks(dur):
    out = np.zeros(int((dur + 0.1) * SR))
    for k in range(1, 11):                              # one tick per +5GB (count eases out)
        x = 1 - (1 - k / 10) ** (1 / 3)
        dd = 0.03
        s = np.sin(2 * np.pi * (2400 + 90 * k) * t_axis(dd)) * env(dd, 0.0005, 0.006)
        i = int(x * dur * SR)
        out[i:i + len(s)] += 0.15 * s
    return out, 0.0


def neon():
    d = 0.95
    t = t_axis(d)
    saw = 2 * ((t * 100) % 1) - 1
    buzz = saw + 0.5 * np.sin(2 * np.pi * 200 * t)
    steps = [1, 0.15, 1, 0.3, 0.9, 0.2, 1, 1]
    gate = np.array([steps[min(int(x / 0.5 * 8), 7)] if x < 0.5 else 1.0 for x in t])
    tail = np.where(t < 0.5, 1.0, np.exp(-(t - 0.5) / 0.18))
    crackle = band_noise(d, 3000, 10000) * (np.abs(np.diff(gate, prepend=gate[0])) > 0).astype(float)
    crackle = np.convolve(crackle, np.ones(240) / 240 * 40, mode="same")
    return 0.07 * buzz * gate * tail + 0.05 * crackle, 0.0


def impact():
    d = 1.2
    t = t_axis(d)
    boom = sweep(d, 70, 38) * env(d, 0.004, 0.32)
    thud = band_noise(d, 30, 900) * env(d, 0.001, 0.07)
    return 0.30 * boom + 0.14 * thud, 0.0


VOICES = {"key": key, "click": click, "pop": pop, "pop2": lambda: pop(480, 1250), "whoosh": whoosh,
          "chime": chime, "neon": neon, "impact": impact}


# ---------------------------------------------------------------- mix
def main():
    cues = json.load(open("sfx-events.json"))
    n = int(cues["duration"] * SR) + SR
    mix = np.zeros((n, 2))
    for c in cues["events"]:
        if c["type"] == "ticks":
            sig, pan = ticks(c.get("dur", 0.7))
        else:
            sig, pan = VOICES[c["type"]]()
        i = int(c["t"] * SR)
        sig = sig[: n - i]
        if pan is None:                                 # sweep left → right
            p = np.linspace(-0.6, 0.6, len(sig))
        else:
            p = np.full(len(sig), pan)
        mix[i:i + len(sig), 0] += sig * np.sqrt((1 - p) / 2)
        mix[i:i + len(sig), 1] += sig * np.sqrt((1 + p) / 2)
    mix = mix[: int(cues["duration"] * SR)]
    mix = np.tanh(mix * 2.0) / np.tanh(2.0)             # gentle limiter
    mix *= 0.89 / (np.abs(mix).max() + 1e-9)            # peak ≈ -1 dBFS
    with wave.open("sfx.wav", "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((mix * 32767).astype("<i2").tobytes())
    print(f"sfx.wav: {len(cues['events'])} cues, {cues['duration']}s")


if __name__ == "__main__":
    main()
