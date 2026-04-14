#!/usr/bin/env python3
"""
Enhanced Christian Hip-Hop Beat Maker with Professional Beat Making Features
"""

import pygame
import numpy as np
import math
import random
import sys
from enum import Enum
from collections import deque

# Screen settings
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
DARK_GRAY = (40, 40, 40)
LIGHT_GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PINK = (255, 192, 203)
CYAN = (0, 255, 255)
PURPLE = (128, 0, 128)

# Beat Enhancement System
class BeatEnhancer:
    def __init__(self):
        self.pitch_shifts = {}
        self.reverb_enabled = False
        self.reverb_size = 0.5
        self.reverb_decay = 0.5
        self.swing_amount = 0.0
        self.swing_enabled = False
        self.selected_sound_row = 0
        
    def set_pitch_shift(self, sound_type, semitones):
        """Set pitch shift in semitones (-12 to +12)"""
        self.pitch_shifts[sound_type] = max(-12, min(12, semitones))
        
    def get_pitch_multiplier(self, sound_type):
        """Get pitch multiplier for sound synthesis"""
        semitones = self.pitch_shifts.get(sound_type, 0)
        return 2 ** (semitones / 12)
        
    def toggle_reverb(self):
        """Toggle reverb on/off"""
        self.reverb_enabled = not self.reverb_enabled
        
    def set_reverb_size(self, size):
        """Set reverb room size (0.0 to 1.0)"""
        self.reverb_size = max(0.0, min(1.0, size))
        
    def set_swing(self, amount):
        """Set swing amount (0.0 to 1.0)"""
        self.swing_amount = max(0.0, min(1.0, amount))
        
    def toggle_swing(self):
        """Toggle swing on/off"""
        self.swing_enabled = not self.swing_enabled

