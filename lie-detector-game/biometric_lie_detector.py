#!/usr/bin/env python3
"""
REAL BIOMETRIC LIE DETECTOR GAME
Uses actual computer touch detection and simulated vital sign monitoring
"""

import pygame
import random
import math
import time
import sys
from enum import Enum
from datetime import datetime

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (50, 50, 50)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
PINK = (255, 192, 203)

# Game States
class GameState(Enum):
    MENU = "menu"
    CALIBRATION = "calibration"
    PLAYING = "playing"
    QUESTION = "question"
    ANALYSIS = "analysis"
    RESULT = "result"
    GAME_OVER = "game_over"

class BiometricSensor:
    def __init__(self):
        self.is_touching = False
        self.touch_duration = 0
        self.heart_rate = 70
        self.blood_pressure = 120
        self.sweat_level = 0
        self.respiration_rate = 16
        self.stress_level = 0
        self.temperature = 98.6
        self.baseline_heart_rate = 70
        self.baseline_pressure = 120
        self.calibrated = False
        self.sensor_quality = 0
        
    def detect_touch(self, mouse_pos, keys_pressed):
        """Detect if user is touching the computer (simulated)"""
        # Check if mouse is in sensor area
        sensor_area = pygame.Rect(500, 300, 200, 200)
        
        # Check for touch indicators
        mouse_in_sensor = sensor_area.collidepoint(mouse_pos)
        space_pressed = keys_pressed[pygame.K_SPACE]
        shift_pressed = keys_pressed[pygame.K_LSHIFT] or keys_pressed[pygame.K_RSHIFT]
        
        # Simulate touch detection
        was_touching = self.is_touching
        self.is_touching = mouse_in_sensor and (space_pressed or shift_pressed)
        
        if self.is_touching:
            self.touch_duration += 1
            self.sensor_quality = min(100, self.touch_duration / 2)
        else:
            self.touch_duration = max(0, self.touch_duration - 2)
            self.sensor_quality = max(0, self.sensor_quality - 1)
        
        return self.is_touching
    
    def update_vitals(self, stress_factor=0, is_lying=False):
        """Update vital signs based on touch and stress"""
        if not self.is_touching:
            # Gradually return to baseline when not touching
            self.heart_rate += (self.baseline_heart_rate - self.heart_rate) * 0.1
            self.blood_pressure += (self.baseline_pressure - self.blood_pressure) * 0.1
            self.sweat_level *= 0.95
            self.stress_level *= 0.9
            return
        
        # Natural fluctuations
        self.heart_rate += random.uniform(-2, 2)
        self.blood_pressure += random.uniform(-3, 3)
        self.respiration_rate += random.uniform(-1, 1)
        
        # Stress and lie detection effects
        if is_lying:
            self.heart_rate += random.uniform(8, 20)
            self.blood_pressure += random.uniform(15, 30)
            self.sweat_level = min(100, self.sweat_level + random.uniform(8, 20))
            self.respiration_rate += random.uniform(3, 8)
            self.stress_level = min(100, self.stress_level + random.uniform(15, 30))
        else:
            self.heart_rate += random.uniform(-3, 5)
            self.blood_pressure += random.uniform(-5, 5)
            self.sweat_level = max(0, self.sweat_level - random.uniform(0, 8))
            self.stress_level = max(0, self.stress_level - random.uniform(0, 10))
        
        # Add stress factor
        self.heart_rate += stress_factor * random.uniform(2, 8)
        self.blood_pressure += stress_factor * random.uniform(3, 12)
        
        # Clamp values
        self.heart_rate = max(50, min(120, self.heart_rate))
        self.blood_pressure = max(90, min(180, self.blood_pressure))
        self.respiration_rate = max(10, min(30, self.respiration_rate))
        self.sweat_level = max(0, min(100, self.sweat_level))
        self.stress_level = max(0, min(100, self.stress_level))
    
    def calibrate(self):
        """Calibrate baseline vital signs"""
        if self.is_touching and self.touch_duration > 120:  # 2 seconds of touch
            if not self.calibrated:
                self.baseline_heart_rate = self.heart_rate
                self.baseline_pressure = self.blood_pressure
                self.calibrated = True
                return True
        return False

class Question:
    def __init__(self, text, is_truth, difficulty=1):
        self.text = text
        self.is_truth = is_truth
        self.difficulty = difficulty
        self.player_answer = None
        self.analysis_complete = False

