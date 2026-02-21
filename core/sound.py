"""
Realm of Shadows — Sound Engine (M8)
All sounds generated procedurally — no audio files needed.
Gracefully handles missing/failed audio initialization.
"""
import math, array, random

# Try to init mixer; if it fails, all functions become no-ops
_enabled = False
_mixer = None
_sounds = {}       # cached Sound objects by name
_channels = {}     # named channel reservations
_music_channel = None
_ambient_channel = None
_master_vol = 0.6
_sfx_vol = 0.7
_music_vol = 0.35
_ambient_vol = 0.25

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
        _music_channel = _mixer.Channel(10)
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


# ══════════════════════════════════════════════════════════
#  WAVEFORM GENERATORS
# ══════════════════════════════════════════════════════════

SR = 22050  # sample rate


def _make_sound(samples_list):
    """Convert list of int16 samples to a pygame Sound."""
    if not _mixer:
        return None
    buf = array.array('h', samples_list)
    try:
        return _mixer.Sound(buffer=buf)
    except Exception:
        return None


def _sine(freq, duration, volume=0.5, fade_out=True):
    """Generate a sine wave tone."""
    n = int(SR * duration)
    amp = int(32000 * volume)
    samples = []
    for i in range(n):
        t = i / SR
        env = max(0.0, 1.0 - t / duration) if fade_out else 1.0
        v = int(amp * env * math.sin(2 * math.pi * freq * t))
        samples.append(max(-32767, min(32767, v)))
    return samples


def _square(freq, duration, volume=0.3, fade_out=True):
    """Generate a square wave (retro/chiptune feel)."""
    n = int(SR * duration)
    amp = int(32000 * volume)
    samples = []
    period = SR / freq
    for i in range(n):
        t = i / SR
        env = max(0.0, 1.0 - t / duration) if fade_out else 1.0
        v = amp if (i % int(period)) < (period / 2) else -amp
        samples.append(max(-32767, min(32767, int(v * env))))
    return samples


def _noise(duration, volume=0.3, fade_out=True):
    """Generate white noise (for impacts, whooshes)."""
    n = int(SR * duration)
    amp = int(32000 * volume)
    rng = random.Random(42)
    samples = []
    for i in range(n):
        t = i / SR
        env = max(0.0, 1.0 - t / duration) if fade_out else 1.0
        v = int(amp * env * (rng.random() * 2 - 1))
        samples.append(max(-32767, min(32767, v)))
    return samples


def _sweep(f_start, f_end, duration, volume=0.4):
    """Frequency sweep (for magic, whoosh effects)."""
    n = int(SR * duration)
    amp = int(32000 * volume)
    samples = []
    for i in range(n):
        t = i / SR
        frac = t / duration
        freq = f_start + (f_end - f_start) * frac
        env = max(0.0, 1.0 - frac)
        v = int(amp * env * math.sin(2 * math.pi * freq * t))
        samples.append(max(-32767, min(32767, v)))
    return samples


def _mix(*sample_lists):
    """Mix multiple sample lists together."""
    max_len = max(len(s) for s in sample_lists)
    result = [0] * max_len
    for sl in sample_lists:
        for i, v in enumerate(sl):
            result[i] = max(-32767, min(32767, result[i] + v))
    return result


def _concat(*sample_lists):
    """Concatenate sample lists sequentially."""
    result = []
    for sl in sample_lists:
        result.extend(sl)
    return result


def _silence(duration):
    return [0] * int(SR * duration)


# ══════════════════════════════════════════════════════════
#  SOUND DEFINITIONS
# ══════════════════════════════════════════════════════════

