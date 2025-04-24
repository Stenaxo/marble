# graphics/renderer.py
import pygame
from config import BALL_RADIUS, BLUE, SCREEN_WIDTH, SCREEN_HEIGHT, SMOKE_COLOR

def draw_hearts(surface, center_x, center_y, count, color):
    spacing = 20
    radius = 6
    for i in range(count):
        x = center_x - (spacing * (count - 1) // 2) + i * spacing
        pygame.draw.circle(surface, color, (x, center_y), radius)

def draw_players(surface, players, lives, shield_states, player_images, centers, circle_radius, colors):
    for key in players:
        if lives.get(key, 0) > 0:
            # Surface circulaire vide avec transparence
            circle_surface = pygame.Surface((circle_radius * 2, circle_radius * 2), pygame.SRCALPHA)

            # Redimensionner et dessiner l'image du joueur
            image = pygame.transform.smoothscale(player_images[key], (circle_radius * 2, circle_radius * 2))
            circle_surface.blit(image, (0, 0))

            # Appliquer un masque rond
            mask = pygame.Surface((circle_radius * 2, circle_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(mask, (255, 255, 255), (circle_radius, circle_radius), circle_radius)
            circle_surface.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

            # Afficher la bulle circulaire à sa position
            pos = centers[key]
            surface.blit(circle_surface, (pos[0] - circle_radius, pos[1] - circle_radius))

            if shield_states[key]:
                pygame.draw.circle(surface, BLUE, pos, circle_radius + 3, 4)

            draw_hearts(surface, pos[0], pos[1] - 50, lives[key], colors[key])

def draw_explosions(surface, explosions):
    for explosion in explosions[:]:
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        explosion["alpha"] -= 15
        explosion["radius"] += 2
        if explosion["alpha"] <= 0:
            explosions.remove(explosion)
        else:
            pygame.draw.circle(overlay, (255, 200, 0, explosion["alpha"]),
                               explosion["center"], explosion["radius"])
            surface.blit(overlay, (0, 0))

def draw_smokes(surface, smokes):
    for smoke in smokes[:]:
        smoke["lifetime"] -= 1
        if smoke["lifetime"] <= 0:
            smokes.remove(smoke)
        else:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            pygame.draw.circle(overlay, (*SMOKE_COLOR, 60), smoke["center"], 40)
            surface.blit(overlay, (0, 0))

def draw_shield_break(surface, shield_break_animation):
    for animation in shield_break_animation[:]:
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        animation["alpha"] -= 10
        if animation["alpha"] <= 0:
            shield_break_animation.remove(animation)
        else:
            pygame.draw.circle(overlay, (*BLUE, animation["alpha"]),
                               animation["center"], animation["radius"], 6)
            surface.blit(overlay, (0, 0))