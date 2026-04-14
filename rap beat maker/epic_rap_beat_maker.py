#!/usr/bin/env python3
"""
🎤 EPIC RAP BEAT MAKER & HIP-HOP SONG CREATOR! 🎵
Create the sickest beats and rap songs ever!
"""

import pygame
import numpy as np
import math
import random
import sys
import json
from enum import Enum
from collections import deque

# Screen settings
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
PINK = (255, 192, 203)
CYAN = (0, 255, 255)
DARK_GRAY = (40, 40, 40)
LIGHT_GRAY = (200, 200, 200)
BEAT_COLOR = (255, 69, 0)
BASS_COLOR = (138, 43, 226)
SNARE_COLOR = (255, 215, 0)
HIHAT_COLOR = (192, 192, 192)


# Beat Enhancement System
class BeatEnhancer:
    def __init__(self):
        self.pitch_shifts = {
            SoundType.SNARE: 0.0,
            SoundType.CLAP: 0.0,
            SoundType.BASS: 0.0,
            SoundType.FX: 0.0,
            SoundType.EXPLOSION: 0.0,
            SoundType.LASER: 0.0,
            SoundType.ZAPPER: 0.0,
            SoundType.BASS_808: 0.0,
            SoundType.KICK_808: 0.0,
            SoundType.HIHAT_OPEN: 0.0,
            SoundType.HIHAT_CLOSED: 0.0,
            SoundType.RIMSHOT: 0.0,
            SoundType.COWBELL: 0.0,
            SoundType.SYNTH_LEAD: 0.0,
            SoundType.VOCAL_CHOP: 0.0,
            SoundType.REVERSE_CYMBAL: 0.0
        }
        self.reverb_enabled = False
        self.reverb_size = 0.5
        self.reverb_decay = 0.5
        self.swing_amount = 0.0
        self.swing_enabled = False
        
    def set_pitch_shift(self, sound_type, semitones):
        """Set pitch shift in semitones (-12 to +12)"""
        self.pitch_shifts[sound_type] = max(-12, min(12, semitones))
        
    def get_pitch_multiplier(self, sound_type):
        """Get pitch multiplier for sound synthesis"""
        semitones = self.pitch_shifts[sound_type]
        return 2 ** (semitones / 12)
        
    def toggle_reverb(self):
        """Toggle reverb on/off"""
        self.reverb_enabled = not self.reverb_enabled
        
    def set_reverb_size(self, size):
        """Set reverb room size (0.0 to 1.0)"""
        self.reverb_size = max(0.0, min(1.0, size))
        
    def set_reverb_decay(self, decay):
        """Set reverb decay time (0.0 to 1.0)"""
        self.reverb_decay = max(0.0, min(1.0, decay))
        
    def set_swing(self, amount):
        """Set swing amount (0.0 to 1.0)"""
        self.swing_amount = max(0.0, min(1.0, amount))
        
    def toggle_swing(self):
        """Toggle swing on/off"""
        self.swing_enabled = not self.swing_enabled
        
    def apply_swing_timing(self, step):
        """Apply swing timing to step"""
        if not self.swing_enabled or self.swing_amount == 0:
            return step
            
        # Apply swing to 8th notes
        if step % 2 == 1:  # Off-beat
            swing_offset = self.swing_amount * 0.5
            return step + swing_offset
        return step

# Beat Pattern Management System
class BeatPatternManager:
    def __init__(self):
        self.clipboard = None
        self.pattern_slots = {
            'A': None,
            'B': None, 
            'C': None,
            'D': None
        }
        self.current_slot = 'A'
        
    def copy_pattern(self, pattern):
        """Copy pattern to clipboard"""
        self.clipboard = [row[:] for row in pattern]
        return True
        
    def paste_pattern(self, pattern):
        """Paste pattern from clipboard"""
        if self.clipboard:
            for i in range(len(pattern)):
                pattern[i] = self.clipboard[i][:]
            return True
        return False
        
    def duplicate_pattern(self, pattern):
        """Duplicate current pattern"""
        return [row[:] for row in pattern]
        
    def mirror_pattern_horizontal(self, pattern):
        """Mirror pattern horizontally (reverse steps)"""
        mirrored = []
        for row in pattern:
            mirrored.append(row[::-1])
        return mirrored
        
    def mirror_pattern_vertical(self, pattern):
        """Mirror pattern vertically (reverse sounds)"""
        return pattern[::-1]
        
    def rotate_pattern_left(self, pattern):
        """Rotate pattern left by 1 step"""
        rotated = []
        for row in pattern:
            rotated.append(row[1:] + [row[0]])
        return rotated
        
    def rotate_pattern_right(self, pattern):
        """Rotate pattern right by 1 step"""
        rotated = []
        for row in pattern:
            rotated.append([row[-1]] + row[:-1])
        return rotated
        
    def save_to_slot(self, slot, pattern):
        """Save pattern to slot A/B/C/D"""
        if slot in self.pattern_slots:
            self.pattern_slots[slot] = [row[:] for row in pattern]
            return True
        return False
        
    def load_from_slot(self, slot, pattern):
        """Load pattern from slot A/B/C/D"""
        if slot in self.pattern_slots and self.pattern_slots[slot]:
            for i in range(len(pattern)):
                pattern[i] = self.pattern_slots[slot][i][:]
            return True
        return False
        
    def clear_slot(self, slot):
        """Clear pattern slot"""
        if slot in self.pattern_slots:
            self.pattern_slots[slot] = None
            return True
        return False

# Random Beat Generator
class RandomBeatGenerator:
    def __init__(self):
        self.genre_patterns = {
            'trap': {
                'kick_density': 0.3,
                'snare_density': 0.2,
                'hihat_density': 0.6,
                'bass_density': 0.4,
                '808_density': 0.3,
                'swing_chance': 0.7
            },
            'boom_bap': {
                'kick_density': 0.4,
                'snare_density': 0.3,
                'hihat_density': 0.5,
                'bass_density': 0.5,
                '808_density': 0.1,
                'swing_chance': 0.3
            },
            'lo_fi': {
                'kick_density': 0.2,
                'snare_density': 0.2,
                'hihat_density': 0.4,
                'bass_density': 0.3,
                '808_density': 0.1,
                'swing_chance': 0.5
            },
            'techno': {
                'kick_density': 0.5,
                'snare_density': 0.3,
                'hihat_density': 0.7,
                'bass_density': 0.4,
                '808_density': 0.2,
                'swing_chance': 0.1
            }
        }
        
    def generate_random_pattern(self, genre='random', complexity=0.5):
        """Generate a random beat pattern"""
        if genre == 'random':
            genre = random.choice(list(self.genre_patterns.keys()))
        
        pattern = [[False for _ in range(16)] for _ in range(16)]
        settings = self.genre_patterns[genre]
        
        # Adjust densities based on complexity
        multiplier = 0.5 + (complexity * 1.0)  # 0.5 to 1.5 multiplier
        
        # Generate kick pattern (row 8 = KICK_808)
        self._generate_drum_pattern(pattern, 8, settings['kick_density'] * multiplier)
        
        # Generate snare pattern (row 0 = SNARE)
        self._generate_drum_pattern(pattern, 0, settings['snare_density'] * multiplier)
        
        # Generate hi-hat patterns (rows 10-11 = HIHAT_OPEN/CLOSED)
        self._generate_drum_pattern(pattern, 10, settings['hihat_density'] * multiplier * 0.3)  # Open hats
        self._generate_drum_pattern(pattern, 11, settings['hihat_density'] * multiplier)  # Closed hats
        
        # Generate bass pattern (row 2 = BASS)
        self._generate_drum_pattern(pattern, 2, settings['bass_density'] * multiplier)
        
        # Generate 808 bass (row 7 = BASS_808)
        self._generate_drum_pattern(pattern, 7, settings['808_density'] * multiplier)
        
        # Add some random percussion
        if random.random() < 0.3:
            self._generate_drum_pattern(pattern, 12, 0.2)  # RIMSHOT
        if random.random() < 0.2:
            self._generate_drum_pattern(pattern, 13, 0.1)  # COWBELL
            
        # Add occasional FX
        if random.random() < 0.15:
            self._generate_drum_pattern(pattern, 3, 0.1)  # FX
        if random.random() < 0.1:
            self._generate_drum_pattern(pattern, 4, 0.05)  # EXPLOSION
            
        return pattern, genre
    
    def _generate_drum_pattern(self, pattern, row, density):
        """Generate a drum pattern for a specific row"""
        for step in range(16):
            if random.random() < density:
                # Add some rhythmic intelligence
                if row == 8:  # Kick - emphasize downbeats
                    if step % 4 == 0:  # Strong downbeats
                        pattern[row][step] = True if random.random() < 0.8 else False
                    elif step % 4 == 2:  # Off-beats
                        pattern[row][step] = True if random.random() < 0.3 else False
                    else:  # Other beats
                        pattern[row][step] = True if random.random() < 0.1 else False
                elif row == 0:  # Snare - emphasize 2 and 4
                    if step % 4 == 2:  # Beat 3
                        pattern[row][step] = True if random.random() < 0.7 else False
                    elif step % 4 == 0 and step > 0:  # Beat 2 and 4
                        pattern[row][step] = True if random.random() < 0.6 else False
                    else:  # Ghost notes
                        pattern[row][step] = True if random.random() < 0.1 else False
                elif row in [10, 11]:  # Hi-hats - more varied
                    if step % 2 == 0:  # Even steps
                        pattern[row][step] = True if random.random() < density * 1.5 else False
                    else:  # Odd steps
                        pattern[row][step] = True if random.random() < density * 0.7 else False
                else:  # Other instruments
                    pattern[row][step] = True
    
    def generate_evolution(self, base_pattern, mutation_rate=0.1):
        """Evolve an existing pattern"""
        new_pattern = [row[:] for row in base_pattern]
        
        for row in range(16):
            for step in range(16):
                if random.random() < mutation_rate:
                    # Flip this beat
                    new_pattern[row][step] = not new_pattern[row][step]
                    
        return new_pattern
    
    def get_genre_info(self):
        """Get information about available genres"""
        return list(self.genre_patterns.keys())

