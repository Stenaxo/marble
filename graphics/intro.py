# graphics/intro.py
import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE, SKIN
import os

# Chargement des images des joueurs
def load_player_images(folder=SKIN):
    base_path = os.path.join("assets", folder)
    keys = ["left", "right", "top_left", "top_right", "upper_left", "upper_right"]

    images = {}
    for key in keys:
        path = os.path.join(base_path, f"{key}.png")
        if not os.path.exists(path):
            raise FileNotFoundError(f"Image manquante : {path}")
        images[key] = pygame.image.load(path).convert_alpha()

    return images

def show_intro_screen(screen, clock, font_large):
    players_images = load_player_images()

    # Affichage des images en mosaïque
    screen.fill(BLACK)
    rows, cols = 2, 3
    img_w = SCREEN_WIDTH // cols
    img_h = SCREEN_HEIGHT // rows
    for i, key in enumerate(players_images):
        image = pygame.transform.scale(players_images[key], (img_w, img_h))
        x = (i % cols) * img_w
        y = (i // cols) * img_h
        screen.blit(image, (x, y))

    # Effet 3D "READY"
    for i in range(10, 0, -1):
        shadow = font_large.render("READY", True, BLACK)
        rect = shadow.get_rect(center=(SCREEN_WIDTH // 2 + i, SCREEN_HEIGHT // 2 + i))
        screen.blit(shadow, rect)

    text = font_large.render("READY", True, WHITE)
    rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text, rect)
    pygame.display.flip()

    # Son d’intro
    fight_sound = pygame.mixer.Sound("assets/fight.wav")
    fight_sound.play()

    # Pause d’intro avec gestion des événements
    intro_start = pygame.time.get_ticks()
    while pygame.time.get_ticks() - intro_start < 3000:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        clock.tick(60)