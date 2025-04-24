# graphics/ui.py
import pygame

def wait_for_start(screen, font_large, background=None):
    screen.fill((0, 0, 0))
    if background:
        screen.blit(background, (0, 0))

    button_color = (50, 200, 50)
    button_rect = pygame.Rect(140, 350, 200, 80)
    pygame.draw.rect(screen, button_color, button_rect, border_radius=12)

    text = font_large.render("JOUER", True, (255, 255, 255))
    text_rect = text.get_rect(center=button_rect.center)
    screen.blit(text, text_rect)

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and button_rect.collidepoint(event.pos):
                waiting = False

def show_end_menu(screen, font_large):
    screen.fill((0, 0, 0))
    
    replay_rect = pygame.Rect(90, 350, 140, 60)
    quit_rect = pygame.Rect(250, 350, 140, 60)

    pygame.draw.rect(screen, (100, 180, 250), replay_rect, border_radius=10)
    pygame.draw.rect(screen, (250, 100, 100), quit_rect, border_radius=10)

    replay_txt = font_large.render("Rejouer", True, (255, 255, 255))
    quit_txt = font_large.render("Quitter", True, (255, 255, 255))
    screen.blit(replay_txt, replay_txt.get_rect(center=replay_rect.center))
    screen.blit(quit_txt, quit_txt.get_rect(center=quit_rect.center))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if replay_rect.collidepoint(event.pos):
                    return "replay"
                elif quit_rect.collidepoint(event.pos):
                    return "quit"