# Sound types
class SoundType(Enum):
    SNARE = "snare"
    CLAP = "clap"
    BASS = "bass"
    FX = "fx"
    EXPLOSION = "explosion"
    LASER = "laser"
    ZAPPER = "zapper"
    BASS_808 = "bass_808"
    KICK_808 = "kick_808"
    HIHAT_OPEN = "hihat_open"
    HIHAT_CLOSED = "hihat_closed"
    RIMSHOT = "rimshot"
    COWBELL = "cowbell"
    SYNTH_LEAD = "synth_lead"
    VOCAL_CHOP = "vocal_chop"
    REVERSE_CYMBAL = "reverse_cymbal"

# Beat Enhancement System
class BeatEnhancer:
    def __init__(self):
        self.pitch_shifts = {
            SoundType.SNARE: 0.0,
            SoundType.CLAP: 0.0,
            SoundType.BASS: 0.0,
            SoundType.FX: 0.0,
            SoundType.EXPLOSION: 0.0,
            SoundType.LASER: 0.0,
            SoundType.ZAPPER: 0.0,
            SoundType.BASS_808: 0.0,
            SoundType.KICK_808: 0.0,
            SoundType.HIHAT_OPEN: 0.0,
            SoundType.HIHAT_CLOSED: 0.0,
            SoundType.RIMSHOT: 0.0,
            SoundType.COWBELL: 0.0,
            SoundType.SYNTH_LEAD: 0.0,
            SoundType.VOCAL_CHOP: 0.0,
            SoundType.REVERSE_CYMBAL: 0.0
        }
        self.reverb_enabled = False
        self.reverb_size = 0.5
        self.reverb_decay = 0.5
        self.swing_amount = 0.0
        self.swing_enabled = False
        
    def set_pitch_shift(self, sound_type, semitones):
        """Set pitch shift in semitones (-12 to +12)"""
        self.pitch_shifts[sound_type] = max(-12, min(12, semitones))
        
    def get_pitch_multiplier(self, sound_type):
        """Get pitch multiplier for sound synthesis"""
        semitones = self.pitch_shifts[sound_type]
        return 2 ** (semitones / 12)
        
    def toggle_reverb(self):
        """Toggle reverb on/off"""
        self.reverb_enabled = not self.reverb_enabled
        
    def set_reverb_size(self, size):
        """Set reverb room size (0.0 to 1.0)"""
        self.reverb_size = max(0.0, min(1.0, size))
        
    def set_reverb_decay(self, decay):
        """Set reverb decay time (0.0 to 1.0)"""
        self.reverb_decay = max(0.0, min(1.0, decay))
        
    def set_swing(self, amount):
        """Set swing amount (0.0 to 1.0)"""
        self.swing_amount = max(0.0, min(1.0, amount))
        
    def toggle_swing(self):
        """Toggle swing on/off"""
        self.swing_enabled = not self.swing_enabled
        
    def apply_swing_timing(self, step):
        """Apply swing timing to step"""
        if not self.swing_enabled or self.swing_amount == 0:
            return step
            
        # Apply swing to 8th notes
        if step % 2 == 1:  # Off-beat
            swing_offset = self.swing_amount * 0.5
            return step + swing_offset
        return step

class BeatPattern:
    def __init__(self):
        self.pattern = [[False for _ in range(16)] for _ in range(16)]
        self.tempo = 120
        self.current_step = 0
        self.sound_types = [
            SoundType.SNARE, SoundType.CLAP, SoundType.BASS, SoundType.FX,
            SoundType.EXPLOSION, SoundType.LASER, SoundType.ZAPPER, SoundType.BASS_808,
            SoundType.KICK_808, SoundType.HIHAT_OPEN, SoundType.HIHAT_CLOSED, SoundType.RIMSHOT,
            SoundType.COWBELL, SoundType.SYNTH_LEAD, SoundType.VOCAL_CHOP, SoundType.REVERSE_CYMBAL
        ]
        
