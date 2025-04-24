# main.py
import pygame
from config import setup_environment
from graphics.intro import show_intro_screen
from logic.game import run_game_loop
from graphics.ui import wait_for_start, show_end_menu


def main():
    # Initialisation Pygame
    pygame.init()
    pygame.mixer.init()
    screen, clock, font, font_large, font_mini = setup_environment()

    wait_for_start(screen, font_large)
    # Intro READY + affichage
    show_intro_screen(screen, clock, font_large)

    # Lancer le jeu
    winner = run_game_loop(screen, clock, font, font_large, font_mini)
    choice = show_end_menu(screen, font_large)
    if choice == "replay":
        main()
    else:
        pygame.quit()
        exit()
if __name__ == "__main__":
    main()