def _generate_all_sounds():
    """Pre-generate all game sounds."""
    global _sounds

    # ── UI ──
    _sounds["ui_click"] = _make_sound(_sine(800, 0.05, 0.2))
    _sounds["ui_confirm"] = _make_sound(_concat(
        _sine(600, 0.06, 0.25), _sine(900, 0.08, 0.25)))
    _sounds["ui_cancel"] = _make_sound(_sine(300, 0.12, 0.2, True))
    _sounds["ui_open"] = _make_sound(_sweep(400, 800, 0.15, 0.2))
    _sounds["ui_close"] = _make_sound(_sweep(800, 400, 0.12, 0.2))

    # ── Combat ──
    _sounds["hit_physical"] = _make_sound(_mix(
        _noise(0.08, 0.35), _sine(200, 0.1, 0.25)))
    _sounds["hit_critical"] = _make_sound(_mix(
        _noise(0.12, 0.45), _sine(150, 0.15, 0.35),
        _sine(300, 0.1, 0.2)))
    _sounds["hit_magic"] = _make_sound(_mix(
        _sweep(800, 200, 0.25, 0.3), _sine(440, 0.2, 0.15)))
    _sounds["miss"] = _make_sound(_sweep(600, 400, 0.15, 0.15))
    _sounds["heal"] = _make_sound(_concat(
        _sine(523, 0.1, 0.25), _sine(659, 0.1, 0.25),
        _sine(784, 0.15, 0.3)))
    _sounds["buff"] = _make_sound(_sweep(300, 900, 0.3, 0.2))
    _sounds["debuff"] = _make_sound(_sweep(700, 200, 0.35, 0.25))
    _sounds["death"] = _make_sound(_mix(
        _sweep(400, 80, 0.5, 0.3), _noise(0.3, 0.15)))
    _sounds["victory"] = _make_sound(_concat(
        _sine(523, 0.12, 0.3), _sine(659, 0.12, 0.3),
        _sine(784, 0.12, 0.3), _sine(1047, 0.25, 0.35)))
    _sounds["defeat"] = _make_sound(_concat(
        _sine(400, 0.2, 0.3), _sine(350, 0.2, 0.3),
        _sine(300, 0.2, 0.3), _sine(200, 0.4, 0.3)))
    _sounds["combat_start"] = _make_sound(_mix(
        _noise(0.15, 0.3),
        _concat(_sine(220, 0.08, 0.3), _sine(330, 0.08, 0.3), _sine(440, 0.12, 0.35))))
    _sounds["block"] = _make_sound(_mix(
        _noise(0.06, 0.3), _sine(180, 0.08, 0.2)))
    _sounds["poison"] = _make_sound(_mix(
        _sweep(500, 300, 0.2, 0.15), _noise(0.1, 0.08)))

    # ── Dungeon ──
    _sounds["door_open"] = _make_sound(_mix(
        _noise(0.15, 0.2), _sine(120, 0.2, 0.15)))
    _sounds["stairs"] = _make_sound(_concat(
        _sine(300, 0.1, 0.2), _sine(350, 0.1, 0.2), _sine(400, 0.15, 0.25)))
    _sounds["treasure_open"] = _make_sound(_concat(
        _sine(600, 0.08, 0.2), _sine(800, 0.08, 0.25),
        _sine(1000, 0.08, 0.3), _sine(1200, 0.15, 0.3)))
    _sounds["trap_trigger"] = _make_sound(_mix(
        _noise(0.2, 0.4), _sweep(800, 100, 0.25, 0.3)))
    _sounds["trap_disarm"] = _make_sound(_concat(
        _sine(500, 0.08, 0.2), _sine(700, 0.12, 0.25)))
    _sounds["journal_find"] = _make_sound(_concat(
        _sine(440, 0.1, 0.2), _sine(554, 0.1, 0.2),
        _sine(659, 0.15, 0.25)))
    _sounds["footstep"] = _make_sound(_noise(0.04, 0.1))

    # ── World map ──
    _sounds["encounter"] = _make_sound(_mix(
        _noise(0.1, 0.3),
        _concat(_square(220, 0.08, 0.2), _square(330, 0.08, 0.25),
                _square(440, 0.12, 0.3))))
    _sounds["discovery"] = _make_sound(_concat(
        _sine(523, 0.1, 0.25), _sine(659, 0.12, 0.25),
        _sine(784, 0.15, 0.3)))
    _sounds["camp_rest"] = _make_sound(_concat(
        _sine(330, 0.15, 0.15), _sine(392, 0.15, 0.15),
        _sine(440, 0.2, 0.2)))

    # ── Town ──
    _sounds["shop_buy"] = _make_sound(_concat(
        _sine(500, 0.06, 0.2), _sine(700, 0.08, 0.25)))
    _sounds["shop_sell"] = _make_sound(_concat(
        _sine(700, 0.06, 0.2), _sine(500, 0.08, 0.2)))
    _sounds["npc_talk"] = _make_sound(_sine(600, 0.06, 0.15))
    _sounds["quest_accept"] = _make_sound(_concat(
        _sine(440, 0.08, 0.2), _sine(554, 0.08, 0.2),
        _sine(659, 0.08, 0.25), _sine(880, 0.15, 0.3)))
    _sounds["quest_complete"] = _make_sound(_concat(
        _sine(523, 0.1, 0.3), _sine(659, 0.1, 0.3),
        _sine(784, 0.1, 0.3), _sine(1047, 0.12, 0.35),
        _silence(0.05), _sine(1047, 0.2, 0.35)))

    # ── Ambient loops (longer, generated on demand) ──
    # These are generated when first requested to save startup time