class RapLyrics:
    def __init__(self):
        self.lines = []
        self.current_line = ""
        self.rhyme_scheme = []
        self.syllables = []
        
    def add_line(self, line):
        self.lines.append(line)
        self.analyze_line(line)
        
    def analyze_line(self, line):
        # Count syllables (simplified)
        words = line.split()
        syllable_count = sum(len(word) // 2 for word in words)
        self.syllables.append(syllable_count)
        
    def get_rhyme_words(self):
        rhymes = ["fire", "desire", "higher", "inspire", "empire", "retire",
                 "flow", "show", "go", "know", "grow", "though", "dough",
                 "beat", "street", "feet", "complete", "elite", "discrete",
                 "mic", "like", "strike", "night", "light", "right", "tight",
                 "game", "fame", "name", "blame", "flame", "same", "claim",
                 "real", "feel", "steel", "deal", "reveal", "appeal", "seal",
                 "trap", "rap", "map", "snap", "clap", "gap", "strap"]
        return rhymes

class SoundGenerator:
    def __init__(self):
        self.sample_rate = 22050
        pygame.mixer.init(frequency=self.sample_rate, size=-16, channels=2, buffer=512)
        
    def generate_kick(self):
        """Generate a kick drum sound"""
        duration = 0.2
        sample_rate = self.sample_rate
        samples = int(duration * sample_rate)
        
        frequency = 60
        wave = []
        for i in range(samples):
            t = i / sample_rate
            # Pitch envelope
            pitch = frequency * math.exp(-t * 30)
            # Amplitude envelope
            amplitude = math.exp(-t * 10)
            sample = amplitude * math.sin(2 * math.pi * pitch * t)
            wave.append([int(sample * 32767), int(sample * 32767)])
        
        return pygame.sndarray.make_sound(np.array(wave, dtype=np.int16))
        
    def generate_snare(self):
        """Generate a snare drum sound"""
        duration = 0.15
        sample_rate = self.sample_rate
        samples = int(duration * sample_rate)
        
        wave = []
        for i in range(samples):
            t = i / sample_rate
            # Mix of tone and noise
            tone = math.sin(2 * math.pi * 200 * t) * math.exp(-t * 20)
            noise = random.uniform(-0.3, 0.3) * math.exp(-t * 15)
            sample = (tone + noise) * 0.5
            wave.append([int(sample * 32767), int(sample * 32767)])
        
        return pygame.sndarray.make_sound(np.array(wave, dtype=np.int16))
        
    def generate_hihat(self):
        """Generate a hihat sound"""
        duration = 0.05
        sample_rate = self.sample_rate
        samples = int(duration * sample_rate)
        
        wave = []
        for i in range(samples):
            noise = random.uniform(-0.5, 0.5)
            sample = noise * math.exp(-i / samples * 10)
            wave.append([int(sample * 32767), int(sample * 32767)])
        
        return pygame.sndarray.make_sound(np.array(wave, dtype=np.int16))
        
    def generate_clap(self):
        """Generate a life-like clap sound"""
        duration = 0.08
        sample_rate = self.sample_rate
        samples = int(duration * sample_rate)
        
        wave = []
        for i in range(samples):
            t = i / sample_rate
            # Multiple hand clap layers for realistic sound
            clap1 = random.uniform(-0.8, 0.8) * math.exp(-t * 50)
            clap2 = random.uniform(-0.6, 0.6) * math.exp(-t * 40)
            clap3 = random.uniform(-0.4, 0.4) * math.exp(-t * 30)
            
            # Add some mid-frequency content for body
            mid_freq = math.sin(2 * math.pi * 1500 * t) * 0.1 * math.exp(-t * 25)
            
            # Combine all clap layers
            sample = (clap1 + clap2 + clap3 + mid_freq) * 0.7
            
            # Add slight reverb effect
            if i > 10:
                reverb = wave[i-10][0] * 0.1 if i > 10 else 0
                sample = sample * 0.9 + reverb
            
            sample = max(-1, min(1, sample))  # Clamp to prevent overflow
            wave.append([int(sample * 32767), int(sample * 32767)])
        
        return pygame.sndarray.make_sound(np.array(wave, dtype=np.int16))
        
    def generate_bass(self, frequency=55):
        """Generate a bass sound"""
        duration = 0.3
        sample_rate = self.sample_rate
        samples = int(duration * sample_rate)
        
        wave = []
        for i in range(samples):
            t = i / sample_rate
            # Bass wave with envelope
            sample = math.sin(2 * math.pi * frequency * t) * 0.8
            sample += math.sin(2 * math.pi * frequency * 2 * t) * 0.3
            sample *= math.exp(-t * 3)
            wave.append([int(sample * 32767), int(sample * 32767)])
        
        return pygame.sndarray.make_sound(np.array(wave, dtype=np.int16))
        
    def generate_lead(self, frequency=440):
        """Generate a lead synth sound"""
        duration = 0.2
        sample_rate = self.sample_rate
        samples = int(duration * sample_rate)
        
        wave = []
        for i in range(samples):
            t = i / sample_rate
            # Square wave with envelope
            sample = (1 if math.sin(2 * math.pi * frequency * t) > 0 else -1) * 0.3
            sample += math.sin(2 * math.pi * frequency * 2 * t) * 0.2
            sample *= math.exp(-t * 5)
            wave.append([int(sample * 32767), int(sample * 32767)])
        
        return pygame.sndarray.make_sound(np.array(wave, dtype=np.int16))
        
    def generate_explosion(self):
        """Generate an explosion sound"""
        duration = 0.8
        sample_rate = self.sample_rate
        samples = int(duration * sample_rate)
        
        wave = []
        for i in range(samples):
            t = i / sample_rate
            # Complex noise with low frequency rumble
            noise = random.uniform(-1, 1)
            low_freq = math.sin(2 * math.pi * 30 * t) * 0.5
            mid_freq = math.sin(2 * math.pi * 100 * t) * random.uniform(-0.3, 0.3)
            
            # Envelope
            envelope = math.exp(-t * 2)
            sample = (noise + low_freq + mid_freq) * envelope * 0.8
            sample = max(-1, min(1, sample))  # Clamp to prevent overflow
            wave.append([int(sample * 32767), int(sample * 32767)])
        
        return pygame.sndarray.make_sound(np.array(wave, dtype=np.int16))
        
    def generate_laser(self):
        """Generate a laser sound"""
        duration = 0.3
        sample_rate = self.sample_rate
        samples = int(duration * sample_rate)
        
        wave = []
        for i in range(samples):
            t = i / sample_rate
            # Frequency sweep from high to low
            freq = 2000 * math.exp(-t * 10)
            sample = math.sin(2 * math.pi * freq * t) * math.exp(-t * 5)
            sample = max(-1, min(1, sample))  # Clamp to prevent overflow
            wave.append([int(sample * 32767), int(sample * 32767)])
        
        return pygame.sndarray.make_sound(np.array(wave, dtype=np.int16))
        
    def generate_zapper(self):
        """Generate a zapper/electric sound"""
        duration = 0.2
        sample_rate = self.sample_rate
        samples = int(duration * sample_rate)
        
        wave = []
        for i in range(samples):
            t = i / sample_rate
            # Electric buzz with random spikes
            buzz = math.sin(2 * math.pi * 1000 * t) * 0.3
            spike = random.uniform(-0.5, 0.5) if random.random() < 0.1 else 0
            sample = (buzz + spike) * math.exp(-t * 8)
            sample = max(-1, min(1, sample))  # Clamp to prevent overflow
            wave.append([int(sample * 32767), int(sample * 32767)])
        
        return pygame.sndarray.make_sound(np.array(wave, dtype=np.int16))
        
    def generate_mythical_trumpet(self):
        """Generate a sick mythical trumpet sound"""
        duration = 0.4
        sample_rate = self.sample_rate
        samples = int(duration * sample_rate)
        
        wave = []
        for i in range(samples):
            t = i / sample_rate
            # Mythical trumpet with harmonics and vibrato
            base_freq = 440  # A4
            vibrato = math.sin(2 * math.pi * 5 * t) * 0.05  # 5Hz vibrato
            freq = base_freq * (1 + vibrato)
            
            # Add harmonics for rich trumpet sound
            harmonic1 = math.sin(2 * math.pi * freq * t) * 0.6
            harmonic2 = math.sin(2 * math.pi * freq * 2 * t) * 0.3
            harmonic3 = math.sin(2 * math.pi * freq * 3 * t) * 0.1
            harmonic4 = math.sin(2 * math.pi * freq * 4 * t) * 0.05
            
            # Add some mystical shimmer
            shimmer = math.sin(2 * math.pi * freq * 8 * t) * 0.02 * math.sin(2 * math.pi * 0.5 * t)
            
            # Combine all harmonics
            sample = harmonic1 + harmonic2 + harmonic3 + harmonic4 + shimmer
            
            # Apply envelope for realistic trumpet attack/decay
            if t < 0.05:  # Quick attack
                envelope = t / 0.05
            else:  # Sustain and decay
                envelope = math.exp(-(t - 0.05) * 3)
            
            sample *= envelope
            sample = max(-1, min(1, sample))  # Clamp to prevent overflow
            wave.append([int(sample * 32767), int(sample * 32767)])
        
        return pygame.sndarray.make_sound(np.array(wave, dtype=np.int16))
        
    def generate_bass_808(self):
        """Generate deep 808 bass sound"""
        duration = 0.5
        sample_rate = self.sample_rate
        samples = int(duration * sample_rate)
        
        wave = []
        for i in range(samples):
            t = i / sample_rate
            # Deep sine wave with envelope
            freq = 40  # Deep 808 frequency
            sample = math.sin(2 * math.pi * freq * t)
            # ADSR envelope for 808
            if t < 0.01:  # Attack
                envelope = t / 0.01
            elif t < 0.1:  # Decay
                envelope = 1.0 - (t - 0.01) * 0.8 / 0.09
            else:  # Sustain/Release
                envelope = 0.2 * math.exp(-(t - 0.1) * 3)
            sample *= envelope
            sample = max(-1, min(1, sample))
            wave.append([int(sample * 32767), int(sample * 32767)])
        
        return pygame.sndarray.make_sound(np.array(wave, dtype=np.int16))
        
    def generate_kick_808(self):
        """Generate classic 808 kick sound"""
        duration = 0.3
        sample_rate = self.sample_rate
        samples = int(duration * sample_rate)
        
        wave = []
        for i in range(samples):
            t = i / sample_rate
            # Pitch sweep from high to low
            freq = 60 * math.exp(-t * 10)
            sample = math.sin(2 * math.pi * freq * t)
            # Punch envelope
            envelope = math.exp(-t * 8)
            sample *= envelope
            sample = max(-1, min(1, sample))
            wave.append([int(sample * 32767), int(sample * 32767)])
        
        return pygame.sndarray.make_sound(np.array(wave, dtype=np.int16))
        
    def generate_hihat_open(self):
        """Generate open hi-hat sound"""
        duration = 0.2
        sample_rate = self.sample_rate
        samples = int(duration * sample_rate)
        
        wave = []
        for i in range(samples):
            t = i / sample_rate
            # Metallic noise with longer decay
            noise = random.uniform(-0.3, 0.3)
            metallic = math.sin(2 * math.pi * 8000 * t) * 0.1
            sample = (noise + metallic) * math.exp(-t * 5)
            sample = max(-1, min(1, sample))
            wave.append([int(sample * 32767), int(sample * 32767)])
        
        return pygame.sndarray.make_sound(np.array(wave, dtype=np.int16))
        
    def generate_hihat_closed(self):
        """Generate closed hi-hat sound"""
        duration = 0.05
        sample_rate = self.sample_rate
        samples = int(duration * sample_rate)
        
        wave = []
        for i in range(samples):
            t = i / sample_rate
            # Short metallic noise
            noise = random.uniform(-0.4, 0.4)
            metallic = math.sin(2 * math.pi * 10000 * t) * 0.1
            sample = (noise + metallic) * math.exp(-t * 30)
            sample = max(-1, min(1, sample))
            wave.append([int(sample * 32767), int(sample * 32767)])
        
        return pygame.sndarray.make_sound(np.array(wave, dtype=np.int16))
        
    def generate_rimshot(self):
        """Generate classic hip-hop rimshot sound"""
        duration = 0.03
        sample_rate = self.sample_rate
        samples = int(duration * sample_rate)
        
        wave = []
        for i in range(samples):
            t = i / sample_rate
            # Clicky rim sound
            click = random.uniform(-0.6, 0.6) * math.exp(-t * 50)
            tone = math.sin(2 * math.pi * 800 * t) * 0.3 * math.exp(-t * 40)
            sample = click + tone
            sample = max(-1, min(1, sample))
            wave.append([int(sample * 32767), int(sample * 32767)])
        
        return pygame.sndarray.make_sound(np.array(wave, dtype=np.int16))
        
    def generate_cowbell(self):
        """Generate funky cowbell sound"""
        duration = 0.1
        sample_rate = self.sample_rate
        samples = int(duration * sample_rate)
        
        wave = []
        for i in range(samples):
            t = i / sample_rate
            # Cowbell harmonics
            fundamental = math.sin(2 * math.pi * 800 * t) * 0.5
            harmonic1 = math.sin(2 * math.pi * 1600 * t) * 0.3
            harmonic2 = math.sin(2 * math.pi * 2400 * t) * 0.2
            sample = (fundamental + harmonic1 + harmonic2) * math.exp(-t * 10)
            sample = max(-1, min(1, sample))
            wave.append([int(sample * 32767), int(sample * 32767)])
        
        return pygame.sndarray.make_sound(np.array(wave, dtype=np.int16))
        
    def generate_synth_lead(self):
        """Generate melodic synth lead sound"""
        duration = 0.3
        sample_rate = self.sample_rate
        samples = int(duration * sample_rate)
        
        wave = []
        for i in range(samples):
            t = i / sample_rate
            # Sawtooth wave for synth lead
            phase = (2 * math.pi * 440 * t) % (2 * math.pi)
            sawtooth = (2 * phase / (2 * math.pi)) - 1
            # Filter envelope
            filter_cutoff = 2000 * math.exp(-t * 2)
            sample = sawtooth * 0.4 * math.exp(-t * 3)
            sample = max(-1, min(1, sample))
            wave.append([int(sample * 32767), int(sample * 32767)])
        
        return pygame.sndarray.make_sound(np.array(wave, dtype=np.int16))
        
    def generate_vocal_chop(self):
        """Generate vocal chop sound ("Yeah!" "Uh!")"""
        duration = 0.15
        sample_rate = self.sample_rate
        samples = int(duration * sample_rate)
        
        wave = []
        for i in range(samples):
            t = i / sample_rate
            # Simulated vocal formants
            vowel1 = math.sin(2 * math.pi * 300 * t) * 0.4  # Fundamental
            vowel2 = math.sin(2 * math.pi * 900 * t) * 0.3  # First formant
            vowel3 = math.sin(2 * math.pi * 2500 * t) * 0.2  # Second formant
            # Add some noise for breathiness
            breath = random.uniform(-0.1, 0.1)
            sample = (vowel1 + vowel2 + vowel3 + breath) * math.exp(-t * 4)
            sample = max(-1, min(1, sample))
            wave.append([int(sample * 32767), int(sample * 32767)])
        
        return pygame.sndarray.make_sound(np.array(wave, dtype=np.int16))
        
    def generate_reverse_cymbal(self):
        """Generate reverse cymbal build-up effect"""
        duration = 0.4
        sample_rate = self.sample_rate
        samples = int(duration * sample_rate)
        
        wave = []
        for i in range(samples):
            t = i / sample_rate
            # Reverse envelope (starts quiet, gets loud)
            envelope = t / duration  # Linear fade in
            # Cymbal noise
            noise = random.uniform(-0.5, 0.5)
            metallic = math.sin(2 * math.pi * 5000 * t) * 0.2
            sample = (noise + metallic) * envelope * 0.7
            sample = max(-1, min(1, sample))
            wave.append([int(sample * 32767), int(sample * 32767)])
        
        return pygame.sndarray.make_sound(np.array(wave, dtype=np.int16))

class EpicRapBeatMaker:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("🎤 EPIC RAP BEAT MAKER - HIP-HOP SONG CREATOR! 🎵")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Fonts
        self.font_small = pygame.font.Font(None, 24)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_large = pygame.font.Font(None, 48)
        self.font_huge = pygame.font.Font(None, 72)
        
        # Sound generator
        self.sound_gen = SoundGenerator()
        
        # Beat patterns
        self.beat_pattern = BeatPattern()
        self.sounds = {
            SoundType.SNARE: self.sound_gen.generate_snare(),
            SoundType.CLAP: self.sound_gen.generate_clap(),
            SoundType.BASS: self.sound_gen.generate_bass(),
            SoundType.FX: self.sound_gen.generate_lead(880),
            SoundType.EXPLOSION: self.sound_gen.generate_explosion(),
            SoundType.LASER: self.sound_gen.generate_laser(),
            SoundType.ZAPPER: self.sound_gen.generate_zapper(),
            SoundType.BASS_808: self.sound_gen.generate_bass_808(),
            SoundType.KICK_808: self.sound_gen.generate_kick_808(),
            SoundType.HIHAT_OPEN: self.sound_gen.generate_hihat_open(),
            SoundType.HIHAT_CLOSED: self.sound_gen.generate_hihat_closed(),
            SoundType.RIMSHOT: self.sound_gen.generate_rimshot(),
            SoundType.COWBELL: self.sound_gen.generate_cowbell(),
            SoundType.SYNTH_LEAD: self.sound_gen.generate_synth_lead(),
            SoundType.VOCAL_CHOP: self.sound_gen.generate_vocal_chop(),
            SoundType.REVERSE_CYMBAL: self.sound_gen.generate_reverse_cymbal()
        }
        
        # Rap lyrics
        self.rap_lyrics = RapLyrics()
        self.lyric_input = ""
        self.input_active = False
        
        # Sequencer
        self.playing = False
        self.current_step = 0
        self.step_timer = 0
        self.step_interval = 60000 // (self.beat_pattern.tempo * 4)  # 16th notes
        
        # Visual effects
        self.visualizer = deque(maxlen=100)
        self.particles = []
        self.screen_shake = 0
        
        # UI Elements
        self.grid_x = 50
        self.grid_y = 150
        self.cell_width = 40
        self.cell_height = 30
        self.selected_cell = None
        
        # Recording
        self.recording = False
        self.recorded_pattern = []
        self.recording_start_step = 0
        self.easy_record_mode = False  # New easy recording mode
        
        # Background tracks
        self.background_track = None
        self.background_playing = False
        self.background_volume = 0.5
        self.background_tracks = self.create_background_tracks()
        
        # Beat Enhancement System
        self.beat_enhancer = BeatEnhancer()
        
        # Beat Pattern Management System
        self.pattern_manager = BeatPatternManager()
        
        # Random Beat Generator
        self.beat_generator = RandomBeatGenerator()
        
        # Presets
        self.presets = {
            "Trap": self.create_trap_preset(),
            "Boom Bap": self.create_boom_bap_preset(),
            "Lo-Fi": self.create_lofi_preset(),
            "Club": self.create_club_preset()
        }
        
    def create_trap_preset(self):
        """Create trap beat preset"""
        pattern = [[False for _ in range(16)] for _ in range(16)]
        # 808 Bass
        for step in [0, 4, 8, 12]:
            pattern[7][step] = True  # 808 Bass
        # 808 Kick
        for step in [0, 8]:
            pattern[8][step] = True  # 808 Kick
        # Hi-hats
        for step in range(0, 16, 2):
            pattern[10][step] = True  # Open hi-hat
        for step in range(1, 16, 2):
            pattern[11][step] = True  # Closed hi-hat
        # Snare
        for step in [4, 12]:
            pattern[0][step] = True  # Snare
        return pattern
        
    def create_boom_bap_preset(self):
        """Create a boom bap preset"""
        pattern = [[False for _ in range(16)] for _ in range(16)]
        # Bass
        for step in [0, 2, 4, 6, 8, 10, 12, 14]:
            pattern[2][step] = True  # Bass
        # Snare on 3, 7, 11, 15
        for step in [4, 12]:
            pattern[0][step] = True  # Snare
        # Rimshot
        for step in [1, 3, 5, 7, 9, 11, 13, 15]:
            pattern[12][step] = True  # Rimshot
        # Clap
        for step in [4, 12]:
            pattern[1][step] = True  # Clap
        return pattern
        
    def create_lofi_preset(self):
        """Create a lo-fi preset"""
        pattern = [[False for _ in range(16)] for _ in range(16)]
        # Slow kick
        for step in [0, 8]:
            pattern[2][step] = True
        # Snare
        for step in [4, 12]:
            pattern[0][step] = True
        # Gentle hi-hats
        for step in range(0, 16, 4):
            pattern[3][step] = True
        # FX
        for step in [0, 4, 8, 12]:
            pattern[4][step] = True
        # Synth Lead
        for step in [1, 5, 9, 13]:
            pattern[14][step] = True
        return pattern
        
    def create_club_preset(self):
        """Create a club preset"""
        pattern = [[False for _ in range(16)] for _ in range(16)]
        # Four on the floor kick
        for step in range(0, 16, 4):
            pattern[8][step] = True
        # Snare on 2, 4
        for step in [2, 6, 10, 14]:
            pattern[0][step] = True
        # Clap
        for step in [2, 6, 10, 14]:
            pattern[1][step] = True
        # Laser effects
        for step in [1, 5, 9, 13]:
            pattern[5][step] = True
        # Vocal Chops
        for step in [0, 4, 8, 12]:
            pattern[15][step] = True
        return pattern
        
    def create_background_tracks(self):
        """Create sick background tracks"""
        tracks = {}
        
        # Trap Background
        trap_pattern = [[False for _ in range(16)] for _ in range(16)]
        # Deep 808 bass line
        for step in [0, 4, 8, 12]:
            trap_pattern[7][step] = True  # 808 Bass (row 7)
        # 808 Kick
        for step in [0, 8]:
            trap_pattern[8][step] = True  # 808 Kick (row 8)
        # Hi-hats
        for step in range(0, 16, 2):
            trap_pattern[10][step] = True  # Open hi-hat (row 10)
        for step in range(1, 16, 2):
            trap_pattern[11][step] = True  # Closed hi-hat (row 11)
        tracks["Trap Background"] = trap_pattern
        
        # Boom Bap Background
        boom_pattern = [[False for _ in range(16)] for _ in range(16)]
        # Jazz bass line
        for step in [0, 2, 4, 6, 8, 10, 12, 14]:
            boom_pattern[2][step] = True  # Bass (row 2)
        # Classic snare
        for step in [4, 12]:
            boom_pattern[0][step] = True  # Snare (row 0)
        # Rimshot
        for step in [1, 3, 5, 7, 9, 11, 13, 15]:
            boom_pattern[12][step] = True  # Rimshot (row 12)
        # Cowbell
        for step in [0, 8]:
            boom_pattern[13][step] = True  # Cowbell (row 13)
        tracks["Boom Bap Background"] = boom_pattern
        
        # Lo-Fi Background
        lofi_pattern = [[False for _ in range(16)] for _ in range(16)]
        # Chill bass
        for step in [0, 8]:
            lofi_pattern[2][step] = True  # Bass (row 2)
        # Soft snare
        for step in [4, 12]:
            lofi_pattern[0][step] = True  # Snare (row 0)
        # Clap
        for step in [2, 6, 10, 14]:
            lofi_pattern[1][step] = True  # Clap (row 1)
        # Ambient FX
        for step in [0, 4, 8, 12]:
            lofi_pattern[3][step] = True  # FX (row 3)
        # Synth Lead
        for step in [1, 5, 9, 13]:
            lofi_pattern[14][step] = True  # Synth Lead (row 14)
        tracks["Lo-Fi Background"] = lofi_pattern
        
        # Club Background
        club_pattern = [[False for _ in range(16)] for _ in range(16)]
        # Snare on 2, 4
        for step in [2, 6, 10, 14]:
            club_pattern[0][step] = True  # Snare (row 0)
        # Clap
        for step in [2, 6, 10, 14]:
            club_pattern[1][step] = True  # Clap (row 1)
        # Laser effects
        for step in [1, 5, 9, 13]:
            club_pattern[5][step] = True  # Laser (row 5)
        # Vocal Chops
        for step in [0, 4, 8, 12]:
            club_pattern[15][step] = True  # Vocal Chop (row 15)
        # Reverse Cymbal
        for step in [15]:
            club_pattern[15][step] = True  # Reverse Cymbal (row 15)
        tracks["Club Background"] = club_pattern
        
        return tracks
        
    def create_particle(self, x, y, color):
        """Create a visual particle"""
        particle = {
            'x': x,
            'y': y,
            'vx': random.uniform(-5, 5),
            'vy': random.uniform(-8, -2),
            'color': color,
            'life': random.randint(20, 40),
            'size': random.randint(2, 6)
        }
        self.particles.append(particle)
        
    def update_particles(self):
        """Update particle effects"""
        for particle in self.particles[:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['vy'] += 0.3  # Gravity
            particle['life'] -= 1
            
            if particle['life'] <= 0:
                self.particles.remove(particle)
                
    def draw_particles(self):
        """Draw particle effects"""
        for particle in self.particles:
            alpha = particle['life'] / 40
            size = int(particle['size'] * alpha)
            if size > 0:
                pygame.draw.circle(self.screen, particle['color'], 
                                 (int(particle['x']), int(particle['y'])), size)
    
    def draw_sequencer_grid(self):
        """Draw the beat sequencer grid"""
        # Draw grid background
        grid_rect = pygame.Rect(self.grid_x - 5, self.grid_y - 5, 
                               self.cell_width * 16 + 10, 
                               self.cell_height * 16 + 10)
        pygame.draw.rect(self.screen, DARK_GRAY, grid_rect)
        pygame.draw.rect(self.screen, WHITE, grid_rect, 2)
        
        # Draw cells
        for row in range(16):
            for col in range(16):
                x = self.grid_x + col * self.cell_width
                y = self.grid_y + row * self.cell_height
                
                # Cell color based on state
                if self.beat_pattern.pattern[row][col]:
                    color = self.get_sound_color(self.beat_pattern.sound_types[row])
                    if col == self.current_step and self.playing:
                        color = tuple(min(255, c + 50) for c in color)
                else:
                    color = LIGHT_GRAY
                    if col == self.current_step and self.playing:
                        color = (150, 150, 150)
                
                # Draw cell
                cell_rect = pygame.Rect(x, y, self.cell_width - 2, self.cell_height - 2)
                pygame.draw.rect(self.screen, color, cell_rect)
                pygame.draw.rect(self.screen, BLACK, cell_rect, 1)
                
                # Highlight selected cell
                if self.selected_cell == (row, col):
                    pygame.draw.rect(self.screen, YELLOW, cell_rect, 3)
        
        # Draw sound labels
        for row, sound_type in enumerate(self.beat_pattern.sound_types):
            label = self.font_small.render(sound_type.value.upper(), True, WHITE)
            self.screen.blit(label, (self.grid_x - 45, self.grid_y + row * self.cell_height + 5))
        
        # Draw step numbers
        for col in range(16):
            step_num = str(col + 1)
            color = YELLOW if col == self.current_step and self.playing else WHITE
            label = self.font_small.render(step_num, True, color)
            self.screen.blit(label, (self.grid_x + col * self.cell_width + 10, self.grid_y - 25))
            
    def get_sound_color(self, sound_type):
        """Get color for sound type"""
        colors = {
            SoundType.SNARE: SNARE_COLOR,
            SoundType.CLAP: ORANGE,
            SoundType.BASS: BASS_COLOR,
            SoundType.FX: CYAN,
            SoundType.EXPLOSION: RED,
            SoundType.LASER: PINK,
            SoundType.ZAPPER: YELLOW,
            SoundType.BASS_808: (138, 43, 226),  # Deep purple
            SoundType.KICK_808: (255, 69, 0),    # Orange-red
            SoundType.HIHAT_OPEN: (255, 255, 100),  # Bright yellow
            SoundType.HIHAT_CLOSED: (100, 255, 255),  # Cyan
            SoundType.RIMSHOT: (255, 255, 255),  # White
            SoundType.COWBELL: (255, 215, 0),    # Gold
            SoundType.SYNTH_LEAD: (0, 255, 127),  # Spring green
            SoundType.VOCAL_CHOP: (255, 105, 180),  # Hot pink
            SoundType.REVERSE_CYMBAL: (0, 191, 255)  # Deep sky blue
        }
        return colors.get(sound_type, WHITE)
        
    def draw_visualizer(self):
        """Draw audio visualizer"""
        viz_x = 700
        viz_y = 150
        viz_width = 600
        viz_height = 200
        
        # Background
        viz_rect = pygame.Rect(viz_x, viz_y, viz_width, viz_height)
        pygame.draw.rect(self.screen, DARK_GRAY, viz_rect)
        pygame.draw.rect(self.screen, WHITE, viz_rect, 2)
        
        # Draw visualizer bars
        if len(self.visualizer) > 0:
            bar_width = viz_width // len(self.visualizer)
            for i, value in enumerate(self.visualizer):
                bar_height = int(value * viz_height)
                bar_x = viz_x + i * bar_width
                bar_y = viz_y + viz_height - bar_height
                
                # Rainbow colors
                hue = (i * 360 // len(self.visualizer)) % 360
                color = pygame.Color(0)
                color.hsva = (hue, 100, 100, 100)
                
                pygame.draw.rect(self.screen, color, 
                               (bar_x, bar_y, bar_width - 1, bar_height))
        
        # Title
        title = self.font_medium.render("AUDIO VISUALIZER", True, WHITE)
        self.screen.blit(title, (viz_x + viz_width // 2 - 100, viz_y - 30))
        
    def draw_lyrics_editor(self):
        """Draw rap lyrics editor"""
        editor_x = 700
        editor_y = 400
        editor_width = 600
        editor_height = 300
        
        # Background
        editor_rect = pygame.Rect(editor_x, editor_y, editor_width, editor_height)
        pygame.draw.rect(self.screen, DARK_GRAY, editor_rect)
        pygame.draw.rect(self.screen, WHITE if self.input_active else LIGHT_GRAY, editor_rect, 3)
        
        # Title
        title = self.font_medium.render("RAP LYRICS EDITOR", True, WHITE)
        self.screen.blit(title, (editor_x + editor_width // 2 - 100, editor_y - 30))
        
        # Current input
        input_text = self.font_small.render(f"> {self.lyric_input}", True, YELLOW)
        self.screen.blit(input_text, (editor_x + 10, editor_y + 10))
        
        # Previous lines
        y_offset = 40
        for i, line in enumerate(self.rap_lyrics.lines[-8:]):  # Show last 8 lines
            color = WHITE if i < len(self.rap_lyrics.lines) - 1 else YELLOW
            line_text = self.font_small.render(f"{i+1}. {line}", True, color)
            self.screen.blit(line_text, (editor_x + 10, editor_y + y_offset))
            y_offset += 25
            
        # Instructions
        inst_text = self.font_small.render("Press ENTER to add line, BACKSPACE to delete", True, LIGHT_GRAY)
        self.screen.blit(inst_text, (editor_x + 10, editor_y + editor_height - 25))
        
    def draw_controls(self):
        """Draw control panel"""
        control_x = 900  # Right side
        control_y = 280  # Moved lower
        
        # Title
        title = self.font_large.render("BEAT CONTROLS", True, WHITE)
        self.screen.blit(title, (control_x, control_y))
        
        # Controls - split into columns to prevent overlapping
        left_controls = [
            "SPACE: Play/Pause",
            "R: Easy Record",
            "E: Auto-Record", 
            "C: Clear Pattern",
            "T: Change Tempo",
            "1-4: Load Presets",
            "5-8: Random Beats",
            "G: Random Beat"
        ]
        
        right_controls = [
            "Shift+G: Cycle Genre",
            "Alt+E: Evolve Pattern",
            "Click: Toggle Beat",
            "Type: Add Lyrics",
            "S: Save Song",
            "",
            "PATTERN MGMT:",
            "Ctrl+C: Copy",
            "Ctrl+V: Paste",
            "Ctrl+X: Cut",
            "Ctrl+D: Duplicate",
            "Ctrl+M: Mirror",
            "Ctrl+R/L: Rotate"
        ]
        
        # Draw left column
        for i, control in enumerate(left_controls):
            color = YELLOW if "Play" in control and self.playing else WHITE
            text = self.font_small.render(control, True, color)
            self.screen.blit(text, (control_x, control_y + 40 + i * 20))
        
        # Draw right column
        right_x = control_x + 150  # Adjusted for new position
        for i, control in enumerate(right_controls):
            if control == "PATTERN MGMT:":
                color = CYAN
            elif control.startswith("Ctrl+"):
                color = LIGHT_GRAY
            else:
                color = WHITE
            text = self.font_small.render(control, True, color)
            self.screen.blit(text, (right_x, control_y + 40 + i * 20))
            
        # Recording status
        if self.recording:
            rec_text = self.font_large.render("RECORDING", True, RED)
            self.screen.blit(rec_text, (SCREEN_WIDTH // 2 - 100, 50))
            
        if self.easy_record_mode:
            easy_text = self.font_medium.render("AUTO-RECORD ON", True, GREEN)
            self.screen.blit(easy_text, (SCREEN_WIDTH // 2 - 80, 90))
            
        # Pattern slots display (moved to match controls)
        slots_y = control_y + 320
        slots_title = self.font_medium.render("PATTERN SLOTS", True, WHITE)
        self.screen.blit(slots_title, (control_x, slots_y))
        
        for i, (slot_name, pattern) in enumerate(self.pattern_manager.pattern_slots.items()):
            slot_x = control_x + i * 80
            slot_y = slots_y + 40
            
            # Slot background
            if pattern:
                # Check if current pattern matches this slot
                matches = (pattern == self.beat_pattern.pattern)
                color = GREEN if matches else YELLOW
                slot_text = f"{slot_name}"
            else:
                color = LIGHT_GRAY
                slot_text = f"{slot_name}:"
                
            # Draw slot
            slot_rect = pygame.Rect(slot_x, slot_y, 70, 25)
            pygame.draw.rect(self.screen, color, slot_rect, 2)
            
            # Slot text
            text = self.font_small.render(slot_text, True, color)
            text_rect = text.get_rect(center=(slot_x + 35, slot_y + 12))
            self.screen.blit(text, text_rect)
        
        # Instructions for slots
        inst_text = self.font_small.render("F1-F4: Save | Shift+F1-F4: Load", True, LIGHT_GRAY)
        self.screen.blit(inst_text, (control_x, slots_y + 75))
            
        # Tempo display
        tempo_text = self.font_medium.render(f"Tempo: {self.beat_pattern.tempo} BPM", True, WHITE)
        self.screen.blit(tempo_text, (control_x, control_y + 250))
            
    def get_sound_color(self, sound_type):
        """Get color for sound type"""
        colors = {
            SoundType.SNARE: SNARE_COLOR,
            SoundType.CLAP: ORANGE,
            SoundType.BASS: BASS_COLOR,
            SoundType.FX: GREEN,
            SoundType.EXPLOSION: RED,
            SoundType.LASER: CYAN,
            SoundType.ZAPPER: PINK,
            SoundType.BASS_808: PURPLE,
            SoundType.KICK_808: ORANGE,
            SoundType.HIHAT_OPEN: HIHAT_COLOR,
            SoundType.HIHAT_CLOSED: LIGHT_GRAY,
            SoundType.RIMSHOT: WHITE,
            SoundType.COWBELL: YELLOW,
            SoundType.SYNTH_LEAD: GREEN,
            SoundType.VOCAL_CHOP: PINK,
            SoundType.REVERSE_CYMBAL: CYAN
        }
        return colors.get(sound_type, WHITE)
        
    def draw_visualizer(self):
        """Draw audio visualizer"""
        viz_x = 700
        viz_y = 150
        viz_width = 300
        viz_height = 100
        
        # Background
        viz_rect = pygame.Rect(viz_x, viz_y, viz_width, viz_height)
        pygame.draw.rect(self.screen, DARK_GRAY, viz_rect)
        pygame.draw.rect(self.screen, WHITE, viz_rect, 2)
        
        # Draw visualizer bars
        if len(self.visualizer) > 0:
            bar_width = viz_width // len(self.visualizer)
            for i, value in enumerate(self.visualizer):
                bar_height = int(value * viz_height)
                bar_x = viz_x + i * bar_width
                bar_y = viz_y + viz_height - bar_height
                pygame.draw.rect(self.screen, GREEN, (bar_x, bar_y, bar_width - 2, bar_height))
    
    def draw_presets(self):
        """Draw preset buttons"""
        preset_x = 50
        preset_y = 700  # Moved up from 750
        
        for i, (name, pattern) in enumerate(self.presets.items()):
            x = preset_x + i * 150
            color = GREEN if self.beat_pattern.pattern == pattern else LIGHT_GRAY
            button_rect = pygame.Rect(x, preset_y, 140, 30)
            pygame.draw.rect(self.screen, color, button_rect)
            pygame.draw.rect(self.screen, BLACK, button_rect, 2)
            
            text = self.font_small.render(name, True, BLACK)
            text_rect = text.get_rect(center=(x + 70, preset_y + 15))
            self.screen.blit(text, text_rect)
            
    def draw_title(self):
        """Draw main title"""
        title = self.font_huge.render("🎤 EPIC RAP BEAT MAKER 🎤", True, YELLOW)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 50))
        self.screen.blit(title, title_rect)
        
        subtitle = self.font_large.render("Create the sickest hip-hop tracks ever!", True, WHITE)
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.screen.blit(subtitle, subtitle_rect)
        
    def handle_grid_click(self, pos):
        """Handle clicks on the sequencer grid"""
        x, y = pos
        
        # Check if click is within grid
        if (self.grid_x <= x <= self.grid_x + self.cell_width * 16 and
            self.grid_y <= y <= self.grid_y + self.cell_height * 16):  # Changed from 8 to 16
            
            col = (x - self.grid_x) // self.cell_width
            row = (y - self.grid_y) // self.cell_height
            
            if 0 <= row < 16 and 0 <= col < 16:  # Changed from 8 to 16
                # Toggle beat
                self.beat_pattern.pattern[row][col] = not self.beat_pattern.pattern[row][col]
                self.selected_cell = (row, col)
                
                # Create particle effect
                cell_x = self.grid_x + col * self.cell_width + self.cell_width // 2
                cell_y = self.grid_y + row * self.cell_height + self.cell_height // 2
                color = self.get_sound_color(self.beat_pattern.sound_types[row])
                self.create_particle(cell_x, cell_y, color)
                
                # Play sound
                if self.beat_pattern.pattern[row][col]:
                    self.sounds[self.beat_pattern.sound_types[row]].play()
                    
    def handle_preset_click(self, pos):
        """Handle preset button clicks"""
        x, y = pos
        preset_y = 700  # Updated to match new position
        
        if preset_y <= y <= preset_y + 30:
            for i, name in enumerate(self.presets.keys()):
                button_x = 50 + i * 150  # Match drawing coordinates
                if button_x <= x <= button_x + 140:
                    self.beat_pattern.pattern = [row[:] for row in self.presets[name]]
                    print(f"Loaded {name} preset")  # Add debug output
                    break
                    
    def play_step(self):
        """Play current step of the pattern"""
        for row in range(16):
            if self.beat_pattern.pattern[row][self.current_step]:
                sound = self.sounds[self.beat_pattern.sound_types[row]]
                sound.play()
                
                # Add to visualizer
                self.visualizer.append(random.uniform(0.3, 1.0))
                
                # Create particle effect
                cell_x = self.grid_x + self.current_step * self.cell_width + self.cell_width // 2
                cell_y = self.grid_y + row * self.cell_height + self.cell_height // 2
                color = self.get_sound_color(self.beat_pattern.sound_types[row])
                self.create_particle(cell_x, cell_y, color)
                
                # Screen shake for explosions
                if self.beat_pattern.sound_types[row] == SoundType.EXPLOSION:
                    self.screen_shake = 5
                    
                # Recording
                if self.recording:
                    self.recorded_pattern.append({
                        'step': self.current_step,
                        'row': row,
                        'sound': self.beat_pattern.sound_types[row].value
                    })
                    
                # Easy record mode - automatically record any playing beat
                if self.easy_record_mode and not self.recording:
                    if not hasattr(self, 'easy_recorded_pattern'):
                        self.easy_recorded_pattern = []
                    self.easy_recorded_pattern.append({
                        'step': self.current_step,
                        'row': row,
                        'sound': self.beat_pattern.sound_types[row].value
                    })
                    
    def update_sequencer(self):
        """Update sequencer"""
        if self.playing:
            self.step_timer += self.clock.get_time()
            
            if self.step_timer >= self.step_interval:
                self.step_timer = 0
                self.play_step()
                
                if self.recording:
                    self.recorded_pattern.append(self.current_step)
                    
                self.current_step = (self.current_step + 1) % 16
                
    def handle_events(self):
        """Handle events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.playing = not self.playing
                    if not self.playing:
                        self.current_step = 0
                        self.step_timer = 0
                        
                elif event.key == pygame.K_r:
                    # Easy recording - one press to start, another to stop and save
                    if not self.recording:
                        self.recording = True
                        self.recorded_pattern = []
                        self.recording_start_step = self.current_step
                        print("🎤 RECORDING STARTED! Press R again to stop and save...")
                    else:
                        self.recording = False
                        self.save_recorded_beat()
                        print("✅ RECORDING SAVED!")
                        
                elif event.key == pygame.K_e:
                    # Easy record mode - automatically records your beat playing
                    self.easy_record_mode = not self.easy_record_mode
                    if self.easy_record_mode:
                        print("🎵 EASY RECORD MODE ON - Playing automatically records!")
                    else:
                        print("⏹️ EASY RECORD MODE OFF")
                        
                elif event.key == pygame.K_c:
                    self.beat_pattern.pattern = [[False for _ in range(16)] for _ in range(16)]
                    
                elif event.key == pygame.K_t:
                    self.beat_pattern.tempo = (self.beat_pattern.tempo % 180) + 60
                    self.step_interval = 60000 // (self.beat_pattern.tempo * 4)
                    
                # Beat Pattern Management Controls
                elif event.key == pygame.K_x and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    # Ctrl+X: Cut pattern (copy and clear)
                    self.pattern_manager.copy_pattern(self.beat_pattern.pattern)
                    self.beat_pattern.pattern = [[False for _ in range(16)] for _ in range(16)]
                    print("Pattern cut to clipboard")
                    
                elif event.key == pygame.K_c and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    # Ctrl+C: Copy pattern
                    self.pattern_manager.copy_pattern(self.beat_pattern.pattern)
                    print("Pattern copied to clipboard")
                    
                elif event.key == pygame.K_v and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    # Ctrl+V: Paste pattern
                    if self.pattern_manager.paste_pattern(self.beat_pattern.pattern):
                        print("Pattern pasted from clipboard")
                    else:
                        print("No pattern in clipboard")
                        
                elif event.key == pygame.K_d and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    # Ctrl+D: Duplicate pattern
                    self.beat_pattern.pattern = self.pattern_manager.duplicate_pattern(self.beat_pattern.pattern)
                    print("Pattern duplicated")
                    
                elif event.key == pygame.K_m and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    # Ctrl+M: Mirror pattern horizontally
                    self.beat_pattern.pattern = self.pattern_manager.mirror_pattern_horizontal(self.beat_pattern.pattern)
                    print("Pattern mirrored horizontally")
                    
                elif event.key == pygame.K_r and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    # Ctrl+R: Rotate pattern right
                    self.beat_pattern.pattern = self.pattern_manager.rotate_pattern_right(self.beat_pattern.pattern)
                    print("Pattern rotated right")
                    
                elif event.key == pygame.K_l and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    # Ctrl+L: Rotate pattern left
                    self.beat_pattern.pattern = self.pattern_manager.rotate_pattern_left(self.beat_pattern.pattern)
                    print("Pattern rotated left")
                    
                # Pattern slot controls (F1-F4 for slots A-D)
                elif event.key == pygame.K_F1:
                    # Save to slot A
                    if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        # Shift+F1: Load from slot A
                        if self.pattern_manager.load_from_slot('A', self.beat_pattern.pattern):
                            print("Loaded pattern from slot A")
                        else:
                            print("Slot A is empty")
                    else:
                        # F1: Save to slot A
                        self.pattern_manager.save_to_slot('A', self.beat_pattern.pattern)
                        print("Pattern saved to slot A")
                        
                elif event.key == pygame.K_F2:
                    # Save to slot B
                    if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        # Shift+F2: Load from slot B
                        if self.pattern_manager.load_from_slot('B', self.beat_pattern.pattern):
                            print("Loaded pattern from slot B")
                        else:
                            print("Slot B is empty")
                    else:
                        # F2: Save to slot B
                        self.pattern_manager.save_to_slot('B', self.beat_pattern.pattern)
                        print("Pattern saved to slot B")
                        
                elif event.key == pygame.K_F3:
                    # Save to slot C
                    if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        # Shift+F3: Load from slot C
                        if self.pattern_manager.load_from_slot('C', self.beat_pattern.pattern):
                            print("Loaded pattern from slot C")
                        else:
                            print("Slot C is empty")
                    else:
                        # F3: Save to slot C
                        self.pattern_manager.save_to_slot('C', self.beat_pattern.pattern)
                        print("Pattern saved to slot C")
                        
                elif event.key == pygame.K_F4:
                    # Save to slot D
                    if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        # Shift+F4: Load from slot D
                        if self.pattern_manager.load_from_slot('D', self.beat_pattern.pattern):
                            print("Loaded pattern from slot D")
                        else:
                            print("Slot D is empty")
                    else:
                        # F4: Save to slot D
                        self.pattern_manager.save_to_slot('D', self.beat_pattern.pattern)
                        print("Pattern saved to slot D")
                    
                # Random Beat Generator Controls
                elif event.key == pygame.K_g:
                    # Generate random beat
                    pattern, genre = self.beat_generator.generate_random_pattern()
                    self.beat_pattern.pattern = pattern
                    print(f"Generated {genre.title()} beat!")
                    
                elif event.key == pygame.K_g and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    # Shift+G: Generate specific genre
                    genres = self.beat_generator.get_genre_info()
                    current_genre = getattr(self, '_current_genre', 0)
                    current_genre = (current_genre + 1) % len(genres)
                    self._current_genre = current_genre
                    
                    genre = genres[current_genre]
                    pattern, _ = self.beat_generator.generate_random_pattern(genre)
                    self.beat_pattern.pattern = pattern
                    print(f"Generated {genre.title()} beat!")
                    
                elif event.key == pygame.K_e and pygame.key.get_mods() & pygame.KMOD_ALT:
                    # Alt+E: Evolve current pattern
                    if hasattr(self, '_last_pattern'):
                        self.beat_pattern.pattern = self.beat_generator.generate_evolution(self.beat_pattern.pattern)
                        print("Pattern evolved!")
                    else:
                        print("No pattern to evolve (create one first)")
                    self._last_pattern = True
                    
                elif event.key == pygame.K_5:
                    # Generate trap beat
                    pattern, _ = self.beat_generator.generate_random_pattern('trap')
                    self.beat_pattern.pattern = pattern
                    print("Generated Trap beat!")
                    
                elif event.key == pygame.K_6:
                    # Generate boom bap beat
                    pattern, _ = self.beat_generator.generate_random_pattern('boom_bap')
                    self.beat_pattern.pattern = pattern
                    print("Generated Boom Bap beat!")
                    
                elif event.key == pygame.K_7:
                    # Generate lo-fi beat
                    pattern, _ = self.beat_generator.generate_random_pattern('lo_fi')
                    self.beat_pattern.pattern = pattern
                    print("Generated Lo-Fi beat!")
                    
                elif event.key == pygame.K_8:
                    # Generate techno beat
                    pattern, _ = self.beat_generator.generate_random_pattern('techno')
                    self.beat_pattern.pattern = pattern
                    print("Generated Techno beat!")
                    
                elif event.key == pygame.K_1:
                    self.beat_pattern.pattern = [row[:] for row in self.presets["Trap"]]
                elif event.key == pygame.K_2:
                    self.beat_pattern.pattern = [row[:] for row in self.presets["Boom Bap"]]
                elif event.key == pygame.K_3:
                    self.beat_pattern.pattern = [row[:] for row in self.presets["Lo-Fi"]]
                elif event.key == pygame.K_4:
                    self.beat_pattern.pattern = [row[:] for row in self.presets["Club"]]
                    
                elif event.key == pygame.K_RETURN:
                    if self.lyric_input.strip():
                        self.rap_lyrics.add_line(self.lyric_input.strip())
                        self.lyric_input = ""
                        
                elif event.key == pygame.K_BACKSPACE:
                    if self.lyric_input:
                        self.lyric_input = self.lyric_input[:-1]
                    elif self.rap_lyrics.lines:
                        self.rap_lyrics.lines.pop()
                        
                elif event.key == pygame.K_s:
                    self.save_song()
                    
                else:
                    # Add character to lyric input
                    if event.unicode and len(event.unicode) == 1:
                        self.lyric_input += event.unicode
                        
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    self.handle_grid_click(event.pos)
                    self.handle_preset_click(event.pos)
                    
    def load_christian_beat(self, beat_name):
        """Load a Christian hip-hop beat for learning"""
        print("Artist beats not available")
            
    def save_recorded_beat(self):
        """Save recorded beat to file"""
        if self.recorded_pattern:
            song_data = {
                "pattern": self.beat_pattern.pattern,
                "tempo": self.beat_pattern.tempo,
                "lyrics": self.rap_lyrics.lines,
                "recorded_steps": self.recorded_pattern
            }
            
            filename = f"recorded_beat_{random.randint(1000, 9999)}.json"
            with open(filename, 'w') as f:
                json.dump(song_data, f, indent=2)
                
            print(f"🎵 Beat saved as {filename}")
        else:
            print("❌ No recorded beats to save!")
            
    def save_song(self):
        """Save the current song"""
        song_data = {
            "pattern": self.beat_pattern.pattern,
            "tempo": self.beat_pattern.tempo,
            "lyrics": self.rap_lyrics.lines
        }
        
        filename = f"rap_song_{random.randint(1000, 9999)}.json"
        with open(filename, 'w') as f:
            json.dump(song_data, f, indent=2)
            
        print(f"🎵 Song saved as {filename}")
        
    def draw(self):
        """Draw everything"""
        self.screen.fill(BLACK)
        
        # Apply screen shake (fixed to prevent flashing)
        shake_x = shake_y = 0
        if self.screen_shake > 0:
            shake_x = random.randint(-self.screen_shake, self.screen_shake)
            shake_y = random.randint(-self.screen_shake, self.screen_shake)
            self.screen_shake -= 1
            
        # Draw all elements with shake offset
        def draw_with_offset(element_func, *args, **kwargs):
            if shake_x != 0 or shake_y != 0:
                # Create temporary surface for this element
                temp_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                temp_surface.fill((0, 0, 0, 0))  # Transparent
                
                # Save original screen
                original_screen = self.screen
                
                # Temporarily switch to temp surface
                self.screen = temp_surface
                element_func(*args, **kwargs)
                
                # Restore original screen
                self.screen = original_screen
                
                # Blit with shake
                self.screen.blit(temp_surface, (shake_x, shake_y))
            else:
                element_func(*args, **kwargs)
        
        # Draw everything with shake effect
        draw_with_offset(self.draw_sequencer_grid)
        draw_with_offset(self.draw_controls)
        draw_with_offset(self.draw_presets)
        draw_with_offset(self.draw_visualizer)
        
        # Draw title and subtitle (always on top, no shake)
        title = self.font_huge.render("🎤 EPIC RAP BEAT MAKER", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 50))
        self.screen.blit(title, title_rect)
        
        subtitle = self.font_medium.render("Professional Beat Making Edition", True, CYAN)
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.screen.blit(subtitle, subtitle_rect)
        
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update_sequencer()
            self.update_particles()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

def main():
    """Main function"""
    print("🎤 STARTING EPIC RAP BEAT MAKER! 🎵")
    print("Create the sickest hip-hop beats and rap songs!")
    print("🔥 Fire beats, trap flows, boom bap rhythms! 🔥")
    print("-" * 50)
    
    game = EpicRapBeatMaker()
    game.run()

if __name__ == "__main__":
    main()
