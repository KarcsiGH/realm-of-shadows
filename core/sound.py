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
        if not _mixer.get_init():
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

def set_sfx_volume(v):
    global _sfx_vol
    _sfx_vol = max(0.0, min(1.0, v))

def set_music_volume(v):
    global _music_vol
    _music_vol = max(0.0, min(1.0, v))
    if _music_channel and _enabled:
        _music_channel.set_volume(_master_vol * _music_vol)


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
    global _sounds

    # ── UI ──────────────────────────────────────────────────────
    _sounds["ui_click"]   = _make_sound(_sine(800, 0.10, 0.22))
    _sounds["ui_confirm"] = _make_sound(_concat(_sine(600, 0.10, 0.28), _sine(900, 0.14, 0.28)))
    _sounds["ui_cancel"]  = _make_sound(_sine(280, 0.22, 0.22))
    _sounds["ui_open"]    = _make_sound(_sweep(400,  820, 0.28, 0.22))
    _sounds["ui_close"]   = _make_sound(_sweep(820,  380, 0.22, 0.22))

    # ── Combat ──────────────────────────────────────────────────
    _sounds["hit_physical"] = _make_sound(_mix(
        _noise(0.18, 0.38), _sine(160, 0.20, 0.28)))
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
        _mix(
            _creak(1.5, 380, 90,  volume=0.28, slip_count=10, seed=7),
            _bandpass_noise(1.5, 140, 60, volume=0.06, seed=21),
        ),
        _silence(0.05), _thud(0.14, 0.14),
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


def stop_all():
    """Stop all currently playing sounds."""
    if _enabled and _mixer:
        _mixer.stop()
