# logic/ball.py
import pygame
import random
from config import (
    CANON_X, CANON_Y, BALL_RADIUS, INITIAL_SPEED_MIN_X, INITIAL_SPEED_MAX_X,
    INITIAL_SPEED_Y, GRAVITY, RELOAD_TIME_MIN, RELOAD_TIME_MAX, TOP_BOX_HEIGHT,
    BONUS_TYPES, BONUS_WIDTHS, SCREEN_WIDTH
)

class Ball:
    def __init__(self, owner, color, lives, shield_states, balls,
                 shoot_animations, marble_ready, bonus_zones,
                 shield_sound, shoot_sound, death_sound, explosion_sound,
                 nuke_animation, font_mini, centers):
        self.owner = owner
        self.color = color
        self.ephemeral = False
        self.reset()
        self.lives = lives
        self.shield_states = shield_states
        self.balls = balls
        self.shoot_animations = shoot_animations
        self.marble_ready = marble_ready
        self.bonus_zones = bonus_zones
        self.shield_sound = shield_sound
        self.shoot_sound = shoot_sound
        self.death_sound = death_sound
        self.explosion_sound = explosion_sound
        self.nuke_animation = nuke_animation
        self.centers = centers
        self.font_mini = font_mini

    def reset(self):
        self.x = CANON_X
        self.y = CANON_Y
        self.dx = random.uniform(INITIAL_SPEED_MIN_X, INITIAL_SPEED_MAX_X) * random.choice([-1, 1])
        self.dy = INITIAL_SPEED_Y
        self.in_air = False
        self.timer = pygame.time.get_ticks()
        self.wait_duration = random.randint(RELOAD_TIME_MIN, RELOAD_TIME_MAX)

    def update(self):
        if self.lives[self.owner] <= 0:
            return

        if self.in_air:
            self.x += self.dx
            self.y += self.dy
            self.dy += GRAVITY

            if self.x - BALL_RADIUS <= 0 or self.x + BALL_RADIUS >= SCREEN_WIDTH:
                self.dx *= -1

            if self.y + BALL_RADIUS >= TOP_BOX_HEIGHT:
                self.in_air = False
                self.timer = pygame.time.get_ticks()

                for start, width, bonus in self.bonus_zones:
                    if start <= self.x <= start + width:
                        if bonus == "shield":
                            self.shield_states[self.owner] = True
                            self.shield_sound.play()

                        elif bonus == "nuke":
                            targets = [k for k in self.lives if k != self.owner and self.lives[k] > 0]
                            if targets:
                                target = random.choice(targets)
                                self.nuke_animation["value"] = {
                                    "from": self.centers[self.owner],
                                    "to": self.centers[target],
                                    "progress": 0,
                                    "target": target
                                }

                        elif bonus == "shoot":
                            targets = [k for k in self.lives if k != self.owner and self.lives[k] > 0]
                            if targets:
                                target = random.choice(targets)
                                self.shoot_animations.append({
                                    "from": self.centers[self.owner],
                                    "to": self.centers[target],
                                    "progress": 0,
                                    "owner": self.owner,
                                    "target": target
                                })

                        elif bonus == "marble":
                            new_ball = Ball(self.owner, self.color, self.lives, self.shield_states, self.balls,
                                            self.shoot_animations, self.marble_ready, self.bonus_zones,
                                            self.shield_sound, self.shoot_sound, self.death_sound, self.explosion_sound,
                                            self.nuke_animation, self.font_mini, self.centers)
                            new_ball.ephemeral = True
                            self.balls.append(new_ball)

                        if self.ephemeral and bonus != "marble":
                            self.balls.remove(self)
                        break

        else:
            if pygame.time.get_ticks() - self.timer > self.wait_duration:
                if self.lives[self.owner] > 0:
                    self.reset()
                    self.in_air = True
                    if self.marble_ready[self.owner]:
                        new_ball = Ball(self.owner, self.color, self.lives, self.shield_states, self.balls,
                                        self.shoot_animations, self.marble_ready, self.bonus_zones,
                                        self.shield_sound, self.shoot_sound, self.death_sound, self.explosion_sound,
                                        self.nuke_animation, self.font_mini, self.centers)
                        new_ball.ephemeral = True
                        self.balls.append(new_ball)
                        self.marble_ready[self.owner] = False

    def draw(self, surface):
        if self.lives[self.owner] <= 0:
            return
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), BALL_RADIUS)
        if self.ephemeral:
            label = self.font_mini.render("M", True, (0, 0, 0))
            rect = label.get_rect(center=(int(self.x), int(self.y)))
            surface.blit(label, rect)