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
    if not _HAS_NUMPY: return [0]*n
    from scipy import signal as _sci
    x = _np.random.default_rng(seed).standard_normal(n).astype(_np.float64)
    lo = max(20.0, cf-bw/2); hi = min(float(SR)/2-1, cf+bw/2)
    b, a = _sci.iirfilter(4, [lo, hi], btype='band', fs=SR, ftype='butter')
    r = _sci.lfilter(b, a, x).astype(_np.float32)
    pk = _np.max(_np.abs(r)) or 1.0
    return r / pk

def _np_lp(sig, cutoff):
    if not _HAS_NUMPY: return sig
    from scipy import signal as _sci
    b, a = _sci.iirfilter(2, min(cutoff, SR//2-1), btype='low', fs=SR, ftype='butter')
    return _sci.lfilter(b, a, sig).astype(_np.float32)

def _np_hp_filt(sig, cutoff):
    if not _HAS_NUMPY: return sig
    from scipy import signal as _sci
    b, a = _sci.iirfilter(2, max(cutoff, 20), btype='high', fs=SR, ftype='butter')
    return _sci.lfilter(b, a, sig).astype(_np.float32)

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
    n=int(SR*.28); crack=_np_bp(n,1200,800,1)*_np_exp(n,.025); crackle=_np_bp(n,2800,1500,2)*_np_exp(n,.08)*.4; whomp=_np_bp(n,180,80,3)*_np_exp(n,.04)*.5
    return _np_norm(_np_mix2(crack,crackle,whomp))
def _gen_hit_ice():
    n=int(SR*.35); n2=int(SR*.04); shatter=_np_hp_filt(_np.random.default_rng(4).standard_normal(n2).astype(_np.float32)*_np_exp(n2,.01),.2000)*.7
    ring=_np.zeros(n,_np.float32)
    for f,v in [(3200,.30),(4100,.22),(5300,.14),(6800,.09),(2600,.18)]: ring+=_np_sinev(n,f,v)*_np_exp(n,.06)
    ring=_np_lp(ring,7000)*.5; base=_np.zeros(n,_np.float32); base[:n2]+=shatter[:n]
    return _np_norm(_np_mix2(base,ring))
def _gen_hit_lightning():
    n=int(SR*.22); snap=_np_hp_filt(_np.random.default_rng(5).standard_normal(int(SR*.008)).astype(_np.float32),3000)*1.5
    buzz=_np_bp(int(SR*.06),1800,900,6)*_np_exp(int(SR*.06),.02); body=_np_bp(n,300,200,7)*_np_exp(n,.035)*.35
    base=_np.zeros(n,_np.float32); ns=len(snap); nb=len(buzz)
    base[:min(ns,n)]+=snap[:min(ns,n)]; base[:nb]+=buzz
    env=_np.ones(n,_np.float32); r=int(SR*.10); env[-r:]=_np.linspace(1,0,r)
    return _np_norm(_np_mix2(base*env,body))
def _gen_hit_shadow():
    n=int(SR*.32); thud=_np_bp(n,220,90,8)*_np_exp(n,.05); dark=_np_sinev(n,95,.3)*_np_exp(n,.09); hollow=_np_bp(n,550,200,9)*_np_exp(n,.025)*.35
    e=_np.ones(n,_np.float32); e[:int(SR*.01)]=_np.linspace(0,1,int(SR*.01))
    return _np_norm(_np_mix2(thud*e,dark*e,hollow*e)*.9)
def _gen_hit_divine():
    n=int(SR*.40); bell=_np.zeros(n,_np.float32)
    for f,v,tau in [(880,.5,.20),(2637,.3,.12),(4400,.15,.08),(1320,.2,.15)]: bell+=_np_sinev(n,f,v)*_np_exp(n,tau)
    n_c=int(SR*.005); click=_np_hp_filt(_np.random.default_rng(11).standard_normal(n_c).astype(_np.float32)*.6,4000)
    base=_np.zeros(n,_np.float32); base[:n_c]+=click
    r=int(SR*.22); env=_np.ones(n,_np.float32); env[-r:]=_np.linspace(1,0,r)
    return _np_norm(_np_mix2(base*.4,bell*env))
def _gen_hit_nature():
    n=int(SR*.26); thunk=_np_bp(n,320,120,12)*_np_exp(n,.04); earth=_np_sinev(n,78,.25)*_np_exp(n,.07); rustle=_np_bp(n,2200,1400,13)*_np_exp(n,.025)*.22
    return _np_norm(_np_mix2(thunk,earth,rustle))
def _gen_hit_arcane():
    n=int(SR*.30); sweep=_np.zeros(n,_np.float32); phase=0.0
    for i in range(n):
        frac=i/n; freq=800+1600*frac*(1-frac)*4; phase+=2*_np.pi*freq/SR; sweep[i]=_np.sin(phase)
    sweep=sweep*_np_fade2(sweep,.005,.12)*.5; shimmer=_np_bp(n,1400,600,15)*_np_exp(n,.05)*.4
    cryst=_np.zeros(n,_np.float32)
    for f in [1760,2640,3520]: cryst+=_np_sinev(n,f,.12)*_np_exp(n,.04)
    return _np_norm(_np_mix2(sweep,shimmer,cryst))

# ── Physical hit variants ─────────────────────────────────────
def _gen_hit_light():
    n=int(SR*.14); tick=_np_bp(n,900,400,30)*_np_exp(n,.025); flesh=_np_bp(n,320,120,31)*_np_exp(n,.018)*.4
    return _np_norm(_np_mix2(tick,flesh)*_np_fade2(_np.ones(n,_np.float32),.001,.06))
def _gen_hit_medium():
    n=int(SR*.20); thwack=_np_bp(n,450,200,33)*_np_exp(n,.04); low=_np_bp(n,140,60,34)*_np_exp(n,.055)*.45
    nc=int(SR*.015); crack=_np_hp_filt(_np.random.default_rng(35).standard_normal(nc).astype(_np.float32)*.6,1800)*_np_exp(nc,.008)
    base=_np.zeros(n,_np.float32); base[:nc]+=crack
    return _np_norm(_np_mix2(thwack,low,base)*_np_fade2(_np.ones(n,_np.float32),.001,.09))
def _gen_hit_heavy():
    n=int(SR*.32); boom=_np_bp(n,120,55,37)*_np_exp(n,.08); sub=_np_sinev(n,55,.35)*_np_exp(n,.10)
    crack=_np_bp(n,280,120,38)*_np_exp(n,.04)*.5; stone=_np_bp(n,700,300,39)*_np_exp(n,.02)*.25
    return _np_norm(_np_mix2(boom,sub,crack,stone)*_np_fade2(_np.ones(n,_np.float32),.002,.15))
def _gen_hit_critical():
    n1=int(SR*.05); crack_hi=_np_hp_filt(_np.random.default_rng(20).standard_normal(n1).astype(_np.float32),2000)*_np_exp(n1,.008)*1.2
    crack_lo=_np_bp(n1,200,100,21)*_np_exp(n1,.015)*.8; sub_hit=_np_sinev(n1,60,.6)*_np_exp(n1,.02)
    impact=_np_norm(_np_mix2(crack_hi,crack_lo,sub_hit),.95)
    gap=_np_sil(.028); n3=int(SR*.42)
    ring_lo=_np_sinev(n3,140,.45)*_np_exp(n3,.12); ring_mid=_np_sinev(n3,220,.30)*_np_exp(n3,.09)
    ring_hi=_np_sinev(n3,380,.15)*_np_exp(n3,.06); rumble=_np_sinev(n3,55,.35)*_np_exp(n3,.15)
    shimmer=_np_bp(n3,800,350,22)*_np_exp(n3,.04)*.18
    tail=_np_norm(_np_mix2(ring_lo,ring_mid,ring_hi,rumble,shimmer),.80)
    full=_np.concatenate([impact,gap,tail])
    return _np_norm(_np_fade2(full,.001,.18))
def _gen_hit_skill_fast():
    def strike(seed):
        n=int(SR*.08)
        return _np_norm(_np_mix2(_np_bp(n,600,250,seed)*_np_exp(n,.018),_np_bp(n,200,80,seed+1)*_np_exp(n,.025)*.4),.65)
    s1=strike(70); s2=strike(72); s3=strike(74); gap=int(SR*.07)
    n_t=len(s1)+gap+len(s2)+gap+len(s3); out=_np.zeros(n_t,_np.float32)
    o=0; out[o:o+len(s1)]+=s1; o+=len(s1)+gap; out[o:o+len(s2)]+=s2*.88; o+=len(s2)+gap; out[o:o+len(s3)]+=s3*.78
    return _np_norm(out)

# ── Miss sounds ───────────────────────────────────────────────
def _gen_miss_physical():
    n=int(SR*.22); swing=_np_bp(n,350,200,40)*_np_exp(n,.06)
    swing*=(_np.linspace(.4,1.0,n)**.5*_np.linspace(1.0,0.0,n)**.3).astype(_np.float32)
    n2=int(SR*.06); s=int(SR*.16); stumble=_np_bp(n2,180,80,41)*_np_exp(n2,.03)*.3
    base=_np.zeros(n,_np.float32); e=min(n,s+n2); base[s:e]+=stumble[:e-s]
    return _np_norm(_np_fade2(_np_mix2(swing,base),.005,.08))
def _gen_miss_magic():
    build=_np_bp(int(SR*.08),1400,600,42)*_np.linspace(0,1,int(SR*.08)).astype(_np.float32)**.5*.5
    n_f=int(SR*.20); fizzle=_np_bp(n_f,900,500,43)*_np_exp(n_f,.06)*.4+_np_sinev(n_f,320,.15)*_np_exp(n_f,.08)
    return _np_norm(_np_fade2(_np.concatenate([build,fizzle]),.005,.10))
def _gen_miss_elemental():
    surge=_np_bp(int(SR*.06),1600,900,44)*_np_exp(int(SR*.06),.015)*.7
    n2=int(SR*.18); die=_np_bp(n2,800,400,45)*_np_exp(n2,.04)*.35+_np_sinev(n2,280,.12)*_np_exp(n2,.07)
    return _np_norm(_np_fade2(_np.concatenate([surge,die]),.002,.09))

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
    n=int(SR*.55); t=_np.arange(n)/SR
    brs=_np.zeros(n,_np.float32)
    for f,v in [(110,.30),(165,.18),(220,.12),(330,.08)]:
        brs+=_np_sinev(n,f,v)*(_np.sin(_np.pi*t/t[-1])**.6).astype(_np.float32)
    punch=_np_bp(n,400,160,90)*_np_exp(n,.08)*.2
    return _np_norm(_np_mix2(brs,punch)*_np_fade2(_np.ones(n,_np.float32),.02,.18))
def _gen_buff_magic():
    n=int(SR*.48); sweep=_np.zeros(n,_np.float32); phase=0.0
    for i in range(n):
        freq=400+1000*(i/n)**1.5; phase+=2*_np.pi*freq/SR; sweep[i]=_np.sin(phase)*.35
    cryst=_np.zeros(n,_np.float32)
    for f in [880,1320,1760,2640]: cryst+=_np_sinev(n,f,.12)*_np_exp(n,.08)
    return _np_norm(_np_mix2(sweep,cryst)*_np_fade2(_np.ones(n,_np.float32),.015,.20))
def _gen_buff_divine():
    n=int(SR*.50); bell=_np.zeros(n,_np.float32)
    for f,v,tau in [(880,.4,.18),(2200,.25,.10),(3300,.15,.07),(1320,.2,.14)]: bell+=_np_sinev(n,f,v)*_np_exp(n,tau)
    soft=_np_bp(n,3000,1200,94)*_np_exp(n,.03)*.06
    n_c=int(SR*.004); click=_np_hp_filt(_np.random.default_rng(95).standard_normal(n_c).astype(_np.float32)*.5,5000)
    base=_np.zeros(n,_np.float32); base[:n_c]+=click
    r=int(SR*.22); env=_np.ones(n,_np.float32); env[-r:]=_np.linspace(1,0,r)
    return _np_norm(_np_mix2(base*.3,bell*env,soft))
def _gen_buff_nature():
    n=int(SR*.45); root=_np_sinev(n,110,.28)*_np_exp(n,.12); fifth=_np_sinev(n,165,.15)*_np_exp(n,.10)
    rustle=_np_bp(n,2400,1200,96)*_np_exp(n,.04)*.15; thud=_np_bp(n,200,80,97)*_np_exp(n,.05)*.22
    return _np_norm(_np_mix2(root,fifth,rustle,thud)*_np_fade2(_np.ones(n,_np.float32),.01,.18))

# ── Debuff variants ───────────────────────────────────────────
def _gen_debuff_physical():
    n=int(SR*.48); grind=_np_bp(n,280,120,100)*_np_exp(n,.10)
    sweep=_np.zeros(n,_np.float32); phase=0.0
    for i in range(n):
        freq=600-450*(i/n)**.7; phase+=2*_np.pi*freq/SR; sweep[i]=_np.sin(phase)*.3*(1-i/n)**.4
    return _np_norm(_np_mix2(grind,sweep)*_np_fade2(_np.ones(n,_np.float32),.005,.15))
def _gen_debuff_magic():
    n=int(SR*.50); dark=_np_sinev(n,82,.25)*_np_exp(n,.12); clash=_np_sinev(n,87,.15)*_np_exp(n,.10)
    hiss=_np_bp(n,800,400,102)*_np_exp(n,.06)*.18; sub=_np_sinev(n,41,.2)*_np_exp(n,.14)
    return _np_norm(_np_mix2(dark,clash,hiss,sub)*_np_fade2(_np.ones(n,_np.float32),.005,.18))
def _gen_debuff_divine():
    n=int(SR*.55); toll=_np_sinev(n,440,.4)*_np_exp(n,.15); clash=_np_sinev(n,466,.3)*_np_exp(n,.12)
    low=_np_sinev(n,110,.2)*_np_exp(n,.12); ne=_np_bp(n,2000,800,103)*_np_exp(n,.03)*.10
    return _np_norm(_np_mix2(toll,clash,low,ne)*_np_fade2(_np.ones(n,_np.float32),.003,.22))

# ── Dungeon music tracks ──────────────────────────────────────
def _gen_dungeon(fn):
    if not _HAS_NUMPY: return None
    try:
        sig = fn()
        d = (_np.clip(sig,-1,1)*32767).astype(_np.int16)
        return _make_sound(list(d))
    except Exception:
        return None

def _dungeon_goblin_warren():
    N=int(SR*16.0); drums=_np.zeros(N,_np.float32)
    hits=[0.0,.18,.36,.75,.90,1.13,1.50,1.65,1.88,2.25,2.40,2.63,3.0,3.15,3.38,3.75,3.88,4.13,4.50,4.65,4.88,5.25,5.40,5.63,6.0,6.13,6.38,6.75,6.88,7.13,7.50,7.63,7.88,8.25,8.40,8.63,9.0,9.13,9.36,9.75,9.88,10.13,10.5,10.63,10.88,11.25,11.38,11.63,12.0,12.13,12.38,12.75,12.88,13.13,13.5,13.63,13.88,14.25,14.38,14.63,15.0,15.13,15.38,15.75]
    for i,t in enumerate(hits):
        if i%3==0:
            n_h=int(SR*.18); h=_np_sinev(n_h,80+(i%5)*15,.45)*_np_exp(n_h,.04)+_np_bp(n_h,300,150,i)*_np_exp(n_h,.02)*.2
        else:
            n_h=int(SR*.10); h=_np_bp(n_h,600+i*30,250,i+50)*_np_exp(n_h,.025)*.3
        _np_place2(drums,t,h)
    drums=_np_lp(drums,1200)
    horn_notes=[(110,.5),(147,.4),(165,.4),(147,.3),(130,.5),(110,.8)]; horn_times=[0.0,2.0,2.4,2.8,4.0,4.5]
    horn=_np.zeros(N,_np.float32)
    for rep in range(2):
        for (freq,dur),t in zip(horn_notes,horn_times):
            if rep*8.0+t<16.0: _np_place2(horn,rep*8.0+t,_np_note(freq,dur,.22,.08))
    horn=_np_lp(horn,500)
    drone=_np_sinev(N,55,.08)*_np_swell2(N,7.0,0,.4)+_np_bp(N,130,50,5)*_np_swell2(N,4.5,2,.5)*.05
    scurry=_np_bp(N,2400,1200,6)*_np_swell2(N,1.1,.3,.8)*.04
    return _np_seamless2(_np_norm(_np_mix2(drums*.8,horn*.7,drone,scurry)))

def _dungeon_spiders_nest():
    N=int(SR*20.0); mel_freqs=[880,622,740,554,880,831,622,740]; mel_times=[0.0,1.8,3.2,5.0,7.5,9.0,11.5,14.0]
    mel=_np.zeros(N,_np.float32)
    for freq,t in zip(mel_freqs,mel_times):
        if t<20.0: _np_place2(mel,t,_np_note(freq,1.2,.12,.4))
    mel=_np_lp(mel,2000)
    skitter=_np.zeros(N,_np.float32); rng=_np.random.default_rng(99); t_s=0.0
    while t_s<19.5:
        gap=float(rng.uniform(.08,.55)); n_s=int(SR*.025)
        s=_np_hp_filt(_np.random.default_rng(int(t_s*100)).standard_normal(n_s).astype(_np.float32),3000)*_np_exp(n_s,.008)*float(rng.uniform(.1,.25))
        _np_place2(skitter,t_s,s); t_s+=gap
    web=_np_sinev(N,62,.10)*_np_swell2(N,12.0,0,.35)+_np_sinev(N,93,.05)*_np_swell2(N,8.0,3.0,.45)
    fading=_np_bp(N,3500,1500,7)*_np_swell2(N,6.0,1.5,.7)*.04*_np_swell2(N,2.2,0,.85)
    snaps=_np.zeros(N,_np.float32)
    for snap_t in [3.5,7.2,11.8,16.4]:
        n_sn=int(SR*.06); sn=_np_bp(n_sn,1200,600,int(snap_t*10))*_np_exp(n_sn,.015)*.15
        _np_place2(snaps,snap_t,sn)
    return _np_seamless2(_np_norm(_np_mix2(mel,skitter*.6,web,fading,snaps)))

def _dungeon_abandoned_mine():
    N=int(SR*18.0); beat=60.0/72; picks=_np.zeros(N,_np.float32)
    for i in range(int(18.0/beat)):
        t=i*beat; vol=.28 if i%4==0 else (.18 if i%2==0 else .10); n_p=int(SR*.15)
        strike=_np_bp(n_p,800,400,i)*_np_exp(n_p,.04)*vol+_np_bp(n_p,2200,800,i+100)*_np_exp(n_p,.02)*vol*.3
        _np_place2(picks,t,strike)
    stone=_np.zeros(N,_np.float32)
    for (freq,dur),t in zip([(65,.30),(55,.30),(49,.30),(58,.30)],[0.0,4.5,9.0,13.5]):
        n_st=min(int(SR*dur*4),N-int(SR*t)); n_st=max(0,n_st)
        if n_st>0:
            s=(_np_sinev(n_st,freq,.25)+_np_sinev(n_st,freq*2,.25*.3))*_np.minimum(_np.arange(n_st)/(SR*.15),1.0).astype(_np.float32)*_np_exp(n_st,.8)
            _np_place2(stone,t,s)
    stone=_np_lp(stone,200)
    corrupt=_np.zeros(N,_np.float32)
    for t in [2.0,5.5,8.0,11.5,14.5,17.0]:
        n_c=int(SR*.5); c=(_np_sinev(n_c,110,.15)+_np_sinev(n_c,116,.10))*_np_exp(n_c,.12); _np_place2(corrupt,t,c)
    creak=_np_bp(N,280,100,8)*_np_swell2(N,9.0,0,.6)*.06; sub=_np_sinev(N,42,.06)*_np_swell2(N,15.0,0,.4)
    return _np_seamless2(_np_norm(_np_mix2(picks*.7,stone,corrupt,creak,sub)))

def _dungeon_ruins_ashenmoor():
    N=int(SR*22.0)
    heat=_np_lp(_np_sinev(N,87,.16)*_np_swell2(N,11.0,0,.45)+_np_sinev(N,92,.10)*_np_swell2(N,8.0,4,.50)+_np_sinev(N,58,.12)*_np_swell2(N,15.0,2,.35),300)
    ash=_np_bp(N,650,250,10)*_np_swell2(N,7.0,0,.6)*.10+_np_bp(N,1400,600,11)*_np_swell2(N,4.5,2.5,.7)*.05
    flares=_np.zeros(N,_np.float32)
    for t in [3.5,8.0,13.5,19.0]:
        n_f=int(SR*1.2); f=(_np_sinev(n_f,65,.20)+_np_bp(n_f,500,200,int(t*10))*.12)*_np.hanning(n_f).astype(_np.float32)**.5*.8
        _np_place2(flares,t,_np_lp(f,400))
    shadow=_np.zeros(N,_np.float32)
    for t,freq in [(1.0,196),(5.5,185),(11.0,175),(16.5,196)]:
        n_sh=int(SR*2.5); sh=(_np_sinev(n_sh,freq,.14)*_np_exp(n_sh,.6)+_np_sinev(n_sh,freq*1.5,.07)*_np_exp(n_sh,.4))
        _np_place2(shadow,t,sh)
    wail=_np_bp(N,1800,400,12)*_np_swell2(N,18.0,0,.75)*.06
    return _np_seamless2(_np_norm(_np_mix2(heat,ash,flares,shadow,wail)))

def _dungeon_sunken_crypt():
    N=int(SR*20.0); drips=_np.zeros(N,_np.float32)
    drip_times=[0.0,1.35,2.1,3.7,4.8,5.55,7.2,8.3,9.0,10.5,11.6,12.35,14.0,15.1,15.85,17.5,18.6,19.35]
    rng_d=_np.random.default_rng(33)
    for i,t in enumerate(drip_times):
        freq=float(rng_d.uniform(900,2400)); n_d=int(SR*.05)
        d=_np_bp(n_d,freq,400,i+200)*_np_exp(n_d,.012)*float(rng_d.uniform(.12,.22)); _np_place2(drips,t,d)
    crypt=_np_lp(_np_sinev(N,73,.14)*_np_swell2(N,13.0,0,.40)+_np_sinev(N,55,.10)*_np_swell2(N,9.0,3,.45),250)
    moan=_np.zeros(N,_np.float32)
    for t,freq in [(2.5,165),(7.0,147),(13.5,155),(18.0,165)]:
        n_m=int(SR*2.0); m=(_np_sinev(n_m,freq,.08)+_np_sinev(n_m,freq*1.5,.04))*_np.hanning(n_m).astype(_np.float32)
        _np_place2(moan,t,_np_lp(m,500))
    water=_np_bp(N,180,80,14)*_np_swell2(N,6.0,0,.5)*.08+_np_bp(N,80,35,15)*_np_swell2(N,8.5,2,.55)*.06
    groans=_np.zeros(N,_np.float32)
    for t in [5.0,12.0,18.5]:
        n_g=int(SR*.8); g=_np_bp(n_g,200,80,int(t*5))*_np_exp(n_g,.2)*.18; _np_place2(groans,t,g)
    return _np_seamless2(_np_norm(_np_mix2(drips*.8,crypt,moan,water,groans)))

def _dungeon_pale_coast():
    N=int(SR*24.0); mel_data=[(293,1.5),(329,1.0),(349,1.5),(329,.8),(293,2.0),(261,1.5),(293,1.0),(329,2.5),(293,1.5),(261,1.0),(220,1.5),(247,1.0),(293,2.5)]
    mel_t=[0.0]
    for _,d in mel_data[:-1]: mel_t.append(mel_t[-1]+d)
    melody=_np.zeros(N,_np.float32)
    for (freq,dur),t in zip(mel_data,mel_t):
        if t<24.0: _np_place2(melody,t,_np_note(freq,dur*1.1,.18,.5))
    melody=_np_lp(melody,600)
    ocean=_np_lp(_np_bp(N,85,45,16)*_np_swell2(N,8.5,0,.55)*.18+_np_bp(N,55,25,17)*_np_swell2(N,12.0,4,.50)*.12,250)
    drips=_np.zeros(N,_np.float32)
    for i,t in enumerate([1.5,4.2,6.8,9.1,11.7,14.3,16.9,19.4,21.8]):
        n_d=int(SR*.06); d=_np_bp(n_d,600+i*80,200,i+300)*_np_exp(n_d,.018)*.15; _np_place2(drips,t,d)
    presence=_np_sinev(N,293,.06)*_np_swell2(N,20.0,0,.6)+_np_sinev(N,440,.03)*_np_swell2(N,15.0,6,.7)
    return _np_seamless2(_np_norm(_np_mix2(melody*.75,ocean,drips,presence)))

def _dungeon_windswept_isle():
    N=int(SR*22.0); harm_data=[(165,3.0),(175,2.0),(196,2.5),(175,1.5),(165,3.5),(147,2.0),(165,3.0),(196,4.5)]
    harm_t=[0.0]
    for _,d in harm_data[:-1]: harm_t.append(harm_t[-1]+d)
    harmony=_np.zeros(N,_np.float32)
    for (freq,dur),t in zip(harm_data,harm_t):
        if t<22.0:
            n_h=int(SR*dur); h=(_np_sinev(n_h,freq,.20)+_np_sinev(n_h,freq*2,.10)+_np_sinev(n_h,freq*3,.05))
            env=_np.minimum(_np.arange(n_h)/(SR*.1),1.0).astype(_np.float32)*_np_exp(n_h,.8)
            _np_place2(harmony,t,(h*env).astype(_np.float32))
    wind_int=_np_bp(N,380,200,18)*_np_swell2(N,5.0,0,.6)*.14+_np_bp(N,180,80,19)*_np_swell2(N,7.5,2.5,.5)*.08
    stone_hum=_np_sinev(N,82,.10)*_np_swell2(N,18.0,0,.4)+_np_sinev(N,123,.06)*_np_swell2(N,11.0,5,.5)
    guardian=_np.zeros(N,_np.float32)
    for t,freq in [(0.0,55),(11.0,49),(0.0,73),(11.0,67)]:
        n_g=int(SR*11.0); g=_np_sinev(n_g,freq,.08)*_np_exp(n_g,4.0); _np_place2(guardian,t,g)
    guardian=_np_lp(guardian,150)
    return _np_seamless2(_np_norm(_np_mix2(harmony*.70,wind_int,stone_hum,guardian)))

def _dungeon_dragons_tooth():
    N=int(SR*20.0)
    seismic=_np_lp(_np_sinev(N,28,.22)*_np_swell2(N,9.0,0,.50)+_np_sinev(N,42,.14)*_np_swell2(N,6.5,3,.55),100)
    heat=_np_bp(N,220,90,20)*_np_swell2(N,4.5,0,.6)*.14+_np_bp(N,120,55,21)*_np_swell2(N,7.0,2.5,.55)*.10
    breath=_np.zeros(N,_np.float32)
    for t,vol in [(0.0,.22),(5.0,.18),(10.0,.25),(15.5,.20)]:
        n_b=int(SR*3.5); b=_np_bp(n_b,95,45,int(t*5))*_np_swell2(n_b,3.5,0,.6)*vol*_np.hanning(n_b).astype(_np.float32)**.6
        _np_place2(breath,t,_np_lp(b,300))
    stones=_np.zeros(N,_np.float32)
    for t,vol in [(1.5,.35),(4.2,.28),(7.8,.40),(11.3,.32),(14.0,.38),(17.5,.30)]:
        n_s=int(SR*.45); s=(_np_sinev(n_s,55,.5)+_np_bp(n_s,300,150,int(t*20))*.3)*_np_exp(n_s,.08)*vol
        _np_place2(stones,t,s)
    stones=_np_lp(stones,400)
    karreth=_np.zeros(N,_np.float32)
    for t,freq in [(2.0,98),(6.5,87),(11.0,98),(15.5,73)]:
        _np_place2(karreth,t,_np_note(freq,2.0,.22,.35))
    karreth=_np_lp(karreth,400)
    return _np_seamless2(_np_norm(_np_mix2(seismic,heat,breath,stones,karreth*.8)))

def _dungeon_valdris_spire():
    N=int(SR*28.0)
    foundation=_np_lp(_np_sinev(N,36,.20)*_np_swell2(N,14.0,0,.40)+_np_sinev(N,54,.12)*_np_swell2(N,9.5,5,.45)+_np_sinev(N,27,.10)*_np_swell2(N,20.0,0,.35),180)
    valdris_mel=[(123,2.5),(147,2.0),(165,2.5),(185,3.0),(196,2.0),(220,2.5),(196,1.5),(185,2.0),(165,2.5),(147,2.0),(123,3.5)]
    vm_t=[0.0]
    for _,d in valdris_mel[:-1]: vm_t.append(vm_t[-1]+d)
    v_mel=_np.zeros(N,_np.float32); dark_h=_np.zeros(N,_np.float32)
    for (freq,dur),t in zip(valdris_mel,vm_t):
        if t<28.0:
            _np_place2(v_mel,t,_np_note(freq,dur*1.2,.20,.6))
            _np_place2(dark_h,t,_np_note(freq*1.414,dur*1.2,.10,.5))
        t2=t+14.0
        if t2<28.0: _np_place2(v_mel,t2,_np_note(freq*2,dur*1.2,.14,.5))
    v_mel=_np_lp(v_mel,800); dark_h=_np_lp(dark_h,600)
    beat=60.0/65; drums=_np.zeros(N,_np.float32)
    for i in range(int(28.0/beat)):
        t=i*beat; vol=.32 if i%4==0 else (.20 if i%2==0 else .12); n_d=int(SR*.35)
        d=_np_sinev(n_d,45,.5)*_np_exp(n_d,.06)*vol+_np_bp(n_d,250,120,i*7)*_np_exp(n_d,.03)*vol*.4
        _np_place2(drums,t,d)
    drums=_np_lp(drums,300)
    fading_hiss=_np_bp(N,4000,2000,22)*_np_swell2(N,7.0,0,.8)*.05*_np_swell2(N,3.5,1.5,.7)
    ascend=_np_bp(N,550,200,23)*_np_swell2(N,28.0,_np.pi,.70)*.10+_np_bp(N,380,150,24)*_np_swell2(N,28.0,_np.pi*.7,.65)*.07
    return _np_seamless2(_np_norm(_np_mix2(foundation,v_mel*.75,dark_h*.6,drums*.7,fading_hiss,ascend)))

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
        _sounds["no_resource"]    = _make_sound(_mix(_sine(180, 0.28, 0.16), _noise(0.10, 0.08)))
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
        _sounds["death"]        = _make_sound(_mix(_sweep(380, 65, 0.80, 0.32), _noise(0.50, 0.16)))
        _sounds["enemy_death"] = _make_sound(_concat(
            _mix(_noise(0.55, 0.06), _sine(220, 0.55, 0.06)), _silence(0.04),
            _sweep(500, 40, 0.70, 0.32),
            _mix(_sine(40, 0.50, 0.22), _noise(0.25, 0.16)),
            _sweep(80, 20, 0.80, 0.18), _silence(0.06)))
        _sounds["victory"]      = _make_sound(_concat(
            _sine(523, 0.18, 0.32), _sine(659, 0.18, 0.32),
            _sine(784, 0.18, 0.32), _sine(1047, 0.40, 0.38)))
        _sounds["defeat"]       = _make_sound(_concat(
            _sine(400, 0.28, 0.30), _sine(350, 0.28, 0.30),
            _sine(300, 0.28, 0.30), _sine(200, 0.55, 0.30)))
        _sounds["combat_start"] = _make_sound(_mix(
            _noise(0.25, 0.32),
            _concat(_sine(220, 0.14, 0.32), _sine(330, 0.14, 0.32), _sine(440, 0.20, 0.38))))
        _sounds["block"]        = _make_sound(_mix(_noise(0.12, 0.32), _sine(170, 0.16, 0.22)))
        _sounds["poison"]       = _make_sound(_mix(_sweep(520, 280, 0.38, 0.18), _noise(0.20, 0.10)))

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
        _sounds["step"]       = _make_sound(
            _mix(_noise(0.08, 0.12, seed=17), _sine(90, 0.08, 0.10)))

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