class RealLieDetector:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("REAL BIOMETRIC LIE DETECTOR - TOUCH SENSING")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = GameState.MENU
        
        # Fonts
        self.font_small = pygame.font.Font(None, 24)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_large = pygame.font.Font(None, 48)
        self.font_huge = pygame.font.Font(None, 72)
        
        # Game variables
        self.current_question = None
        self.questions_asked = 0
        self.correct_detections = 0
        self.total_questions = 10
        self.score = 0
        
        # Biometric sensor
        self.sensor = BiometricSensor()
        
        # Animation variables
        self.animation_timer = 0
        self.pulse_animation = 0
        self.graph_data = []
        self.max_graph_points = 100
        
        # Questions database
        self.question_database = self.create_question_database()
        self.used_questions = []
        
        # Visual effects
        self.screen_flash = 0
        self.result_revealed = False
        self.confidence_meter = 0
        self.calibration_complete = False
        
    def create_question_database(self):
        """Create a database of questions with truth/lie values"""
        questions = [
            # Easy questions
            ("The sky is blue during the day", True, 1),
            ("2 + 2 equals 5", False, 1),
            ("Water freezes at 0 degrees Celsius", True, 1),
            ("Dogs have the ability to fly", False, 1),
            ("The sun rises in the east", True, 1),
            ("Fish live in trees and branches", False, 1),
            ("Ice melts when heated", True, 1),
            ("Birds are mammals that lay eggs", False, 1),
            
            # Medium questions
            ("The capital of Japan is Tokyo", True, 2),
            ("Humans have four chambers in their heart", True, 2),
            ("The Great Wall of China is over 13,000 miles long", True, 2),
            ("Spiders have six legs like insects", False, 2),
            ("Light travels at approximately 186,000 miles per second", True, 2),
            ("Diamonds are formed from compressed coal", False, 2),
            ("The first man on the moon was Neil Armstrong in 1969", True, 2),
            ("Goldfish can remember things for only 3 seconds", False, 2),
            
            # Hard questions
            ("The human body contains exactly 206 bones in adulthood", True, 3),
            ("Octopuses have three hearts and blue blood", True, 3),
            ("A group of crows is called a 'murder'", True, 3),
            ("The shortest war in history lasted only 38 minutes", True, 3),
            ("Bananas are botanically classified as berries", True, 3),
            ("The first computer bug was an actual insect found in a Harvard Mark II", True, 3),
            ("Venus rotates clockwise while most planets rotate counterclockwise", True, 3),
            ("Honey has an indefinite shelf life and never spoils", True, 3),
        ]
        
        return questions
    
    def get_random_question(self):
        """Get a random question that hasn't been used"""
        available_questions = [q for q in self.question_database if q not in self.used_questions]
        
        if not available_questions:
            self.used_questions = []
            available_questions = self.question_database
        
        question_tuple = random.choice(available_questions)
        question = Question(question_tuple[0], question_tuple[1], question_tuple[2])
        self.used_questions.append(question_tuple)
        
        return question
    
    def update_biometric_graph(self):
        """Update the biometric data graph"""
        if self.sensor.is_touching:
            self.graph_data.append(self.sensor.heart_rate)
        else:
            self.graph_data.append(0)
        
        if len(self.graph_data) > self.max_graph_points:
            self.graph_data.pop(0)
    
    def analyze_response(self, player_said_truth):
        """Analyze player's response using real biometric data"""
        if not self.current_question:
            return False
        
        self.current_question.player_answer = player_said_truth
        actual_truth = self.current_question.is_truth
        
        # Calculate confidence based on sensor quality and biometric readings
        base_confidence = 60
        sensor_bonus = self.sensor.sensor_quality * 0.3
        stress_penalty = self.sensor.stress_level * 0.15
        
        self.confidence_meter = max(25, min(95, base_confidence + sensor_bonus - stress_penalty))
        
        # Analyze heart rate variation
        heart_rate_variation = abs(self.sensor.heart_rate - self.sensor.baseline_heart_rate)
        if heart_rate_variation > 15:
            self.confidence_meter -= 10
        
        # Add some randomness for realism
        confidence_variation = random.uniform(-8, 8)
        self.confidence_meter = max(20, min(99, self.confidence_meter + confidence_variation))
        
        # Determine if player was correct
        player_correct = (player_said_truth == actual_truth)
        
        # Add error based on confidence and sensor quality
        error_chance = (100 - self.confidence_meter + (100 - self.sensor.sensor_quality)) / 200
        if random.random() < error_chance:
            player_correct = not player_correct
        
        return player_correct
    
    def draw_touch_sensor(self):
        """Draw the touch sensor interface"""
        # Sensor area
        sensor_rect = pygame.Rect(500, 300, 200, 200)
        
        # Color based on touch status
        if self.sensor.is_touching:
            if self.sensor.sensor_quality > 80:
                sensor_color = GREEN
                status_text = "EXCELLENT CONTACT"
            elif self.sensor.sensor_quality > 50:
                sensor_color = YELLOW
                status_text = "GOOD CONTACT"
            else:
                sensor_color = ORANGE
                status_text = "POOR CONTACT"
        else:
            sensor_color = RED
            status_text = "NO CONTACT - PLACE HANDS HERE"
        
        # Draw sensor with pulse effect
        pulse = abs(math.sin(self.animation_timer * 0.1)) * 10
        pulse_rect = pygame.Rect(sensor_rect.x - pulse, sensor_rect.y - pulse, 
                                sensor_rect.width + pulse * 2, sensor_rect.height + pulse * 2)
        pygame.draw.rect(self.screen, (*sensor_color, 50), pulse_rect)
        
        pygame.draw.rect(self.screen, sensor_color, sensor_rect, 3)
        
        # Draw hand icon
        if self.sensor.is_touching:
            # Draw handprint effect
            for i in range(5):
                x = 550 + i * 25
                y = 350 + math.sin(self.animation_timer * 0.05 + i) * 5
                pygame.draw.circle(self.screen, WHITE, (x, y), 8)
            pygame.draw.circle(self.screen, WHITE, (600, 400), 15)
        else:
            # Draw instruction
            inst_text = self.font_small.render("TOUCH HERE", True, WHITE)
            inst_rect = inst_text.get_rect(center=(600, 400))
            self.screen.blit(inst_text, inst_rect)
        
        # Status text
        status = self.font_medium.render(status_text, True, sensor_color)
        status_rect = status.get_rect(center=(600, 520))
        self.screen.blit(status, status_rect)
        
        # Sensor quality meter
        quality_text = self.font_small.render(f"Sensor Quality: {self.sensor.sensor_quality:.0f}%", True, WHITE)
        quality_rect = quality_text.get_rect(center=(600, 550))
        self.screen.blit(quality_text, quality_rect)
    
    def draw_biometric_monitors(self):
        """Draw all biometric monitoring displays"""
        # Heart Rate Monitor
        self.draw_vital_monitor("HEART RATE", 50, 100, self.sensor.heart_rate, "BPM", RED)
        
        # Blood Pressure Monitor
        self.draw_vital_monitor("BLOOD PRESSURE", 50, 170, self.sensor.blood_pressure, "SYS", ORANGE)
        
        # Respiration Monitor
        self.draw_vital_monitor("RESPIRATION", 50, 240, self.sensor.respiration_rate, "BPM", GREEN)
        
        # Sweat Level Monitor
        self.draw_vital_monitor("SWEAT LEVEL", 50, 310, self.sensor.sweat_level, "%", YELLOW)
        
        # Temperature Monitor
        self.draw_vital_monitor("TEMPERATURE", 50, 380, self.sensor.temperature, "°F", CYAN)
        
        # Stress Level Meter
        self.draw_stress_meter(50, 450, 400, 100)
        
        # ECG Graph
        self.draw_ecg_graph(750, 100, 400, 150)
        
        # Touch Sensor
        self.draw_touch_sensor()
    
    def draw_vital_monitor(self, label, x, y, value, unit, color):
        """Draw a vital sign monitor"""
        # Monitor background
        monitor_rect = pygame.Rect(x, y, 400, 50)
        pygame.draw.rect(self.screen, BLACK, monitor_rect)
        pygame.draw.rect(self.screen, color, monitor_rect, 2)
        
        # Label
        label_text = self.font_small.render(label, True, color)
        self.screen.blit(label_text, (x + 5, y + 5))
        
        # Value with animation
        if self.sensor.is_touching:
            value_color = WHITE
            # Add pulsing effect
            pulse = abs(math.sin(self.animation_timer * 0.1 + value * 0.1)) * 2
            display_value = value + pulse
        else:
            value_color = GRAY
            display_value = value
        
        value_text = self.font_medium.render(f"{display_value:.0f} {unit}", True, value_color)
        self.screen.blit(value_text, (x + 250, y + 10))
        
        # Warning indicators
        if label == "HEART RATE" and value > 90:
            pygame.draw.circle(self.screen, RED, (x + 380, y + 25), 5)
        elif label == "BLOOD PRESSURE" and value > 140:
            pygame.draw.circle(self.screen, RED, (x + 380, y + 25), 5)
        elif label == "SWEAT LEVEL" and value > 70:
            pygame.draw.circle(self.screen, RED, (x + 380, y + 25), 5)
    
    def draw_ecg_graph(self, x, y, width, height):
        """Draw ECG/EKG graph"""
        # Graph background
        graph_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, BLACK, graph_rect)
        pygame.draw.rect(self.screen, GREEN, graph_rect, 2)
        
        # Grid lines
        for i in range(0, width, 40):
            pygame.draw.line(self.screen, DARK_GRAY, (x + i, y), (x + i, y + height), 1)
        for i in range(0, height, 30):
            pygame.draw.line(self.screen, DARK_GRAY, (x, y + i), (x + width, y + i), 1)
        
        # ECG line
        if len(self.graph_data) > 1:
            points = []
            for i, value in enumerate(self.graph_data):
                if value > 0:  # Only draw if sensor is touching
                    point_x = x + (i * width // self.max_graph_points)
                    point_y = y + height - ((value - 50) * height // 70)
                    points.append((point_x, point_y))
                else:
                    # Draw flat line when not touching
                    point_x = x + (i * width // self.max_graph_points)
                    point_y = y + height // 2
                    points.append((point_x, point_y))
            
            if len(points) > 1:
                pygame.draw.lines(self.screen, GREEN, False, points, 2)
        
        # Title
        title = self.font_small.render("HEART RATE VARIABILITY", True, GREEN)
        title_rect = title.get_rect(center=(x + width // 2, y - 10))
        self.screen.blit(title, title_rect)
        
        # Connection status
        if self.sensor.is_touching:
            status_text = "CONNECTED"
            status_color = GREEN
        else:
            status_text = "NO SIGNAL"
            status_color = RED
        
        status = self.font_small.render(status_text, True, status_color)
        status_rect = status.get_rect(center=(x + width // 2, y + height + 15))
        self.screen.blit(status, status_rect)
    
    def draw_stress_meter(self, x, y, width, height):
        """Draw stress level meter"""
        # Meter background
        meter_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, BLACK, meter_rect)
        pygame.draw.rect(self.screen, RED, meter_rect, 2)
        
        # Stress level bar
        stress_width = int((self.sensor.stress_level / 100) * (width - 20))
        stress_rect = pygame.Rect(x + 10, y + 40, stress_width, height - 80)
        
        # Color based on stress level
        if self.sensor.stress_level < 30:
            stress_color = GREEN
        elif self.sensor.stress_level < 60:
            stress_color = YELLOW
        else:
            stress_color = RED
        
        pygame.draw.rect(self.screen, stress_color, stress_rect)
        
        # Title
        title = self.font_medium.render("STRESS LEVEL", True, WHITE)
        title_rect = title.get_rect(center=(x + width // 2, y + 20))
        self.screen.blit(title, title_rect)
        
        # Percentage
        percent_text = self.font_large.render(f"{self.sensor.stress_level:.0f}%", True, WHITE)
        percent_rect = percent_text.get_rect(center=(x + width // 2, y + height // 2))
        self.screen.blit(percent_text, percent_rect)
    
    def draw_calibration_screen(self):
        """Draw calibration screen"""
        self.screen.fill(BLACK)
        
        # Title
        title = self.font_huge.render("BIOMETRIC CALIBRATION", True, CYAN)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.screen.blit(title, title_rect)
        
        # Instructions
        instructions = [
            "Place your hands on the sensor area",
            "Hold SPACE or SHIFT while touching",
            "Keep your hands steady for 5 seconds",
            "This will establish your baseline vital signs"
        ]
        
        y_offset = 200
        for instruction in instructions:
            inst_text = self.font_medium.render(instruction, True, WHITE)
            inst_rect = inst_text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
            self.screen.blit(inst_text, inst_rect)
            y_offset += 50
        
        # Draw biometric monitors
        self.draw_biometric_monitors()
        
        # Calibration status
        if self.sensor.calibrated:
            status_text = "CALIBRATION COMPLETE!"
            status_color = GREEN
            next_text = "Press SPACE to begin"
        else:
            status_text = f"Calibrating... {self.sensor.touch_duration // 60}/5 seconds"
            status_color = YELLOW
            next_text = ""
        
        status = self.font_large.render(status_text, True, status_color)
        status_rect = status.get_rect(center=(SCREEN_WIDTH // 2, 600))
        self.screen.blit(status, status_rect)
        
        if next_text:
            next_inst = self.font_medium.render(next_text, True, WHITE)
            next_rect = next_inst.get_rect(center=(SCREEN_WIDTH // 2, 650))
            self.screen.blit(next_inst, next_rect)
    
    def draw_question_display(self):
        """Draw the current question"""
        if not self.current_question:
            return
        
        # Question box
        question_rect = pygame.Rect(100, 50, SCREEN_WIDTH - 200, 80)
        pygame.draw.rect(self.screen, DARK_GRAY, question_rect)
        pygame.draw.rect(self.screen, WHITE, question_rect, 3)
        
        # Question text
        question_text = self.font_large.render(self.current_question.text, True, WHITE)
        question_rect = question_text.get_rect(center=(SCREEN_WIDTH // 2, 90))
        self.screen.blit(question_text, question_rect)
        
        # Instructions
        if self.state == GameState.QUESTION:
            if self.sensor.is_touching:
                inst_text = self.font_medium.render("Press T for TRUTH or F for FALSE", True, GREEN)
            else:
                inst_text = self.font_medium.render("PLACE HANDS ON SENSOR TO ANSWER", True, RED)
            inst_rect = inst_text.get_rect(center=(SCREEN_WIDTH // 2, 580))
            self.screen.blit(inst_text, inst_rect)
    
    def draw_menu(self):
        """Draw main menu"""
        self.screen.fill(BLACK)
        
        # Title
        title = self.font_huge.render("REAL BIOMETRIC", True, CYAN)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.screen.blit(title, title_rect)
        
        subtitle = self.font_huge.render("LIE DETECTOR", True, RED)
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, 180))
        self.screen.blit(subtitle, subtitle_rect)
        
        tagline = self.font_large.render("TOUCH-SENSING POLYGRAPH SYSTEM", True, WHITE)
        tagline_rect = tagline.get_rect(center=(SCREEN_WIDTH // 2, 250))
        self.screen.blit(tagline, tagline_rect)
        
        # Features
        features = [
            "REAL BIOMETRIC MONITORING",
            "TOUCH-SENSING TECHNOLOGY",
            "HEART RATE DETECTION",
            "STRESS LEVEL ANALYSIS",
            "PROFESSIONAL POLYGRAPH INTERFACE"
        ]
        
        y_offset = 320
        for feature in features:
            feature_text = self.font_medium.render(feature, True, YELLOW)
            feature_rect = feature_text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
            self.screen.blit(feature_text, feature_rect)
            y_offset += 40
        
        # Instructions
        inst_text = self.font_medium.render("Press SPACE to begin calibration", True, WHITE)
        inst_rect = inst_text.get_rect(center=(SCREEN_WIDTH // 2, 550))
        self.screen.blit(inst_text, inst_rect)
        
        quit_text = self.font_small.render("Press ESC to quit", True, GRAY)
        quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH // 2, 600))
        self.screen.blit(quit_text, quit_rect)
    
    def draw_game_ui(self):
        """Draw game UI elements"""
        # Score
        score_text = self.font_medium.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # Questions remaining
        questions_text = self.font_medium.render(f"Questions: {self.questions_asked}/{self.total_questions}", True, WHITE)
        self.screen.blit(questions_text, (10, 50))
        
        # Accuracy
        if self.questions_asked > 0:
            accuracy = (self.correct_detections / self.questions_asked) * 100
            accuracy_text = self.font_medium.render(f"Accuracy: {accuracy:.1f}%", True, WHITE)
            self.screen.blit(accuracy_text, (10, 90))
        
        # Sensor status
        if self.sensor.is_touching:
            sensor_status = "SENSOR ACTIVE"
            sensor_color = GREEN
        else:
            sensor_status = "SENSOR INACTIVE"
            sensor_color = RED
        
        sensor_text = self.font_medium.render(sensor_status, True, sensor_color)
        self.screen.blit(sensor_text, (SCREEN_WIDTH - 200, 10))
    
    def handle_events(self):
        """Handle game events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.state == GameState.MENU:
                        self.running = False
                    else:
                        self.state = GameState.MENU
                        self.reset_game()
                
                elif event.key == pygame.K_SPACE:
                    if self.state == GameState.MENU:
                        self.state = GameState.CALIBRATION
                    elif self.state == GameState.CALIBRATION and self.sensor.calibrated:
                        self.state = GameState.PLAYING
                        self.start_new_question()
                    elif self.state == GameState.RESULT:
                        if self.questions_asked < self.total_questions:
                            self.start_new_question()
                        else:
                            self.state = GameState.GAME_OVER
                    elif self.state == GameState.GAME_OVER:
                        self.reset_game()
                        self.state = GameState.MENU
                
                elif event.key == pygame.K_t:
                    if self.state == GameState.QUESTION and self.sensor.is_touching:
                        self.process_answer(True)
                
                elif event.key == pygame.K_f:
                    if self.state == GameState.QUESTION and self.sensor.is_touching:
                        self.process_answer(False)
    
    def start_new_question(self):
        """Start a new question"""
        self.current_question = self.get_random_question()
        self.state = GameState.QUESTION
        self.sensor.stress_level = random.uniform(10, 30)
        self.result_revealed = False
        self.confidence_meter = 0
    
    def process_answer(self, player_said_truth):
        """Process player's answer"""
        if not self.current_question:
            return
        
        self.state = GameState.ANALYSIS
        self.current_question.analysis_complete = True
        
        # Simulate lie during analysis
        is_lying = (player_said_truth != self.current_question.is_truth)
        
        # Update vitals based on whether they're lying
        for _ in range(60):  # 1 second of analysis
            self.sensor.update_vitals(self.current_question.difficulty * 10, is_lying)
        
        # Analyze the response
        player_correct = self.analyze_response(player_said_truth)
        
        # Update score
        if player_correct:
            self.correct_detections += 1
            self.score += 100 * self.current_question.difficulty
        
        self.questions_asked += 1
        
        # Switch to result after analysis
        pygame.time.wait(2000)
        self.state = GameState.RESULT
    
    def reset_game(self):
        """Reset game state"""
        self.current_question = None
        self.questions_asked = 0
        self.correct_detections = 0
        self.score = 0
        self.used_questions = []
        self.graph_data = []
        self.sensor = BiometricSensor()
        self.calibration_complete = False
    
    def update(self):
        """Update game state"""
        self.animation_timer += 1
        self.pulse_animation = math.sin(self.animation_timer * 0.1) * 10
        
        # Get mouse position and keys
        mouse_pos = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()
        
        # Update sensor
        self.sensor.detect_touch(mouse_pos, keys)
        
        # Update vitals
        if self.state in [GameState.PLAYING, GameState.QUESTION]:
            self.sensor.update_vitals()
        
        # Update graph
        self.update_biometric_graph()
        
        # Handle calibration
        if self.state == GameState.CALIBRATION:
            if self.sensor.calibrate():
                self.calibration_complete = True
        
        # Handle screen flash
        if self.screen_flash > 0:
            self.screen_flash -= 1
    
    def draw(self):
        """Draw everything"""
        if self.state == GameState.MENU:
            self.draw_menu()
        elif self.state == GameState.CALIBRATION:
            self.draw_calibration_screen()
        else:
            self.screen.fill(BLACK)
            
            # Draw biometric monitors
            self.draw_biometric_monitors()
            
            # Draw question if in question state
            if self.state == GameState.QUESTION:
                self.draw_question_display()
            elif self.state == GameState.ANALYSIS:
                # Draw analysis screen
                analysis_rect = pygame.Rect(200, 200, SCREEN_WIDTH - 400, 300)
                pygame.draw.rect(self.screen, DARK_GRAY, analysis_rect)
                pygame.draw.rect(self.screen, YELLOW, analysis_rect, 3)
                
                analysis_text = self.font_large.render("ANALYZING BIOMETRIC DATA...", True, YELLOW)
                analysis_rect = analysis_text.get_rect(center=(SCREEN_WIDTH // 2, 300))
                self.screen.blit(analysis_text, analysis_rect)
                
                # Loading animation
                for i in range(5):
                    x = SCREEN_WIDTH // 2 - 100 + i * 50
                    y = 350
                    size = 10 + abs(math.sin(self.animation_timer * 0.1 + i) * 5)
                    pygame.draw.circle(self.screen, YELLOW, (x, y), int(size))
                
                confidence_text = self.font_medium.render(f"Confidence: {self.confidence_meter:.0f}%", True, WHITE)
                confidence_rect = confidence_text.get_rect(center=(SCREEN_WIDTH // 2, 400))
                self.screen.blit(confidence_text, confidence_rect)
                
            elif self.state == GameState.RESULT:
                # Draw result screen
                if self.current_question:
                    result_rect = pygame.Rect(200, 200, SCREEN_WIDTH - 400, 300)
                    
                    if self.current_question.player_answer == self.current_question.is_truth:
                        result_color = GREEN
                        result_text = "CORRECT DETECTION!"
                        explanation = f"The statement was {'TRUE' if self.current_question.is_truth else 'FALSE'}"
                    else:
                        result_color = RED
                        result_text = "INCORRECT DETECTION!"
                        explanation = f"The statement was {'TRUE' if self.current_question.is_truth else 'FALSE'}"
                    
                    pygame.draw.rect(self.screen, DARK_GRAY, result_rect)
                    pygame.draw.rect(self.screen, result_color, result_rect, 3)
                    
                    result_display = self.font_huge.render(result_text, True, result_color)
                    result_display_rect = result_display.get_rect(center=(SCREEN_WIDTH // 2, 280))
                    self.screen.blit(result_display, result_display_rect)
                    
                    explanation_text = self.font_medium.render(explanation, True, WHITE)
                    explanation_rect = explanation_text.get_rect(center=(SCREEN_WIDTH // 2, 350))
                    self.screen.blit(explanation_text, explanation_rect)
                    
                    confidence_text = self.font_medium.render(f"Confidence: {self.confidence_meter:.0f}%", True, WHITE)
                    confidence_rect = confidence_text.get_rect(center=(SCREEN_WIDTH // 2, 400))
                    self.screen.blit(confidence_text, confidence_rect)
                    
                    continue_text = self.font_small.render("Press SPACE to continue", True, WHITE)
                    continue_rect = continue_text.get_rect(center=(SCREEN_WIDTH // 2, 450))
                    self.screen.blit(continue_text, continue_rect)
            
            elif self.state == GameState.GAME_OVER:
                # Draw game over screen
                if self.questions_asked > 0:
                    final_accuracy = (self.correct_detections / self.questions_asked) * 100
                else:
                    final_accuracy = 0
                
                title = self.font_huge.render("ANALYSIS COMPLETE", True, YELLOW)
                title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 150))
                self.screen.blit(title, title_rect)
                
                results = [
                    f"Final Score: {self.score}",
                    f"Questions Analyzed: {self.questions_asked}",
                    f"Correct Detections: {self.correct_detections}",
                    f"Accuracy: {final_accuracy:.1f}%"
                ]
                
                y_offset = 250
                for result in results:
                    result_text = self.font_large.render(result, True, WHITE)
                    result_rect = result_text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
                    self.screen.blit(result_text, result_rect)
                    y_offset += 60
                
                # Performance rating
                if final_accuracy >= 80:
                    rating = "EXPERT DETECTIVE!"
                    rating_color = GREEN
                elif final_accuracy >= 60:
                    rating = "SKILLED ANALYST!"
                    rating_color = YELLOW
                elif final_accuracy >= 40:
                    rating = "DEVELOPING DETECTIVE!"
                    rating_color = ORANGE
                else:
                    rating = "NEEDS TRAINING!"
                    rating_color = RED
                
                rating_text = self.font_huge.render(rating, True, rating_color)
                rating_rect = rating_text.get_rect(center=(SCREEN_WIDTH // 2, 500))
                self.screen.blit(rating_text, rating_rect)
                
                continue_text = self.font_medium.render("Press SPACE to play again or ESC to quit", True, WHITE)
                continue_rect = continue_text.get_rect(center=(SCREEN_WIDTH // 2, 580))
                self.screen.blit(continue_text, continue_rect)
            
            # Draw UI
            if self.state != GameState.GAME_OVER:
                self.draw_game_ui()
        
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()

def main():
    """Main function"""
    game = RealLieDetector()
    game.run()

if __name__ == "__main__":
    main()
