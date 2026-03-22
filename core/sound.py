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
        _generate_all_sounds()
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
#  SOUND DEFINITIONS
# ═══════════════════════════════════════════════════════════════



def _generate_all_sounds():
    # ── UI ──────────────────────────────────────────────────────
    _sounds["ui_click"]   = _make_sound(_sine(800, 0.10, 0.22))
    _sounds["ui_confirm"] = _make_sound(_concat(_sine(600, 0.10, 0.28), _sine(900, 0.14, 0.28)))
    _sounds["ui_cancel"]  = _make_sound(_sine(280, 0.22, 0.22))
    _sounds["ui_open"]    = _make_sound(_sweep(400,  820, 0.28, 0.22))
    _sounds["ui_close"]   = _make_sound(_sweep(820,  380, 0.22, 0.22))

    # ── Combat ──────────────────────────────────────────────────
    _sounds["hit_physical"] = _make_sound(_mix(
        _noise(0.18, 0.38), _sine(160, 0.20, 0.28)))
    # Skill attack: heavier, deeper impact — used for STR-SP/DEX-SP/Ki abilities
    # hit_skill: heavy physical blow — meaty crack, bone-deep impact, low rumble
    # Completely different frequency profile from hit_magic (low vs high)
    _sounds["hit_skill"] = _make_sound(_concat(
        _mix(_noise(0.55, 0.07), _sine(80, 0.60, 0.09)),   # deep bone crack
        _mix(_sine(55, 0.65, 0.20), _noise(0.40, 0.12)),   # body thud resonance
        _sweep(100, 40, 0.50, 0.14),                        # low decay rumble
        _silence(0.03),
        _sine(45, 0.30, 0.06),                              # sub-bass tail
    ))
    _sounds["hit_critical"] = _make_sound(_mix(
        _noise(0.22, 0.48), _sine(130, 0.26, 0.38), _sine(260, 0.18, 0.22)))
    # hit_magic: bright high-frequency burst — clearly magical, short and sharp
    _sounds["hit_magic"] = _make_sound(_concat(
        _mix(_sine(1200, 0.06, 0.35), _sine(800, 0.08, 0.28)),  # sharp bright crack
        _mix(_sweep(700, 300, 0.20, 0.22), _sine(440, 0.22, 0.14)),  # magical shimmer
        _silence(0.02),
        _sine(220, 0.12, 0.08),   # brief low resonance
    ))
    _sounds["miss"]         = _make_sound(_concat(
        _sweep(800, 200, 0.18, 0.22),   # fast whoosh sweep
        _noise(0.08, 0.08)))              # brief thud of miss
    # No resource: dry buzzing click — "nope, can't do that"
    _sounds["no_resource"]  = _make_sound(_mix(
        _sine(180, 0.28, 0.16), _noise(0.10, 0.08)))
    # Spell miss/resist: magic whoosh that dissipates without impact
    _sounds["spell_miss"]   = _make_sound(_concat(
        _sweep(1200, 400, 0.22, 0.16),  # high magical rise
        _silence(0.03),
        _sweep(400, 150, 0.28, 0.18),   # fizzle descend
        _noise(0.06, 0.10)))              # dissipation noise
    _sounds["heal"]         = _make_sound(_concat(
        _sine(523, 0.18, 0.28), _sine(659, 0.18, 0.28), _sine(784, 0.24, 0.32)))
    _sounds["buff"]         = _make_sound(_sweep(280, 940, 0.50, 0.22))
    _sounds["debuff"]       = _make_sound(_sweep(720, 180, 0.55, 0.26))
    _sounds["death"]        = _make_sound(_mix(
        _sweep(380, 65, 0.80, 0.32), _noise(0.50, 0.16)))
    # Enemy death: sharp impact crack → low tumble → silence — distinctive & satisfying
    # enemy_death: unmistakable kill sound — 3 distinct stages
    # Stage 1: sharp impact (the killing blow lands)
    # Stage 2: slow dramatic descend (enemy falling)
    # Stage 3: deep bass thud + silence (final stillness)
    _sounds["enemy_death"] = _make_sound(_concat(
        _mix(_noise(0.55, 0.06), _sine(220, 0.55, 0.06)),  # killing impact
        _silence(0.04),                                      # breath before fall
        _sweep(500, 40, 0.70, 0.32),                        # long dramatic descend
        _mix(_sine(40, 0.50, 0.22), _noise(0.25, 0.16)),   # ground impact thud
        _sweep(80, 20, 0.80, 0.18),                         # low bass decay
        _silence(0.06),                                      # final silence
    ))
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

    # ── Dungeon ─────────────────────────────────────────────────
    _sounds["door_open"] = _make_sound(_concat(
        # Quick wooden creak (0.18s) — the hinge, not a long scrape
        _creak(0.18, 280, 80, volume=0.30, slip_count=4, seed=7),
        # Brief mid-frequency wood-on-wood grind as door moves (0.14s)
        _mix(
            _creak(0.14, 180, 60, volume=0.18, slip_count=3, seed=23),
            _bandpass_noise(0.14, 220, 80, volume=0.05, seed=31),
        ),
        # Door settles: low thud as it opens fully
        _silence(0.04), _thud(0.12, 0.18),
    ))
    _sounds["treasure_open"] = _make_sound(_concat(
        _creak(0.45, 620, 140, volume=0.25, slip_count=7, seed=33),
        _silence(0.05),
        _creak(0.55, 480, 110, volume=0.20, slip_count=8, seed=44),
        _silence(0.07), _thud(0.10, 0.10),
    ))
    _sounds["stairs"]       = _make_sound(_concat(
        _sine(300, 0.16, 0.22), _sine(350, 0.16, 0.22), _sine(420, 0.22, 0.28)))
    _sounds["trap_trigger"] = _make_sound(_mix(
        _noise(0.35, 0.42), _sweep(900, 80, 0.40, 0.32)))
    _sounds["journal_find"] = _make_sound(_concat(
        _sine(440, 0.16, 0.22), _sine(554, 0.16, 0.22), _sine(659, 0.24, 0.28)))

    # ── Town ────────────────────────────────────────────────────
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

    # ── Exploration ─────────────────────────────────────────────
    _sounds["encounter"]  = _make_sound(_mix(               # random combat starts
        _noise(0.20, 0.40),
        _concat(_sine(180, 0.10, 0.28), _sine(240, 0.10, 0.32), _sine(320, 0.18, 0.38))))
    _sounds["discovery"]  = _make_sound(_concat(            # new area / secret found
        _sine(523, 0.14, 0.22), _sine(659, 0.14, 0.26),
        _sine(784, 0.14, 0.28), _sine(1047, 0.32, 0.36)))
    _sounds["camp_rest"]  = _make_sound(_concat(            # resting at camp or inn
        _sine(330, 0.30, 0.18), _silence(0.10),
        _sine(370, 0.30, 0.18), _silence(0.10),
        _sine(440, 0.50, 0.20)))
    _sounds["trap"]       = _make_sound(_mix(               # trap detected / stepped on
        _noise(0.28, 0.36), _sweep(700, 120, 0.32, 0.28)))
    _sounds["step"]       = _make_sound(                    # footstep in dungeon
        _mix(_noise(0.08, 0.12, seed=17), _sine(90, 0.08, 0.10)))

    # ── Ambient loops (kept short; play() on loop channel) ──────
    # Town music: ~32-bar looping folk piece in G major (3/4 waltz, 100 BPM)
    # Four phrases (A/B/C/B), four layers: melody, counter-melody, bass, pad.
    # Softer harmonics, gentle vibrato, smoother loop seam than old version.
    def _flute(freq, dur, vol=0.16):
        """Soft flute with gentle vibrato and smooth attack/release."""
        n = int(SR * dur)
        out = []
        for i in range(n):
            t   = i / SR
            env = math.sin(math.pi * t / dur) ** 0.6
            vib = 1.0 + 0.012 * math.sin(2 * math.pi * 5.5 * t)   # 5.5 Hz vibrato
            v   = (math.sin(2*math.pi*freq*vib*t)
                   + math.sin(2*math.pi*freq*2*t) * 0.14   # softer 2nd harmonic
                   + math.sin(2*math.pi*freq*3*t) * 0.04)
            out.append(max(-32767, min(32767, int(32000 * vol * env * v))))
        return out

    def _flute2(freq, dur, vol=0.10):
        """Slightly breathy counter-melody flute — weaker, higher register."""
        n = int(SR * dur)
        out = []
        rng2 = random.Random(freq)
        for i in range(n):
            t   = i / SR
            env = math.sin(math.pi * t / dur) ** 0.5
            breath = rng2.gauss(0, 0.04)   # subtle breathiness
            v = math.sin(2*math.pi*freq*t) + math.sin(2*math.pi*freq*2*t)*0.08 + breath
            out.append(max(-32767, min(32767, int(32000 * vol * env * v))))
        return out

    def _plk(freq, dur, vol=0.11):
        """Plucked lute — warmer decay, gentle 2nd harmonic."""
        n   = int(SR * dur)
        tau = SR * 0.22    # slower decay → warmer
        out = []
        for i in range(n):
            env = math.exp(-i / tau)
            v   = (math.sin(2*math.pi*freq*i/SR)
                   + math.sin(2*math.pi*freq*2*i/SR)*0.28
                   + math.sin(2*math.pi*freq*3*i/SR)*0.08)
            out.append(max(-32767, min(32767, int(32000 * vol * env * v))))
        return out

    def _chd(freqs, dur, vol=0.055):
        """Warm pad chord with slow attack and fade."""
        n   = int(SR * dur)
        out = [0.0] * n
        for freq in freqs:
            for i in range(n):
                t   = i / SR
                env = min(1.0, t * 4.0) * math.sin(math.pi * t / dur) ** 0.35
                v   = math.sin(2*math.pi*freq*t) + math.sin(2*math.pi*freq*2*t)*0.10
                out[i] += vol * env * v / len(freqs)
        return [max(-32767, min(32767, int(32000 * v))) for v in out]

    def _sil(d): return [0] * int(SR * d)

    # Note frequencies (Hz) — G major pentatonic core
    G3,D3,C3,E3 = 196.0, 146.8, 130.8, 164.8
    G4,A4,B4    = 392.0, 440.0, 493.9
    C5,D5,E5,F5 = 523.3, 587.3, 659.3, 698.5

    BPM  = 100
    beat = 60.0 / BPM       # 3/4 waltz
    bar  = beat * 3

    # ── Melody: 4 phrases × 8 bars = 32 bars ──────────────────
    #  Phrase A — rises and settles (bars 1-8)
    phA = (
        _flute(G4,beat)+_flute(A4,beat)+_flute(B4,beat) +          # bar 1
        _flute(C5,beat)+_flute(C5,beat)+_flute(B4,beat) +          # bar 2
        _flute(G4,beat*0.5)+_flute(E5,beat*0.5)+_flute(D5,beat)+_flute(B4,beat) +  # bar 3
        _flute(G4,bar) +                                            # bar 4 (held)
        _flute(D5,beat)+_flute(C5,beat)+_flute(B4,beat) +          # bar 5
        _flute(A4,beat)+_flute(G4,beat)+_flute(A4,beat) +          # bar 6
        _flute(B4,beat)+_flute(D5,beat)+_flute(G4,beat*2) +        # bar 7
        _flute(G4,bar)                                              # bar 8
    )
    #  Phrase B — wandering middle (bars 9-16)
    phB = (
        _flute(C5,beat)+_flute(D5,beat)+_flute(E5,beat) +          # bar 9
        _flute(E5,beat)+_flute(D5,beat)+_flute(C5,beat) +          # bar 10
        _flute(B4,beat*0.5)+_flute(G4,beat*0.5)+_flute(B4,beat)+_flute(D5,beat)+  # bar 11
        _flute(G4,bar) +                                            # bar 12
        _flute(E5,beat)+_flute(D5,beat)+_flute(C5,beat) +          # bar 13
        _flute(B4,beat)+_flute(A4,beat)+_flute(G4,beat) +          # bar 14
        _flute(A4,beat)+_flute(C5,beat)+_flute(B4,beat) +          # bar 15
        _flute(G4,bar)                                              # bar 16
    )
    #  Phrase C — higher register excursion (bars 17-24)
    phC = (
        _flute(E5,beat)+_flute(F5,beat*0.5)+_flute(E5,beat*0.5)+_flute(D5,beat) +  # bar 17
        _flute(C5,beat)+_flute(D5,beat)+_flute(E5,beat) +          # bar 18
        _flute(D5,bar) +                                            # bar 19
        _flute(C5,beat)+_flute(B4,beat)+_flute(A4,beat) +          # bar 20
        _flute(G4,beat)+_flute(A4,beat)+_flute(B4,beat) +          # bar 21
        _flute(C5,beat)+_flute(B4,beat)+_flute(A4,beat) +          # bar 22
        _flute(B4,beat)+_flute(G4,beat*2) +                        # bar 23
        _flute(G4,bar)                                              # bar 24
    )
    #  Phrase B (reprise, bars 25-32) — resolves loop back to A
    phB2 = (
        _flute(C5,beat)+_flute(D5,beat)+_flute(E5,beat) +          # bar 25
        _flute(D5,beat)+_flute(C5,beat)+_flute(B4,beat) +          # bar 26
        _flute(A4,beat*0.5)+_flute(G4,beat*0.5)+_flute(A4,beat)+_flute(B4,beat) +  # bar 27
        _flute(G4,bar) +                                            # bar 28
        _flute(B4,beat)+_flute(A4,beat)+_flute(G4,beat) +          # bar 29
        _flute(G4,beat)+_flute(A4,beat)+_flute(B4,beat) +          # bar 30
        _flute(D5,beat)+_flute(B4,beat)+_flute(G4,beat) +          # bar 31
        _flute(G4,bar)                                              # bar 32 → loops to bar 1
    )
    mel = phA + phB + phC + phB2

    # ── Counter-melody: low harmony below the melody ───────────
    # Stays in the lower register (G3–D4) so it warms the sound
    # rather than adding shrillness. Sparse — rests on most bars.
    def _rest(d): return _sil(d)
    # Use the plucked lute for a rounder tone in the harmony voice
    def _hmny(freq, dur, vol=0.07):
        """Soft held harmony note — sine with gentle envelope."""
        n = int(SR * dur)
        out = []
        for i in range(n):
            t   = i / SR
            env = math.sin(math.pi * t / dur) ** 0.55
            v   = math.sin(2 * math.pi * freq * t) + math.sin(2 * math.pi * freq * 2 * t) * 0.12
            out.append(max(-32767, min(32767, int(32000 * vol * env * v))))
        return out
    D4 = D3 * 2    # 293.7 Hz
    E4 = E3 * 2    # 329.6 Hz
    B3 = 246.9
    ctr = (
        # Phrase A — soft low harmony on key bars only
        _rest(bar)+_hmny(D4,bar)+_rest(bar)+_hmny(B3,bar) +         # bars 1-4
        _rest(bar)+_hmny(E4,bar)+_rest(bar)+_rest(bar) +             # bars 5-8
        # Phrase B — sparse root support
        _hmny(E4,bar)+_rest(bar)+_hmny(D4,bar)+_rest(bar) +         # bars 9-12
        _hmny(E4,bar)+_rest(bar)+_hmny(D4,bar)+_rest(bar) +         # bars 13-16
        # Phrase C — stay low, no high register
        _hmny(D4,bar)+_rest(bar)+_hmny(E4,bar)+_rest(bar) +         # bars 17-20
        _hmny(D4,bar)+_rest(bar)+_hmny(E4,bar)+_rest(bar) +         # bars 21-24
        # Phrase B2 — mirror of B
        _hmny(E4,bar)+_rest(bar)+_hmny(D4,bar)+_rest(bar) +         # bars 25-28
        _hmny(D4,bar)+_rest(bar)+_hmny(B3,bar)+_rest(bar)           # bars 29-32
    )

    # ── Bass: root on 1, fifth on 3 of each bar × 32 bars ─────
    bass_prog = [
        G3,G3,G3,G3, C3,C3,G3,G3,  # A (bars 1-8)
        C3,C3,G3,G3, C3,G3,G3,G3,  # B (bars 9-16)
        C3,C3,G3,G3, G3,G3,C3,G3,  # C (bars 17-24)
        C3,C3,G3,G3, G3,G3,G3,G3,  # B2 (bars 25-32)
    ]
    B3 = 246.9
    fifth_map = {G3:D3, C3:G3, E3:B3}
    bas = []
    for rt in bass_prog:
        fi = fifth_map.get(rt, D3)
        bas += (_plk(rt, beat*0.85)+_sil(beat*0.15) +
                _sil(beat) +
                _plk(fi, beat*0.85)+_sil(beat*0.15))

    # ── Chord pad × 32 bars ────────────────────────────────────
    chord_prog = [
        [G3*2,392.0,493.9],[G3*2,392.0,493.9],[G3*2,392.0,493.9],[G3*2,392.0,493.9],  # A
        [C3*2,329.6,392.0],[C3*2,329.6,392.0],[G3*2,392.0,493.9],[G3*2,392.0,493.9],
        [C3*2,329.6,392.0],[C3*2,329.6,392.0],[G3*2,392.0,493.9],[G3*2,392.0,493.9],  # B
        [C3*2,329.6,392.0],[G3*2,392.0,493.9],[G3*2,392.0,493.9],[G3*2,392.0,493.9],
        [C3*2,329.6,392.0],[C3*2,329.6,392.0],[G3*2,392.0,493.9],[G3*2,392.0,493.9],  # C
        [G3*2,392.0,493.9],[G3*2,392.0,493.9],[C3*2,329.6,392.0],[G3*2,392.0,493.9],
        [C3*2,329.6,392.0],[C3*2,329.6,392.0],[G3*2,392.0,493.9],[G3*2,392.0,493.9],  # B2
        [G3*2,392.0,493.9],[G3*2,392.0,493.9],[G3*2,392.0,493.9],[G3*2,392.0,493.9],
    ]
    pad = []
    for ch in chord_prog:
        pad += _chd(ch, bar)

    # Mix all layers to shortest length
    total = min(len(mel), len(ctr), len(bas), len(pad))
    town_music_samples = []
    for i in range(total):
        v = mel[i] + ctr[i] + bas[i] + pad[i]
        town_music_samples.append(max(-32767, min(32767, v)))

    # Longer fade-in/out (150 ms) to hide the loop seam more cleanly
    fade = int(SR * 0.15)
    for i in range(min(fade, total)):
        frac = i / fade
        town_music_samples[i]         = int(town_music_samples[i]         * frac)
        town_music_samples[total-1-i] = int(town_music_samples[total-1-i] * frac)

    _sounds["town_ambient"] = _make_sound(town_music_samples)

    # Town environment ambience: soft crowd hum + distant bell dings
    # Layered onto the ambient channel (separate from music channel).
    # ~8-second loop: low bandpass murmur + occasional light bell tones.
    env_dur = 8.0
    env_n   = int(SR * env_dur)
    # Low crowd murmur: narrow bandpass around 250 Hz
    crowd   = _bandpass_noise(env_dur, 250, 60, volume=0.025, seed=71)
    # Distant wind sweep (very soft)
    wind    = _bandpass_noise(env_dur, 380, 120, volume=0.018, seed=99)
    # Occasional bell dings at 2 s and 5 s marks
    bell_rng = random.Random(42)
    bell = [0] * env_n
    for t_hit in (1.8, 4.6, 7.1):
        pos   = int(t_hit * SR)
        freq  = 880.0     # high bell tone
        bdur  = int(SR * 0.8)
        for j in range(min(bdur, env_n - pos)):
            env_bell = math.exp(-j / (SR * 0.25))
            bell[pos + j] += int(3500 * env_bell * math.sin(2*math.pi*freq*j/SR))
    town_env_samples = [
        max(-32767, min(32767, crowd[i] + wind[i] + bell[i]))
        for i in range(env_n)
    ]
    # Fade edges
    fade_e = int(SR * 0.12)
    for i in range(min(fade_e, env_n)):
        frac = i / fade_e
        town_env_samples[i]          = int(town_env_samples[i]          * frac)
        town_env_samples[env_n-1-i]  = int(town_env_samples[env_n-1-i]  * frac)
    _sounds["town_env"] = _make_sound(town_env_samples)

    # World map: open wind-like sweep (kept as fallback)
    _sounds["world_ambient"] = _make_sound(
        _bandpass_noise(3.0, 180, 80, volume=0.08, seed=88))

    # ── Biome ambient sounds (layered, numpy-based) ──────────
    _sounds["ambient_grassland"] = _make_biome(_biome_grassland)
    _sounds["ambient_forest"]    = _make_biome(_biome_forest)
    _sounds["ambient_hills"]     = _make_biome(_biome_hills)
    _sounds["ambient_swamp"]     = _make_biome(_biome_swamp)
    _sounds["ambient_coast"]     = _make_biome(_biome_coast)
    _sounds["ambient_desert"]    = _make_biome(_biome_desert)

    # Dungeon: low resonant drone
    _sounds["dungeon_ambient"] = _make_sound(_mix(
        _sine(65, 2.5, 0.08, fade_out=False),
        _bandpass_noise(2.5, 110, 40, volume=0.05, seed=66)))
    # Combat music: short tense loop — percussive noise bursts on a rhythm
    _sounds["combat_music"]  = _make_sound(_concat(
        _mix(_noise(0.10, 0.32), _sine(110, 0.10, 0.18)), _silence(0.15),
        _mix(_noise(0.08, 0.28), _sine(110, 0.08, 0.15)), _silence(0.10),
        _mix(_noise(0.10, 0.32), _sine(110, 0.10, 0.18)), _silence(0.20),
        _mix(_noise(0.12, 0.36), _sine(90,  0.12, 0.22)), _silence(0.12),
        _mix(_noise(0.08, 0.28), _sine(110, 0.08, 0.15)), _silence(0.15),
        _mix(_noise(0.10, 0.32), _sine(110, 0.10, 0.18)), _silence(0.10),
        _mix(_noise(0.08, 0.28), _sine(110, 0.08, 0.15)), _silence(0.28)))


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
