"""
Realm of Shadows — Sound Engine
All sounds generated procedurally at startup — no audio files needed.
Gracefully handles missing/failed audio initialization.
"""
import math, array, random

_enabled        = False
_mixer          = None
_sounds         = {}
_music_channel  = None
_ambient_channel= None
_master_vol     = 0.6
_sfx_vol        = 0.7
_music_vol      = 0.35
_ambient_vol    = 0.25

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
        # Re-init if not initialized or if format doesn't match (freq, size, channels)
        if not current or current[0] != 22050 or current[2] != 1:
            if current:
                _mixer.quit()
            _mixer.init(22050, -16, 1, 1024)
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
    _sounds["hit_skill"] = _make_sound(_concat(
        _mix(_noise(0.38, 0.08), _sine(110, 0.50, 0.08)),  # heavy impact crack
        _mix(_sine(75, 0.55, 0.22), _noise(0.28, 0.14)),   # low body thud
        _sweep(130, 60, 0.40, 0.18),                        # brief decay rumble
    ))
    _sounds["hit_critical"] = _make_sound(_mix(
        _noise(0.22, 0.48), _sine(130, 0.26, 0.38), _sine(260, 0.18, 0.22)))
    _sounds["hit_magic"]    = _make_sound(_mix(
        _sweep(900, 180, 0.40, 0.32), _sine(440, 0.35, 0.18)))
    _sounds["miss"]         = _make_sound(_sweep(620, 380, 0.28, 0.16))
    _sounds["heal"]         = _make_sound(_concat(
        _sine(523, 0.18, 0.28), _sine(659, 0.18, 0.28), _sine(784, 0.24, 0.32)))
    _sounds["buff"]         = _make_sound(_sweep(280, 940, 0.50, 0.22))
    _sounds["debuff"]       = _make_sound(_sweep(720, 180, 0.55, 0.26))
    _sounds["death"]        = _make_sound(_mix(
        _sweep(380, 65, 0.80, 0.32), _noise(0.50, 0.16)))
    # Enemy death: sharp impact crack → low tumble → silence — distinctive & satisfying
    _sounds["enemy_death"] = _make_sound(_concat(
        # Initial sharp crack (impact)
        _mix(_noise(0.28, 0.06), _sine(220, 0.30, 0.06)),
        # Heavy mid thud
        _mix(_sine(90, 0.55, 0.18), _noise(0.35, 0.12)),
        # Low rumble fadeout
        _sweep(160, 35, 0.70, 0.28),
        _silence(0.04),
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

    # World map: open wind-like sweep
    _sounds["world_ambient"] = _make_sound(
        _bandpass_noise(3.0, 180, 80, volume=0.08, seed=88))
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
