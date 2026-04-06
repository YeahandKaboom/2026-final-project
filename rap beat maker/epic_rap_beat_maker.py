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

# Christian Hip-Hop Songs
class ChristianSong(Enum):
    LET_GO_LET_GOD = "let_go_let_god"

class ChristianRapSong:
    def __init__(self, song_name, tempo, lyrics, pattern):
        self.song_name = song_name
        self.tempo = tempo
        self.lyrics = lyrics
        self.pattern = pattern
        self.current_lyric_line = 0
        self.playing = False
        
class ChristianRapSongs:
    """Christian rap songs with full lyrics and beats"""
    
    def __init__(self):
        self.songs = self.create_christian_songs()
        
    def create_christian_songs(self):
        """Create Christian rap songs with beats and lyrics"""
        songs = {}
        
        # Let Go Let God - Full Christian Rap Song
        let_go_song = ChristianRapSong(
            "Let Go Let God",
            120,
            [
                "🎤 VERSE 1:",
                "I was walking in darkness, lost in my own way",
                "Trying to fix my problems, but I couldn't see the day",
                "Then I heard a voice saying 'Child, give it all to Me'",
                "Let Go Let God, that's the only way to be free",
                "",
                "🎤 CHORUS:",
                "Let Go Let God, He's got your back",
                "Let Go Let God, no turning back",
                "Let Go Let God, His love will guide you through",
                "Let Go Let God, His promises are true",
                "",
                "🎤 VERSE 2:",
                "Stop trying to control what you can't understand",
                "Give your worries to Him, He's got it in His hand",
                "His strength is made perfect when you're weak and feeling low",
                "Let Go Let God, watch your faith start to grow",
                "",
                "🎤 BRIDGE:",
                "Every burden, every care, every worry, every fear",
                "Lay them down at His feet, He's always here",
                "Trust in His timing, trust in His plan",
                "Let Go Let God, He's the great I AM",
                "",
                "🎤 OUTRO:",
                "Let Go Let God... yeah...",
                "Let Go Let God... amen...",
                "His grace is sufficient, His love never ends",
                "Let Go Let God, where your new life begins"
            ],
            [[False for _ in range(16)] for _ in range(16)]
        )
        
        # Create the beat pattern for Let Go Let God
        # Uplifting Christian hip-hop beat
        let_go_song.pattern[8][0] = True   # 808 Kick on 1
        let_go_song.pattern[8][4] = True   # 808 Kick on 2  
        let_go_song.pattern[8][8] = True   # 808 Kick on 3
        let_go_song.pattern[8][12] = True  # 808 Kick on 4
        let_go_song.pattern[0][4] = True   # Snare on 2
        let_go_song.pattern[0][12] = True  # Snare on 4
        let_go_song.pattern[1][4] = True   # Clap on 2
        let_go_song.pattern[1][12] = True  # Clap on 4
        let_go_song.pattern[2][0] = True   # Bass on 1
        let_go_song.pattern[2][2] = True   # Bass on 1&
        let_go_song.pattern[2][4] = True   # Bass on 2
        let_go_song.pattern[2][6] = True   # Bass on 2&
        let_go_song.pattern[2][8] = True   # Bass on 3
        let_go_song.pattern[2][10] = True  # Bass on 3&
        let_go_song.pattern[2][12] = True  # Bass on 4
        let_go_song.pattern[2][14] = True  # Bass on 4&
        let_go_song.pattern[14][2] = True  # Synth Lead
        let_go_song.pattern[14][6] = True  # Synth Lead
        let_go_song.pattern[14][10] = True # Synth Lead
        let_go_song.pattern[14][14] = True # Synth Lead
        let_go_song.pattern[15][8] = True  # Vocal Chop on 3
        
        songs["Let Go Let God"] = let_go_song
        return songs

# Christian Hip-Hop Artists and Their Styles
class ChristianArtist(Enum):
    HULVEY = "hulvey"
    FORREST_FRANK = "forrest_frank"
    KB = "kb"
    ONEK_PHIEW = "onek_phiew"

