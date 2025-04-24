# config.py
import os
from datetime import datetime
import pygame
import cv2

SKIN = "skin/italien"
# --- Dimensions écran
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 853

# --- Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
GREEN = (0, 255, 0)
BLUE = (0, 100, 255)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
PURPLE = (160, 32, 240)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
PINK = (255, 105, 180)
NAVY = (0, 0, 128)
SMOKE_COLOR = (100, 100, 100)

# --- Gameplay
TIME_SCALE = 0.45
TOP_BOX_HEIGHT = 120
BORDER_THICKNESS = 4
BALL_RADIUS = 6
GRAVITY = 0.5 * TIME_SCALE
INITIAL_SPEED_MIN_X = 0 * TIME_SCALE
INITIAL_SPEED_MAX_X = 20 * TIME_SCALE
INITIAL_SPEED_Y = -10 * TIME_SCALE
CANON_X = 20
CANON_Y = TOP_BOX_HEIGHT // 2
RELOAD_TIME_MIN = 1300
RELOAD_TIME_MAX = 1600
FONT_SIZE = 14
MAX_LIVES = 5

# --- Bonus
BONUS_TYPES = ["shoot", "shield", "shoot", "marble", "shoot", "nuke"]
BONUS_WIDTHS = [0.75, 1.5, 1.5, 0.75, 1.4, 0.3]



# --- Initialisation Pygame & vidéo
def setup_environment():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Canon avec zones de retombée")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, FONT_SIZE)
    font_large = pygame.font.SysFont(None, 72)
    font_mini = pygame.font.SysFont(None, 12)
    return screen, clock, font, font_large, font_mini
