#!/usr/bin/env python3
"""
PROFESSIONAL LIE DETECTOR GAME
A realistic lie detection simulation game with advanced polygraph mechanics
"""

import pygame
import random
import math
import time
from enum import Enum

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

# Game States
class GameState(Enum):
    MENU = "menu"
    PLAYING = "playing"
    QUESTION = "question"
    ANALYSIS = "analysis"
    RESULT = "result"
    GAME_OVER = "game_over"

class Question:
    def __init__(self, text, is_truth, difficulty=1):
        self.text = text
        self.is_truth = is_truth
        self.difficulty = difficulty
        self.player_answer = None
        self.analysis_complete = False
        
class LieDetector:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("PROFESSIONAL LIE DETECTOR - POLYGRAPH SIMULATION")
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
        
        # Polygraph readings
        self.heart_rate = 70  # BPM
        self.blood_pressure = 120  # Systolic
        self.sweat_level = 0  # 0-100
        self.respiration_rate = 16  # Breaths per minute
        self.stress_level = 0  # 0-100
        
        # Animation variables
        self.animation_timer = 0
        self.pulse_animation = 0
        self.needle_animation = 0
        self.graph_data = []
        self.max_graph_points = 100
        
        # Questions database
        self.question_database = self.create_question_database()
        self.used_questions = []
        
        # Visual effects
        self.screen_flash = 0
        self.result_revealed = False
        self.confidence_meter = 0
        
    def create_question_database(self):
        """Create a database of questions with truth/lie values"""
        questions = [
            # Easy questions
            ("The sky is blue", True, 1),
            ("2 + 2 = 5", False, 1),
            ("Water is wet", True, 1),
            ("Dogs can fly", False, 1),
            ("The sun is hot", True, 1),
            ("Fish live in trees", False, 1),
            ("Ice is cold", True, 1),
            ("Birds swim underwater", False, 1),
            
            # Medium questions
            ("The capital of France is Paris", True, 2),
            ("Humans have three lungs", False, 2),
            ("The Earth orbits the Sun", True, 2),
            ("Spiders are insects", False, 2),
            ("Light travels faster than sound", True, 2),
            ("Diamonds are the hardest natural substance", True, 2),
            ("The Great Wall of China is visible from space", False, 2),
            ("Goldfish have a 3-second memory", False, 2),
            
            # Hard questions
            ("The human body has 206 bones", True, 3),
            ("Octopuses have three hearts", True, 3),
            ("A group of crows is called a murder", True, 3),
            ("The shortest war in history lasted 38 minutes", True, 3),
            ("Bananas are berries, but strawberries aren't", True, 3),
            ("The first computer bug was an actual bug", True, 3),
            ("Venus rotates backwards compared to most planets", True, 3),
            ("Honey never spoils", True, 3),
        ]
        
        return questions
    
    def get_random_question(self):
        """Get a random question that hasn't been used"""
        available_questions = [q for q in self.question_database if q not in self.used_questions]
        
        if not available_questions:
            # Reset used questions if all have been used
            self.used_questions = []
            available_questions = self.question_database
        
        question_tuple = random.choice(available_questions)
        question = Question(question_tuple[0], question_tuple[1], question_tuple[2])
        self.used_questions.append(question_tuple)
        
        return question
    
    def update_polygraph_readings(self):
        """Update polygraph readings based on current state"""
        # Base readings fluctuate naturally
        self.heart_rate += random.uniform(-2, 2)
        self.heart_rate = max(60, min(100, self.heart_rate))
        
        self.blood_pressure += random.uniform(-3, 3)
        self.blood_pressure = max(100, min(160, self.blood_pressure))
        
        self.respiration_rate += random.uniform(-1, 1)
        self.respiration_rate = max(12, min(24, self.respiration_rate))
        
        # Add stress based on question difficulty
        if self.current_question and not self.current_question.analysis_complete:
            difficulty_stress = self.current_question.difficulty * 10
            self.stress_level = min(100, self.stress_level + random.uniform(0, difficulty_stress))
            
            # Lie detection affects readings
            if not self.current_question.is_truth:
                # Lies cause more stress
                self.heart_rate += random.uniform(5, 15)
                self.blood_pressure += random.uniform(10, 25)
                self.sweat_level = min(100, self.sweat_level + random.uniform(5, 15))
                self.respiration_rate += random.uniform(2, 6)
            else:
                # Truth causes less stress
                self.heart_rate += random.uniform(-5, 5)
                self.blood_pressure += random.uniform(-5, 5)
                self.sweat_level = max(0, self.sweat_level - random.uniform(0, 5))
        
        # Natural decay of stress
        self.stress_level = max(0, self.stress_level - random.uniform(0, 2))
        self.sweat_level = max(0, self.sweat_level - random.uniform(0, 1))
        
        # Update graph data
        self.graph_data.append(self.heart_rate)
        if len(self.graph_data) > self.max_graph_points:
            self.graph_data.pop(0)
    
    def analyze_response(self, player_said_truth):
        """Analyze player's response and determine if they were correct"""
        if not self.current_question:
            return False
        
        self.current_question.player_answer = player_said_truth
        actual_truth = self.current_question.is_truth
        
        # Calculate confidence based on polygraph readings
        base_confidence = 70  # Base accuracy
        
        # Stress affects confidence
        stress_penalty = self.stress_level * 0.2
        self.confidence_meter = max(30, min(95, base_confidence - stress_penalty))
        
        # Add some randomness for realism
        confidence_variation = random.uniform(-10, 10)
        self.confidence_meter = max(20, min(99, self.confidence_meter + confidence_variation))
        
        # Determine if player was correct
        player_correct = (player_said_truth == actual_truth)
        
        # Add some error based on confidence
        if random.randint(1, 100) > self.confidence_meter:
            player_correct = not player_correct
        
        return player_correct
    
    def draw_polygraph_machine(self):
        """Draw the polygraph machine interface"""
        # Machine background
        machine_rect = pygame.Rect(50, 150, 400, 400)
        pygame.draw.rect(self.screen, DARK_GRAY, machine_rect)
        pygame.draw.rect(self.screen, WHITE, machine_rect, 3)
        
        # Title
        title = self.font_medium.render("POLYGRAPH SYSTEM", True, CYAN)
        title_rect = title.get_rect(center=(250, 180))
        self.screen.blit(title, title_rect)
        
        # Heart rate monitor
        self.draw_vital_monitor("HEART RATE", 70, 220, self.heart_rate, "BPM", RED)
        
        # Blood pressure monitor
        self.draw_vital_monitor("BLOOD PRESSURE", 70, 290, self.blood_pressure, "SYS", ORANGE)
        
        # Respiration monitor
        self.draw_vital_monitor("RESPIRATION", 70, 360, self.respiration_rate, "BPM", GREEN)
        
        # Sweat level monitor
        self.draw_vital_monitor("SWEAT LEVEL", 70, 430, self.sweat_level, "%", YELLOW)
        
        # ECG/EKG graph
        self.draw_ecg_graph(470, 150, 680, 200)
        
        # Stress meter
        self.draw_stress_meter(470, 370, 680, 180)
    
    def draw_vital_monitor(self, label, x, y, value, unit, color):
        """Draw a vital sign monitor"""
        # Monitor background
        monitor_rect = pygame.Rect(x, y, 320, 50)
        pygame.draw.rect(self.screen, BLACK, monitor_rect)
        pygame.draw.rect(self.screen, color, monitor_rect, 2)
        
        # Label
        label_text = self.font_small.render(label, True, color)
        self.screen.blit(label_text, (x + 5, y + 5))
        
        # Value
        value_text = self.font_medium.render(f"{value:.0f} {unit}", True, WHITE)
        self.screen.blit(value_text, (x + 200, y + 10))
        
        # Warning indicator
        if value > 90 and unit == "BPM":
            pygame.draw.circle(self.screen, RED, (x + 300, y + 25), 5)
        elif value > 140 and unit == "SYS":
            pygame.draw.circle(self.screen, RED, (x + 300, y + 25), 5)
    
    def draw_ecg_graph(self, x, y, width, height):
        """Draw ECG/EKG graph"""
        # Graph background
        graph_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, BLACK, graph_rect)
        pygame.draw.rect(self.screen, GREEN, graph_rect, 2)
        
        # Grid lines
        for i in range(0, width, 40):
            pygame.draw.line(self.screen, DARK_GRAY, (x + i, y), (x + i, y + height), 1)
        for i in range(0, height, 40):
            pygame.draw.line(self.screen, DARK_GRAY, (x, y + i), (x + width, y + i), 1)
        
        # ECG line
        if len(self.graph_data) > 1:
            points = []
            for i, value in enumerate(self.graph_data):
                point_x = x + (i * width // self.max_graph_points)
                point_y = y + height - ((value - 60) * height // 40)
                points.append((point_x, point_y))
            
            pygame.draw.lines(self.screen, GREEN, False, points, 2)
        
        # Title
        title = self.font_small.render("HEART RATE VARIABILITY", True, GREEN)
        title_rect = title.get_rect(center=(x + width // 2, y - 10))
        self.screen.blit(title, title_rect)
    
    def draw_stress_meter(self, x, y, width, height):
        """Draw stress level meter"""
        # Meter background
        meter_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, BLACK, meter_rect)
        pygame.draw.rect(self.screen, RED, meter_rect, 2)
        
        # Stress level bar
        stress_width = int((self.stress_level / 100) * (width - 20))
        stress_rect = pygame.Rect(x + 10, y + 40, stress_width, height - 80)
        
        # Color based on stress level
        if self.stress_level < 30:
            stress_color = GREEN
        elif self.stress_level < 60:
            stress_color = YELLOW
        else:
            stress_color = RED
        
        pygame.draw.rect(self.screen, stress_color, stress_rect)
        
        # Title
        title = self.font_medium.render("STRESS LEVEL", True, WHITE)
        title_rect = title.get_rect(center=(x + width // 2, y + 20))
        self.screen.blit(title, title_rect)
        
        # Percentage
        percent_text = self.font_large.render(f"{self.stress_level:.0f}%", True, WHITE)
        percent_rect = percent_text.get_rect(center=(x + width // 2, y + height // 2))
        self.screen.blit(percent_text, percent_rect)
    
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
            inst_text = self.font_medium.render("Press T for TRUTH or F for FALSE", True, YELLOW)
            inst_rect = inst_text.get_rect(center=(SCREEN_WIDTH // 2, 580))
            self.screen.blit(inst_text, inst_rect)
    
    def draw_analysis_screen(self):
        """Draw the analysis screen"""
        # Analysis background
        analysis_rect = pygame.Rect(200, 200, SCREEN_WIDTH - 400, 300)
        pygame.draw.rect(self.screen, DARK_GRAY, analysis_rect)
        pygame.draw.rect(self.screen, YELLOW, analysis_rect, 3)
        
        # Analysis text
        analysis_text = self.font_large.render("ANALYZING RESPONSE...", True, YELLOW)
        analysis_rect = analysis_text.get_rect(center=(SCREEN_WIDTH // 2, 300))
        self.screen.blit(analysis_text, analysis_rect)
        
        # Loading animation
        for i in range(5):
            x = SCREEN_WIDTH // 2 - 100 + i * 50
            y = 350
            size = 10 + abs(math.sin(self.animation_timer * 0.1 + i) * 5)
            pygame.draw.circle(self.screen, YELLOW, (x, y), int(size))
        
        # Confidence meter
        confidence_text = self.font_medium.render(f"Confidence: {self.confidence_meter:.0f}%", True, WHITE)
        confidence_rect = confidence_text.get_rect(center=(SCREEN_WIDTH // 2, 400))
        self.screen.blit(confidence_text, confidence_rect)
    
    def draw_result_screen(self):
        """Draw the result screen"""
        if not self.current_question:
            return
        
        # Result background
        result_rect = pygame.Rect(200, 200, SCREEN_WIDTH - 400, 300)
        
        # Determine result
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
        
        # Result text
        result_display = self.font_huge.render(result_text, True, result_color)
        result_display_rect = result_display.get_rect(center=(SCREEN_WIDTH // 2, 280))
        self.screen.blit(result_display, result_display_rect)
        
        # Explanation
        explanation_text = self.font_medium.render(explanation, True, WHITE)
        explanation_rect = explanation_text.get_rect(center=(SCREEN_WIDTH // 2, 350))
        self.screen.blit(explanation_text, explanation_rect)
        
        # Confidence
        confidence_text = self.font_medium.render(f"Confidence: {self.confidence_meter:.0f}%", True, WHITE)
        confidence_rect = confidence_text.get_rect(center=(SCREEN_WIDTH // 2, 400))
        self.screen.blit(confidence_text, confidence_rect)
        
        # Continue instruction
        continue_text = self.font_small.render("Press SPACE to continue", True, WHITE)
        continue_rect = continue_text.get_rect(center=(SCREEN_WIDTH // 2, 450))
        self.screen.blit(continue_text, continue_rect)
    
    def draw_menu(self):
        """Draw main menu"""
        self.screen.fill(BLACK)
        
        # Title
        title = self.font_huge.render("LIE DETECTOR", True, RED)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(title, title_rect)
        
        subtitle = self.font_large.render("PROFESSIONAL POLYGRAPH SIMULATION", True, WHITE)
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, 220))
        self.screen.blit(subtitle, subtitle_rect)
        
        # Draw polygraph machine in background
        self.draw_polygraph_machine()
        
        # Instructions
        instructions = [
            "Test your lie detection skills!",
            "Analyze polygraph readings to detect truth or lies",
            "Press SPACE to start",
            "",
            "Controls:",
            "T - Mark as TRUTH",
            "F - Mark as FALSE",
            "ESC - Quit game"
        ]
        
        y_offset = 350
        for instruction in instructions:
            inst_text = self.font_medium.render(instruction, True, WHITE)
            inst_rect = inst_text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
            self.screen.blit(inst_text, inst_rect)
            y_offset += 40
    
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
    
    def draw_game_over(self):
        """Draw game over screen"""
        self.screen.fill(BLACK)
        
        # Calculate final accuracy
        if self.questions_asked > 0:
            final_accuracy = (self.correct_detections / self.questions_asked) * 100
        else:
            final_accuracy = 0
        
        # Title
        title = self.font_huge.render("ANALYSIS COMPLETE", True, YELLOW)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(title, title_rect)
        
        # Results
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
        
        # Continue instruction
        continue_text = self.font_medium.render("Press SPACE to play again or ESC to quit", True, WHITE)
        continue_rect = continue_text.get_rect(center=(SCREEN_WIDTH // 2, 580))
        self.screen.blit(continue_text, continue_rect)
    
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
                    if self.state == GameState.QUESTION:
                        self.process_answer(True)
                
                elif event.key == pygame.K_f:
                    if self.state == GameState.QUESTION:
                        self.process_answer(False)
    
    def start_new_question(self):
        """Start a new question"""
        self.current_question = self.get_random_question()
        self.state = GameState.QUESTION
        self.stress_level = random.uniform(10, 30)  # Base stress
        self.result_revealed = False
        self.confidence_meter = 0
    
    def process_answer(self, player_said_truth):
        """Process player's answer"""
        if not self.current_question:
            return
        
        self.state = GameState.ANALYSIS
        self.current_question.analysis_complete = True
        
        # Analyze the response
        player_correct = self.analyze_response(player_said_truth)
        
        # Update score
        if player_correct:
            self.correct_detections += 1
            self.score += 100 * self.current_question.difficulty
        
        self.questions_asked += 1
        
        # Switch to result after analysis
        pygame.time.wait(2000)  # Simulate analysis time
        self.state = GameState.RESULT
    
    def reset_game(self):
        """Reset game state"""
        self.current_question = None
        self.questions_asked = 0
        self.correct_detections = 0
        self.score = 0
        self.used_questions = []
        self.graph_data = []
        self.stress_level = 0
        self.confidence_meter = 0
    
    def update(self):
        """Update game state"""
        self.animation_timer += 1
        self.pulse_animation = math.sin(self.animation_timer * 0.1) * 10
        self.needle_animation = math.sin(self.animation_timer * 0.2) * 5
        
        # Update polygraph readings
        if self.state in [GameState.PLAYING, GameState.QUESTION]:
            self.update_polygraph_readings()
        
        # Handle screen flash
        if self.screen_flash > 0:
            self.screen_flash -= 1
    
    def draw(self):
        """Draw everything"""
        self.screen.fill(BLACK)
        
        if self.state == GameState.MENU:
            self.draw_menu()
        else:
            # Draw polygraph machine
            self.draw_polygraph_machine()
            
            # Draw question if in question state
            if self.state == GameState.QUESTION:
                self.draw_question_display()
            elif self.state == GameState.ANALYSIS:
                self.draw_analysis_screen()
            elif self.state == GameState.RESULT:
                self.draw_result_screen()
            elif self.state == GameState.GAME_OVER:
                self.draw_game_over()
            
            # Draw UI
            if self.state != GameState.GAME_OVER:
                self.draw_game_ui()
        
        # Screen flash effect
        if self.screen_flash > 0:
            flash_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            flash_surface.set_alpha(self.screen_flash * 5)
            flash_surface.fill(WHITE)
            self.screen.blit(flash_surface, (0, 0))
        
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
    game = LieDetector()
    game.run()

if __name__ == "__main__":
    main()