class ArtistBeatPattern:
    def __init__(self, artist, song_name, tempo, description):
        self.artist = artist
        self.song_name = song_name
        self.tempo = tempo
        self.description = description
        self.pattern = [[False for _ in range(16)] for _ in range(16)]
        self.sound_tips = []
        self.technique_notes = []
        
class ChristianHipHopBeats:
    """Christian hip-hop beat patterns and learning system"""
    
    def __init__(self):
        self.artist_beats = self.create_christian_beats()
        
    def create_christian_beats(self):
        """Create authentic Christian hip-hop beat patterns"""
        beats = {}
        
        # Hulvey Style - Melodic trap with worship elements
        hulvey_beat = ArtistBeatPattern(
            ChristianArtist.HULVEY,
            "ECHO",
            140,
            "Melodic trap with atmospheric pads and 808s"
        )
        # Hulvey's signature pattern
        hulvey_beat.pattern[7][0] = True  # 808 Bass on beat 1
        hulvey_beat.pattern[7][4] = True  # 808 Bass on beat 2
        hulvey_beat.pattern[7][8] = True  # 808 Bass on beat 3
        hulvey_beat.pattern[7][12] = True # 808 Bass on beat 4
        hulvey_beat.pattern[8][0] = True  # 808 Kick on beat 1
        hulvey_beat.pattern[0][8] = True  # Snare on beat 3
        hulvey_beat.pattern[14][2] = True # Synth Lead
        hulvey_beat.pattern[14][6] = True # Synth Lead
        hulvey_beat.pattern[14][10] = True# Synth Lead
        hulvey_beat.pattern[14][14] = True# Synth Lead
        hulvey_beat.sound_tips = [
            "Use deep 808 bass for worship atmosphere",
            "Add melodic synth leads for memorable hooks",
            "Keep tempo around 140 BPM for modern trap feel"
        ]
        hulvey_beat.technique_notes = [
            "Hulvey blends trap with worship music",
            "Focus on emotional, atmospheric sounds",
            "Simple patterns that support vocals"
        ]
        beats["Hulvey - ECHO"] = hulvey_beat
        
        # Forrest Frank Style - High energy trap with gospel influences
        forrest_beat = ArtistBeatPattern(
            ChristianArtist.FORREST_FRANK,
            "LIFESYTLE",
            150,
            "High energy trap with fast hi-hats and gospel chops"
        )
        # Forrest Frank's pattern
        forrest_beat.pattern[8][0] = True  # 808 Kick
        forrest_beat.pattern[8][8] = True  # 808 Kick
        forrest_beat.pattern[0][4] = True  # Snare
        forrest_beat.pattern[0][12] = True # Snare
        forrest_beat.pattern[10][2] = True # Open Hi-Hat
        forrest_beat.pattern[11][1] = True # Closed Hi-Hat
        forrest_beat.pattern[11][3] = True # Closed Hi-Hat
        forrest_beat.pattern[11][5] = True # Closed Hi-Hat
        forrest_beat.pattern[11][7] = True # Closed Hi-Hat
        forrest_beat.pattern[15][6] = True # Vocal Chops
        forrest_beat.pattern[15][14] = True# Vocal Chops
        forrest_beat.sound_tips = [
            "Fast hi-hat rolls for energy",
            "Vocal chops add gospel flavor",
            "Strong 808 foundation"
        ]
        forrest_beat.technique_notes = [
            "Forrest Frank uses gospel samples",
            "High energy patterns for worship",
            "Complex hi-hat patterns"
        ]
        beats["Forrest Frank - LIFESTYLE"] = forrest_beat
        
        # KB Style - Lyrical hip-hop with boom bap elements
        kb_beat = ArtistBeatPattern(
            ChristianArtist.KB,
            "MASTERPIECE",
            120,
            "Lyrical hip-hop with strong boom bap foundation"
        )
        # KB's pattern
        kb_beat.pattern[2][0] = True  # Bass
        kb_beat.pattern[2][2] = True  # Bass
        kb_beat.pattern[2][4] = True  # Bass
        kb_beat.pattern[2][6] = True  # Bass
        kb_beat.pattern[2][8] = True  # Bass
        kb_beat.pattern[2][10] = True # Bass
        kb_beat.pattern[2][12] = True # Bass
        kb_beat.pattern[2][14] = True # Bass
        kb_beat.pattern[0][4] = True  # Snare
        kb_beat.pattern[0][12] = True # Snare
        kb_beat.pattern[12][1] = True # Rimshot
        kb_beat.pattern[12][5] = True # Rimshot
        kb_beat.pattern[12][9] = True # Rimshot
        kb_beat.pattern[12][13] = True# Rimshot
        kb_beat.sound_tips = [
            "Boom bap bass lines for lyrical focus",
            "Rimshots add hip-hop authenticity",
            "Simple, strong patterns support lyrics"
        ]
        kb_beat.technique_notes = [
            "KB focuses on lyrical content",
            "Boom bap influences from classic hip-hop",
            "Clean patterns that don't distract"
        ]
        beats["KB - MASTERPIECE"] = kb_beat
        
        # 1K Phew Style - Trap with unique vocal delivery
        onek_beat = ArtistBeatPattern(
            ChristianArtist.ONEK_PHIEW,
            "PRAYING",
            135,
            "Modern trap with unique vocal patterns and 808s"
        )
        # 1K Phew's pattern
        onek_beat.pattern[7][0] = True  # 808 Bass
        onek_beat.pattern[7][6] = True  # 808 Bass
        onek_beat.pattern[7][12] = True # 808 Bass
        onek_beat.pattern[8][2] = True  # 808 Kick
        onek_beat.pattern[8][10] = True # 808 Kick
        onek_beat.pattern[0][4] = True  # Snare
        onek_beat.pattern[0][12] = True # Snare
        onek_beat.pattern[1][4] = True  # Clap
        onek_beat.pattern[1][12] = True # Clap
        onek_beat.pattern[10][1] = True # Open Hi-Hat
        onek_beat.pattern[10][5] = True # Open Hi-Hat
        onek_beat.pattern[10][9] = True # Open Hi-Hat
        onek_beat.pattern[10][13] = True# Open Hi-Hat
        onek_beat.sound_tips = [
            "Unique 808 patterns for signature sound",
            "Combine snares and claps for impact",
            "Open hi-hats create space"
        ]
        onek_beat.technique_notes = [
            "1K Phew has unique vocal delivery",
            "Trap beats with gospel messaging",
            "Signature 808 patterns"
        ]
        beats["1K Phew - PRAYING"] = onek_beat
        
        return beats

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
        
        # Christian Hip-Hop Learning System
        self.christian_beats = ChristianHipHopBeats()
        self.current_artist_beat = None
        self.learning_mode = False
        self.show_tips = True
        
        # Christian Rap Songs
        self.christian_songs = ChristianRapSongs()
        self.current_song = None
        self.song_playing = False
        self.lyric_timer = 0
        self.lyric_display_time = 3000  # Show each lyric for 3 seconds
        self.last_lyric_change = 0
        
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
            SoundType.HIHAT_OPEN: (192, 192, 192),  # Light gray
            SoundType.HIHAT_CLOSED: (128, 128, 128),  # Dark gray
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
        control_x = 50
        control_y = 450
        
        # Title
        title = self.font_large.render("🎤 BEAT CONTROLS 🎤", True, WHITE)
        self.screen.blit(title, (control_x, control_y))
        
        # Controls
        controls = [
            "SPACE: Play/Pause",
            "R: Easy Record (Press to start, press again to save)",
            "E: Auto-Record Mode (Records while playing)",
            "C: Clear Pattern",
            "T: Change Tempo / Toggle Tips",
            "1-4: Load Presets",
            "Click Grid: Toggle Beat",
            "Type: Add Lyrics",
            "S: Save Song",
            "",
            "🎵 CHRISTIAN HIP-HOP LEARNING:",
            "H: Load Hulvey Beat",
            "F: Load Forrest Frank Beat", 
            "K: Load KB Beat",
            "Shift+1: Load 1K Phew Beat",
            "L: Toggle Learning Mode",
            "",
            "🎤 PLAY SONG:",
            "G: Play 'Let Go Let God' (Full Song!)"
        ]
        
        for i, control in enumerate(controls):
            color = YELLOW if "Play" in control and self.playing else WHITE
            text = self.font_small.render(control, True, color)
            self.screen.blit(text, (control_x, control_y + 40 + i * 25))
            
        # Recording status
        if self.recording:
            rec_text = self.font_large.render("🔴 RECORDING", True, RED)
            self.screen.blit(rec_text, (SCREEN_WIDTH // 2 - 100, 50))
            
        if self.easy_record_mode:
            easy_text = self.font_medium.render("🎵 AUTO-RECORD ON", True, GREEN)
            self.screen.blit(easy_text, (SCREEN_WIDTH // 2 - 80, 90))
            
        # Tempo display
        tempo_text = self.font_medium.render(f"Tempo: {self.beat_pattern.tempo} BPM", True, WHITE)
        self.screen.blit(tempo_text, (control_x, control_y + 250))
            
    def draw_song_lyrics(self):
        """Draw Christian song lyrics"""
        if not self.song_playing or not self.current_song:
            return
            
        # Update lyrics
        self.update_song_lyrics()
        
        # Lyrics display area
        lyrics_x = 200
        lyrics_y = 650
        lyrics_width = 800
        lyrics_height = 100
        
        # Background for lyrics
        lyrics_rect = pygame.Rect(lyrics_x, lyrics_y, lyrics_width, lyrics_height)
        pygame.draw.rect(self.screen, DARK_GRAY, lyrics_rect)
        pygame.draw.rect(self.screen, WHITE, lyrics_rect, 2)
        
        # Current lyric line
        if self.current_song.current_lyric_line < len(self.current_song.lyrics):
            current_lyric = self.current_song.lyrics[self.current_song.current_lyric_line]
            
            # Word wrap for long lyrics
            words = current_lyric.split()
            lines = []
            current_line = ""
            
            for word in words:
                test_line = current_line + word + " "
                if self.font_medium.size(test_line)[0] < lyrics_width - 20:
                    current_line = test_line
                else:
                    if current_line:
                        lines.append(current_line.strip())
                    current_line = word + " "
            if current_line:
                lines.append(current_line.strip())
            
            # Draw lyrics
            y_offset = lyrics_y + 10
            for line in lines[:3]:  # Max 3 lines
                if line.strip():
                    # Color code different parts
                    if "VERSE" in line or "CHORUS" in line or "BRIDGE" in line or "OUTRO" in line:
                        color = YELLOW
                    elif "Let Go Let God" in line:
                        color = CYAN
                    else:
                        color = WHITE
                    
                    lyric_text = self.font_medium.render(line, True, color)
                    text_rect = lyric_text.get_rect(center=(lyrics_x + lyrics_width // 2, y_offset + 20))
                    self.screen.blit(lyric_text, text_rect)
                    y_offset += 30
        
        # Song info
        song_info = self.font_small.render(f"🎵 {self.current_song.song_name} - {self.current_song.tempo} BPM", True, GREEN)
        self.screen.blit(song_info, (lyrics_x, lyrics_y - 25))
        
        # Instructions
        inst_text = self.font_small.render("Press G to stop song", True, LIGHT_GRAY)
        self.screen.blit(inst_text, (lyrics_x + lyrics_width - 150, lyrics_y - 25))
    
    def draw_christian_learning(self):
        """Draw Christian hip-hop learning interface"""
        if not self.learning_mode or not self.current_artist_beat:
            return
            
        # Learning panel
        panel_x = 750
        panel_y = 400
        panel_width = 400
        panel_height = 300
        
        # Panel background
        panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
        pygame.draw.rect(self.screen, DARK_GRAY, panel_rect)
        pygame.draw.rect(self.screen, WHITE, panel_rect, 2)
        
        # Artist info
        y_offset = panel_y + 10
        
        # Artist name and song
        title = self.font_medium.render(f"🎵 {self.current_artist_beat.song_name}", True, WHITE)
        self.screen.blit(title, (panel_x + 10, y_offset))
        y_offset += 40
        
        # Artist name
        artist = self.font_small.render(f"Artist: {self.current_artist_beat.artist.value.title()}", True, CYAN)
        self.screen.blit(artist, (panel_x + 10, y_offset))
        y_offset += 30
        
        # Description
        desc = self.font_small.render(f"Style: {self.current_artist_beat.description}", True, YELLOW)
        self.screen.blit(desc, (panel_x + 10, y_offset))
        y_offset += 30
        
        # Tempo
        tempo = self.font_small.render(f"Tempo: {self.current_artist_beat.tempo} BPM", True, GREEN)
        self.screen.blit(tempo, (panel_x + 10, y_offset))
        y_offset += 40
        
        # Sound tips
        if self.show_tips:
            tips_title = self.font_small.render("🎯 Sound Tips:", True, WHITE)
            self.screen.blit(tips_title, (panel_x + 10, y_offset))
            y_offset += 25
            
            for tip in self.current_artist_beat.sound_tips:
                if y_offset < panel_y + panel_height - 60:
                    # Wrap long tips
                    words = tip.split()
                    line = ""
                    for word in words:
                        test_line = line + word + " "
                        if self.font_small.size(test_line)[0] < panel_width - 20:
                            line = test_line
                        else:
                            if line:
                                tip_text = self.font_small.render(line.strip(), True, LIGHT_GRAY)
                                self.screen.blit(tip_text, (panel_x + 10, y_offset))
                                y_offset += 20
                            line = word + " "
                    if line:
                        tip_text = self.font_small.render(line.strip(), True, LIGHT_GRAY)
                        self.screen.blit(tip_text, (panel_x + 10, y_offset))
                        y_offset += 20
            
            y_offset += 10
            
            # Technique notes
            tech_title = self.font_small.render("🎓 Techniques:", True, WHITE)
            self.screen.blit(tech_title, (panel_x + 10, y_offset))
            y_offset += 25
            
            for note in self.current_artist_beat.technique_notes:
                if y_offset < panel_y + panel_height - 20:
                    # Wrap long notes
                    words = note.split()
                    line = ""
                    for word in words:
                        test_line = line + word + " "
                        if self.font_small.size(test_line)[0] < panel_width - 20:
                            line = test_line
                        else:
                            if line:
                                note_text = self.font_small.render(line.strip(), True, LIGHT_GRAY)
                                self.screen.blit(note_text, (panel_x + 10, y_offset))
                                y_offset += 20
                            line = word + " "
                    if line:
                        note_text = self.font_small.render(line.strip(), True, LIGHT_GRAY)
                        self.screen.blit(note_text, (panel_x + 10, y_offset))
                        y_offset += 20
        
        # Instructions
        inst_y = panel_y + panel_height - 60
        instructions = [
            "Press L: Toggle Learning Mode",
            "Press T: Toggle Tips",
            "Modify the beat to learn!"
        ]
        
        for i, instruction in enumerate(instructions):
            inst_text = self.font_small.render(instruction, True, GREEN)
            self.screen.blit(inst_text, (panel_x + 10, inst_y + i * 20))
    
    def draw_presets(self):
        """Draw preset buttons"""
        preset_x = 50
        preset_y = 750
        
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
            self.grid_y <= y <= self.grid_y + self.cell_height * 8):
            
            col = (x - self.grid_x) // self.cell_width
            row = (y - self.grid_y) // self.cell_height
            
            if 0 <= row < 8 and 0 <= col < 16:
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
        preset_y = 750
        
        if preset_y <= y <= preset_y + 30:
            for i, name in enumerate(self.presets.keys()):
                button_x = 50 + i * 150
                if button_x <= x <= button_x + 140:
                    self.beat_pattern.pattern = [row[:] for row in self.presets[name]]
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
                    
                # Christian Hip-Hop Learning Controls
                elif event.key == pygame.K_h:
                    # Hulvey beat
                    self.load_christian_beat("Hulvey - ECHO")
                    
                elif event.key == pygame.K_f:
                    # Forrest Frank beat
                    self.load_christian_beat("Forrest Frank - LIFESTYLE")
                    
                elif event.key == pygame.K_k:
                    # KB beat
                    self.load_christian_beat("KB - MASTERPIECE")
                    
                elif event.key == pygame.K_1 and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    # 1K Phew beat (Shift+1)
                    self.load_christian_beat("1K Phew - PRAYING")
                    
                elif event.key == pygame.K_l:
                    # Toggle learning mode
                    self.learning_mode = not self.learning_mode
                    if self.learning_mode:
                        print("🎓 LEARNING MODE ON - Study Christian hip-hop beats!")
                    else:
                        print("📚 LEARNING MODE OFF")
                        
                elif event.key == pygame.K_t:
                    # Toggle tips display
                    self.show_tips = not self.show_tips
                    
                elif event.key == pygame.K_g:
                    # Toggle "Let Go Let God" song
                    if self.song_playing and self.current_song and self.current_song.song_name == "Let Go Let God":
                        # Stop the song
                        self.song_playing = False
                        self.current_song = None
                        self.playing = False
                        print("🎵 Stopped 'Let Go Let God'")
                    else:
                        # Play the song
                        self.play_christian_song("Let Go Let God")
                    
                elif event.key == pygame.K_t:
                    self.beat_pattern.tempo = (self.beat_pattern.tempo % 180) + 60
                    self.step_interval = 60000 // (self.beat_pattern.tempo * 4)
                    
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
        if beat_name in self.christian_beats.artist_beats:
            self.current_artist_beat = self.christian_beats.artist_beats[beat_name]
            self.beat_pattern.pattern = [row[:] for row in self.current_artist_beat.pattern]
            self.beat_pattern.tempo = self.current_artist_beat.tempo
            self.step_interval = 60000 // (self.beat_pattern.tempo * 4)
            self.learning_mode = True
            print(f"🎵 Loaded {beat_name} - {self.current_artist_beat.description}")
            print(f"🎓 Tempo: {self.current_artist_beat.tempo} BPM")
            print("💡 Press L to toggle learning mode, T to toggle tips")
            
    def play_christian_song(self, song_name):
        """Play a Christian rap song with lyrics"""
        if song_name in self.christian_songs.songs:
            self.current_song = self.christian_songs.songs[song_name]
            self.beat_pattern.pattern = [row[:] for row in self.current_song.pattern]
            self.beat_pattern.tempo = self.current_song.tempo
            self.step_interval = 60000 // (self.beat_pattern.tempo * 4)
            self.song_playing = True
            self.current_song.current_lyric_line = 0
            self.last_lyric_change = pygame.time.get_ticks()
            
            # Start playing the beat
            self.playing = True
            
            print(f"🎵 Now playing: {song_name}")
            print(f"🎤 Tempo: {self.current_song.tempo} BPM")
            print("🎵 Press G again to stop, SPACE to pause/resume")
            
    def update_song_lyrics(self):
        """Update which lyric line is currently being displayed"""
        if self.song_playing and self.current_song:
            current_time = pygame.time.get_ticks()
            
            # Move to next lyric line after display time
            if current_time - self.last_lyric_change >= self.lyric_display_time:
                self.current_song.current_lyric_line += 1
                self.last_lyric_change = current_time
                
                # Loop back to beginning if reached end
                if self.current_song.current_lyric_line >= len(self.current_song.lyrics):
                    self.current_song.current_lyric_line = 0
                    
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
        
        # Apply screen shake
        if self.screen_shake > 0:
            shake_x = random.randint(-self.screen_shake, self.screen_shake)
            shake_y = random.randint(-self.screen_shake, self.screen_shake)
            self.screen_shake -= 1
        else:
            shake_x = shake_y = 0
            
        # Create a temporary surface for screen shake
        if shake_x != 0 or shake_y != 0:
            temp_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            temp_surface.fill(BLACK)
            
            # Draw everything to temp surface
            self.draw_sequencer_grid()
            self.draw_controls()
            self.draw_presets()
            self.draw_visualizer()
            self.draw_christian_learning()
            self.draw_song_lyrics()
            
            # Blit with shake
            self.screen.blit(temp_surface, (shake_x, shake_y))
        else:
            # Draw directly to screen
            self.draw_sequencer_grid()
            self.draw_controls()
            self.draw_presets()
            self.draw_visualizer()
            self.draw_christian_learning()
            self.draw_song_lyrics()
        
        # Draw title
        title = self.font_huge.render("🎤 EPIC RAP BEAT MAKER", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 50))
        self.screen.blit(title, title_rect)
        
        subtitle = self.font_medium.render("Christian Hip-Hop Learning Edition", True, CYAN)
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
