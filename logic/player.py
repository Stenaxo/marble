# logic/player.py
from config import SCREEN_WIDTH, SCREEN_HEIGHT, MAX_LIVES, RED, ORANGE, PURPLE, CYAN, PINK, NAVY

def init_players():
    players = ["left", "right", "top_left", "top_right", "upper_left", "upper_right"]

    lives = {p: MAX_LIVES for p in players}
    shield_states = {p: False for p in players}
    marble_ready = {p: False for p in players}

    colors = {
        "left": RED,
        "right": ORANGE,
        "top_left": PURPLE,
        "top_right": CYAN,
        "upper_left": PINK,
        "upper_right": NAVY
    }

    gap = 200
    circle_radius = 45
    base_y = SCREEN_HEIGHT - 100
    centers = {
        "left": (SCREEN_WIDTH // 4, base_y),
        "right": (3 * SCREEN_WIDTH // 4, base_y),
        "top_left": (SCREEN_WIDTH // 4, base_y - gap),
        "top_right": (3 * SCREEN_WIDTH // 4, base_y - gap),
        "upper_left": (SCREEN_WIDTH // 4, base_y - 2 * gap),
        "upper_right": (3 * SCREEN_WIDTH // 4, base_y - 2 * gap)
    }

    return players, lives, shield_states, marble_ready, colors, centers