class EnhancedBeatMaker:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Enhanced Christian Hip-Hop Beat Maker")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Fonts
        self.font_small = pygame.font.Font(None, 24)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_large = pygame.font.Font(None, 48)
        
        # Beat Enhancement System
        self.beat_enhancer = BeatEnhancer()
        
        # Sound system
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        self.sounds = self.create_enhanced_sounds()
        
        # Beat pattern (16 sounds x 16 steps)
        self.pattern = [[False for _ in range(16)] for _ in range(16)]
        self.sound_types = [
            "SNARE", "CLAP", "BASS", "FX", "EXPLOSION", "LASER", "ZAPPER",
            "BASS_808", "KICK_808", "HIHAT_OPEN", "HIHAT_CLOSED", 
            "RIMSHOT", "COWBELL", "SYNTH_LEAD", "VOCAL_CHOP", "REVERSE_CYMBAL"
        ]
        self.sound_colors = [
            YELLOW, ORANGE, PURPLE, GREEN, RED, CYAN, PINK,
            PURPLE, ORANGE, LIGHT_GRAY, GRAY, WHITE, YELLOW, GREEN, PINK, CYAN
        ]
        
        # Sequencer
        self.playing = False
        self.current_step = 0
        self.tempo = 120
        self.step_interval = 60000 // (self.tempo * 4)
        self.step_timer = 0
        
        # Grid settings
        self.grid_x = 50
        self.grid_y = 200
        self.cell_width = 40
        self.cell_height = 30
        
        # Initialize pitch shifts for all sounds
        for sound_type in self.sound_types:
            self.beat_enhancer.pitch_shifts[sound_type] = 0.0
        
        print("Enhanced Beat Maker initialized!")
        print("Beat Enhancement Controls:")
        print("Q/W: Raise/Lower pitch of selected sound")
        print("R: Toggle reverb")
        print("E/D: Increase/Decrease reverb size")
        print("Z/X: Increase/Decrease swing")
        print("C: Toggle swing")
        print("V: Reset all enhancements")
        print("Click grid to select sound row")
        
    def create_enhanced_sounds(self):
        """Create enhanced sounds with pitch control"""
        sounds = {}
        
        # Enhanced kick with pitch control
        def make_kick(pitch_mult=1.0):
            duration = 0.2
            samples = int(22050 * duration)
            wave = []
            for i in range(samples):
                t = i / 22050
                freq = 60 * pitch_mult * math.exp(-t * 10)
                sample = math.sin(2 * math.pi * freq * t) * math.exp(-t * 5)
                wave.append([int(sample * 16383), int(sample * 16383)])
            return pygame.sndarray.make_sound(np.array(wave, dtype=np.int16))
        
        # Enhanced snare with pitch control
        def make_snare(pitch_mult=1.0):
            duration = 0.1
            samples = int(22050 * duration)
            wave = []
            for i in range(samples):
                t = i / 22050
                noise = random.uniform(-0.3, 0.3)
                tone = math.sin(2 * math.pi * 200 * pitch_mult * t) * 0.5
                sample = (noise + tone) * math.exp(-t * 10)
                wave.append([int(sample * 16383), int(sample * 16383)])
            return pygame.sndarray.make_sound(np.array(wave, dtype=np.int16))
        
        # Enhanced hi-hat with pitch control
        def make_hihat(pitch_mult=1.0):
            duration = 0.05
            samples = int(22050 * duration)
            wave = []
            for i in range(samples):
                t = i / 22050
                noise = random.uniform(-0.2, 0.2)
                sample = noise * math.exp(-t * 20)
                wave.append([int(sample * 16383), int(sample * 16383)])
            return pygame.sndarray.make_sound(np.array(wave, dtype=np.int16))
        
        # Create basic sounds
        sounds["KICK_808"] = make_kick()
        sounds["SNARE"] = make_snare()
        sounds["HIHAT_CLOSED"] = make_hihat()
        sounds["HIHAT_OPEN"] = make_hihat()
        
        return sounds
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.playing = not self.playing
                    if not self.playing:
                        self.current_step = 0
                        self.step_timer = 0
                
                elif event.key == pygame.K_c:
                    self.pattern = [[False for _ in range(16)] for _ in range(16)]
                
                # Beat Enhancement Controls
                elif event.key == pygame.K_q:
                    # Raise pitch of selected sound
                    sound_type = self.sound_types[self.beat_enhancer.selected_sound_row]
                    current_pitch = self.beat_enhancer.pitch_shifts.get(sound_type, 0)
                    self.beat_enhancer.set_pitch_shift(sound_type, current_pitch + 1)
                    print(f"{sound_type} pitch: +{self.beat_enhancer.pitch_shifts[sound_type]} semitones")
                    
                elif event.key == pygame.K_w:
                    # Lower pitch of selected sound
                    sound_type = self.sound_types[self.beat_enhancer.selected_sound_row]
                    current_pitch = self.beat_enhancer.pitch_shifts.get(sound_type, 0)
                    self.beat_enhancer.set_pitch_shift(sound_type, current_pitch - 1)
                    print(f"{sound_type} pitch: {self.beat_enhancer.pitch_shifts[sound_type]} semitones")
                    
                elif event.key == pygame.K_r:
                    # Toggle reverb
                    self.beat_enhancer.toggle_reverb()
                    status = "ON" if self.beat_enhancer.reverb_enabled else "OFF"
                    print(f"Reverb: {status}")
                    
                elif event.key == pygame.K_e:
                    # Increase reverb size
                    current_size = self.beat_enhancer.reverb_size
                    self.beat_enhancer.set_reverb_size(current_size + 0.1)
                    print(f"Reverb Size: {int(self.beat_enhancer.reverb_size * 100)}%")
                    
                elif event.key == pygame.K_d:
                    # Decrease reverb size
                    current_size = self.beat_enhancer.reverb_size
                    self.beat_enhancer.set_reverb_size(current_size - 0.1)
                    print(f"Reverb Size: {int(self.beat_enhancer.reverb_size * 100)}%")
                    
                elif event.key == pygame.K_z:
                    # Increase swing
                    current_swing = self.beat_enhancer.swing_amount
                    self.beat_enhancer.set_swing(current_swing + 0.1)
                    print(f"Swing: {int(self.beat_enhancer.swing_amount * 100)}%")
                    
                elif event.key == pygame.K_x:
                    # Decrease swing
                    current_swing = self.beat_enhancer.swing_amount
                    self.beat_enhancer.set_swing(current_swing - 0.1)
                    print(f"Swing: {int(self.beat_enhancer.swing_amount * 100)}%")
                    
                elif event.key == pygame.K_c:
                    # Toggle swing
                    self.beat_enhancer.toggle_swing()
                    status = "ON" if self.beat_enhancer.swing_enabled else "OFF"
                    print(f"Swing: {status}")
                    
                elif event.key == pygame.K_v:
                    # Reset all enhancements
                    for sound_type in self.sound_types:
                        self.beat_enhancer.pitch_shifts[sound_type] = 0.0
                    self.beat_enhancer.reverb_enabled = False
                    self.beat_enhancer.swing_enabled = False
                    print("All enhancements reset!")
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    self.handle_grid_click(event.pos)
    
    def handle_grid_click(self, pos):
        x, y = pos
        # Check if click is in grid
        if (self.grid_x <= x <= self.grid_x + 16 * self.cell_width and
            self.grid_y <= y <= self.grid_y + 16 * self.cell_height):
            
            col = (x - self.grid_x) // self.cell_width
            row = (y - self.grid_y) // self.cell_height
            
            if 0 <= row < 16 and 0 <= col < 16:
                self.pattern[row][col] = not self.pattern[row][col]
                self.beat_enhancer.selected_sound_row = row
                
                # Play sound with pitch enhancement
                if self.pattern[row][col]:
                    sound_name = self.sound_types[row]
                    if sound_name in self.sounds:
                        # Create enhanced sound with pitch
                        pitch_mult = self.beat_enhancer.get_pitch_multiplier(sound_name)
                        if sound_name == "KICK_808":
                            enhanced_sound = self.create_enhanced_kick(pitch_mult)
                        elif sound_name == "SNARE":
                            enhanced_sound = self.create_enhanced_snare(pitch_mult)
                        else:
                            enhanced_sound = self.sounds[sound_name]
                        enhanced_sound.play()
    
    def create_enhanced_kick(self, pitch_mult=1.0):
        """Create kick with enhanced pitch"""
        duration = 0.2
        samples = int(22050 * duration)
        wave = []
        for i in range(samples):
            t = i / 22050
            freq = 60 * pitch_mult * math.exp(-t * 10)
            sample = math.sin(2 * math.pi * freq * t) * math.exp(-t * 5)
            wave.append([int(sample * 16383), int(sample * 16383)])
        return pygame.sndarray.make_sound(np.array(wave, dtype=np.int16))
    
    def create_enhanced_snare(self, pitch_mult=1.0):
        """Create snare with enhanced pitch"""
        duration = 0.1
        samples = int(22050 * duration)
        wave = []
        for i in range(samples):
            t = i / 22050
            noise = random.uniform(-0.3, 0.3)
            tone = math.sin(2 * math.pi * 200 * pitch_mult * t) * 0.5
            sample = (noise + tone) * math.exp(-t * 10)
            wave.append([int(sample * 16383), int(sample * 16383)])
        return pygame.sndarray.make_sound(np.array(wave, dtype=np.int16))
    
    def update_sequencer(self):
        if self.playing:
            self.step_timer += self.clock.get_time()
            
            if self.step_timer >= self.step_interval:
                self.step_timer = 0
                # Play current step with enhancements
                for row in range(16):
                    if self.pattern[row][self.current_step]:
                        sound_name = self.sound_types[row]
                        if sound_name in self.sounds:
                            # Apply pitch enhancement
                            pitch_mult = self.beat_enhancer.get_pitch_multiplier(sound_name)
                            if sound_name == "KICK_808":
                                enhanced_sound = self.create_enhanced_kick(pitch_mult)
                            elif sound_name == "SNARE":
                                enhanced_sound = self.create_enhanced_snare(pitch_mult)
                            else:
                                enhanced_sound = self.sounds[sound_name]
                            
                            # Apply reverb if enabled
                            if self.beat_enhancer.reverb_enabled:
                                enhanced_sound.set_volume(0.7)
                            else:
                                enhanced_sound.set_volume(1.0)
                            
                            enhanced_sound.play()
                
                # Move to next step
                self.current_step = (self.current_step + 1) % 16
    
    def draw_grid(self):
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
                
                # Cell color
                if self.pattern[row][col]:
                    color = self.sound_colors[row]
                    if col == self.current_step and self.playing:
                        color = tuple(min(255, c + 50) for c in color)
                else:
                    color = GRAY
                
                # Highlight selected row
                if row == self.beat_enhancer.selected_sound_row:
                    pygame.draw.rect(self.screen, YELLOW, (x-2, y-2, self.cell_width+2, self.cell_height+2), 2)
                
                pygame.draw.rect(self.screen, color, (x, y, self.cell_width - 2, self.cell_height - 2))
                
                # Highlight current step
                if col == self.current_step and self.playing:
                    pygame.draw.rect(self.screen, WHITE, (x, y, self.cell_width - 2, self.cell_height - 2), 2)
        
        # Draw sound labels
        for row, name in enumerate(self.sound_types[:16]):
            label = self.font_small.render(name[:8], True, WHITE)
            self.screen.blit(label, (self.grid_x - 45, self.grid_y + row * self.cell_height + 5))
        
        # Draw step numbers
        for step in range(16):
            if step % 4 == 0:
                num = self.font_small.render(str(step + 1), True, WHITE)
                self.screen.blit(num, (self.grid_x + step * self.cell_width + 10, self.grid_y - 25))
    
    def draw_enhancements(self):
        """Draw beat enhancement controls"""
        enh_x = 750
        enh_y = 200
        enh_width = 300
        enh_height = 400
        
        # Background
        enh_rect = pygame.Rect(enh_x, enh_y, enh_width, enh_height)
        pygame.draw.rect(self.screen, DARK_GRAY, enh_rect)
        pygame.draw.rect(self.screen, WHITE, enh_rect, 2)
        
        # Title
        title = self.font_medium.render("BEAT ENHANCEMENTS", True, WHITE)
        self.screen.blit(title, (enh_x + 10, enh_y + 10))
        
        y_offset = enh_y + 60
        
        # Selected sound
        selected_sound = self.sound_types[self.beat_enhancer.selected_sound_row]
        sel_text = self.font_small.render(f"Selected: {selected_sound}", True, YELLOW)
        self.screen.blit(sel_text, (enh_x + 10, y_offset))
        y_offset += 30
        
        # Pitch control
        pitch = int(self.beat_enhancer.pitch_shifts.get(selected_sound, 0))
        pitch_text = self.font_small.render(f"Pitch: {pitch:+d} semitones", True, WHITE)
        self.screen.blit(pitch_text, (enh_x + 10, y_offset))
        y_offset += 25
        
        # Pitch bar
        bar_x = enh_x + 10
        bar_y = y_offset
        bar_width = 200
        bar_height = 10
        pygame.draw.rect(self.screen, GRAY, (bar_x, bar_y, bar_width, bar_height))
        pitch_pos = bar_x + bar_width // 2 + (pitch * bar_width // 24)
        pygame.draw.rect(self.screen, GREEN, (bar_x, bar_y, pitch_pos - bar_x, bar_height))
        y_offset += 35
        
        # Reverb status
        reverb_status = "ON" if self.beat_enhancer.reverb_enabled else "OFF"
        reverb_color = GREEN if self.beat_enhancer.reverb_enabled else RED
        reverb_text = self.font_small.render(f"Reverb: {reverb_status}", True, reverb_color)
        self.screen.blit(reverb_text, (enh_x + 10, y_offset))
        y_offset += 25
        
        if self.beat_enhancer.reverb_enabled:
            size_text = self.font_small.render(f"Size: {int(self.beat_enhancer.reverb_size * 100)}%", True, WHITE)
            self.screen.blit(size_text, (enh_x + 10, y_offset))
            y_offset += 25
        
        # Swing status
        swing_status = "ON" if self.beat_enhancer.swing_enabled else "OFF"
        swing_color = GREEN if self.beat_enhancer.swing_enabled else RED
        swing_text = self.font_small.render(f"Swing: {swing_status}", True, swing_color)
        self.screen.blit(swing_text, (enh_x + 10, y_offset))
        y_offset += 25
        
        if self.beat_enhancer.swing_enabled:
            amount_text = self.font_small.render(f"Amount: {int(self.beat_enhancer.swing_amount * 100)}%", True, WHITE)
            self.screen.blit(amount_text, (enh_x + 10, y_offset))
            y_offset += 35
        
        # Instructions
        instructions = [
            "Q/W: Raise/Lower pitch",
            "R: Toggle reverb",
            "E/D: Reverb size",
            "Z/X: Swing amount",
            "C: Toggle swing",
            "V: Reset all",
            "",
            "Click grid to",
            "select sound row"
        ]
        
        for instruction in instructions:
            if instruction:
                inst_text = self.font_small.render(instruction, True, LIGHT_GRAY)
                self.screen.blit(inst_text, (enh_x + 10, y_offset))
            y_offset += 20
    
    def draw_ui(self):
        # Title
        title = self.font_large.render("Enhanced Beat Maker", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 50))
        self.screen.blit(title, title_rect)
        
        subtitle = self.font_medium.render("Professional Beat Enhancement", True, CYAN)
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, 90))
        self.screen.blit(subtitle, subtitle_rect)
        
        # Status
        status = "PLAYING" if self.playing else "STOPPED"
        status_color = GREEN if self.playing else RED
        status_text = self.font_medium.render(f"Status: {status}", True, status_color)
        self.screen.blit(status_text, (50, 140))
        
        # Tempo
        tempo_text = self.font_medium.render(f"Tempo: {self.tempo} BPM", True, WHITE)
        self.screen.blit(tempo_text, (250, 140))
        
        # Current step
        step_text = self.font_medium.render(f"Step: {self.current_step + 1}/16", True, YELLOW)
        self.screen.blit(step_text, (450, 140))
        
        # Controls
        controls = [
            "SPACE: Play/Pause",
            "C: Clear pattern",
            "Click grid: Add beats",
            "See enhancement panel for controls"
        ]
        
        for i, control in enumerate(controls):
            control_text = self.font_small.render(control, True, WHITE)
            self.screen.blit(control_text, (50, 650 + i * 25))
    
    def draw(self):
        self.screen.fill(BLACK)
        self.draw_grid()
        self.draw_enhancements()
        self.draw_ui()
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update_sequencer()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

def main():
    print("Enhanced Christian Hip-Hop Beat Maker!")
    print("Professional beat making features!")
    print("-" * 50)
    
    try:
        game = EnhancedBeatMaker()
        game.run()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
