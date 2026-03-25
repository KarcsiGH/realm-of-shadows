"""
Realm of Shadows — Sound Engine
All sounds generated procedurally at startup — no audio files needed.
Gracefully handles missing/failed audio initialization.
"""
import math, array, random
try:
    import numpy as _np
    from scipy import signal as _signal
    _HAS_NUMPY = True
except ImportError:
    _HAS_NUMPY = False

_enabled        = False
_mixer          = None
_sounds         = {}
_music_channel  = None
_ambient_channel= None
_master_vol     = 0.6
_sfx_vol        = 0.7
_music_vol      = 0.35
_ambient_vol    = 0.65  # raised to match combat SFX level

# ── Incremental generation queues ─────────────────────────────────────────
_gen_batch1     = []   # (name, callable) — fast SFX, generates during Splash 1
_gen_batch2     = []   # (name, callable) — music/ambient, generates during Splash 2
_b1_idx         = 0    # next batch1 item to generate
_b2_idx         = 0    # next batch2 item to generate
_gen_ready      = False  # True when all sounds generated

try:
    import pygame.mixer as _mixer
except ImportError:
    _mixer = None


def init():
    """Initialize the sound system. Call once at startup."""
    global _enabled, _music_channel, _ambient_channel
    if _mixer is None:
        return
    try:
        current = _mixer.get_init()
        if not current:
            # Not yet initialized — try preferred settings, fall back gracefully
            try:
                _mixer.init(22050, -16, 1, 1024)
            except Exception:
                try:
                    _mixer.init()  # Let pygame pick defaults (works on macOS)
                except Exception:
                    return
        # Accept whatever the mixer is running at — pygame resamples on playback
        _mixer.set_num_channels(12)
        _music_channel   = _mixer.Channel(10)
        _ambient_channel = _mixer.Channel(11)
        _build_gen_queues()   # populate queues; generation happens incrementally
        _enabled = True
    except Exception:
        _enabled = False


def set_master_volume(v):
    global _master_vol
    _master_vol = max(0.0, min(1.0, v))
    # Re-apply to live channels so the change is immediately audible
    if _music_channel and _enabled:
        _music_channel.set_volume(_master_vol * _music_vol)
    if _ambient_channel and _enabled:
        _ambient_channel.set_volume(_master_vol * _ambient_vol)

def set_sfx_volume(v):
    global _sfx_vol
    _sfx_vol = max(0.0, min(1.0, v))

def set_music_volume(v):
    global _music_vol
    _music_vol = max(0.0, min(1.0, v))
    if _music_channel and _enabled:
        _music_channel.set_volume(_master_vol * _music_vol)

def set_ambient_volume(v):
    global _ambient_vol
    _ambient_vol = max(0.0, min(1.0, v))
    if _ambient_channel and _enabled:
        _ambient_channel.set_volume(_master_vol * _ambient_vol)

def get_master_volume():  return _master_vol
def get_sfx_volume():     return _sfx_vol
def get_music_volume():   return _music_vol
def get_ambient_volume(): return _ambient_vol


# ═══════════════════════════════════════════════════════════════
#  SETTINGS PERSISTENCE
# ═══════════════════════════════════════════════════════════════

_SETTINGS_FILE = "settings.json"

_display_mode = "fullscreen"  # "fullscreen" | "1440x900" | "1280x800"

def get_display_mode():
    return _display_mode

def set_display_mode(mode):
    global _display_mode
    _display_mode = mode

def save_settings():
    """Persist current volume settings to settings.json."""
    import json, os
    data = {
        "master_vol":  _master_vol,
        "sfx_vol":     _sfx_vol,
        "music_vol":   _music_vol,
        "ambient_vol": _ambient_vol,
        "display_mode": _display_mode,
    }
    try:
        with open(_SETTINGS_FILE, "w") as f:
            json.dump(data, f, indent=2)
    except Exception:
        pass

def load_settings():
    """Load volume settings from settings.json if it exists."""
    import json
    try:
        with open(_SETTINGS_FILE) as f:
            data = json.load(f)
        set_master_volume(float(data.get("master_vol",  _master_vol)))
        set_sfx_volume(   float(data.get("sfx_vol",     _sfx_vol)))
        set_music_volume( float(data.get("music_vol",   _music_vol)))
        set_ambient_volume(float(data.get("ambient_vol",_ambient_vol)))
        set_display_mode(data.get("display_mode", "fullscreen"))
    except (FileNotFoundError, Exception):
        pass  # Use defaults if file missing or corrupt


# ═══════════════════════════════════════════════════════════════
#  WAVEFORM GENERATORS
# ═══════════════════════════════════════════════════════════════

SR = 22050


def _make_sound(samples):
    if not _mixer:
        return None
    try:
        return _mixer.Sound(buffer=array.array('h', samples))
    except Exception:
        return None



# ═══════════════════════════════════════════════════════════════
#  NUMPY BIOME HELPERS  (used only if numpy/scipy available)
# ═══════════════════════════════════════════════════════════════

def _np_make_sound(sig):
    """Convert a numpy float32 array [-1,1] to a pygame Sound."""
    if not _mixer or not _HAS_NUMPY:
        return None
    try:
        d = (_np.clip(sig, -1.0, 1.0) * 32767).astype(_np.int16)
        return _mixer.Sound(buffer=array.array('h', d.tolist()))
    except Exception:
        return None

def _np_sine(n, freq, vol=0.4, phase=0.0):
    t = _np.arange(n, dtype=_np.float32) / SR
    return (vol * _np.sin(2 * _np.pi * freq * t + phase))

def _np_bandpass(n, cf, bw, vol=0.5, seed=0):
    rng = _np.random.default_rng(seed)
    noise = rng.standard_normal(n).astype(_np.float64)
    b, a = _signal.iirfilter(4,
        [max(20.0, cf - bw/2), min(float(SR)/2 - 1, cf + bw/2)],
        btype='band', fs=SR, ftype='butter')
    filtered = _signal.lfilter(b, a, noise)
    peak = _np.max(_np.abs(filtered)) or 1.0
    return (filtered / peak * vol).astype(_np.float32)

def _np_swell(n, period, phase=0.0, depth=0.55):
    t = _np.arange(n, dtype=_np.float32) / SR
    return (1.0 - depth + depth * (0.5 + 0.5 * _np.sin(2*_np.pi*t/period + phase)))

