# logic/game.py
import pygame
import os
from logic.player import init_players
from logic.ball import Ball
from graphics.renderer import draw_players, draw_explosions, draw_smokes, draw_shield_break
from graphics.intro import load_player_images
from config import (
    WHITE, BLACK, BLUE, YELLOW, GRAY, GREEN,
    TIME_SCALE, SCREEN_WIDTH, TOP_BOX_HEIGHT, BORDER_THICKNESS,
    BONUS_TYPES, BONUS_WIDTHS, SCREEN_HEIGHT, CANON_X, CANON_Y, SKIN
)


def run_game_loop(screen, clock, font, font_large, font_mini):
    # Initialisation des joueurs
    players, lives, shield_states, marble_ready, colors, centers = init_players()
    player_images = load_player_images(SKIN)  # ou ce que tu veux
    balls = []
    shoot_animations = []
    shield_break_animation = []
    explosions = []
    smokes = []
    nuke_animation = {"value": None}

    # Initialisation zones bonus
    bonus_zones = []
    total_units = sum(BONUS_WIDTHS)
    unit_width = SCREEN_WIDTH / total_units
    start_x = 0
    for i in range(len(BONUS_TYPES)):
        width = BONUS_WIDTHS[i] * unit_width
        bonus_zones.append((start_x, width, BONUS_TYPES[i]))
        start_x += width

    # Sons
    explosion_sound = pygame.mixer.Sound("assets/explosion.wav")
    shoot_sound = pygame.mixer.Sound("assets/shoot.wav")
    shield_sound = pygame.mixer.Sound("assets/shield.wav")
    death_sound = pygame.mixer.Sound("assets/heart.wav")
    win_sound = pygame.mixer.Sound("assets/win.wav")

    nuke_image = pygame.image.load("assets/nuke.png").convert_alpha()
    nuke_image = pygame.transform.smoothscale(nuke_image, (32, 32))
    shoot_image = pygame.image.load("assets/shoot.png").convert_alpha()
    shoot_image = pygame.transform.smoothscale(shoot_image, (32, 32))  # ajuste à volonté
    canon_image = pygame.image.load("assets/canon.png").convert_alpha()
    canon_image = pygame.transform.smoothscale(canon_image, (32, 32))  # ou la taille que tu veux
    background_image = pygame.image.load("assets/background.png").convert()
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    # Balles de départ
    for p in players:
        b = Ball(p, colors[p], lives, shield_states, balls, shoot_animations,
                 marble_ready, bonus_zones, shield_sound, shoot_sound,
                 death_sound, explosion_sound, nuke_animation, font_mini, centers)
        balls.append(b)

    winner = None
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.blit(background_image, (0, 0))

        # Vérifie le gagnant
        alive = [p for p in players if lives[p] > 0]
        if len(alive) == 1:
            winner = alive[0]
            running = False

        # Bonus zones
        pygame.draw.line(screen, BLACK, (0, TOP_BOX_HEIGHT), (SCREEN_WIDTH, TOP_BOX_HEIGHT), BORDER_THICKNESS)
        for start, width, bonus in bonus_zones:
            color = {
                "shoot": GRAY,
                "shield": BLUE,
                "nuke": YELLOW,
                "marble": GREEN
            }.get(bonus, BLACK)
            pygame.draw.rect(screen, color, (start, TOP_BOX_HEIGHT, width, 10))
            label = font.render(bonus, True, BLACK)
            screen.blit(label, (start + width / 2 - label.get_width() / 2, TOP_BOX_HEIGHT + 20))

        # Mouvements des balles
        for b in balls[:]:
            b.update()
            b.draw(screen)

        # Tir : animation + dégâts
        for anim in shoot_animations[:]:
            anim["progress"] += 0.05 * TIME_SCALE
            if anim["progress"] >= 1:
                shoot_sound.play()
                target = anim["target"]
                if lives[target] > 0:
                    if shield_states[target]:
                        shield_states[target] = False
                        shield_break_animation.append({"center": centers[target], "radius": 48, "alpha": 255})
                    else:
                        lives[target] = max(0, lives[target] - 1)
                        if lives[target] == 0:
                            death_sound.play()
                shoot_animations.remove(anim)
            else:
                fx, fy = anim["from"]
                tx, ty = anim["to"]
                px = fx + (tx - fx) * anim["progress"]
                py = fy + (ty - fy) * anim["progress"]
                screen.blit(shoot_image, (int(px - shoot_image.get_width() // 2),
                          int(py - shoot_image.get_height() // 2)))

        # Bombe nucléaire
        if nuke_animation["value"]:
            anim = nuke_animation["value"]
            anim["progress"] += 0.03 * TIME_SCALE
            if anim["progress"] >= 1:
                target = anim["target"]
                explosion_sound.play()
                explosions.append({"center": centers[target], "radius": 10, "alpha": 255})
                smokes.append({"center": centers[target], "lifetime": 300})
                if shield_states[target]:
                    shield_states[target] = False
                    shield_break_animation.append({"center": centers[target], "radius": 48, "alpha": 255})
                else:
                    lives[target] = 0
                nuke_animation["value"] = None
            else:
                fx, fy = anim["from"]
                tx, ty = anim["to"]
                px = fx + (tx - fx) * anim["progress"]
                py = fy + (ty - fy) * anim["progress"]
                screen.blit(nuke_image, (int(px - nuke_image.get_width() // 2),
                                        int(py - nuke_image.get_height() // 2)))

        # Dessiner joueurs & effets
        draw_players(screen, players, lives, shield_states, player_images, centers, 45, colors)
        draw_shield_break(screen, shield_break_animation)
        draw_explosions(screen, explosions)
        draw_smokes(screen, smokes)

        screen.blit(canon_image, (CANON_X - canon_image.get_width() // 2,
                          CANON_Y - canon_image.get_height() // 2))
        pygame.display.flip()
        clock.tick(60)

    # Affichage final du gagnant
    if winner:
        
        image = pygame.transform.scale(player_images[winner], (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(image, (0, 0))
        win_sound.play()

        for i in range(10, 0, -1):
            shadow = font_large.render("WINNER", True, BLACK)
            rect = shadow.get_rect(center=(SCREEN_WIDTH // 2 + i, SCREEN_HEIGHT // 2 + i))
            screen.blit(shadow, rect)

        text = font_large.render("WINNER", True, (255, 255, 255))
        rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(text, rect)

        # Boucle d’enregistrement de 7 secondes
        win_start = pygame.time.get_ticks()
        pygame.display.flip()
        pygame.time.delay(7000)

    return winner