def _generate_ambient(name):
    """Generate longer ambient loops on demand."""
    if name == "dungeon_ambient":
        # Low drone + occasional drips
        dur = 4.0
        drone = _sine(65, dur, 0.08, False)
        drone2 = _sine(98, dur, 0.05, False)
        # Random drip sounds
        drips = [0] * int(SR * dur)
        rng = random.Random(123)
        for _ in range(6):
            pos = rng.randint(0, len(drips) - int(SR * 0.15))
            freq = rng.randint(800, 1400)
            drip = _sine(freq, 0.08, 0.06)
            for j, v in enumerate(drip):
                if pos + j < len(drips):
                    drips[pos + j] = max(-32767, min(32767, drips[pos + j] + v))
        return _make_sound(_mix(drone, drone2, drips))

    elif name == "town_ambient":
        # Gentle background hum with bird-like chirps
        dur = 5.0
        base = _sine(180, dur, 0.04, False)
        base2 = _sine(220, dur, 0.03, False)
        chirps = [0] * int(SR * dur)
        rng = random.Random(456)
        for _ in range(4):
            pos = rng.randint(0, len(chirps) - int(SR * 0.2))
            f = rng.randint(1200, 2000)
            chirp = _sweep(f, f + 400, 0.08, 0.04)
            for j, v in enumerate(chirp):
                if pos + j < len(chirps):
                    chirps[pos + j] = max(-32767, min(32767, chirps[pos + j] + v))
        return _make_sound(_mix(base, base2, chirps))

    elif name == "world_ambient":
        # Wind-like noise, very gentle
        dur = 4.0
        wind = _noise(dur, 0.04, False)
        # Low-pass filter simulation: average neighboring samples
        filtered = [0] * len(wind)
        for i in range(2, len(wind) - 2):
            filtered[i] = (wind[i-2] + wind[i-1] + wind[i] + wind[i+1] + wind[i+2]) // 5
        return _make_sound(filtered)

    elif name == "combat_music":
        # Rhythmic pulse
        dur = 4.0
        n = int(SR * dur)
        samples = [0] * n
        bpm = 120
        beat_samples = int(SR * 60 / bpm)
        for beat in range(int(dur * bpm / 60)):
            pos = beat * beat_samples
            # Kick
            kick = _sine(80, 0.1, 0.15)
            for j, v in enumerate(kick):
                if pos + j < n:
                    samples[pos + j] = max(-32767, min(32767, samples[pos + j] + v))
            # Off-beat hi-hat
            hh_pos = pos + beat_samples // 2
            hh = _noise(0.03, 0.06)
            for j, v in enumerate(hh):
                if hh_pos + j < n:
                    samples[hh_pos + j] = max(-32767, min(32767, samples[hh_pos + j] + v))
        # Bass drone
        drone = _sine(55, dur, 0.06, False)
        return _make_sound(_mix(samples, drone))

    return None


# ══════════════════════════════════════════════════════════
#  PUBLIC API
# ══════════════════════════════════════════════════════════

def play(name):
    """Play a one-shot sound effect."""
    if not _enabled:
        return
    snd = _sounds.get(name)
    if snd:
        snd.set_volume(_master_vol * _sfx_vol)
        snd.play()


def play_ambient(name):
    """Start a looping ambient sound."""
    if not _enabled or not _ambient_channel:
        return
    if name not in _sounds:
        _sounds[name] = _generate_ambient(name)
    snd = _sounds.get(name)
    if snd:
        _ambient_channel.set_volume(_master_vol * _ambient_vol)
        _ambient_channel.play(snd, loops=-1)


def stop_ambient():
    """Stop ambient loop."""
    if _enabled and _ambient_channel:
        _ambient_channel.fadeout(500)


def play_music(name):
    """Start a looping music track."""
    if not _enabled or not _music_channel:
        return
    if name not in _sounds:
        _sounds[name] = _generate_ambient(name)
    snd = _sounds.get(name)
    if snd:
        _music_channel.set_volume(_master_vol * _music_vol)
        _music_channel.play(snd, loops=-1)


def stop_music():
    """Stop music loop."""
    if _enabled and _music_channel:
        _music_channel.fadeout(800)


def stop_all():
    """Stop everything."""
    if _enabled:
        stop_ambient()
        stop_music()
        if _mixer:
            _mixer.stop()