def _np_fade(sig, attack=0.05, release=0.1):
    out = sig.copy(); n = len(sig)
    a = min(int(SR*attack), n//2); r = min(int(SR*release), n//2)
    if a: out[:a] *= _np.linspace(0, 1, a, dtype=_np.float32)
    if r: out[-r:] *= _np.linspace(1, 0, r, dtype=_np.float32)
    return out

def _np_mix(*arrays):
    n = max(len(a) for a in arrays)
    out = _np.zeros(n, _np.float32)
    for a in arrays: out[:len(a)] += a
    return _np.clip(out, -1.0, 1.0)

def _np_place(buf, onset_s, chunk):
    s = int(SR * onset_s); e = min(len(buf), s + len(chunk))
    buf[s:e] += chunk[:e-s]

def _np_seamless(sig, fade=0.08):
    n = len(sig); f = int(SR * fade); out = sig.copy()
    ramp = _np.linspace(0, 1, f, dtype=_np.float32)
    out[:f]  += sig[-f:] * (1 - ramp)
    out[-f:] += sig[:f]  * (1 - ramp[::-1])
    return _np.clip(out, -1.0, 1.0)

def _make_biome(fn):
    """Generate a biome sound using numpy (if available) or return silence."""
    if not _HAS_NUMPY:
        return _make_sound([0] * int(SR * 4.0))
    return _np_make_sound(_np_seamless(fn()))

def _biome_grassland():
    N = int(SR * 8.0)
    wind1 = _np_bandpass(N, 280, 160, .22, 11) * _np_swell(N, 2.8, 0.0, .6)
    wind2 = _np_bandpass(N, 180,  80, .12, 22) * _np_swell(N, 4.1, 1.2, .5)
    rustle= _np_bandpass(N, 600, 350, .07, 33) * _np_swell(N, 1.3, 0.5, .7)
    gust_n= _np_bandpass(N, 320, 200, .18, 44)
    gust_e= _np.zeros(N, _np.float32)
    gs, ge = int(SR*2.8), int(SR*4.2)
    gust_e[gs:ge] = _np.hanning(ge-gs)
    birds = _np.zeros(N, _np.float32)
    for onset, freq, dur in [(1.2,3800,.08),(1.31,4200,.07),(1.42,3600,.09),(5.5,4000,.08),(5.61,4400,.07)]:
        n2 = int(SR*dur)
        _np_place(birds, onset, _np_fade(_np_sine(n2,freq,.08),.01,.03))
    return _np_mix(wind1, wind2, rustle, gust_n*gust_e, birds)

def _biome_forest():
    N = int(SR * 8.0)
    canopy = _np_bandpass(N, 400, 200, .18, 21) * _np_swell(N, 2.1, 0.0, .65)
    foliage= _np_bandpass(N, 160,  70, .14, 31) * _np_swell(N, 3.7, 2.0, .5)
    hum    = _np_sine(N, 55, .05)              * _np_swell(N, 5.0, 0.0, .4)
    birds  = _np.zeros(N, _np.float32)
    for onset, freq in [(0.8,2200),(0.95,2600),(1.1,3100),(1.25,3600)]:
        n2=int(SR*.12); _np_place(birds, onset, _np_fade(_np_sine(n2,freq,.07),.01,.04))
    for onset in [4.2,4.32,4.44,4.56]:
        n2=int(SR*.09); _np_place(birds, onset, _np_fade(_np_sine(n2,3200,.05),.01,.02))
    drips  = _np.zeros(N, _np.float32)
    rng = _np.random.default_rng(41)
    for _ in range(6):
        t = float(rng.uniform(0.5, 7.7)); n2=int(SR*.04)
        _np_place(drips, t, _np_fade(_np_bandpass(n2,1800,800,.04,int(t*100)),.002,.02))
    return _np_mix(canopy, foliage, hum, birds, drips)

def _biome_hills():
    N = int(SR * 8.0)
    wind_hi = _np_bandpass(N, 350, 200, .25, 41) * _np_swell(N, 2.4, 0.0, .55)
    wind_lo = _np_bandpass(N, 100,  50, .15, 51) * _np_swell(N, 3.8, 1.5, .5)
    moan    = _np_sine(N, 95, .06)               * _np_swell(N, 4.5, 0.8, .7)
    gusts   = _np.zeros(N, _np.float32)
    for gs_t, ge_t in [(0.5,2.0),(5.5,7.5)]:
        gs, ge = int(SR*gs_t), int(SR*ge_t); n2 = ge-gs
        bump = _np_bandpass(n2, 380, 220, .22, int(gs_t*10)) * _np.hanning(n2).astype(_np.float32)
        gusts[gs:ge] += bump
    whistle = _np.zeros(N, _np.float32)
    _np_place(whistle, 3.2, _np_fade(_np_sine(int(SR*.7),680,.06),.15,.25))
    return _np_mix(wind_hi, wind_lo, moan, gusts, whistle)

def _biome_swamp():
    N = int(SR * 8.0)
    d1   = _np_sine(N, 58, .10) * _np_swell(N, 4.2, 0.0, .4)
    d2   = _np_sine(N, 87, .06) * _np_swell(N, 6.1, 2.1, .5)
    murk = _np_bandpass(N, 130, 60, .10, 61) * _np_swell(N, 3.0, 0.5, .5)
    bugs = _np_bandpass(N, 3500, 1500, .06, 71) * _np_swell(N, 0.4, 0.0, .8) * _np_swell(N, 2.5, 1.0, .6)
    frogs = _np.zeros(N, _np.float32)
    for onset, freq in [(1.4,280),(1.55,260),(4.2,300),(4.35,285)]:
        n2=int(SR*.18); _np_place(frogs, onset, _np_fade(_np_bandpass(n2,freq,80,.12,int(onset*100)),.02,.06))
    bubbles = _np.zeros(N, _np.float32)
    for onset in [2.3,6.1]:
        n2=int(SR*.06); _np_place(bubbles, onset, _np_fade(_np_bandpass(n2,400,200,.08,int(onset*50)),.005,.04))
    return _np_mix(d1, d2, murk, bugs, frogs, bubbles)

def _biome_coast():
    N = int(SR * 8.0)
    deep  = _np_bandpass(N, 80, 50, .22, 81)   * _np_swell(N, 3.5, 0.0, .65)
    crash = _np_bandpass(N, 350, 300, .18, 91)
    crash_e = _np.zeros(N, _np.float32)
    for pt in [1.2, 4.3, 7.1]:
        s,e = int(SR*max(0,pt-1.0)), int(SR*min(8.0,pt+0.8))
        if e>s: crash_e[s:e] += _np.hanning(e-s)**0.7
    spray   = _np_bandpass(N, 2000, 1200, .06, 12)
    spray_e = _np.zeros(N, _np.float32)
    for pt in [1.2,4.3,7.1]:
        s,e = int(SR*max(0,pt-.2)), int(SR*min(8.0,pt+.4))
        if e>s: spray_e[s:e] += _np.hanning(e-s)
    gulls = _np.zeros(N, _np.float32)
    for onset, freq in [(2.5,1800),(2.7,1950),(2.9,1800),(6.0,1700),(6.2,1900)]:
        n2=int(SR*.16)
        cry = _np_sine(n2,freq,.07) + _np_sine(n2,int(freq*1.5),.03)
        _np_place(gulls, onset, _np_fade(cry,.03,.06))
    wind = _np_bandpass(N, 250, 130, .10, 92) * _np_swell(N, 3.1, 1.0, .4)
    return _np_mix(deep, crash*crash_e, spray*spray_e, gulls, wind)

def _biome_desert():
    """Arid, sparse — sustained hot wind, sand hiss, no birds, eerie emptiness."""
    N = int(SR * 8.0)
    # Hot dry wind: narrow high-mid bandpass, very slow swell
    wind_hot = _np_bandpass(N, 320, 100, .20, 14) * _np_swell(N, 5.2, 0.0, .5)
    # Low sand rumble: sub-bass hiss
    sand_lo  = _np_bandpass(N, 90, 40, .12, 24) * _np_swell(N, 3.8, 1.6, .55)
    # Blowing sand: high-freq sibilant hiss that gusts
    sand_hi  = _np_bandpass(N, 4000, 2000, .05, 34) * _np_swell(N, 1.8, 0.4, .7)
    # Gust event: one strong blast midway
    gust_n = _np_bandpass(N, 380, 180, .22, 54)
    gust_e = _np.zeros(N, _np.float32)
    gs, ge = int(SR*3.0), int(SR*5.5)
    gust_e[gs:ge] = _np.hanning(ge-gs)
    # Occasional lone sand devil (brief high-freq swirl)
    devil = _np.zeros(N, _np.float32)
    n2 = int(SR*.35)
    swirl = _np_bandpass(n2, 1800, 800, .07, 74) * _np.hanning(n2).astype(_np.float32)
    _np_place(devil, 6.2, swirl)
    # Subtle low resonant tone (heat shimmer effect)
    shimmer = _np_sine(N, 62, .03) * _np_swell(N, 7.0, 0.0, .6)
    return _np_mix(wind_hot, sand_lo, sand_hi, gust_n*gust_e, devil, shimmer)


def _sine(freq, duration, volume=0.5, fade_out=True):
    n, amp = int(SR * duration), int(32000 * volume)
    return [max(-32767, min(32767, int(
        amp * (max(0.0, 1.0 - i/SR/duration) if fade_out else 1.0)
        * math.sin(2 * math.pi * freq * i/SR))))
        for i in range(n)]


def _noise(duration, volume=0.3, fade_out=True, seed=42):
    n, amp, rng = int(SR * duration), int(32000 * volume), random.Random(seed)
    return [max(-32767, min(32767, int(
        amp * (max(0.0, 1.0 - i/SR/duration) if fade_out else 1.0)
        * (rng.random() * 2 - 1))))
        for i in range(n)]


def _sweep(f_start, f_end, duration, volume=0.4):
    n, amp, phase = int(SR * duration), int(32000 * volume), 0.0
    out = []
    for i in range(n):
        frac   = i / n
        phase += 2 * math.pi * (f_start + (f_end - f_start) * frac) / SR
        out.append(max(-32767, min(32767, int(amp * max(0.0, 1.0 - frac) * math.sin(phase)))))
    return out


def _bandpass_noise(duration, center_freq, bandwidth, volume=0.5, seed=42):
    """White noise through a biquad bandpass filter — core of creak sounds."""
    n     = int(SR * duration)
    rng   = random.Random(seed)
    w0    = 2 * math.pi * center_freq / SR
    alpha = math.sin(w0) / (2 * center_freq / bandwidth)
    b0    =  alpha / (1 + alpha)
    b2    = -alpha / (1 + alpha)
    a1    = -2 * math.cos(w0) / (1 + alpha)
    a2    = (1 - alpha) / (1 + alpha)
    x1 = x2 = y1 = y2 = 0.0
    raw = []
    for _ in range(n):
        x0 = rng.random() * 2 - 1
        y0 = b0*x0 + b2*x2 - a1*y1 - a2*y2
        x2, x1 = x1, x0;  y2, y1 = y1, y0
        raw.append(y0)
    peak  = max(abs(v) for v in raw) or 1.0
    scale = 32000 * volume / peak
    return [max(-32767, min(32767, int(v * scale))) for v in raw]


def _stick_slip_env(n, slip_count=12, seed=5):
    """Irregular amplitude envelope simulating a hinge catching and releasing."""
    rng = random.Random(seed)
    env = [1.0] * n
    for i in range(int(SR * 0.04)):
        env[i] *= i / int(SR * 0.04)
    for i in range(int(SR * 0.18)):
        env[n - 1 - i] *= i / int(SR * 0.18)
    for _ in range(slip_count):
        pos   = rng.randint(int(n * 0.05), int(n * 0.85))
        surge = rng.uniform(1.1, 1.6)
        drop  = rng.uniform(0.3, 0.65)
        width = rng.randint(int(SR * 0.015), int(SR * 0.05))
        tail  = rng.randint(int(SR * 0.03),  int(SR * 0.10))
        for j in range(width):
            if pos + j < n:
                env[pos + j] *= min(2.0, surge * (1 - j/width) + j/width)
        for j in range(tail):
            if pos + width + j < n:
                env[pos + width + j] *= drop + (1.0 - drop) * j / tail
    return [max(0.0, min(2.0, e)) for e in env]


def _creak(duration, center_freq, bandwidth, volume, slip_count, seed):
    n     = int(SR * duration)
    noise = _bandpass_noise(duration, center_freq, bandwidth, volume, seed)
    env   = _stick_slip_env(n, slip_count, seed + 1)
    return [max(-32767, min(32767, int(s * e))) for s, e in zip(noise, env)]


def _thud(duration=0.12, volume=0.14):
    return [max(-32767, min(32767,
        int(32000 * volume * math.exp(-i/SR * 32) * math.sin(2 * math.pi * 58 * i/SR))))
        for i in range(int(SR * duration))]


def _coin_clink(freq, duration=0.12, volume=0.4):
    out = []
    for i in range(int(SR * duration)):
        t   = i / SR
        env = math.exp(-t * 22)
        v   = int(32000 * volume * env * (
            math.sin(2 * math.pi * freq * t)
            + math.sin(2 * math.pi * freq * 1.41 * t) * 0.25))
        out.append(max(-32767, min(32767, v)))
    return out


def _coin_scatter(num_coins=6, seed=7):
    rng, total = random.Random(seed), int(SR * 1.1)
    out = [0] * total
    for _ in range(num_coins):
        freq, offset, vol = rng.randint(1400, 2800), rng.randint(0, int(SR * 0.55)), rng.uniform(0.28, 0.42)
        for j, v in enumerate(_coin_clink(freq, 0.14, vol)):
            if offset + j < total:
                out[offset + j] = max(-32767, min(32767, out[offset + j] + v))
    settle_off = int(SR * 0.65)
    for j, v in enumerate(_coin_clink(rng.randint(900, 1200), 0.18, 0.22)):
        if settle_off + j < total:
            out[settle_off + j] = max(-32767, min(32767, out[settle_off + j] + v))
    return out


def _wah_note(freq, duration, volume=0.38):
    out = []
    for i in range(int(SR * duration)):
        t, frac = i / SR, i / int(SR * duration)
        env = (frac / 0.08) if frac < 0.08 else math.exp(-(frac - 0.08) * 3.5)
        wah = math.sin(math.pi * frac)
        sig = (math.sin(2 * math.pi * freq * t)
               + math.sin(2 * math.pi * freq * 3 * t) * 0.18
               + math.sin(2 * math.pi * freq * 5 * t) * 0.08
               + math.sin(2 * math.pi * (500 + 600 * wah) * t) * 0.35 * wah)
        out.append(max(-32767, min(32767, int(32000 * volume * env * sig))))
    return out


def _peanuts_talk(num_syllables=5, seed=99):
    rng, parts, i = random.Random(seed), [], 0
    while i < num_syllables:
        word_len = rng.randint(1, 3)
        for w in range(word_len):
            if i >= num_syllables:
                break
            parts += _wah_note(240 * rng.uniform(0.82, 1.22), rng.uniform(0.13, 0.21), rng.uniform(0.30, 0.40))
            if w < word_len - 1:
                parts += [0] * int(SR * 0.04)
            i += 1
        parts += [0] * int(SR * 0.13)
    return parts


def _mix(*lists):
    n, out = max(len(s) for s in lists), []
    out = [0] * n
    for sl in lists:
        for i, v in enumerate(sl):
            out[i] = max(-32767, min(32767, out[i] + v))
    return out


def _concat(*lists):
    out = []
    for sl in lists:
        out.extend(sl)
    return out


def _silence(duration):
    return [0] * int(SR * duration)


# ═══════════════════════════════════════════════════════════════
#  NUMPY COMBAT + DUNGEON GENERATORS
# ═══════════════════════════════════════════════════════════════

def _np_bp(n, cf, bw, seed=0):
    if not _HAS_NUMPY: return _np.zeros(n, _np.float32)
    from scipy import signal as _sci
    x = _np.random.default_rng(seed).standard_normal(n).astype(_np.float64)
    lo = max(20.0, cf - bw / 2); hi = min(float(SR) / 2 - 1, cf + bw / 2)
    b, a = _sci.iirfilter(4, [lo, hi], btype='band', fs=SR, ftype='butter')
    r = _sci.lfilter(b, a, x)           # keep float64 — no overflow
    r = _np.nan_to_num(r, nan=0.0, posinf=0.0, neginf=0.0)
    pk = _np.max(_np.abs(r))
    if pk > 0:
        r = r / pk
    return r.astype(_np.float32)

def _np_lp(sig, cutoff):
    if not _HAS_NUMPY: return sig
    from scipy import signal as _sci
    b, a = _sci.iirfilter(2, min(cutoff, SR // 2 - 1), btype='low', fs=SR, ftype='butter')
    r = _sci.lfilter(b, a, sig.astype(_np.float64))
    return _np.nan_to_num(r, nan=0.0, posinf=0.0, neginf=0.0).astype(_np.float32)

def _np_hp_filt(sig, cutoff):
    if not _HAS_NUMPY: return sig
    from scipy import signal as _sci
    b, a = _sci.iirfilter(2, max(cutoff, 20), btype='high', fs=SR, ftype='butter')
    r = _sci.lfilter(b, a, sig.astype(_np.float64))
    return _np.nan_to_num(r, nan=0.0, posinf=0.0, neginf=0.0).astype(_np.float32)

def _np_exp(n, tau): return _np.exp(-_np.arange(n)/(SR*tau)).astype(_np.float32)
def _np_norm(sig, t=0.88): pk = _np.max(_np.abs(sig)) or 1; return sig/pk*t
def _np_sil(d): return _np.zeros(int(SR*d), _np.float32)
def _np_fade2(sig, attack=0.003, release=0.12):
    out = sig.copy(); n = len(sig)
    a = min(int(SR*attack), n//2); r = min(int(SR*release), n//2)
    if a: out[:a] *= _np.linspace(0,1,a).astype(_np.float32)
    if r: out[-r:] *= _np.linspace(1,0,r).astype(_np.float32)
    return out
def _np_mix2(*arrs):
    n = max(len(a) for a in arrs); out = _np.zeros(n, _np.float32)
    for a in arrs: out[:len(a)] += a
    return _np.clip(out, -1, 1)
def _np_place2(buf, t_s, chunk):
    s = int(SR*t_s)
    if s >= len(buf): return
    e = min(len(buf), s+len(chunk)); buf[s:e] += chunk[:e-s]
def _np_sinev(n, freq, vol=1.0):
    return (vol * _np.sin(2*_np.pi*(freq/SR)*_np.arange(n))).astype(_np.float32)
def _np_seamless2(sig, fade=0.12):
    n = len(sig); f = int(SR*fade); out = sig.copy()
    ramp = _np.linspace(0,1,f).astype(_np.float32)
    out[:f] += sig[-f:]*(1-ramp); out[-f:] += sig[:f]*(1-ramp[::-1])
    return _np.clip(out,-1,1)
def _np_swell2(n, period, phase=0.0, depth=0.5):
    t = _np.arange(n)/_np.float32(SR)
    return (1-depth + depth*(0.5+0.5*_np.sin(2*_np.pi*t/period+phase))).astype(_np.float32)
def _np_note(freq, dur, vol=0.3, tau=0.12):
    n = int(SR*dur); sig = _np_sinev(n,freq,vol)
    env = _np_exp(n,tau); env[:min(int(SR*.02),n//4)] *= _np.linspace(0,1,min(int(SR*.02),n//4))
    return (sig*env).astype(_np.float32)

def _make_np_sound(fn):
    if not _HAS_NUMPY: return None
    try:
        sig = fn()
        d = (_np.clip(sig,-1,1)*32767).astype(_np.int16)
        return _make_sound(list(d))
    except Exception:
        return None

# ── Element hit sounds ────────────────────────────────────────
def _gen_hit_fire():
    """Fire hit: deep whomp → crackling tail. Low-end first, then scatter."""
    n=int(SR*.38)
    whomp=_np_sinev(n,68,.50)*_np_exp(n,.06)             # deep ignition thud
    body=_np_bp(n,160,70,3)*_np_exp(n,.05)*.55           # fire body
    crackle=_np_bp(n,1400,700,2)*_np_exp(n,.09)*.38      # crackle burst
    hiss=_np_bp(n,3200,1800,1)*_np_exp(n,.03)*.18        # hiss tail
    env=_np_fade2(_np.ones(n,_np.float32),.001,.15)
    return _np_norm(_np_mix2(whomp,body,crackle,hiss)*env)

def _gen_hit_ice():
    """Ice hit: crystalline crack → ringing freeze. Sharp attack, pure tones."""
    n=int(SR*.45)
    # Shatter transient
    n2=int(SR*.03)
    shatter=_np_hp_filt(_np.random.default_rng(4).standard_normal(n2).astype(_np.float32)*_np_exp(n2,.008),2500)*.80
    # Pure crystal ring tones (long decay)
    ring=_np.zeros(n,_np.float32)
    for f,v,tau in [(2800,.32,.20),(3600,.24,.16),(4800,.14,.12),(1800,.20,.22)]:
        ring+=_np_sinev(n,f,v)*_np_exp(n,tau)
    ring=_np_lp(ring,6000)*.65
    # Cold sub body
    cold=_np_sinev(n,120,.18)*_np_exp(n,.10)
    base=_np.zeros(n,_np.float32); base[:n2]+=shatter
    env=_np_fade2(_np.ones(n,_np.float32),.001,.20)
    return _np_norm(_np_mix2(base,ring,cold)*env)

def _gen_hit_lightning():
    """Lightning hit: instant crack → buzzing aftershock → deep thunder."""
    n=int(SR*.30)
    # Instant electric snap
    ns=int(SR*.006)
    snap=_np_hp_filt(_np.random.default_rng(5).standard_normal(ns).astype(_np.float32),4000)*1.8
    # Buzzing arc discharge
    nb=int(SR*.08)
    buzz=_np_bp(nb,2200,1100,6)*_np_exp(nb,.018)*.70
    # Deep thunder body
    body=_np_sinev(n,75,.38)*_np_exp(n,.045)
    body2=_np_bp(n,220,100,7)*_np_exp(n,.040)*.40
    base=_np.zeros(n,_np.float32)
    base[:min(ns,n)]+=snap; base[:nb]+=buzz
    env=_np.ones(n,_np.float32); r=int(SR*.12); env[-r:]=_np.linspace(1,0,r)
    return _np_norm(_np_mix2(base*env,body,body2))

def _gen_hit_shadow():
    """Shadow hit: silent approach → hollow thud → dark resonance."""
    n=int(SR*.40)
    # Soft attack ramp (shadow creeps in)
    thud=_np_bp(n,180,75,8)*_np_exp(n,.06)
    dark=_np_sinev(n,78,.38)*_np_exp(n,.11)
    low=_np_sinev(n,52,.28)*_np_exp(n,.14)
    hollow=_np_bp(n,420,160,9)*_np_exp(n,.030)*.30
    e=_np.ones(n,_np.float32)
    e[:int(SR*.015)]=_np.linspace(0,1,int(SR*.015))   # slow shadow attack
    env=_np_fade2(_np.ones(n,_np.float32),.015,.18)
    return _np_norm(_np_mix2(thud,dark,low,hollow)*e*env)

def _gen_hit_divine():
    """Divine hit: bright click → sustaining bell chord. Light and ringing."""
    n=int(SR*.55)
    # Bright transient click
    n_c=int(SR*.004)
    click=_np_hp_filt(_np.random.default_rng(11).standard_normal(n_c).astype(_np.float32)*.8,5000)
    # Rich bell chord — fundamental + harmonics
    bell=_np.zeros(n,_np.float32)
    for f,v,tau in [(880,.45,.22),(1760,.28,.14),(2637,.18,.10),(3520,.10,.07),(1320,.22,.18)]:
        bell+=_np_sinev(n,f,v)*_np_exp(n,tau)
    # Soft shimmer
    shimmer=_np_bp(n,4500,1800,12)*_np_exp(n,.04)*.08
    base=_np.zeros(n,_np.float32); base[:n_c]+=click
    r=int(SR*.28); env=_np.ones(n,_np.float32); env[-r:]=_np.linspace(1,0,r)
    return _np_norm(_np_mix2(base*.5,bell*env,shimmer))

def _gen_hit_nature():
    """Nature hit: earthy thunk → wood resonance → leaf rustle."""
    n=int(SR*.35)
    thunk=_np_bp(n,260,100,12)*_np_exp(n,.05)           # earthy thunk
    earth=_np_sinev(n,68,.32)*_np_exp(n,.09)            # deep earth body
    wood=_np_sinev(n,140,.20)*_np_exp(n,.07)            # wood resonance
    rustle=_np_bp(n,2800,1600,13)*_np_exp(n,.030)*.20   # leaf rustle tail
    env=_np_fade2(_np.ones(n,_np.float32),.001,.14)
    return _np_norm(_np_mix2(thunk,earth,wood,rustle)*env)

def _gen_hit_arcane():
    """Arcane hit: rising sweep → crystalline shimmer → echo decay."""
    n=int(SR*.38)
    # Frequency sweep (low→high)
    sweep=_np.zeros(n,_np.float32); phase=0.0
    for i in range(n):
        frac=i/n; freq=400+2000*frac*(1-frac*0.5); phase+=2*_np.pi*freq/SR
        sweep[i]=_np.sin(phase)*(frac**0.4)*((1-frac)**0.6)
    sweep=_np_lp(sweep*0.55, 4000)
    # Crystal resonance
    cryst=_np.zeros(n,_np.float32)
    for f,tau in [(1320,.10),(1980,.07),(2640,.05)]: cryst+=_np_sinev(n,f,.14)*_np_exp(n,tau)
    shimmer=_np_bp(n,1800,800,15)*_np_exp(n,.06)*.35
    env=_np_fade2(_np.ones(n,_np.float32),.001,.16)
    return _np_norm(_np_mix2(sweep,cryst,shimmer)*env)

# ── Physical hit variants ─────────────────────────────────────
def _gen_hit_light():
    """Light hit: quick snap with flesh impact — dagger, fist, glancing blow."""
    n=int(SR*.18)
    snap=_np_bp(n,600,300,30)*_np_exp(n,.020)            # primary snap
    body=_np_sinev(n,140,.28)*_np_exp(n,.030)            # body resonance
    flesh=_np_bp(n,240,100,31)*_np_exp(n,.025)*.35       # flesh impact
    hiss=_np_bp(n,1800,800,32)*_np_exp(n,.012)*.18       # edge hiss
    env=_np_fade2(_np.ones(n,_np.float32),.001,.07)
    return _np_norm(_np_mix2(snap,body,flesh,hiss)*env)

def _gen_hit_medium():
    """Medium hit: thwack with clear mid impact — sword, mace, staff."""
    n=int(SR*.26)
    thwack=_np_bp(n,380,160,33)*_np_exp(n,.045)          # primary thwack
    low=_np_sinev(n,95,.38)*_np_exp(n,.060)              # sub weight
    mid=_np_bp(n,190,80,34)*_np_exp(n,.050)*.55          # mid body
    crack=_np_bp(n,900,400,35)*_np_exp(n,.018)*.28       # crack transient
    env=_np_fade2(_np.ones(n,_np.float32),.001,.11)
    return _np_norm(_np_mix2(thwack,low,mid,crack)*env)

def _gen_hit_heavy():
    """Heavy hit: deep boom with ground-shaking sub — greataxe, hammer, crushing blow."""
    n=int(SR*.40)
    boom=_np_bp(n,95,45,37)*_np_exp(n,.10)               # deep boom
    sub=_np_sinev(n,48,.50)*_np_exp(n,.12)               # sub-bass thud
    body=_np_sinev(n,82,.32)*_np_exp(n,.09)              # body resonance
    crack=_np_bp(n,240,100,38)*_np_exp(n,.045)*.45       # impact crack
    rumble=_np_bp(n,140,60,39)*_np_exp(n,.08)*.35        # rumble tail
    env=_np_fade2(_np.ones(n,_np.float32),.002,.18)
    return _np_norm(_np_mix2(boom,sub,body,crack,rumble)*env)

def _gen_hit_critical():
    """Critical hit: massive crack → sustained metallic ring. Unmistakable."""
    # Impact transient — big crack with sub thud
    n1=int(SR*.07)
    crack=_np_bp(n1,320,160,20)*_np_exp(n1,.020)*1.0
    sub_hit=_np_sinev(n1,58,.70)*_np_exp(n1,.025)
    body=_np_bp(n1,140,65,21)*_np_exp(n1,.022)*.70
    impact=_np_norm(_np_mix2(crack,sub_hit,body),.95)
    # Gap
    gap=_np_sil(.022)
    # Ringing tail — layered harmonics, slow decay
    n3=int(SR*.55)
    ring_lo=_np_sinev(n3,98,.50)*_np_exp(n3,.20)
    ring_mid=_np_sinev(n3,164,.35)*_np_exp(n3,.14)
    ring_hi=_np_sinev(n3,246,.20)*_np_exp(n3,.10)
    rumble=_np_sinev(n3,49,.40)*_np_exp(n3,.22)
    shimmer=_np_bp(n3,600,260,22)*_np_exp(n3,.06)*.22
    tail=_np_norm(_np_mix2(ring_lo,ring_mid,ring_hi,rumble,shimmer),.85)
    full=_np.concatenate([impact,gap,tail])
    return _np_norm(_np_fade2(full,.001,.22))

def _gen_hit_skill_fast():
    """Three-hit skill: distinct rapid strikes, each with its own character."""
    def strike(seed, pitch=1.0):
        n=int(SR*.10)
        thwack=_np_bp(n,int(420*pitch),int(180*pitch),seed)*_np_exp(n,.025)
        body=_np_sinev(n,int(110*pitch),.32)*_np_exp(n,.035)
        env=_np_fade2(_np.ones(n,_np.float32),.001,.05)
        return _np_norm(_np_mix2(thwack,body)*env,.70)
    s1=strike(70,1.0); s2=strike(72,1.15); s3=strike(74,0.90); gap=int(SR*.065)
    n_t=len(s1)+gap+len(s2)+gap+len(s3); out=_np.zeros(n_t,_np.float32)
    o=0; out[o:o+len(s1)]+=s1; o+=len(s1)+gap
    out[o:o+len(s2)]+=s2*.92; o+=len(s2)+gap
    out[o:o+len(s3)]+=s3*.85
    return _np_norm(out)

# ── Miss sounds (deeper, longer, distinct from hits) ─────────
def _gen_miss_physical():
    """Weapon whiffs through air — whoosh that dissipates, no impact."""
    n = int(SR * 0.38)
    # Air displacement with no contact — peaks then trails off
    env = _np.zeros(n, _np.float32)
    pk = int(n * 0.45)
    env[:pk] = _np.linspace(0.0, 1.0, pk) ** 0.6
    env[pk:] = _np.linspace(1.0, 0.0, n - pk) ** 0.8
    body  = _np_bp(n, 220, 90, 40) * env * 0.60     # air body
    deep  = _np_sinev(n, 78, 0.30) * env * _np_exp(n, 0.20) * 0.55  # low miss weight
    # Slight stumble/recovery thud at end
    n2 = int(SR * 0.10); t2 = int(SR * 0.28)
    stumble = _np_bp(n2, 150, 65, 41) * _np_exp(n2, 0.04) * 0.35
    out = _np_mix2(body, deep)
    out[t2:t2+n2] += stumble
    return _np_norm(_np_fade2(out, .002, .14))

def _gen_miss_magic():
    """Spell fizzles out — energy that built up but didn't release. Low thump."""
    n = int(SR * 0.45)
    # Energy that was building suddenly dissipates — low collapse
    charge = _np.zeros(n, _np.float32)
    phase = 0.0
    for i in range(n):
        frac = i / n
        # Builds then collapses
        freq = 80 + 120 * frac * (1 - frac) * 4
        phase += 2 * _np.pi * freq / SR
        charge[i] = _np.sin(phase) * min(frac * 4, 1.0) * max(1 - frac * 1.5, 0) * 0.40
    charge = _np_lp(charge, 500)
    # Low hollow thud when it collapses
    n3 = int(SR * 0.15); t3 = int(SR * 0.28)
    fizzle = (_np_sinev(n3, 68, 0.35) + _np_bp(n3, 130, 60, 42) * 0.30) * _np_exp(n3, 0.06)
    out = _np.zeros(n, _np.float32)
    out += charge
    out[t3:t3+n3] += fizzle
    return _np_norm(_np_fade2(out, .005, .18))

def _gen_miss_elemental():
    """Elemental attack dissipates — surge of energy that hits nothing and fades."""
    n = int(SR * 0.40)
    # Quick surge then low resonant decay
    n_surge = int(SR * 0.08)
    surge = _np_bp(n_surge, 180, 80, 44) * _np_exp(n_surge, 0.015) * 0.65
    # Resonant fade — the element dissipating
    n_die = int(SR * 0.32); t_die = int(SR * 0.06)
    die = (_np_sinev(n_die, 95, 0.28) + _np_bp(n_die, 160, 70, 45) * 0.35) * _np_exp(n_die, 0.10)
    out = _np.zeros(n, _np.float32)
    out[:n_surge] += surge
    out[t_die:t_die+n_die] += die
    return _np_norm(_np_fade2(out, .002, .16))

# ── Heal / Revive ─────────────────────────────────────────────
def _gen_heal():
    def nn(freq,dur,vol=.35):
        n=int(SR*dur); t=_np.arange(n)/SR; env=_np.sin(_np.pi*t/dur)**.5
        return vol*env*(_np_sinev(n,freq,1.0)+_np_sinev(n,freq*2,.12))
    return _np_norm(_np.concatenate([nn(523,.16),nn(659,.16),nn(784,.22)]))
def _gen_revive():
    n_r=int(SR*.5); hum=_np.zeros(n_r,_np.float32)
    for i in range(n_r):
        frac=i/n_r; freq=180+320*frac**2; hum[i]=_np.sin(2*_np.pi*freq*i/SR)*(frac**1.5)*.3
    hum=_np_lp(hum,800)
    n_p=int(SR*.45); chords=_np.zeros(n_p,_np.float32)
    for freq,vol in [(523,.28),(659,.22),(784,.18),(1047,.14),(1318,.10)]:
        chords+=_np_sinev(n_p,freq,vol)*_np.hanning(n_p).astype(_np.float32)
    shimmer=_np_bp(n_p,3500,1500,60)*_np_exp(n_p,.05)*.12
    peak=_np_norm(_np_mix2(chords,shimmer),.8)
    full=_np.concatenate([hum,_np_sil(.04),peak])
    return _np_norm(_np_fade2(full,.01,.20))

# ── Status ticks ──────────────────────────────────────────────
def _gen_poison_tick():
    n=int(SR*.18); bubble=_np_bp(n,160,70,80)*_np_exp(n,.04); sour=_np_bp(n,620,220,81)*_np_exp(n,.025)*.3; sub=_np_sinev(n,62,.2)*_np_exp(n,.05)
    return _np_norm(_np_mix2(bubble,sour,sub)*_np_fade2(_np.ones(n,_np.float32),.003,.08))
def _gen_burning_tick():
    n=int(SR*.15); crack=_np_bp(n,1600,900,82)*_np_exp(n,.015); whomp=_np_bp(n,300,130,83)*_np_exp(n,.03)*.45
    return _np_norm(_np_mix2(crack,whomp)*_np_fade2(_np.ones(n,_np.float32),.001,.06))

# ── Buff variants ─────────────────────────────────────────────
def _gen_buff_physical():
    """Power-up resolution: weapon strike sound + rising power chord.
    Feels like gaining strength — metallic clank then ascending tones.
    Clear, present, unmistakably 'gained something'. Centroid ~700Hz."""
    n = int(SR * 0.60)
    # Sharp metallic strike at onset — the 'activation' sound
    n_hit = int(SR * 0.06)
    metal = _np.zeros(n_hit, _np.float32)
    for f, v, tau in [(1200, 0.40, 0.03), (800, 0.30, 0.04), (400, 0.25, 0.05)]:
        metal += _np_sinev(n_hit, f, v) * _np_exp(n_hit, tau)
    # Rising three-note power chord (empowering feeling)
    notes = [(220, 0.0, 0.32), (330, 0.08, 0.28), (440, 0.16, 0.24), (550, 0.24, 0.18)]
    chord = _np.zeros(n, _np.float32)
    for freq, onset_s, vol in notes:
        onset = int(SR * onset_s)
        n_note = n - onset
        env_n = _np.linspace(0.0, 1.0, n_note).astype(_np.float32) ** 0.7 * _np_exp(n_note, 0.28)
        chord[onset:] += _np_sinev(n_note, freq, vol) * env_n
    out = _np.zeros(n, _np.float32)
    out[:n_hit] += metal * 0.80
    out += chord * 0.75
    return _np_norm(_np_fade2(out, .001, .20))

def _gen_buff_magic():
    """Magical enhancement: sparkling upward sweep + sustained harmonic chord.
    Feels like power being added — bright shimmer resolving into warmth.
    Centroid ~800Hz — present and clearly 'magical'."""
    n = int(SR * 0.65)
    # Rising frequency sweep — clearly audible upward motion
    sweep = _np.zeros(n, _np.float32); phase = 0.0
    for i in range(n):
        freq = 300 + 700 * (i/n) ** 1.0   # 300 → 1000Hz linear rise
        phase += 2 * _np.pi * freq / SR
        sweep[i] = _np.sin(phase) * (i/n) ** 0.5 * (1 - i/n) ** 0.3 * 0.38
    # Sustaining chord that rings out
    chord = _np.zeros(n, _np.float32)
    for f, v, tau in [(330, 0.30, 0.25), (440, 0.22, 0.20), (550, 0.16, 0.16), (660, 0.10, 0.12)]:
        chord += _np_sinev(n, f, v) * _np_exp(n, tau)
    # Bright sparkle texture
    spark = _np_bp(n, 2200, 800, 93) * _np.linspace(0.5, 1.0, n).astype(_np.float32) * 0.20
    spark *= _np.linspace(1.0, 0.0, n).astype(_np.float32) ** 0.5
    return _np_norm(_np_mix2(sweep, chord, spark) * _np_fade2(_np.ones(n, _np.float32), .010, .22))

def _gen_buff_divine():
    """Divine blessing resolution: warm mid-register bell chord.
    Sounds holy but approachable — like a benediction, not a squeak.
    Centroid ~600Hz — warm, present, clearly 'blessed'."""
    n = int(SR * 0.70)
    # Bell chord in mid register — not too high, not too low
    bell = _np.zeros(n, _np.float32)
    for f, v, tau in [(330, 0.42, 0.28), (440, 0.30, 0.22), (550, 0.20, 0.16),
                      (660, 0.12, 0.12), (247, 0.25, 0.32)]:
        bell += _np_sinev(n, f, v) * _np_exp(n, tau)
    bell = _np_lp(bell, 1800)
    # Soft initial transient — not harsh click
    n_c = int(SR * 0.008)
    click = _np_bp(n_c, 1000, 500, 95) * _np_exp(n_c, 0.003) * 0.35
    base = _np.zeros(n, _np.float32); base[:n_c] += click
    r = int(SR * 0.28); env = _np.ones(n, _np.float32); env[-r:] = _np.linspace(1, 0, r)
    return _np_norm(_np_mix2(base * 0.30, bell * env))

def _gen_buff_nature():
    """Nature buff: earthy growth sound — rising wooden resonance.
    Like roots pulling strength from soil. Centroid ~500Hz — grounded, organic."""
    n = int(SR * 0.60)
    # Root note + fifth with natural envelope (like a wood instrument)
    root  = _np_sinev(n, 165, 0.35) * _np.hanning(n).astype(_np.float32) ** 0.4 * _np_exp(n, 0.22)
    fifth = _np_sinev(n, 247, 0.25) * _np.hanning(n).astype(_np.float32) ** 0.4 * _np_exp(n, 0.18)
    oct2  = _np_sinev(n, 330, 0.18) * _np.hanning(n).astype(_np.float32) ** 0.4 * _np_exp(n, 0.15)
    # Woody texture
    wood  = _np_bp(n, 600, 250, 96) * _np.linspace(0.0, 1.0, n).astype(_np.float32) ** 0.6 * 0.22
    wood *= _np.linspace(1.0, 0.2, n).astype(_np.float32)
    # Initial thump — something taking root
    n_t = int(SR * 0.07)
    thud = (_np_sinev(n_t, 110, 0.45) + _np_bp(n_t, 220, 90, 97) * 0.30) * _np_exp(n_t, 0.04)
    out = _np.zeros(n, _np.float32)
    out[:n_t] += thud
    out += _np_mix2(root, fifth, oct2, wood) * 0.75
    return _np_norm(_np_fade2(out, .001, .20))

# ── Debuff variants (lower, more threatening, distinct per type) ─
def _gen_debuff_physical():
    """Thief mark / physical cripple — scrape and drag, weight being stripped away."""
    n = int(SR * 0.55)
    # Descending scrape (higher → lower, like something being stripped)
    scrape = _np.zeros(n, _np.float32); phase = 0.0
    for i in range(n):
        freq = 280 - 180 * (i/n) ** 0.6   # 280 → 100 Hz drop
        phase += 2 * _np.pi * freq / SR
        scrape[i] = _np.sin(phase) * (1 - i/n) ** 0.5 * 0.38
    scrape = _np_lp(scrape, 400)
    # Low grinding undertone
    grind = _np_bp(n, 140, 65, 100) * _np_exp(n, 0.14) * 0.45
    sub   = _np_sinev(n, 52, 0.28) * _np_exp(n, 0.18)
    return _np_norm(_np_mix2(scrape, grind, sub) * _np_fade2(_np.ones(n, _np.float32), .003, .20))

def _gen_debuff_magic():
    """Magical weakening curse — dark clashing dissonance, unsettling low tones."""
    n = int(SR * 0.60)
    # Two slightly detuned low notes clash — sounds wrong intentionally
    dark  = _np_sinev(n, 78, 0.32) * _np_exp(n, 0.16)
    clash = _np_sinev(n, 82, 0.22) * _np_exp(n, 0.13)    # 4Hz beating against dark
    sub   = _np_sinev(n, 39, 0.28) * _np_exp(n, 0.20)
    hiss  = _np_bp(n, 280, 110, 102) * _np_exp(n, 0.08) * 0.22
    return _np_norm(_np_mix2(dark, clash, sub, hiss) * _np_fade2(_np.ones(n, _np.float32), .005, .22))

def _gen_debuff_divine():
    """Divine curse / smite debuff — deep dissonant toll that feels like a judgement."""
    n = int(SR * 0.65)
    # Low bell toll — but at an unpleasant tritone interval
    toll  = _np_sinev(n, 146, 0.42) * _np_exp(n, 0.20)
    clash = _np_sinev(n, 155, 0.30) * _np_exp(n, 0.16)   # slightly sharp — dissonant
    low   = _np_sinev(n, 73,  0.25) * _np_exp(n, 0.22)
    rumble = _np_bp(n, 120, 55, 103) * _np_exp(n, 0.10) * 0.20
    return _np_norm(_np_mix2(toll, clash, low, rumble) * _np_fade2(_np.ones(n, _np.float32), .003, .25))

# ── Dungeon music tracks ──────────────────────────────────────
def _gen_dungeon(fn):
    if not _HAS_NUMPY: return None
    try:
        sig = fn()
        sig = _np.nan_to_num(sig, nan=0.0, posinf=0.0, neginf=0.0)
        d = (_np.clip(sig, -1, 1) * 32767).astype(_np.int16)
        return _make_sound(list(d))
    except Exception:
        return None


def _dungeon_goblin_warren():
    """Goblin Warren — 48s A-B-A'. Frantic drums + wailing horn + skittering noise."""
    N = int(SR * 48.0)
    # ── Drum pattern (runs full length, variations at 16s and 32s) ──────
    drums = _np.zeros(N, _np.float32)
    hits_a = [0.0,.18,.36,.75,.90,1.13,1.50,1.65,1.88,2.25,2.40,2.63,
               3.0,3.15,3.38,3.75,3.88,4.13,4.50,4.65,4.88,5.25,5.40,5.63,
               6.0,6.13,6.38,6.75,6.88,7.13,7.50,7.63,7.88]
    for rep in range(6):
        for i, dt in enumerate(hits_a):
            t = rep * 8.0 + dt
            if t >= 48.0: break
            # B-section (16-32s): heavier, slower hits
            if 16.0 <= t < 32.0:
                if i % 4 == 0:
                    n_h = int(SR*.22); h = _np_sinev(n_h,65,.55)*_np_exp(n_h,.05)
                elif i % 2 == 0:
                    n_h = int(SR*.12); h = _np_bp(n_h,500+i*20,200,i+30)*_np_exp(n_h,.03)*.35
                else: continue
            else:
                if i % 3 == 0:
                    n_h=int(SR*.18); h=_np_sinev(n_h,80+(i%5)*15,.45)*_np_exp(n_h,.04)+_np_bp(n_h,300,150,i)*_np_exp(n_h,.02)*.2
                else:
                    n_h=int(SR*.10); h=_np_bp(n_h,600+i*30,250,i+50)*_np_exp(n_h,.025)*.3
            _np_place2(drums, t, h)
    drums = _np_lp(drums, 1200)
    # ── Horn melody A (0-16s): short threatening phrase ──────────────────
    horn_a = [(110,.5),(147,.4),(165,.4),(147,.3),(130,.5),(110,.8),(98,.4),(110,1.0)]
    horn_ta = [0.0]; [horn_ta.append(horn_ta[-1]+d) for _,d in horn_a[:-1]]
    # ── Horn melody B (16-32s): answering phrase in different register ───
    horn_b = [(165,.6),(185,.5),(196,.5),(220,.8),(196,.4),(185,.5),(165,.6),(147,.4),(130,.8)]
    horn_tb = [0.0]; [horn_tb.append(horn_tb[-1]+d) for _,d in horn_b[:-1]]
    # ── Horn melody A' (32-48s): original phrase + harmony ───────────────
    horn = _np.zeros(N, _np.float32)
    for (freq, dur), t in zip(horn_a, horn_ta):
        for rep, offset in [(0, 0.0), (1, 8.0)]:
            nt = rep * 8.0 + t
            if nt < 16.0: _np_place2(horn, nt, _np_note(freq, dur, .22, .08))
    for (freq, dur), t in zip(horn_b, horn_tb):
        nt = 16.0 + t
        if nt < 32.0: _np_place2(horn, nt, _np_note(freq, dur, .20, .10))
    for (freq, dur), t in zip(horn_a, horn_ta):
        for rep, offset in [(0, 0.0), (1, 8.0)]:
            nt = 32.0 + rep * 8.0 + t
            if nt < 48.0:
                _np_place2(horn, nt, _np_note(freq, dur, .22, .08))
                if freq > 100:  # add rough harmony
                    _np_place2(horn, nt, _np_note(freq * 1.33, dur, .10, .10))
    horn = _np_lp(horn, 500)
    # ── Drone + scurry ───────────────────────────────────────────────────
    drone = (_np_sinev(N,55,.08)*_np_swell2(N,7.0,0,.4) +
             _np_bp(N,130,50,5)*_np_swell2(N,4.5,2,.5)*.05 +
             _np_sinev(N,41,.05)*_np_swell2(N,11.0,3,.35))   # deeper sub in B
    scurry = (_np_bp(N,2400,1200,6)*_np_swell2(N,1.1,.3,.8)*.04 +
              _np_bp(N,1800,800,7)*_np_swell2(N,1.6,.8,.7)*.03)
    return _np_seamless2(_np_norm(_np_mix2(drums*.8, horn*.7, drone, scurry)))


def _dungeon_spiders_nest():
    """Spider's Nest — 60s. Eerie overtone melody, relentless skittering, web hum."""
    N = int(SR * 60.0)
    # ── A-section melody (0-20s): high sparse tones ──────────────────────
    mel_a = [(880,1.2,.12),(622,1.0,.10),(740,1.4,.11),(554,1.0,.09),
             (880,1.0,.12),(831,.8,.10),(622,1.2,.09),(740,1.6,.11)]
    mel_ta = [0.0,1.8,3.2,5.0,7.5,9.0,11.5,14.0]
    # ── B-section melody (20-40s): drops an octave, darker ──────────────
    mel_b = [(440,1.8,.10),(311,1.4,.09),(370,1.8,.10),(277,1.2,.08),
             (440,1.2,.10),(415,1.0,.09),(311,1.5,.08),(370,2.0,.10)]
    mel_tb = [0.0,2.0,3.8,6.0,9.0,10.5,12.5,15.0]
    # ── A'-section (40-60s): both registers combined softly ──────────────
    mel = _np.zeros(N, _np.float32)
    for (freq, dur, vol), t in zip(mel_a, mel_ta):
        _np_place2(mel, t,       _np_note(freq, dur, vol, .4))
        _np_place2(mel, t+20.0, _np_note(freq*0.5, dur, vol*.7, .4))  # octave below in B
        _np_place2(mel, t+40.0, _np_note(freq, dur, vol*.85, .4))
        _np_place2(mel, t+40.0, _np_note(freq*0.5, dur, vol*.35, .4))
    mel = _np_lp(mel, 2000)
    # ── Skittering (full length, varies density) ─────────────────────────
    skitter = _np.zeros(N, _np.float32)
    rng = _np.random.default_rng(99)
    t_s = 0.0
    while t_s < 59.5:
        # Denser in B-section
        density = 0.25 if 20.0 <= t_s < 40.0 else 0.45
        gap = float(rng.uniform(0.04, density))
        n_s = int(SR * .025)
        s = _np_hp_filt(_np.random.default_rng(int(t_s*100)).standard_normal(n_s).astype(_np.float32), 3000)*_np_exp(n_s,.008)*float(rng.uniform(.1,.28))
        _np_place2(skitter, t_s, s)
        t_s += gap
    # ── Web drone (A/A': 62Hz, B: 52Hz) ──────────────────────────────────
    web_lo = _np_sinev(N,52,.08)*_np_swell2(N,14.0,0,.40)
    web_hi = _np_sinev(N,62,.10)*_np_swell2(N,12.0,0,.35)
    # fade web_hi out in B, back in A'
    env_web = _np.ones(N, _np.float32)
    b_start, b_end = int(SR*20), int(SR*40)
    env_web[b_start:b_end] = _np.linspace(1.0, 0.3, b_end-b_start)
    env_web[b_end:int(SR*48)] = _np.linspace(0.3, 1.0, int(SR*48)-b_end)
    web = (web_lo + web_hi * env_web)*_np_swell2(N,8.0,3.0,.45)
    # ── Snap events scattered throughout ─────────────────────────────────
    snaps = _np.zeros(N, _np.float32)
    for snap_t in [3.5,7.2,11.8,16.4,22.0,27.5,33.0,38.5,43.0,48.5,54.2,58.8]:
        n_sn = int(SR*.06)
        sn = _np_bp(n_sn,1200,600,int(snap_t*10))*_np_exp(n_sn,.015)*.15
        _np_place2(snaps, snap_t, sn)
    fading = _np_bp(N,3500,1500,7)*_np_swell2(N,6.0,1.5,.7)*.04*_np_swell2(N,2.2,0,.85)
    return _np_seamless2(_np_norm(_np_mix2(mel, skitter*.6, web, fading, snaps)))


def _dungeon_abandoned_mine():
    """Abandoned Mine — 54s. Pick rhythm, stone resonance, corrupt harmonic drift."""
    N = int(SR * 54.0)
    beat = 60.0 / 72
    picks = _np.zeros(N, _np.float32)
    for i in range(int(54.0 / beat)):
        t = i * beat
        # B-section (18-36s): slower, heavier strikes
        if 18.0 <= t < 36.0:
            if i % 8 == 0:
                vol = .38; n_p = int(SR*.20)
                strike = (_np_sinev(n_p,70,.50)+_np_bp(n_p,600,300,i)*_np_exp(n_p,.05)*.30)*_np_exp(n_p,.07)
            elif i % 4 == 0:
                vol = .24; n_p = int(SR*.15)
                strike = _np_bp(n_p,900,450,i+100)*_np_exp(n_p,.04)*vol
            else: continue
        else:
            vol = .28 if i%4==0 else (.18 if i%2==0 else .10)
            n_p = int(SR*.15)
            strike = _np_bp(n_p,800,400,i)*_np_exp(n_p,.04)*vol + _np_bp(n_p,2200,800,i+100)*_np_exp(n_p,.02)*vol*.3
        _np_place2(picks, t, strike)
    # ── Stone resonance: three chord zones ──────────────────────────────
    stone = _np.zeros(N, _np.float32)
    # A: E bass (65Hz) family
    for (freq,dur), t in zip([(65,.30),(55,.30),(49,.30),(58,.30)],[0.0,4.5,9.0,13.5]):
        n_st = min(int(SR*dur*4), N-int(SR*t)); n_st = max(0,n_st)
        if n_st>0:
            s = (_np_sinev(n_st,freq,.28)+_np_sinev(n_st,freq*2,.28*.3))*_np.minimum(_np.arange(n_st)/(SR*.15),1.0).astype(_np.float32)*_np_exp(n_st,.8)
            _np_place2(stone, t, s)
    # B: D bass (37Hz) — deeper, more ominous
    for (freq,dur), t in zip([(37,.40),(44,.30),(37,.40),(41,.30)],[18.0,22.5,27.0,31.5]):
        n_st = min(int(SR*dur*4), N-int(SR*t)); n_st = max(0,n_st)
        if n_st>0:
            s = (_np_sinev(n_st,freq,.32)+_np_sinev(n_st,freq*2,.32*.3))*_np.minimum(_np.arange(n_st)/(SR*.15),1.0).astype(_np.float32)*_np_exp(n_st,1.0)
            _np_place2(stone, t, s)
    # A': return to E, now with added dissonance (tritone Bb)
    for (freq,dur), t in zip([(65,.30),(55,.30),(49,.30),(58,.30)],[36.0,40.5,45.0,49.5]):
        n_st = min(int(SR*dur*4), N-int(SR*t)); n_st = max(0,n_st)
        if n_st>0:
            s = (_np_sinev(n_st,freq,.28)+_np_sinev(n_st,freq*2,.28*.3)+_np_sinev(n_st,freq*1.414,.10))*_np.minimum(_np.arange(n_st)/(SR*.15),1.0).astype(_np.float32)*_np_exp(n_st,.8)
            _np_place2(stone, t, s)
    stone = _np_lp(stone, 200)
    # ── Corrupt detuned tones (throughout) ───────────────────────────────
    corrupt = _np.zeros(N, _np.float32)
    for t in [2.0,5.5,8.0,11.5,14.5,17.0,19.5,23.0,26.5,30.0,33.5,
              37.0,40.5,44.0,47.5,50.5,53.0]:
        n_c = int(SR*.5)
        c = (_np_sinev(n_c,110,.15)+_np_sinev(n_c,116,.10))*_np_exp(n_c,.12)
        _np_place2(corrupt, t, c)
    creak = _np_bp(N,280,100,8)*_np_swell2(N,9.0,0,.6)*.06
    sub   = (_np_sinev(N,42,.06)*_np_swell2(N,15.0,0,.4) +
             _np_sinev(N,37,.04)*_np_swell2(N,20.0,5,.45))
    return _np_seamless2(_np_norm(_np_mix2(picks*.7, stone, corrupt, creak, sub)))


def _dungeon_ruins_ashenmoor():
    """Ruins of Ashenmoor — 66s. Heat shimmer, ash wind, rising shadow choir."""
    N = int(SR * 66.0)
    # ── Heat foundation (three oscillator clusters, evolving over 66s) ───
    heat = _np_lp(
        _np_sinev(N,87,.16)*_np_swell2(N,11.0,0,.45) +
        _np_sinev(N,92,.10)*_np_swell2(N,8.0,4,.50) +
        _np_sinev(N,58,.12)*_np_swell2(N,15.0,2,.35) +
        _np_sinev(N,78,.08)*_np_swell2(N,22.0,7,.40),  # slow pulse new
        300)
    ash = (_np_bp(N,650,250,10)*_np_swell2(N,7.0,0,.6)*.10 +
           _np_bp(N,1400,600,11)*_np_swell2(N,4.5,2.5,.7)*.05 +
           _np_bp(N,350,140,12)*_np_swell2(N,9.5,3,.55)*.07)
    # ── Flares — appear more frequently in B-section ────────────────────
    flares = _np.zeros(N, _np.float32)
    for t in [3.5,8.0,13.5,19.0, 23.5,27.0,31.5,36.0,40.5, 45.0,50.5,56.0,62.0]:
        n_f = int(SR*1.2)
        f = (_np_sinev(n_f,65,.20)+_np_bp(n_f,500,200,int(t*10))*.12)*_np.hanning(n_f).astype(_np.float32)**.5*.8
        _np_place2(flares, t, _np_lp(f, 400))
    # ── Shadow choir: A (0-22s) E-area, B (22-44s) Bb-area, A'(44-66s) both
    shadow = _np.zeros(N, _np.float32)
    for t,freq in [(1.0,196),(5.5,185),(11.0,175),(16.5,196)]:           # A
        n_sh=int(SR*2.5); sh=(_np_sinev(n_sh,freq,.14)*_np_exp(n_sh,.6)+_np_sinev(n_sh,freq*1.5,.07)*_np_exp(n_sh,.4))
        _np_place2(shadow, t, sh)
    for t,freq in [(23.0,233),(28.5,220),(34.0,207),(40.5,233)]:         # B: Bb area
        n_sh=int(SR*3.0); sh=(_np_sinev(n_sh,freq,.16)*_np_exp(n_sh,.7)+_np_sinev(n_sh,freq*1.5,.08)*_np_exp(n_sh,.5))
        _np_place2(shadow, t, sh)
    for t,freq in [(45.0,196),(50.5,185),(56.0,175),(61.5,233)]:         # A': E+Bb
        n_sh=int(SR*2.5); sh=(_np_sinev(n_sh,freq,.14)*_np_exp(n_sh,.6)+_np_sinev(n_sh,freq*1.5,.07)*_np_exp(n_sh,.4)+_np_sinev(n_sh,freq*2.76,.05)*_np_exp(n_sh,.3))
        _np_place2(shadow, t, sh)
    wail = (_np_bp(N,1800,400,12)*_np_swell2(N,18.0,0,.75)*.06 +
            _np_bp(N,2400,500,13)*_np_swell2(N,14.0,8,.65)*.04)
    return _np_seamless2(_np_norm(_np_mix2(heat, ash, flares, shadow, wail)))


def _dungeon_sunken_crypt():
    """Sunken Crypt — 60s. Dripping water, stone resonance, undead moans."""
    N = int(SR * 60.0)
    # ── Water drips — irregular, throughout ──────────────────────────────
    drips = _np.zeros(N, _np.float32)
    rng_d = _np.random.default_rng(33)
    drip_t = 0.0
    while drip_t < 59.5:
        freq = float(rng_d.uniform(700, 2800))
        gap  = float(rng_d.uniform(0.8, 3.5))
        n_d  = int(SR * .05)
        d = _np_bp(n_d,freq,400,int(drip_t*10))*_np_exp(n_d,.012)*float(rng_d.uniform(.10,.24))
        _np_place2(drips, drip_t, d)
        drip_t += gap
    # ── Crypt resonance: A (C# bass), B (B bass), A' (C# + chorus) ───────
    crypt = _np_lp(
        _np_sinev(N,73,.14)*_np_swell2(N,13.0,0,.40) +
        _np_sinev(N,55,.10)*_np_swell2(N,9.0,3,.45) +
        _np_sinev(N,61,.07)*_np_swell2(N,17.0,6,.38),   # 5th harmonic
        250)
    # ── Moaning voices: three separate events per section ─────────────────
    moan = _np.zeros(N, _np.float32)
    moan_events = [
        # A: 0-20s
        (2.5,165), (7.0,147), (13.5,155), (18.0,165),
        # B: 20-40s — lower and slower
        (22.0,130), (28.0,123), (33.5,138), (38.5,130),
        # A': 40-60s — both registers layered
        (42.5,165), (47.0,147), (52.5,155), (57.0,165),
        (43.0,123), (48.0,130), (53.5,138),
    ]
    for t,freq in moan_events:
        if t < 60.0:
            n_m = int(SR*2.5)
            m = (_np_sinev(n_m,freq,.09)+_np_sinev(n_m,freq*1.5,.04))*_np.hanning(n_m).astype(_np.float32)
            _np_place2(moan, t, _np_lp(m, 500))
    water = (_np_bp(N,180,80,14)*_np_swell2(N,6.0,0,.5)*.08 +
             _np_bp(N,80,35,15)*_np_swell2(N,8.5,2,.55)*.06 +
             _np_bp(N,240,90,16)*_np_swell2(N,11.0,4,.45)*.05)
    groans = _np.zeros(N, _np.float32)
    for t in [5.0,12.0,18.5,25.0,32.0,39.0,45.0,52.0,58.0]:
        n_g = int(SR*.9)
        g = _np_bp(n_g,200,80,int(t*5))*_np_exp(n_g,.2)*.18
        _np_place2(groans, t, g)
    return _np_seamless2(_np_norm(_np_mix2(drips*.8, crypt, moan, water, groans)))


def _dungeon_pale_coast():
    """Pale Coast — 72s. Haunted sea cave — D minor melody, crashing surf, echo."""
    N = int(SR * 72.0)
    # ── Melody A (0-24s): D minor descending ─────────────────────────────
    mel_a = [(293,1.5),(329,1.0),(349,1.5),(329,.8),(293,2.0),
             (261,1.5),(293,1.0),(329,2.5),(293,1.5),(261,1.0),
             (220,1.5),(247,1.0),(293,2.5)]
    mel_ta = [0.0]; [mel_ta.append(mel_ta[-1]+d) for _,d in mel_a[:-1]]
    # ── Melody B (24-48s): F major colour — brighter, wave-like ─────────
    mel_b = [(349,1.2),(392,1.0),(440,1.5),(392,.8),(349,1.5),
             (329,1.2),(349,1.0),(392,2.0),(349,1.5),(329,1.0),
             (293,2.0),(329,1.5),(349,3.0)]
    mel_tb = [0.0]; [mel_tb.append(mel_tb[-1]+d) for _,d in mel_b[:-1]]
    melody = _np.zeros(N, _np.float32)
    for (freq,dur),t in zip(mel_a, mel_ta):
        if t < 24.0: _np_place2(melody, t, _np_note(freq, dur*1.1, .18, .5))
    for (freq,dur),t in zip(mel_b, mel_tb):
        nt = 24.0 + t
        if nt < 48.0: _np_place2(melody, nt, _np_note(freq, dur*1.1, .16, .5))
    # A' (48-72s): original melody + soft harmony a 3rd above
    for (freq,dur),t in zip(mel_a, mel_ta):
        nt = 48.0 + t
        if nt < 72.0:
            _np_place2(melody, nt, _np_note(freq, dur*1.1, .18, .5))
            _np_place2(melody, nt, _np_note(freq*1.189, dur*1.1, .08, .5))  # minor 3rd
    melody = _np_lp(melody, 600)
    ocean = _np_lp(
        _np_bp(N,85,45,16)*_np_swell2(N,8.5,0,.55)*.18 +
        _np_bp(N,55,25,17)*_np_swell2(N,12.0,4,.50)*.12 +
        _np_bp(N,120,50,18)*_np_swell2(N,6.0,9,.45)*.09,
        250)
    drips = _np.zeros(N, _np.float32)
    for i,t in enumerate([1.5,4.2,6.8,9.1,11.7,14.3,16.9,19.4,21.8,
                           25.0,28.5,32.0,35.5,39.0,42.5,46.0,
                           50.0,53.5,57.0,60.5,64.0,67.5,71.0]):
        n_d = int(SR*.06)
        d = _np_bp(n_d,500+i*60,200,i+300)*_np_exp(n_d,.018)*.14
        _np_place2(drips, t, d)
    presence = (_np_sinev(N,293,.06)*_np_swell2(N,20.0,0,.6) +
                _np_sinev(N,440,.03)*_np_swell2(N,15.0,6,.7) +
                _np_sinev(N,220,.04)*_np_swell2(N,25.0,10,.5))
    return _np_seamless2(_np_norm(_np_mix2(melody*.75, ocean, drips, presence)))


def _dungeon_windswept_isle():
    """Windswept Isle — 66s. Aeolian harmonics, stone guardian hum, howling wind."""
    N = int(SR * 66.0)
    # ── Harmony A (0-22s): E Aeolian long tones ──────────────────────────
    harm_a = [(165,3.0),(175,2.0),(196,2.5),(175,1.5),(165,3.5),(147,2.0),(165,3.0),(196,4.5)]
    harm_ta = [0.0]; [harm_ta.append(harm_ta[-1]+d) for _,d in harm_a[:-1]]
    # ── Harmony B (22-44s): shifts to G — slightly warmer, then back ─────
    harm_b = [(196,3.0),(220,2.5),(247,3.0),(220,2.0),(196,3.5),(175,2.5),(196,3.0),(220,4.0)]
    harm_tb = [0.0]; [harm_tb.append(harm_tb[-1]+d) for _,d in harm_b[:-1]]
    harmony = _np.zeros(N, _np.float32)
    for section_t, harm_data, harm_times in [
        (0.0, harm_a, harm_ta), (22.0, harm_b, harm_tb), (44.0, harm_a, harm_ta)
    ]:
        for (freq,dur),t in zip(harm_data, harm_times):
            nt = section_t + t
            if nt < 66.0:
                n_h = int(SR*dur)
                h = (_np_sinev(n_h,freq,.20)+_np_sinev(n_h,freq*2,.10)+_np_sinev(n_h,freq*3,.05))
                env = _np.minimum(_np.arange(n_h)/(SR*.1),1.0).astype(_np.float32)*_np_exp(n_h,.8)
                _np_place2(harmony, nt, (h*env).astype(_np.float32))
    wind_int = (_np_bp(N,380,200,18)*_np_swell2(N,5.0,0,.6)*.14 +
                _np_bp(N,180,80,19)*_np_swell2(N,7.5,2.5,.5)*.08 +
                _np_bp(N,600,250,20)*_np_swell2(N,3.5,4,.55)*.06)
    stone_hum = (_np_sinev(N,82,.10)*_np_swell2(N,18.0,0,.4) +
                 _np_sinev(N,123,.06)*_np_swell2(N,11.0,5,.5) +
                 _np_sinev(N,61,.07)*_np_swell2(N,22.0,8,.45))
    # ── Guardian low drones — shift register in B ────────────────────────
    guardian = _np.zeros(N, _np.float32)
    for t,freq in [(0.0,55),(22.0,49),(44.0,55)]:
        n_g = int(SR*22.0)
        if int(SR*t)+n_g <= N:
            g = _np_sinev(n_g,freq,.09)*_np_exp(n_g,4.0)
            _np_place2(guardian, t, g)
    for t,freq in [(0.0,73),(22.0,67),(44.0,73)]:
        n_g = int(SR*22.0)
        if int(SR*t)+n_g <= N:
            g = _np_sinev(n_g,freq,.06)*_np_exp(n_g,5.0)
            _np_place2(guardian, t, g)
    guardian = _np_lp(guardian, 150)
    return _np_seamless2(_np_norm(_np_mix2(harmony*.70, wind_int, stone_hum, guardian)))


def _dungeon_dragons_tooth():
    """Dragon's Tooth — 60s. Seismic bass, superheated air, deep dragon breath."""
    N = int(SR * 60.0)
    seismic = _np_lp(
        _np_sinev(N,28,.22)*_np_swell2(N,9.0,0,.50) +
        _np_sinev(N,42,.14)*_np_swell2(N,6.5,3,.55) +
        _np_sinev(N,21,.10)*_np_swell2(N,13.0,5,.42),   # sub-bass undertone
        100)
    heat = (_np_bp(N,220,90,20)*_np_swell2(N,4.5,0,.6)*.14 +
            _np_bp(N,120,55,21)*_np_swell2(N,7.0,2.5,.55)*.10 +
            _np_bp(N,340,130,22)*_np_swell2(N,5.5,6,.50)*.08)
    # ── Dragon breath events — one per ~10s ──────────────────────────────
    breath = _np.zeros(N, _np.float32)
    for t,vol in [(0.0,.22),(10.0,.26),(20.0,.20),(30.0,.28),(40.0,.22),(50.0,.24)]:
        n_b = int(SR*4.0)
        b = _np_bp(n_b,95,45,int(t*5))*_np_swell2(n_b,4.0,0,.6)*vol*_np.hanning(n_b).astype(_np.float32)**.6
        _np_place2(breath, t, _np_lp(b, 300))
    # ── Stone collapse events ─────────────────────────────────────────────
    stones = _np.zeros(N, _np.float32)
    for t,vol in [(1.5,.35),(4.2,.28),(7.8,.40),(11.3,.32),(14.0,.38),(17.5,.30),
                  (21.5,.36),(25.0,.30),(29.0,.42),(33.5,.34),(38.0,.38),
                  (42.5,.36),(46.0,.30),(50.5,.40),(54.0,.34),(57.5,.32)]:
        n_s = int(SR*.45)
        s = (_np_sinev(n_s,55,.5)+_np_bp(n_s,300,150,int(t*20))*.3)*_np_exp(n_s,.08)*vol
        _np_place2(stones, t, s)
    stones = _np_lp(stones, 400)
    # ── Karreth thematic motif: A (B2), B-section (G2), A' (B2+harmony) ─
    karreth = _np.zeros(N, _np.float32)
    for t,freq in [(2.0,98),(6.5,87),(11.0,98),(15.5,73)]:            # A
        _np_place2(karreth, t, _np_note(freq, 2.0, .22, .35))
    for t,freq in [(22.0,82),(27.5,73),(32.0,82),(37.5,61)]:           # B: lower
        _np_place2(karreth, t, _np_note(freq, 2.5, .24, .40))
    for t,freq in [(42.0,98),(46.5,87),(51.0,98),(55.5,73)]:           # A'
        _np_place2(karreth, t, _np_note(freq, 2.0, .22, .35))
        _np_place2(karreth, t, _np_note(freq*1.5, 2.0, .10, .35))     # harmony
    karreth = _np_lp(karreth, 400)
    return _np_seamless2(_np_norm(_np_mix2(seismic, heat, breath, stones, karreth*.8)))


def _dungeon_valdris_spire():
    """Valdris' Spire — 84s. Imperial march decays into Fading corruption. Full arc."""
    N = int(SR * 84.0)
    # ── Foundation: slow swell drones throughout ─────────────────────────
    foundation = _np_lp(
        _np_sinev(N,36,.20)*_np_swell2(N,14.0,0,.40) +
        _np_sinev(N,54,.12)*_np_swell2(N,9.5,5,.45) +
        _np_sinev(N,27,.10)*_np_swell2(N,20.0,0,.35) +
        _np_sinev(N,48,.07)*_np_swell2(N,28.0,8,.38),
        180)
    # ── Melody: A (0-28s), B/development (28-56s), A' climax (56-84s) ───
    mel_a = [(123,2.5),(147,2.0),(165,2.5),(185,3.0),(196,2.0),(220,2.5),(196,1.5),(185,2.0),(165,2.5),(147,2.0),(123,3.5)]
    mel_b = [(185,2.0),(220,2.5),(247,2.0),(277,3.0),(247,1.5),(220,2.5),(185,2.0),(165,3.0),(147,2.5),(165,2.0),(185,3.5)]
    v_mel = _np.zeros(N, _np.float32)
    dark_h = _np.zeros(N, _np.float32)
    for mel, t_offset in [(mel_a, 0.0), (mel_b, 28.0), (mel_a, 56.0)]:
        mt = [0.0]; [mt.append(mt[-1]+d) for _,d in mel[:-1]]
        for (freq,dur),t in zip(mel, mt):
            nt = t_offset + t
            if nt < 84.0:
                _np_place2(v_mel, nt, _np_note(freq, dur*1.2, .20, .6))
                _np_place2(dark_h, nt, _np_note(freq*1.414, dur*1.2, .10, .5))
                # A' gets upper octave too
                if t_offset == 56.0:
                    _np_place2(v_mel, nt, _np_note(freq*2, dur*1.2, .12, .5))
    v_mel  = _np_lp(v_mel,  800)
    dark_h = _np_lp(dark_h, 600)
    # ── Drums: enter at bar 2, more complex in B, thundering in A' ───────
    beat = 60.0 / 65
    drums = _np.zeros(N, _np.float32)
    for i in range(int(84.0 / beat)):
        t = i * beat
        if t < 4.0: continue   # silence before drums enter
        if t >= 56.0:           # A': double-time feel
            vol = .40 if i%4==0 else (.26 if i%2==0 else .16)
        else:
            vol = .32 if i%4==0 else (.20 if i%2==0 else .12)
        n_d = int(SR*.35)
        d = _np_sinev(n_d,45,.5)*_np_exp(n_d,.06)*vol + _np_bp(n_d,250,120,i*7)*_np_exp(n_d,.03)*vol*.4
        _np_place2(drums, t, d)
    drums = _np_lp(drums, 300)
    fading_hiss = (_np_bp(N,4000,2000,22)*_np_swell2(N,7.0,0,.8)*.05*_np_swell2(N,3.5,1.5,.7) +
                   _np_bp(N,6000,3000,23)*_np_swell2(N,4.5,12,.75)*.03)
    ascend = (_np_bp(N,550,200,23)*_np_swell2(N,28.0,_np.pi,.70)*.10 +
              _np_bp(N,380,150,24)*_np_swell2(N,28.0,_np.pi*.7,.65)*.07 +
              _np_bp(N,750,200,25)*_np_swell2(N,42.0,_np.pi*1.2,.60)*.06)
    return _np_seamless2(_np_norm(_np_mix2(foundation, v_mel*.75, dark_h*.6, drums*.7, fading_hiss, ascend)))


def _gen_step_footstep():
    """Footstep on hardwood/stone floor.
    A sharp click-tap with a very brief, tight body — no hollow resonance.
    Think shoe sole striking a hard surface: percussive, present, fast decay.
    Structure: 4ms sharp click → 35ms tight tap body → silence."""
    # Sharp click transient: broadband noise burst shaped with a very fast decay.
    # Not pure sines — those ring too much. Noise + fast exp = natural tap character.
    n_click = int(SR * 0.004)   # 4ms
    rng = _np.random.default_rng(17)
    click_noise = rng.standard_normal(n_click).astype(_np.float32)
    click_noise = _np_bp(n_click, 2200, 1400, 500)     # focus noise on tap frequency
    click_noise *= _np_exp(n_click, 0.0008) * 0.90     # very fast decay
    # Tap body: tight bandpass noise shaped like a struck hard surface
    # 600-900Hz = the "tack" of a sole — not 280Hz which is boxy/hollow
    n_body = int(SR * 0.035)   # 35ms
    body = _np_bp(n_body, 700, 350, 501)               # tap centre frequency
    body *= _np_exp(n_body, 0.008) * 0.65              # fast but not instant decay
    body *= _np_fade2(_np.ones(n_body, _np.float32), 0.0005, 0.010)
    # Very brief low thud (floor gives back a little energy) — kept quiet
    n_thud = int(SR * 0.025)   # 25ms
    thud = _np_sinev(n_thud, 420, 0.22) * _np_exp(n_thud, 0.012)
    thud *= _np_fade2(_np.ones(n_thud, _np.float32), 0.001, 0.008)
    # Assemble: click → body (overlapping slightly) → quiet thud
    n_total = n_click + n_body
    out = _np.zeros(n_total, _np.float32)
    out[:n_click] += click_noise
    out[n_click:n_click + n_body] += body
    out[n_click:n_click + n_thud] += thud * 0.40   # thud under the body
    return _np_norm(out)


# ── Wind-up generators (phase 1 of two-phase combat sounds) ───

def _gen_swing_light():
    """Light weapon: quick snapping whoosh — dagger or short blade cutting air.
    High bright hiss with fast attack, centroid ~2200Hz."""
    n = int(SR * 0.22)
    env = _np.zeros(n, _np.float32)
    peak = int(n * 0.35)   # peaks early — fast snap
    env[:peak] = _np.linspace(0.0, 1.0, peak) ** 0.5
    env[peak:] = _np.linspace(1.0, 0.0, n - peak) ** 1.0
    # Sharp air-cutting hiss — the defining sound of a light blade
    hiss   = _np_bp(n, 2800, 1400, 200) * env * 0.65   # bright edge hiss
    mid    = _np_bp(n, 1100, 500,  201) * env * 0.50   # air body
    body   = _np_bp(n, 420,  180,  202) * env * 0.30   # low presence
    return _np_norm(_np_mix2(hiss, mid, body) * _np_fade2(_np.ones(n, _np.float32), .001, .05))

def _gen_swing_medium():
    """Medium weapon: classic sword whoosh — broad air displacement.
    Clear swooping presence, centroid ~1400Hz."""
    n = int(SR * 0.34)
    env = _np.zeros(n, _np.float32)
    peak = int(n * 0.45)
    env[:peak] = _np.linspace(0.0, 1.0, peak) ** 0.55
    env[peak:] = _np.linspace(1.0, 0.0, n - peak) ** 0.85
    # Broad whoosh — air parted by a full blade
    whoosh = _np_bp(n, 1600, 900, 210) * env * 0.60    # main whoosh band
    hiss   = _np_bp(n, 3200, 1200, 211) * env * 0.30   # edge brightness
    body   = _np_bp(n, 500,  200,  212) * env * 0.45   # displaced air mass
    deep   = _np_sinev(n, 110, 0.18) * env * _np_exp(n, 0.12)  # weapon weight
    return _np_norm(_np_mix2(whoosh, hiss, body, deep) * _np_fade2(_np.ones(n, _np.float32), .001, .08))

def _gen_swing_heavy():
    """Heavy weapon: powerful labouring whoosh — hammer or greataxe.
    Deep air displacement with audible weapon mass, centroid ~900Hz."""
    n = int(SR * 0.48)
    env = _np.zeros(n, _np.float32)
    peak = int(n * 0.45)
    env[:peak] = _np.linspace(0.0, 1.0, peak) ** 0.45   # slower build (weapon is heavy)
    env[peak:] = _np.linspace(1.0, 0.0, n - peak) ** 0.75
    # Broad deep whoosh — massive air displacement
    whoosh = _np_bp(n, 900,  450, 220) * env * 0.65    # main whoosh
    hiss   = _np_bp(n, 2200, 900, 221) * env * 0.35    # air hiss still present
    mass   = _np_bp(n, 350,  150, 222) * env * 0.55    # weapon mass moving
    rumble = _np_sinev(n, 90, 0.28) * env * _np_exp(n, 0.18)  # sub presence
    return _np_norm(_np_mix2(whoosh, hiss, mass, rumble) * _np_fade2(_np.ones(n, _np.float32), .003, .14))

def _gen_swing_skill():
    """Physical skill wind-up: deliberate, powerful preparation — NOT a casual whoosh.
    Sounds like a warrior coiling and releasing focused force.
    Distinct from regular swings: starts with a low grunt-energy build,
    then a short controlled blade snap — 0.45s total, heavier character.
    Regular swing = air movement. Skill swing = focused power being released."""
    n = int(SR * 0.45)
    # Low 'coiling' energy builds for first half — weight shifting, muscles loading
    n_build = int(SR * 0.20)
    build = _np.zeros(n_build, _np.float32)
    for f, v in [(180, 0.35), (260, 0.22), (360, 0.14)]:
        # Each tone rises in volume — energy accumulating
        ramp = _np.linspace(0.0, 1.0, n_build).astype(_np.float32) ** 0.7
        build += _np_sinev(n_build, f, v) * ramp
    build = _np_lp(build, 700)
    # Sharp controlled release — a single decisive blade snap (shorter than casual swing)
    n_snap = int(SR * 0.18)
    env_snap = _np.zeros(n_snap, _np.float32)
    pk = int(n_snap * 0.25)   # peaks early for snappy attack
    env_snap[:pk] = _np.linspace(0.0, 1.0, pk) ** 0.4
    env_snap[pk:] = _np.linspace(1.0, 0.0, n_snap - pk) ** 0.7
    snap_hiss  = _np_bp(n_snap, 2000, 900, 225) * env_snap * 0.65
    snap_body  = _np_bp(n_snap, 700,  300, 226) * env_snap * 0.55
    snap_deep  = _np_sinev(n_snap, 130, 0.25) * env_snap * _np_exp(n_snap, 0.08)
    snap = _np_mix2(snap_hiss, snap_body, snap_deep)
    # Combine: build → snap
    out = _np.zeros(n, _np.float32)
    t_snap = int(SR * 0.22)
    out[:n_build] += build * 0.55
    out[t_snap:t_snap + n_snap] += snap
    return _np_norm(_np_fade2(out, .002, .12))


def _gen_cast_attack():
    """Spell attack charge: rising crackle of energy with clear presence.
    Starts as a low hum, rises through mid frequencies to a bright peak.
    Centroid target ~600Hz — present and audible, not buried."""
    n = int(SR * 0.40)
    ramp = _np.linspace(0.0, 1.0, n).astype(_np.float32)
    # Rising tone sweep — 150Hz → 600Hz, clearly audible build
    charge = _np.zeros(n, _np.float32)
    phase = 0.0
    for i in range(n):
        frac = i / n
        freq = 150 + 450 * (frac ** 1.2)   # 150 → 600Hz
        phase += 2 * _np.pi * freq / SR
        charge[i] = _np.sin(phase) * (frac ** 0.6) * 0.40
    # Harmonic shimmer at mid frequencies — gives "magical" feel
    shimmer = _np.zeros(n, _np.float32)
    for f, v in [(320, 0.20), (480, 0.15), (640, 0.10)]:
        shimmer += _np_sinev(n, f, v) * (ramp ** 1.0)
    shimmer = _np_lp(shimmer, 1200)
    # Electrical crackle texture building in
    crackle = _np_bp(n, 1400, 700, 230) * (ramp ** 1.8) * 0.18
    env = _np_fade2(_np.ones(n, _np.float32), .008, .06)
    return _np_norm(_np_mix2(charge, shimmer, crackle) * env)

def _gen_cast_buff_self():
    """Physical self-buff: weapon raised + short metallic ring + power chord.
    Sounds like a warrior snapping into battle stance — energising, not droning.
    The 'shing' of metal + a rising two-note power motif."""
    n = int(SR * 0.40)
    # Short bright metallic transient at onset — weapon/armor metal
    n_sting = int(SR * 0.08)
    sting = _np.zeros(n_sting, _np.float32)
    for f, v, tau in [(1800, 0.35, 0.04), (2400, 0.22, 0.03), (900, 0.28, 0.05)]:
        sting += _np_sinev(n_sting, f, v) * _np_exp(n_sting, tau)
    sting = _np_lp(sting, 3000)
    # Rising power chord — two notes ascending = gain strength feeling
    chord = _np.zeros(n, _np.float32)
    n_note = int(SR * 0.20)
    note1 = _np_sinev(n_note, 220, 0.32) * _np.hanning(n_note).astype(_np.float32) ** 0.5
    note2 = _np_sinev(n_note, 330, 0.24) * _np.hanning(n_note).astype(_np.float32) ** 0.5
    note3 = _np_sinev(n_note, 440, 0.18) * _np.hanning(n_note).astype(_np.float32) ** 0.5
    chord[:n_note] += note1
    t2 = int(SR * 0.10)
    chord[t2:t2+n_note] += note2
    t3 = int(SR * 0.20)
    chord[t3:min(t3+n_note,n)] += note3[:max(0,n-t3)]
    # Add weight — low body under the brightness
    body = _np_bp(n, 350, 150, 241) * _np.linspace(0.0, 1.0, n).astype(_np.float32) ** 0.8 * 0.35
    out = _np.zeros(n, _np.float32)
    out[:n_sting] += sting * 0.80
    out += chord * 0.70 + body
    return _np_norm(_np_fade2(out, .001, .14))

def _gen_cast_buff_spell():
    """Spell buff/blessing preparation: ethereal rising shimmer — unmistakably magical.
    NO ascending chord tones like cast_buff_self. Instead: pairs of slightly
    detuned sine waves that shimmer and beat against each other, like a singing bowl
    or harp harmonic. Feels like magic being woven, not a warrior steeling himself.
    The beating frequency (4-8Hz) creates a shimmering, alive quality."""
    n = int(SR * 0.50)
    ramp = _np.linspace(0.0, 1.0, n).astype(_np.float32) ** 0.9
    # Three pairs of slightly detuned sines — each pair creates audible beating/shimmer
    # This is completely unlike any physical sound and clearly 'magical'
    shimmer = _np.zeros(n, _np.float32)
    pairs = [
        (523, 527, 0.28),    # ~4Hz beat at C5
        (784, 790, 0.20),    # ~6Hz beat at G5
        (659, 666, 0.14),    # ~7Hz beat at E5
    ]
    for f1, f2, vol in pairs:
        shimmer += (_np_sinev(n, f1, vol) + _np_sinev(n, f2, vol * 0.85)) * ramp
    # Stagger the onset of upper pair — like notes being plucked in sequence
    onset2 = int(SR * 0.12)
    onset3 = int(SR * 0.22)
    shimmer[onset2:] += (_np_sinev(n - onset2, 784, 0.16) +
                          _np_sinev(n - onset2, 790, 0.14)) * ramp[:n - onset2]
    shimmer[onset3:] += (_np_sinev(n - onset3, 1047, 0.10) +
                          _np_sinev(n - onset3, 1052, 0.09)) * ramp[:n - onset3]
    # Low warm pad underneath — a cleric's blessing has a grounded quality
    pad = _np_sinev(n, 261, 0.18) * ramp * _np_exp(n, 0.35)
    pad = _np_lp(pad, 600)
    env = _np_fade2(_np.ones(n, _np.float32), .008, .18)
    return _np_norm(_np_mix2(shimmer, pad) * env)

def _gen_cast_debuff():
    """Enemy debuff: tense descending scrape — knife being drawn across stone.
    Audible threat. Centroid ~800Hz — present, menacing, not too low."""
    n = int(SR * 0.32)
    # Descending sweep — something being pulled down
    sweep = _np.zeros(n, _np.float32)
    phase = 0.0
    for i in range(n):
        frac = i / n
        freq = 1200 - 800 * (frac ** 0.6)   # 1200 → 400Hz descent
        phase += 2 * _np.pi * freq / SR
        sweep[i] = _np.sin(phase) * min(frac * 5, 1.0) * (1 - frac) ** 0.6 * 0.35
    # Scratchy noise texture — knife/blade quality
    scratch = _np_bp(n, 1800, 900, 260) * _np.linspace(0.4, 1.0, n).astype(_np.float32) ** 0.5 * 0.28
    scratch *= _np.linspace(1.0, 0.2, n).astype(_np.float32)   # fade out
    body = _np_bp(n, 500, 220, 261) * _np.linspace(0.0, 1.0, n).astype(_np.float32) ** 0.7 * 0.30
    return _np_norm(_np_fade2(_np_mix2(sweep, scratch, body), .002, .10))


# ── Redesigned resolution generators (all lower, longer) ──────

def _gen_death_enemy():
    """Enemy death: heavy collapse — body weight hitting stone floor.
    Long, low, unmistakable. Three phases: final blow resonance → crumple → ground thud."""
    n = int(SR * 1.20)
    # Phase 1 (0-0.3s): resonance of killing blow
    n1 = int(SR * 0.30)
    ring = _np.zeros(n, _np.float32)
    for f, v, tau in [(78, 0.40, 0.18), (124, 0.25, 0.12), (52, 0.30, 0.22)]:
        ring[:n1] += _np_sinev(n1, f, v) * _np_exp(n1, tau)
    # Phase 2 (0.25-0.65s): crumple / armour scrape
    n2 = int(SR * 0.40); t2 = int(SR * 0.25)
    crumple = _np_bp(n2, 180, 90, 300) * _np_exp(n2, 0.12) * 0.45
    scrape  = _np_bp(n2, 380, 160, 301) * _np_exp(n2, 0.08) * 0.28
    crumple_mix = _np_mix2(crumple, scrape) * _np.hanning(n2).astype(_np.float32) ** 0.4
    out = _np.zeros(n, _np.float32)
    out[:n1] += ring
    out[t2:t2 + n2] += crumple_mix
    # Phase 3 (0.60-1.2s): heavy floor impact thud
    t3 = int(SR * 0.60); n3 = int(SR * 0.55)
    thud = (_np_sinev(n3, 45, 0.55) + _np_sinev(n3, 72, 0.32) +
            _np_bp(n3, 130, 60, 302) * 0.40) * _np_exp(n3, 0.18)
    out[t3:t3 + n3] += thud
    return _np_norm(_np_fade2(out, .001, .35))

def _gen_death_player():
    """Player death: slower, more anguished — armour collapse over a full second.
    Deeper and more resonant than enemy death."""
    n = int(SR * 1.40)
    out = _np.zeros(n, _np.float32)
    # Low toll — like a bell struck in a bad way
    n1 = int(SR * 0.50)
    toll = _np.zeros(n1, _np.float32)
    for f, v, tau in [(58, 0.45, 0.30), (87, 0.28, 0.22), (43, 0.35, 0.38)]:
        toll += _np_sinev(n1, f, v) * _np_exp(n1, tau)
    out[:n1] += toll
    # Armour crumple (0.4-0.9s)
    t2 = int(SR * 0.40); n2 = int(SR * 0.50)
    crumple = _np_bp(n2, 150, 70, 310) * _np_exp(n2, 0.15) * 0.50
    scrape  = _np_bp(n2, 280, 120, 311) * _np_exp(n2, 0.10) * 0.30
    out[t2:t2 + n2] += _np_mix2(crumple, scrape) * _np.hanning(n2).astype(_np.float32) ** 0.5
    # Final floor thud (0.85-1.4s)
    t3 = int(SR * 0.85); n3 = int(SR * 0.55)
    thud = (_np_sinev(n3, 38, 0.60) + _np_bp(n3, 100, 50, 312) * 0.45) * _np_exp(n3, 0.25)
    out[t3:t3 + n3] += thud
    return _np_norm(_np_fade2(out, .001, .40))


# ── Town music generators ──────────────────────────────────────

def _town_briarhollow():
    """Briarhollow — 60s warm G-major folk. A (lute melody) B (counter-melody) A'."""
    N = int(SR * 60.0)
    # ── Melody: two full passes + variation ──────────────────────────────
    mel_a = [(196,.50),(293,.38),(329,.38),(392,.50),(440,.38),(494,.38),
             (392,.75),(440,.38),(293,.75),(196,.50),(247,.38),(293,.38),
             (329,.50),(293,.38),(247,.38),(196,1.00),
             (220,.38),(247,.38),(293,.50),(329,.38),(392,.50),(440,.38),
             (392,.75),(329,.38),(293,.50),(247,.75),(196,1.25)]
    mel_ta = [0.0]; [mel_ta.append(mel_ta[-1]+d) for _,d in mel_a[:-1]]
    # ── B-section melody: higher register, more ornate ───────────────────
    mel_b = [(392,.50),(440,.38),(494,.50),(523,.75),(494,.38),(440,.50),
             (392,.75),(440,.38),(392,.38),(349,.50),(392,.38),(329,.75),
             (293,.50),(329,.38),(349,.50),(392,.75),(329,.38),(293,.50),(247,1.25)]
    mel_tb = [0.0]; [mel_tb.append(mel_tb[-1]+d) for _,d in mel_b[:-1]]
    melody = _np.zeros(N, _np.float32)
    # Pass A (0-20s)
    for (freq,dur),t in zip(mel_a, mel_ta):
        if t < 20.0: _np_place2(melody, t, _np_note(freq, dur*1.1, .22, .18))
    # Pass B (20-40s): high register
    for (freq,dur),t in zip(mel_b, mel_tb):
        nt = 20.0 + t
        if nt < 40.0: _np_place2(melody, nt, _np_note(freq, dur*1.1, .20, .18))
    # Pass A' (40-60s): original + lower harmony
    for (freq,dur),t in zip(mel_a, mel_ta):
        nt = 40.0 + t
        if nt < 60.0:
            _np_place2(melody, nt, _np_note(freq, dur*1.1, .22, .18))
            _np_place2(melody, nt, _np_note(freq*0.75, dur*1.1, .10, .20))
    melody = _np_lp(melody, 1200)
    # ── Counter-melody (enters at 10s, richer in A') ──────────────────────
    cnt = [(98,.75),(123,.50),(147,.75),(130,.50),(98,1.0),(110,.50),(123,.75),(98,1.0),
           (110,.75),(130,.50),(147,.75),(130,.50),(123,1.0),(110,.50),(98,.75),(87,1.25)]
    cnt_t = [0.0]; [cnt_t.append(cnt_t[-1]+d) for _,d in cnt[:-1]]
    counter = _np.zeros(N, _np.float32)
    for (freq,dur),t in zip(cnt, cnt_t):
        for t_off in [10.0, 30.0, 50.0]:
            nt = t_off + t
            if nt < 60.0:
                vol = .16 if t_off < 40.0 else .20
                _np_place2(counter, nt, _np_note(freq, dur*1.3, vol, .25))
    counter = _np_lp(counter, 600)
    # ── Drums: 120bpm throughout, B-section adds hi-hat fills ────────────
    beat = 60.0 / 120
    drum = _np.zeros(N, _np.float32)
    for i in range(int(60.0 / beat)):
        t = i * beat
        if i % 4 == 0:
            n_d = int(SR*.14); d = _np_sinev(n_d,120,.40)*_np_exp(n_d,.04)+_np_bp(n_d,300,150,i)*_np_exp(n_d,.02)*.2
        elif i % 2 == 0:
            n_d = int(SR*.10); d = _np_bp(n_d,800,350,i+40)*_np_exp(n_d,.025)*.28
        elif 20.0 <= t < 40.0:   # B-section hi-hat fills
            n_d = int(SR*.05); d = _np_bp(n_d,4000,2000,i+80)*_np_exp(n_d,.010)*.16
        else:
            n_d = int(SR*.06); d = _np_bp(n_d,3500,1500,i+80)*_np_exp(n_d,.012)*.14
        _np_place2(drum, t, d)
    drum = _np_lp(drum, 2000)
    drone = (_np_sinev(N,98,.10)*_np_swell2(N,10.0,0,.5) +
             _np_sinev(N,196,.06)*_np_swell2(N,7.0,3,.4) +
             _np_sinev(N,147,.04)*_np_swell2(N,14.0,5,.38))
    drone = _np_lp(drone, 400)
    murmur = (_np_bp(N,350,180,42)*_np_swell2(N,4.5,0,.7)*.04 +
              _np_bp(N,600,200,43)*_np_swell2(N,3.0,2,.6)*.02)
    return _np_seamless2(_np_norm(_np_mix2(melody*.75, counter*.55, drum*.55, drone, murmur)))


def _town_woodhaven():
    """Woodhaven — 66s D-Dorian pan flute. A (flowing), B (rhythmic), A' (full)."""
    N = int(SR * 66.0)
    # ── Melody A: D Dorian pan flute flowing ─────────────────────────────
    mel_a = [(293,.60),(329,.40),(349,.60),(392,.80),(440,.60),(494,.40),
             (523,.80),(494,.40),(440,.60),(392,.80),(349,.40),(329,.60),(293,1.20),
             (246,.40),(261,.60),(293,.80),(329,.60),(392,.40),(440,.80),
             (392,.60),(349,.40),(329,.60),(293,.80),(246,.40),(220,1.20)]
    mel_ta = [0.0]; [mel_ta.append(mel_ta[-1]+d) for _,d in mel_a[:-1]]
    # ── Melody B (22-44s): same scale, more rhythmic short notes ─────────
    mel_b = [(293,.30),(329,.30),(392,.40),(440,.30),(392,.30),(349,.30),(329,.40),
             (293,.60),(261,.30),(293,.30),(329,.40),(392,.30),(440,.60),(494,.30),
             (523,.40),(494,.30),(440,.40),(392,.30),(349,.60),(329,.30),(293,.80)]
    mel_tb = [0.0]; [mel_tb.append(mel_tb[-1]+d) for _,d in mel_b[:-1]]
    melody = _np.zeros(N, _np.float32)
    for (freq,dur),t in zip(mel_a, mel_ta):
        if t < 22.0:
            n = int(SR*dur*1.2)
            env = _np.minimum(_np.arange(n)/(SR*.03),1.0).astype(_np.float32)*_np_exp(n,.5)
            s = (_np_sinev(n,freq,.28)+_np_sinev(n,freq*3,.06))*env
            _np_place2(melody, t, _np_lp(s, 1800))
    for (freq,dur),t in zip(mel_b, mel_tb):
        nt = 22.0 + t
        if nt < 44.0:
            n = int(SR*dur*1.1)
            env = _np.minimum(_np.arange(n)/(SR*.02),1.0).astype(_np.float32)*_np_exp(n,.3)
            s = (_np_sinev(n,freq,.24)+_np_sinev(n,freq*2,.08))*env
            _np_place2(melody, nt, _np_lp(s, 2000))
    # A' (44-66s): A melody + harmony a 5th above
    for (freq,dur),t in zip(mel_a, mel_ta):
        nt = 44.0 + t
        if nt < 66.0:
            n = int(SR*dur*1.2)
            env = _np.minimum(_np.arange(n)/(SR*.03),1.0).astype(_np.float32)*_np_exp(n,.5)
            s = (_np_sinev(n,freq,.28)+_np_sinev(n,freq*3,.06))*env
            _np_place2(melody, nt, _np_lp(s, 1800))
            # 5th harmony
            s2 = _np_sinev(n,freq*1.5,.12)*env
            _np_place2(melody, nt, _np_lp(s2, 1600))
    # ── Birdsong (naturalistic, throughout) ──────────────────────────────
    bird_events = []
    for base_t in [1.2, 4.5, 8.1, 12.0, 15.8, 18.5,
                   23.0, 27.5, 31.0, 35.5, 39.0, 42.5,
                   45.0, 49.5, 53.0, 57.5, 61.0, 64.5]:
        bird_events += [(base_t, 1800,.04),(base_t+.1,2200,.05),(base_t+.22,2600,.03)]
    birds = _np.zeros(N, _np.float32)
    for t,freq,vol in bird_events:
        if t < 66.0:
            n_b = int(SR*.04)
            b = _np_bp(n_b,freq,300,int(t*100))*_np_exp(n_b,.008)*vol
            _np_place2(birds, t, b)
    breeze = (_np_bp(N,800,400,55)*_np_swell2(N,5.5,0,.7)*.06 +
              _np_bp(N,1600,600,56)*_np_swell2(N,3.5,2,.6)*.03)
    drone = (_np_sinev(N,73,.09)*_np_swell2(N,11.0,0,.5) +
             _np_sinev(N,146,.05)*_np_swell2(N,8.0,4,.4) +
             _np_sinev(N,109,.04)*_np_swell2(N,15.0,6,.38))
    drone = _np_lp(drone, 350)
    water = _np_bp(N,120,60,57)*_np_swell2(N,7.0,1,.6)*.05
    return _np_seamless2(_np_norm(_np_mix2(melody*.80, birds*.9, breeze, drone, water)))


def _town_ironhearth():
    """Ironhearth — 54s E-Phrygian forge town. A (forge work) B (horn march) A'."""
    N = int(SR * 54.0)
    beat = 60.0 / 95
    forge = _np.zeros(N, _np.float32)
    for i in range(int(54.0 / beat)):
        t = i * beat
        # B-section (18-36s): forge goes quiet, fewer hits, more space
        if 18.0 <= t < 36.0:
            if i % 8 == 0:
                n_h = int(SR*.22); h = (_np_sinev(n_h,82,.55)+_np_bp(n_h,1800,900,i)*_np_exp(n_h,.015)*.30)*_np_exp(n_h,.06)
            elif i % 4 == 2:
                n_h = int(SR*.18); h = (_np_sinev(n_h,73,.30))*_np_exp(n_h,.05)
            else: continue
        else:
            if i % 4 == 0:
                n_h = int(SR*.22); h = (_np_sinev(n_h,82,.55)+_np_bp(n_h,1800,900,i)*_np_exp(n_h,.015)*.30)*_np_exp(n_h,.06)
            elif i % 4 == 2:
                n_h = int(SR*.18); h = (_np_sinev(n_h,73,.40)+_np_bp(n_h,2400,1000,i+20)*_np_exp(n_h,.012)*.22)*_np_exp(n_h,.05)
            elif i % 2 == 1:
                n_h = int(SR*.35); h = (_np_sinev(n_h,1047,.18)+_np_sinev(n_h,1318,.10)+_np_sinev(n_h,880,.08))*_np_exp(n_h,.20)
            else: continue
        _np_place2(forge, t, h)
    forge = _np_lp(forge, 3000)
    # ── Horn melody: A (0-18s), B march (18-36s), A' with harmony ────────
    mel_a = [(164,.50),(174,.38),(196,.50),(220,.75),(246,.38),(220,.50),(196,.75),(174,.38),(164,1.00),(196,.50),(220,.38),(246,.50),(220,.38),(196,.38),(174,.75),(164,1.25)]
    mel_b = [(164,.75),(196,.50),(246,.75),(220,.50),(196,.75),(164,.50),(174,.75),(164,1.00),(196,.50),(220,.75),(246,.50),(220,.75),(196,.50),(174,.75),(164,1.50)]
    mel_ta = [0.0]; [mel_ta.append(mel_ta[-1]+d) for _,d in mel_a[:-1]]
    mel_tb = [0.0]; [mel_tb.append(mel_tb[-1]+d) for _,d in mel_b[:-1]]
    horn = _np.zeros(N, _np.float32)
    for mel, t_off in [(mel_a, 0.0), (mel_b, 18.0), (mel_a, 36.0)]:
        mt = [0.0]; [mt.append(mt[-1]+d) for _,d in mel[:-1]]
        for (freq,dur),t in zip(mel, mt):
            nt = t_off + t
            if nt < 54.0:
                n = int(SR*dur*1.1)
                env = _np.minimum(_np.arange(n)/(SR*.06),1.0).astype(_np.float32)*_np_exp(n,.35)
                s = (_np_sinev(n,freq,.22)+_np_sinev(n,freq*2,.11)+_np_sinev(n,freq*3,.05))*env
                _np_place2(horn, nt, _np_lp(s, 900))
                if t_off == 36.0 and freq > 170:  # A' harmony
                    s2 = (_np_sinev(n,freq*1.33,.10))*env
                    _np_place2(horn, nt, _np_lp(s2, 800))
    bellows = _np.zeros(N, _np.float32)
    for t in [0.0,3.2,6.4,9.6,12.8,16.0,19.5,23.0,26.5,30.0,33.5,
              36.5,39.7,42.9,46.1,49.3,52.5]:
        n_b = int(SR*1.8)
        b = _np_bp(n_b,160,80,int(t*10))*_np_swell2(n_b,1.8,0,.8)*.18*_np.hanning(n_b).astype(_np.float32)**.5
        _np_place2(bellows, t, _np_lp(b, 400))
    drone = (_np_sinev(N,82,.12)*_np_swell2(N,9.0,0,.5) +
             _np_sinev(N,164,.06)*_np_swell2(N,6.0,2,.4) +
             _np_sinev(N,123,.05)*_np_swell2(N,12.0,4,.38))
    drone = _np_lp(drone, 500)
    crackle = _np_bp(N,3000,2000,60)*_np_swell2(N,2.5,0,.9)*.03
    return _np_seamless2(_np_norm(_np_mix2(forge*.70, horn*.65, bellows*.80, drone, crackle)))


def _town_greenwood():
    """Greenwood — 72s A-Phrygian. A (sparse night), B (dawn strings), A' (full)."""
    N = int(SR * 72.0)
    # ── Melody A (0-24s): sparse, mysterious ─────────────────────────────
    mel_a = [(220,1.00),(233,.60),(261,.80),(293,1.20),(329,.60),(349,.80),
             (329,.60),(293,1.00),(261,.80),(233,.60),(220,1.50),
             (246,.60),(261,.80),(293,.60),(329,1.00),(293,.80),(261,.60),(246,.80),(220,2.00)]
    mel_ta = [0.0]; [mel_ta.append(mel_ta[-1]+d) for _,d in mel_a[:-1]]
    # ── Melody B (24-48s): adds a drone strings layer + slight movement ──
    mel_b = [(233,.80),(261,.60),(293,.80),(329,1.00),(349,.60),(393,.80),
             (349,.60),(329,.80),(293,1.00),(261,.60),(233,1.20),
             (220,.60),(246,.80),(261,.60),(293,.80),(261,.60),(246,.80),(220,2.20)]
    mel_tb = [0.0]; [mel_tb.append(mel_tb[-1]+d) for _,d in mel_b[:-1]]
    melody = _np.zeros(N, _np.float32)
    for mel, t_off in [(mel_a, 0.0), (mel_b, 24.0), (mel_a, 48.0)]:
        mt = [0.0]; [mt.append(mt[-1]+d) for _,d in mel[:-1]]
        for (freq,dur),t in zip(mel, mt):
            nt = t_off + t
            if nt < 72.0:
                n = int(SR*dur*1.4)
                vol = .22 if t_off == 48.0 else .20
                env = _np.minimum(_np.arange(n)/(SR*.08),1.0).astype(_np.float32)*_np_exp(n,.55)
                s = (_np_sinev(n,freq,vol)+_np_sinev(n,freq*2,.07))*env
                _np_place2(melody, nt, _np_lp(s, 1000))
                if t_off == 48.0 and freq > 250:  # A' harmony
                    s2 = _np_sinev(n,freq*0.75,.08)*env
                    _np_place2(melody, nt, _np_lp(s2, 800))
    # ── Owls throughout ──────────────────────────────────────────────────
    owls = _np.zeros(N, _np.float32)
    for ot in [2.0,6.5,11.0,15.5,20.0,25.5,30.5,35.0,40.5,46.0,51.5,56.0,61.5,67.0]:
        n_o1 = int(SR*.45)
        o1 = (_np_sinev(n_o1,220,.20)+_np_sinev(n_o1,330,.08))*_np_exp(n_o1,.18)*_np.hanning(n_o1).astype(_np.float32)**.4
        _np_place2(owls, ot, _np_lp(o1, 600))
        n_o2 = int(SR*.55)
        o2 = (_np_sinev(n_o2,293,.22)+_np_sinev(n_o2,440,.09))*_np_exp(n_o2,.22)*_np.hanning(n_o2).astype(_np.float32)**.4
        if ot+0.6 < 72.0: _np_place2(owls, ot+0.6, _np_lp(o2, 700))
    wind = (_np_bp(N,300,150,65)*_np_swell2(N,8.0,0,.65)*.10 +
            _np_bp(N,700,300,66)*_np_swell2(N,5.5,3,.70)*.06 +
            _np_bp(N,150,70,67)*_np_swell2(N,12.0,2,.55)*.08)
    drone = (_np_sinev(N,55,.10)*_np_swell2(N,12.0,0,.5) +
             _np_sinev(N,110,.05)*_np_swell2(N,9.0,5,.4) +
             _np_sinev(N,82,.04)*_np_swell2(N,16.0,7,.38))
    drone = _np_lp(drone, 300)
    crickets = _np_bp(N,5500,2000,68)*_np_swell2(N,1.2,0,.95)*.025
    return _np_seamless2(_np_norm(_np_mix2(melody*.75, owls*.85, wind, drone, crickets)))


def _town_saltmere():
    """Saltmere — 60s 6/8 shanty. A (verse), B (chorus full band), A' (reprise)."""
    N = int(SR * 60.0)
    eighth = 60.0 / 84 / 1.5
    dotted_q = eighth * 3
    # ── Shanty melody sequence (played three times with variation) ────────
    mel_seq = [(293,2),(329,1),(349,2),(392,1),(440,3),(392,1),(349,2),(329,1),
               (293,3),(247,1),(261,2),(293,1),(329,2),(293,1),(247,3),
               (220,1),(247,2),(293,1),(329,2),(392,1),(440,3),(494,1),(523,2),(494,1),
               (440,3),(392,1),(349,2),(329,1),(293,4)]
    mel_t = [0.0]; [mel_t.append(mel_t[-1]+e*eighth) for _,e in mel_seq[:-1]]
    one_pass = mel_t[-1] + mel_seq[-1][1]*eighth  # duration of one full pass
    melody = _np.zeros(N, _np.float32)
    for pass_n, t_off in enumerate([0.0, one_pass, one_pass*2]):
        for (freq,eighths),t in zip(mel_seq, mel_t):
            nt = t_off + t
            if nt >= 60.0: break
            dur = eighths * eighth * 0.88
            n = int(SR*dur)
            # B-section (pass 2): add harmony a 5th below
            env = _np.minimum(_np.arange(n)/(SR*.04),1.0).astype(_np.float32)*_np_exp(n,.28)
            s = (_np_sinev(n,freq,.24)+_np_sinev(n,freq*2,.10)+_np_sinev(n,freq*3,.04))*env
            _np_place2(melody, nt, _np_lp(s, 1600))
            if pass_n == 1 and freq > 280:  # chorus harmony
                s2 = (_np_sinev(n,freq*0.667,.12))*env
                _np_place2(melody, nt, _np_lp(s2, 1200))
    # ── Bass (full length) ────────────────────────────────────────────────
    bass = _np.zeros(N, _np.float32)
    bass_cycle = [73,73,98,98,73,87,73,73,98,87]
    for i in range(int(60.0 / dotted_q)):
        t = i * dotted_q
        freq = bass_cycle[i % len(bass_cycle)]
        n_b = int(SR*.28)
        b = (_np_sinev(n_b,freq,.40)+_np_sinev(n_b,freq*2,.15))*_np_exp(n_b,.12)
        _np_place2(bass, t, _np_lp(b, 500))
    # ── Drum (full length, B chorus adds hand-clap layer) ─────────────────
    drum = _np.zeros(N, _np.float32)
    for bar in range(int(60.0 / (dotted_q * 2))):
        t0 = bar * dotted_q * 2
        for beat_idx in [0, 3]:
            t = t0 + beat_idx * eighth
            if t >= 60.0: break
            n_s = int(SR*.18)
            s = _np_sinev(n_s,90,.48)*_np_exp(n_s,.05)+_np_bp(n_s,400,200,bar)*_np_exp(n_s,.03)*.25
            _np_place2(drum, t, s)
        for beat_idx in [1,2,4,5]:
            t = t0 + beat_idx * eighth
            if t >= 60.0: break
            n_c = int(SR*.08)
            vol = .28 if (one_pass <= t0 < one_pass*2) else .22   # louder in B
            c = _np_bp(n_c,2000,1200,bar+beat_idx)*_np_exp(n_c,.018)*vol
            _np_place2(drum, t, c)
    drum = _np_lp(drum, 3000)
    sea = (_np_bp(N,80,40,70)*_np_swell2(N,6.5,0,.6)*.14 +
           _np_bp(N,55,25,71)*_np_swell2(N,9.0,3,.5)*.10 +
           _np_bp(N,110,50,72)*_np_swell2(N,11.0,6,.45)*.07)
    creak = _np_bp(N,500,200,72)*_np_swell2(N,4.0,1,.8)*.04
    return _np_seamless2(_np_norm(_np_mix2(melody*.80, bass*.70, drum*.55, sea, creak)))


def _town_sanctum():
    """Sanctum — 84s cathedral organ. A (D minor), B (F major ascent), A' (resolve)."""
    N = int(SR * 84.0)
    # ── Three harmonic sections, 28s each ────────────────────────────────
    # A (0-28s): D minor — D(146) F(174) A(220), slow swell
    # B (28-56s): F major → A minor ascending arc
    # A' (56-84s): D minor resolve with fuller organ texture
    chords_A = [
        [(146,.20),(174,.16),(220,.13),(293,.09),(349,.06)],   # Dm
        [(174,.20),(220,.16),(261,.13),(349,.09),(440,.06)],   # F
        [(220,.20),(261,.16),(329,.13),(440,.09),(523,.06)],   # Am
        [(196,.20),(247,.16),(293,.13),(392,.09),(494,.06)],   # G
    ]
    chords_B = [
        [(174,.20),(220,.16),(261,.13),(349,.09),(440,.06)],   # F
        [(220,.20),(261,.16),(329,.13),(440,.09),(523,.06)],   # Am
        [(261,.20),(329,.16),(392,.13),(523,.09),(659,.06)],   # C
        [(220,.20),(261,.16),(329,.13),(440,.09),(523,.06)],   # Am back
    ]
    chords_Ap = [
        [(146,.22),(174,.18),(220,.15),(293,.11),(349,.08)],   # Dm richer
        [(174,.22),(220,.18),(261,.15),(349,.11),(440,.08)],   # F richer
        [(220,.22),(261,.18),(329,.15),(440,.11),(523,.08)],   # Am richer
        [(146,.22),(174,.18),(220,.15),(261,.11),(293,.08)],   # Dm resolve
    ]
    organ = _np.zeros(N, _np.float32)
    choir = _np.zeros(N, _np.float32)
    for section_t, chords in [(0.0, chords_A), (28.0, chords_B), (56.0, chords_Ap)]:
        n_chord = int(SR * 7.0)   # 7s per chord
        env = _np.hanning(n_chord).astype(_np.float32) ** .5
        for ci, chord in enumerate(chords):
            t0 = section_t + ci * 7.0
            if t0 >= 84.0: break
            for freq,vol in chord:
                seg = (_np_sinev(n_chord,freq,vol)+_np_sinev(n_chord,freq*2,vol*.45)+_np_sinev(n_chord,freq*3,vol*.25)+_np_sinev(n_chord,freq*5,vol*.10))*env
                _np_place2(organ, t0, seg)
                choir_seg = (_np_sinev(n_chord,freq*4,vol*.08)+_np_sinev(n_chord,freq*6,vol*.05))*env*_np_swell2(n_chord,7.0*.5,0,.6)
                _np_place2(choir, t0, choir_seg)
    organ = _np_lp(organ, 2500)
    choir = _np_hp_filt(choir, 800)
    # ── Sustained melody line enters in B-section ─────────────────────────
    mel = _np.zeros(N, _np.float32)
    mel_notes = [(349,4.5),(392,3.5),(440,4.0),(392,3.0),(349,4.5),(329,3.5),(349,5.5),
                 (392,4.0),(440,4.5),(494,3.5),(440,4.0),(392,3.5),(349,6.0)]
    mel_t = [0.0]; [mel_t.append(mel_t[-1]+d) for _,d in mel_notes[:-1]]
    for (freq,dur),t in zip(mel_notes, mel_t):
        nt = 28.0 + t
        if nt < 56.0:
            n_m = int(SR*dur)
            env_m = _np.minimum(_np.arange(n_m)/(SR*.3),1.0).astype(_np.float32)*_np_exp(n_m,.6)
            s = (_np_sinev(n_m,freq,.14)+_np_sinev(n_m,freq*2,.06))*env_m
            _np_place2(mel, nt, _np_lp(s, 1500))
    sub = (_np_sinev(N,36,.12)*_np_swell2(N,14.0,0,.45) +
           _np_sinev(N,73,.07)*_np_swell2(N,10.0,5,.40) +
           _np_sinev(N,54,.05)*_np_swell2(N,18.0,8,.38))
    sub = _np_lp(sub, 200)
    stone = _np_bp(N,280,60,75)*_np_swell2(N,22.0,0,.55)*.06
    return _np_seamless2(_np_norm(_np_mix2(organ*.85, choir*.65, mel*.70, sub, stone)))


def _town_crystalspire():
    """Crystalspire — 60s F-Lydian. A (arpeggios), B (slower chords), A' (climax)."""
    N = int(SR * 60.0)
    # ── Arpeggio sequence: A passes at 0s and 40s, slow B at 20-40s ──────
    arp_A = [349,392,440,494,523,587,659,587,523,494,440,392,
             349,392,440,494,587,659,784,659,587,494,440,392,
             523,587,659,784,880,784,659,587,523,440,392,349,
             440,494,523,659,784,659,523,494,440,392,349,392]
    note_dur = 0.155
    arps = _np.zeros(N, _np.float32)
    # A arpeggios (0-20s and 40-60s)
    for pass_t in [0.0, 40.0]:
        for i,freq in enumerate(arp_A):
            t = pass_t + i * note_dur
            if t >= pass_t + 20.0 or t >= 60.0: break
            n = int(SR*note_dur*.92)
            env = _np.minimum(_np.arange(n)/(SR*.008),1.0).astype(_np.float32)*_np_exp(n,.12)
            s = (_np_sinev(n,freq,.18)+_np_sinev(n,freq*2,.07)+_np_sinev(n,freq*4,.03))*env
            # A' louder and adds octave
            vol_mult = 1.2 if pass_t == 40.0 else 1.0
            _np_place2(arps, t, s * vol_mult)
            if pass_t == 40.0:
                s2 = _np_sinev(n,freq*2,.09)*env
                _np_place2(arps, t, s2)
    # B-section (20-40s): slower chord-based texture
    b_chords = [(349,440,659),(392,523,784),(440,587,880),(523,659,988),(440,587,880),(392,523,784)]
    b_dur = 20.0 / len(b_chords)
    for ci,(f1,f2,f3) in enumerate(b_chords):
        t0 = 20.0 + ci * b_dur
        n_c = int(SR * b_dur)
        env_c = _np.hanning(n_c).astype(_np.float32)**.5
        for freq,vol in [(f1,.16),(f2,.12),(f3,.09)]:
            seg = (_np_sinev(n_c,freq,vol)+_np_sinev(n_c,freq*2,vol*.4))*env_c
            _np_place2(arps, t0, seg)
    # ── Sustained harmony throughout ─────────────────────────────────────
    harmony = _np.zeros(N, _np.float32)
    harm_notes = [(174,.14),(220,.11),(261,.09),(349,.08),(494,.06),(659,.04)]
    n_h = int(SR * 60.0)
    for freq,vol in harm_notes:
        seg = _np_sinev(n_h,freq,vol)*_np_swell2(n_h,10.0,0,.5)
        harmony += seg
    harmony = _np_lp(harmony, 1500)
    # ── Bell accents (more frequent in A') ───────────────────────────────
    bells = _np.zeros(N, _np.float32)
    for t,freq in [(0.0,1047),(4.96,1319),(9.92,1568),(14.88,1047),(19.84,1319),
                   (21.0,1568),(23.5,2093),(26.5,1760),(29.5,1568),(33.0,1319),(37.5,1568),
                   (40.0,1047),(44.96,1319),(49.92,1568),(54.88,2093),(59.0,1319)]:
        if t < 60.0:
            n_b = int(SR*.8)
            b = (_np_sinev(n_b,freq,.14)+_np_sinev(n_b,freq*2.76,.07))*_np_exp(n_b,.35)
            _np_place2(bells, t, b)
    shimmer = (_np_bp(N,8000,3000,80)*_np_swell2(N,2.5,0,.9)*.04 +
               _np_bp(N,5000,2000,81)*_np_swell2(N,3.5,1.2,.85)*.03)
    drone = (_np_sinev(N,87,.10)*_np_swell2(N,5.0,0,.6)+_np_sinev(N,174,.06)*_np_swell2(N,3.5,1.5,.7)+_np_sinev(N,349,.04)*_np_swell2(N,2.5,0.5,.8))
    drone = _np_lp(drone, 600)
    return _np_seamless2(_np_norm(_np_mix2(arps*.75, harmony*.60, shimmer, drone, bells*.80)))


def _town_thornhaven():
    """Thornhaven — 60s D-minor imperial. A (march), B (desolate strings), A' (full)."""
    N = int(SR * 60.0)
    beat = 60.0 / 88
    # ── March drum: A (0-20s) full, B (20-40s) sparse, A' (40-60s) full ─
    march_drum = _np.zeros(N, _np.float32)
    for i in range(int(60.0 / beat)):
        t = i * beat
        if 20.0 <= t < 40.0:
            # B-section: only downbeats
            if i % 4 != 0: continue
            n_d = int(SR*.22)
            d = (_np_sinev(n_d,65,.40))*_np_exp(n_d,.07)
        else:
            if i % 4 in (0, 2):
                n_d = int(SR*.20)
                d = (_np_sinev(n_d,65,.50)+_np_bp(n_d,200,100,i)*_np_exp(n_d,.03)*.20)*_np_exp(n_d,.06)
            else:
                n_d = int(SR*.12)
                d = (_np_bp(n_d,2500,1500,i+60)*_np_exp(n_d,.022)+_np_bp(n_d,800,400,i+61)*_np_exp(n_d,.030))*.30
        _np_place2(march_drum, t, d)
    march_drum = _np_lp(march_drum, 3500)
    # ── Brass melody: A and A' (authoritative), absent in B ──────────────
    mel = [(293,.50),(261,.38),(293,.50),(311,.75),(349,.38),(329,.50),(311,.38),(293,.75),
           (261,.50),(293,.38),(311,.50),(329,.38),(293,.38),(261,.75),(220,1.00),
           (220,.38),(246,.50),(261,.38),(293,.75),(329,.50),(349,.38),(329,.50),(311,.38),(293,.50),(261,.38),(220,.75),(174,1.25)]
    mel_t = [0.0]; [mel_t.append(mel_t[-1]+d) for _,d in mel[:-1]]
    brass = _np.zeros(N, _np.float32)
    for t_off in [0.0, 40.0]:
        for (freq,dur),t in zip(mel, mel_t):
            nt = t_off + t
            if nt >= t_off + 20.0 or nt >= 60.0: break
            n = int(SR*dur*1.05)
            env = _np.minimum(_np.arange(n)/(SR*.04),1.0).astype(_np.float32)*_np_exp(n,.30)
            s = (_np_sinev(n,freq,.24)+_np_sinev(n,freq*2,.14)+_np_sinev(n,freq*3,.07)+_np_sinev(n,freq*4,.03))*env
            _np_place2(brass, nt, _np_lp(s, 1200))
            if t_off == 40.0:   # A' adds harmony
                s2 = (_np_sinev(n,freq*1.33,.12))*env
                _np_place2(brass, nt, _np_lp(s2, 1000))
    # ── B-section strings (20-40s): slow D minor chord swells ────────────
    strings = _np.zeros(N, _np.float32)
    b_chords = [(146,220,293),(174,220,261),(146,196,293),(123,196,246),(146,220,293),(174,261,329)]
    b_dur = 20.0 / len(b_chords)
    for ci,(f1,f2,f3) in enumerate(b_chords):
        t0 = 20.0 + ci * b_dur
        n_c = int(SR * b_dur)
        env_c = _np.hanning(n_c).astype(_np.float32)**.6
        for freq,vol in [(f1,.14),(f2,.10),(f3,.08)]:
            seg = (_np_sinev(n_c,freq,vol)+_np_sinev(n_c,freq*2,vol*.4))*env_c
            _np_place2(strings, t0, seg)
    strings = _np_lp(strings, 1000)
    shadow = _np.zeros(N, _np.float32)
    for (freq,dur),t in zip(mel, mel_t):
        for t_off in [0.0, 40.0]:
            nt = t_off + t + 0.04
            if nt >= t_off + 20.0 or nt >= 60.0: break
            n = int(SR*dur*1.05)
            env = _np.minimum(_np.arange(n)/(SR*.06),1.0).astype(_np.float32)*_np_exp(n,.40)
            s = (_np_sinev(n,freq*1.0046,.10)+_np_sinev(n,freq*2.0092,.05))*env
            _np_place2(shadow, nt, _np_lp(s, 900))
    drone = (_np_sinev(N,73,.14)*_np_swell2(N,10.0,0,.45) +
             _np_sinev(N,146,.07)*_np_swell2(N,7.0,2,.40) +
             _np_sinev(N,36,.08)*_np_swell2(N,20.0,0,.35))
    drone = _np_lp(drone, 500)
    bells = _np.zeros(N, _np.float32)
    for t,freq in [(0.0,220),(9.5,196),(0.0,293),(9.5,261),(40.0,220),(49.5,196),(40.0,293),(49.5,261)]:
        if t < 60.0:
            n_b = int(SR*2.5)
            b = (_np_sinev(n_b,freq,.16)+_np_sinev(n_b,freq*2.76,.08))*_np_exp(n_b,.80)
            _np_place2(bells, t, b)
    return _np_seamless2(_np_norm(_np_mix2(march_drum*.65, brass*.80, strings*.75, shadow*.45, drone, bells*.70)))



# ── Public helper ─────────────────────────────────────────────
def play_dungeon_music(dungeon_id):
    """Play the matching dungeon track, falling back to dungeon_ambient."""
    if not _enabled: return
    name = f"dungeon_{dungeon_id}"
    snd = _sounds.get(name)
    if not snd:
        snd = _sounds.get("dungeon_ambient")
    if snd:
        snd.set_volume(_master_vol * _music_vol)
        if _music_channel:
            _music_channel.play(snd, loops=-1)

def play_town_music(town_id):
    """Play the matching town track, falling back to town_ambient."""
    if not _enabled: return
    name = f"town_{town_id}"
    snd = _sounds.get(name)
    if not snd:
        snd = _sounds.get("town_ambient")
    if snd:
        snd.set_volume(_master_vol * _music_vol)
        if _music_channel:
            _music_channel.play(snd, loops=-1)

# ═══════════════════════════════════════════════════════════════
#  SOUND DEFINITIONS
# ═══════════════════════════════════════════════════════════════



def _build_gen_queues():
    """Populate batch1 (fast SFX) and batch2 (music/ambient) generation queues."""
    global _gen_batch1, _gen_batch2

    # ── BATCH 1: Fast SFX — UI, combat, dungeon, town, exploration ─────────
    # All of these are simple math or short numpy operations (<5ms each).
    # Generated during Splash 1 (Bad Bat logo screen).

    def _b1_ui():
        _sounds["ui_click"]   = _make_sound(_sine(800, 0.10, 0.22))
        _sounds["ui_confirm"] = _make_sound(_concat(_sine(600, 0.10, 0.28), _sine(900, 0.14, 0.28)))
        _sounds["ui_cancel"]  = _make_sound(_sine(280, 0.22, 0.22))
        _sounds["ui_open"]    = _make_sound(_sweep(400,  820, 0.28, 0.22))
        _sounds["ui_close"]   = _make_sound(_sweep(820,  380, 0.22, 0.22))

    def _b1_combat_physical():
        # ── Wind-up sounds (phase 1) ──────────────────────────────
        _sounds["swing_light"]    = _make_np_sound(_gen_swing_light)
        _sounds["swing_medium"]   = _make_np_sound(_gen_swing_medium)
        _sounds["swing_heavy"]    = _make_np_sound(_gen_swing_heavy)
        _sounds["swing_skill"]    = _make_np_sound(_gen_swing_skill)
        # ── Impact sounds (phase 2) ──────────────────────────────
        _sounds["hit_light"]      = _make_np_sound(_gen_hit_light)
        _sounds["hit_medium"]     = _make_np_sound(_gen_hit_medium)
        _sounds["hit_heavy"]      = _make_np_sound(_gen_hit_heavy)
        _sounds["hit_physical"]   = _sounds["hit_medium"]
        _sounds["hit_skill"]      = _sounds["hit_heavy"]
        _sounds["hit_skill_fast"] = _make_np_sound(_gen_hit_skill_fast)
        _sounds["hit_critical"]   = _make_np_sound(_gen_hit_critical)

    def _b1_combat_elemental():
        _sounds["hit_fire"]       = _make_np_sound(_gen_hit_fire)
        _sounds["hit_ice"]        = _make_np_sound(_gen_hit_ice)
        _sounds["hit_lightning"]  = _make_np_sound(_gen_hit_lightning)
        _sounds["hit_shadow"]     = _make_np_sound(_gen_hit_shadow)
        _sounds["hit_divine"]     = _make_np_sound(_gen_hit_divine)
        _sounds["hit_nature"]     = _make_np_sound(_gen_hit_nature)
        _sounds["hit_arcane"]     = _make_np_sound(_gen_hit_arcane)
        _sounds["hit_wind"]       = _sounds["hit_nature"]
        _sounds["hit_piercing"]   = _sounds["hit_medium"]
        _sounds["hit_magic"]      = _sounds["hit_arcane"]

    def _b1_combat_miss():
        _sounds["miss_physical"]  = _make_np_sound(_gen_miss_physical)
        _sounds["miss_magic"]     = _make_np_sound(_gen_miss_magic)
        _sounds["miss_elemental"] = _make_np_sound(_gen_miss_elemental)
        _sounds["miss"]           = _sounds["miss_physical"]
        _sounds["spell_miss"]     = _sounds["miss_magic"]

    def _b1_combat_support():
        # ── Preparation sounds (phase 1 for non-physical) ─────────
        _sounds["cast_attack"]    = _make_np_sound(_gen_cast_attack)
        _sounds["cast_buff_self"] = _make_np_sound(_gen_cast_buff_self)
        _sounds["cast_buff_spell"]= _make_np_sound(_gen_cast_buff_spell)
        _sounds["cast_debuff"]    = _make_np_sound(_gen_cast_debuff)
        # ── Resolution sounds (phase 2) ───────────────────────────
        _sounds["no_resource"]    = _make_sound(_mix(_sine(120, 0.35, 0.18), _noise(0.12, 0.06)))
        _sounds["heal"]    = _make_np_sound(_gen_heal)
        _sounds["revive"]  = _make_np_sound(_gen_revive)
        _sounds["buff_physical"] = _make_np_sound(_gen_buff_physical)
        _sounds["buff_magic"]    = _make_np_sound(_gen_buff_magic)
        _sounds["buff_divine"]   = _make_np_sound(_gen_buff_divine)
        _sounds["buff_nature"]   = _make_np_sound(_gen_buff_nature)
        _sounds["buff"]          = _sounds["buff_physical"]
        _sounds["debuff_physical"] = _make_np_sound(_gen_debuff_physical)
        _sounds["debuff_magic"]    = _make_np_sound(_gen_debuff_magic)
        _sounds["debuff_divine"]   = _make_np_sound(_gen_debuff_divine)
        _sounds["debuff"]          = _sounds["debuff_physical"]
        _sounds["poison_tick"]   = _make_np_sound(_gen_poison_tick)
        _sounds["burning_tick"]  = _make_np_sound(_gen_burning_tick)

    def _b1_combat_core():
        # ── Death/kill sounds: long and distinct ─────────────────
        _sounds["enemy_death"]  = _make_np_sound(_gen_death_enemy)
        _sounds["death"]        = _make_np_sound(_gen_death_player)
        _sounds["victory"]      = _make_sound(_concat(
            _sine(392, 0.22, 0.30), _sine(523, 0.22, 0.32),
            _sine(659, 0.22, 0.34), _sine(784, 0.18, 0.36),
            _silence(0.06), _sine(784, 0.45, 0.38)))
        _sounds["defeat"]       = _make_sound(_concat(
            _sine(280, 0.35, 0.30), _sine(240, 0.35, 0.30),
            _sine(200, 0.35, 0.28), _sine(130, 0.70, 0.28)))
        _sounds["combat_start"] = _make_sound(_mix(
            _noise(0.22, 0.28),
            _concat(_sine(165, 0.16, 0.30), _sine(220, 0.16, 0.34), _sine(330, 0.22, 0.36))))
        _sounds["block"]        = _make_sound(_mix(
            _bandpass_noise(0.18, 140, 70, 0.40),
            _sine(130, 0.20, 0.26)))
        _sounds["poison"]       = _make_sound(_mix(
            _sweep(280, 140, 0.45, 0.20), _noise(0.22, 0.08)))

    def _b1_dungeon_sfx():
        _sounds["door_open"] = _make_sound(_concat(
            _creak(0.18, 280, 80, volume=0.30, slip_count=4, seed=7),
            _mix(_creak(0.14, 180, 60, volume=0.18, slip_count=3, seed=23),
                 _bandpass_noise(0.14, 220, 80, volume=0.05, seed=31)),
            _silence(0.04), _thud(0.12, 0.18)))
        _sounds["treasure_open"] = _make_sound(_concat(
            _creak(0.45, 620, 140, volume=0.25, slip_count=7, seed=33),
            _silence(0.05),
            _creak(0.55, 480, 110, volume=0.20, slip_count=8, seed=44),
            _silence(0.07), _thud(0.10, 0.10)))
        _sounds["stairs"]       = _make_sound(_concat(
            _sine(300, 0.16, 0.22), _sine(350, 0.16, 0.22), _sine(420, 0.22, 0.28)))
        _sounds["trap_trigger"] = _make_sound(_mix(
            _noise(0.35, 0.42), _sweep(900, 80, 0.40, 0.32)))
        _sounds["journal_find"] = _make_sound(_concat(
            _sine(440, 0.16, 0.22), _sine(554, 0.16, 0.22), _sine(659, 0.24, 0.28)))

    def _b1_town_sfx():
        _sounds["shop_buy"]       = _make_sound(_coin_scatter(num_coins=6, seed=7))
        _sounds["shop_sell"]      = _make_sound(_coin_scatter(num_coins=4, seed=13))
        _sounds["npc_talk"]       = _make_sound(_peanuts_talk(num_syllables=5, seed=99))
        _sounds["quest_accept"]   = _make_sound(_concat(
            _sine(440, 0.12, 0.22), _sine(554, 0.12, 0.22),
            _sine(659, 0.14, 0.28), _sine(880, 0.26, 0.34)))
        _sounds["quest_complete"] = _make_sound(_concat(
            _sine(523,  0.16, 0.32), _sine(659, 0.16, 0.32),
            _sine(784,  0.16, 0.32), _sine(1047, 0.18, 0.38),
            _silence(0.08), _sine(1047, 0.32, 0.38)))
        _sounds["level_up"]       = _make_sound(_concat(
            _sine(392,  0.16, 0.32), _sine(523, 0.16, 0.32),
            _sine(659,  0.16, 0.32), _sine(784, 0.16, 0.32),
            _sine(1047, 0.38, 0.42)))
        _sounds["item_pickup"]    = _make_sound(_concat(
            _sine(700, 0.10, 0.22), _sine(900, 0.14, 0.28)))

    def _b1_exploration():
        _sounds["encounter"]  = _make_sound(_mix(
            _noise(0.20, 0.40),
            _concat(_sine(180, 0.10, 0.28), _sine(240, 0.10, 0.32), _sine(320, 0.18, 0.38))))
        _sounds["discovery"]  = _make_sound(_concat(
            _sine(523, 0.14, 0.22), _sine(659, 0.14, 0.26),
            _sine(784, 0.14, 0.28), _sine(1047, 0.32, 0.36)))
        _sounds["camp_rest"]  = _make_sound(_concat(
            _sine(330, 0.30, 0.18), _silence(0.10),
            _sine(370, 0.30, 0.18), _silence(0.10),
            _sine(440, 0.50, 0.20)))
        _sounds["trap"]       = _make_sound(_mix(
            _noise(0.28, 0.36), _sweep(700, 120, 0.32, 0.28)))
        # Step: heel-click (short, ~800Hz) then clomp body (~300Hz wood resonance)
        _sounds["step"] = _make_np_sound(_gen_step_footstep)

    _gen_batch1 = [
        ("UI sounds",           _b1_ui),
        ("Physical hits",       _b1_combat_physical),
        ("Elemental hits",      _b1_combat_elemental),
        ("Miss sounds",         _b1_combat_miss),
        ("Support sounds",      _b1_combat_support),
        ("Core combat",         _b1_combat_core),
        ("Dungeon SFX",         _b1_dungeon_sfx),
        ("Town SFX",            _b1_town_sfx),
        ("Exploration sounds",  _b1_exploration),
    ]

    # ── BATCH 2: Music and ambient — generated one per frame during Splash 2 ──
    # Each entry is a label + callable. The callable generates and registers one sound.

    _gen_batch2 = [
        # town_briarhollow FIRST so music can start during loading screen
        ("Briarhollow music",         lambda: _sounds.update({"town_briarhollow": _gen_dungeon(_town_briarhollow)})),
        ("World ambient",             lambda: _generate_world_ambient()),
        ("Town ambient music",        lambda: _generate_town_ambient()),
        ("Town crowd ambience",       lambda: _generate_town_env()),
        ("Grassland sounds",          lambda: _sounds.update({"ambient_grassland": _make_biome(_biome_grassland)})),
        ("Forest sounds",             lambda: _sounds.update({"ambient_forest": _make_biome(_biome_forest)})),
        ("Hills sounds",              lambda: _sounds.update({"ambient_hills": _make_biome(_biome_hills)})),
        ("Swamp sounds",              lambda: _sounds.update({"ambient_swamp": _make_biome(_biome_swamp)})),
        ("Coast sounds",              lambda: _sounds.update({"ambient_coast": _make_biome(_biome_coast)})),
        ("Desert sounds",             lambda: _sounds.update({"ambient_desert": _make_biome(_biome_desert)})),
        ("Dungeon ambience",          lambda: _sounds.update({"dungeon_ambient": _make_sound(_mix(_sine(65, 2.5, 0.08, fade_out=False), _bandpass_noise(2.5, 110, 40, volume=0.05, seed=66)))})),
        ("Goblin Warren music",       lambda: _sounds.update({"dungeon_goblin_warren": _gen_dungeon(_dungeon_goblin_warren)})),
        ("Spider\'s Nest music",     lambda: _sounds.update({"dungeon_spiders_nest": _gen_dungeon(_dungeon_spiders_nest)})),
        ("Abandoned Mine music",      lambda: _sounds.update({"dungeon_abandoned_mine": _gen_dungeon(_dungeon_abandoned_mine)})),
        ("Ruins of Ashenmoor music",  lambda: _sounds.update({"dungeon_ruins_ashenmoor": _gen_dungeon(_dungeon_ruins_ashenmoor)})),
        ("Sunken Crypt music",        lambda: _sounds.update({"dungeon_sunken_crypt": _gen_dungeon(_dungeon_sunken_crypt)})),
        ("Pale Coast music",          lambda: _sounds.update({"dungeon_pale_coast": _gen_dungeon(_dungeon_pale_coast)})),
        ("Windswept Isle music",      lambda: _sounds.update({"dungeon_windswept_isle": _gen_dungeon(_dungeon_windswept_isle)})),
        ("Dragon\'s Tooth music",    lambda: _sounds.update({"dungeon_dragons_tooth": _gen_dungeon(_dungeon_dragons_tooth)})),
        ("Valdris\' Spire music",    lambda: _sounds.update({"dungeon_valdris_spire": _gen_dungeon(_dungeon_valdris_spire)})),
        ("Woodhaven music",           lambda: _sounds.update({"town_woodhaven": _gen_dungeon(_town_woodhaven)})),
        ("Ironhearth music",          lambda: _sounds.update({"town_ironhearth": _gen_dungeon(_town_ironhearth)})),
        ("Greenwood music",           lambda: _sounds.update({"town_greenwood": _gen_dungeon(_town_greenwood)})),
        ("Saltmere music",            lambda: _sounds.update({"town_saltmere": _gen_dungeon(_town_saltmere)})),
        ("Sanctum music",             lambda: _sounds.update({"town_sanctum": _gen_dungeon(_town_sanctum)})),
        ("Crystalspire music",        lambda: _sounds.update({"town_crystalspire": _gen_dungeon(_town_crystalspire)})),
        ("Thornhaven music",          lambda: _sounds.update({"town_thornhaven": _gen_dungeon(_town_thornhaven)})),
    ]


def _generate_world_ambient():
    _sounds["world_ambient"] = _make_sound(_bandpass_noise(3.0, 180, 80, volume=0.08, seed=88))


def _generate_town_ambient():
    """Town ambient — warm Briarhollow-style loop (fallback for all towns)."""
    _sounds["town_ambient"] = _gen_dungeon(_town_briarhollow)


def _generate_town_env():
    """Crowd murmur + distant bell dings — ambient layer played over town music."""
    env_dur = 8.0
    env_n   = int(SR * env_dur)
    crowd   = _bandpass_noise(env_dur, 250, 60, volume=0.025, seed=71)
    wind    = _bandpass_noise(env_dur, 380, 120, volume=0.018, seed=99)
    bell    = [0] * env_n
    for t_hit in (1.8, 4.6, 7.1):
        pos = int(t_hit * SR); freq = 880.0; bdur = int(SR * 0.8)
        for j in range(min(bdur, env_n - pos)):
            env_bell = math.exp(-j / (SR * 0.25))
            bell[pos + j] += int(3500 * env_bell * math.sin(2*math.pi*freq*j/SR))
    samp = [max(-32767, min(32767, crowd[i] + wind[i] + bell[i])) for i in range(env_n)]
    fade_e = int(SR * 0.12)
    for i in range(min(fade_e, env_n)):
        f = i / fade_e
        samp[i] = int(samp[i] * f)
        samp[env_n-1-i] = int(samp[env_n-1-i] * f)
    _sounds["town_env"] = _make_sound(samp)


def step_batch1():
    """Generate ALL batch1 items (fast SFX). Call once during Splash 1."""
    global _b1_idx
    for name, fn in _gen_batch1:
        try:
            fn()
        except Exception:
            pass
    _b1_idx = len(_gen_batch1)


def step_batch2():
    """Generate ONE batch2 item. Call once per frame during Splash 2.
    Returns (is_done, items_done, items_total, current_item_name).
    """
    global _b2_idx, _gen_ready
    total = len(_gen_batch2)
    if _b2_idx >= total:
        _gen_ready = True
        return True, total, total, "Done"
    name, fn = _gen_batch2[_b2_idx]
    try:
        fn()
    except Exception:
        pass
    _b2_idx += 1
    done = _b2_idx >= total
    if done:
        _gen_ready = True
    return done, _b2_idx, total, name


def is_ready():
    """True when all sounds (batch1 + batch2) have been generated."""
    return _gen_ready


def _generate_all_sounds():
    """Legacy: generate everything synchronously (used if incremental path skipped)."""
    global _gen_ready
    _build_gen_queues()
    step_batch1()
    while True:
        done, _, _, _ = step_batch2()
        if done:
            break
    _gen_ready = True


# ═══════════════════════════════════════════════════════════════
#  PUBLIC API
# ═══════════════════════════════════════════════════════════════

def play(name):
    """Play a one-shot sound effect."""
    if not _enabled:
        return
    snd = _sounds.get(name)
    if snd:
        snd.set_volume(_master_vol * _sfx_vol)
        snd.play()


def play_music(name):
    """Play a sound on the music channel, looping indefinitely."""
    if not _enabled or _music_channel is None:
        return
    snd = _sounds.get(name)
    if snd:
        snd.set_volume(_master_vol * _music_vol)
        _music_channel.play(snd, loops=-1)


def play_ambient(name):
    """Play a sound on the ambient channel, looping indefinitely."""
    if not _enabled or _ambient_channel is None:
        return
    snd = _sounds.get(name)
    if snd:
        snd.set_volume(_master_vol * _ambient_vol)
        _ambient_channel.play(snd, loops=-1)


def stop_music():
    """Stop the music channel."""
    if _enabled and _music_channel:
        _music_channel.stop()


def stop_ambient():
    """Stop the ambient channel."""
    if _enabled and _ambient_channel:
        _ambient_channel.stop()


def stop_all():
    """Stop all currently playing sounds."""
    if _enabled and _mixer:
        _mixer.stop()
