import threading
import math
import pygame

from states import LOADING, MAIN_MENU, INSTRUCTIONS, WEAPON_SELECT, FIGHT, FINAL_RESULTS
from logic import random_weapon, rps_outcome
from assets import load_assets
from music import init_music, music_toggle, music_is_playing
from ui import draw_image_button
from version import __version__

WIDTH, HEIGHT = 1280, 720

# timings
REVEAL_DELAY_MS = 2000
COUNTDOWN_TOTAL_MS = 4000
SLIDE_MS = 1000
RESULT_SHOW_MS = 3000

# fake work for loading bar
WORK = 10_000_000


def run_game():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(f"Pawn Claws And Furballs v{__version__}")
    CLOCK = pygame.time.Clock()

    A = load_assets()

    loading_bg_rect = A["loading_bg"].get_rect(center=(WIDTH // 2, HEIGHT // 2))
    finished = A["FONT"].render("OwO", True, "white")
    finished_rect = finished.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    play_button_rect = A["play_idle"].get_rect(center=(WIDTH // 2, 470))
    ready_button_rect = A["ready_idle"].get_rect(center=(WIDTH // 2, 650))

    rock_rect = A["rock"].get_rect(center=(300, 300))
    paper_rect = A["paper"].get_rect(center=(640, 300))
    scissors_rect = A["scissors"].get_rect(center=(990, 300))

    vs_rect = A["vs_icon"].get_rect(center=(WIDTH // 2, HEIGHT // 2))
    play_again_rect = A["play_again_idle"].get_rect(center=(WIDTH // 2, 650))

    music_button_rect = A["music_on"].get_rect(topright=(WIDTH - 20, 20))

    # music
    init_music()
    music_playing = True

    # state
    state = LOADING
    loading_finished = False
    loading_progress = 0

    round_number = 1
    player_score = 0
    computer_score = 0

    weapon_reveal_time = None
    fight_start_time = None
    result_text = ""
    result_shown_time = None
    player_choice = None
    computer_choice = None

    hovered_element = None
    countdown_sound_played = False

    # Background loading thread
    def do_work():
        nonlocal loading_finished, loading_progress
        for i in range(WORK):
            _ = 875234 / 467812 * 56891
            loading_progress = i
        loading_finished = True

    threading.Thread(target=do_work, daemon=True).start()

# main game loop
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        new_hover = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if music_button_rect.collidepoint(event.pos):
                    music_toggle()
                    music_playing = music_is_playing()

                if state == MAIN_MENU:
                    if play_button_rect.collidepoint(event.pos):
                        if A["btn_click"]: A["btn_click"].play()
                        state = INSTRUCTIONS

                elif state == INSTRUCTIONS:
                    if ready_button_rect.collidepoint(event.pos):
                        if A["btn_click"]: A["btn_click"].play()
                        state = WEAPON_SELECT
                        weapon_reveal_time = pygame.time.get_ticks()

                elif state == WEAPON_SELECT:
                    if weapon_reveal_time and pygame.time.get_ticks() - weapon_reveal_time > REVEAL_DELAY_MS:
                        if rock_rect.collidepoint(event.pos):
                            if A["btn_click"]: A["btn_click"].play()
                            player_choice = "rock"
                        elif paper_rect.collidepoint(event.pos):
                            if A["btn_click"]: A["btn_click"].play()
                            player_choice = "paper"
                        elif scissors_rect.collidepoint(event.pos):
                            if A["btn_click"]: A["btn_click"].play()
                            player_choice = "scissors"

                        if player_choice:
                            computer_choice = random_weapon()
                            fight_start_time = pygame.time.get_ticks()
                            countdown_sound_played = False
                            result_shown_time = None
                            state = FIGHT

                elif state == FINAL_RESULTS:
                    if play_again_rect.collidepoint(event.pos):
                        if A["btn_click"]: A["btn_click"].play()
                        round_number = 1
                        player_score = 0
                        computer_score = 0
                        state = MAIN_MENU

        # hover sfx
        if state == MAIN_MENU and play_button_rect.collidepoint(mouse_pos):
            new_hover = "play"
        elif state == INSTRUCTIONS and ready_button_rect.collidepoint(mouse_pos):
            new_hover = "ready"
        elif state == WEAPON_SELECT:
            if rock_rect.collidepoint(mouse_pos):
                new_hover = "rock"
            elif paper_rect.collidepoint(mouse_pos):
                new_hover = "paper"
            elif scissors_rect.collidepoint(mouse_pos):
                new_hover = "scissors"
        elif state == FINAL_RESULTS and play_again_rect.collidepoint(mouse_pos):
            new_hover = "play_again"

        if new_hover != hovered_element:
            if new_hover and A["hover"]: A["hover"].play()
            hovered_element = new_hover

        # -------------- draw --------------
        screen.fill((13, 14, 46))

        if state == LOADING:
            if not loading_finished:
                bar_w = loading_progress / WORK * 720
                scaled_bar = pygame.transform.scale(A["loading_bar"], (max(1, int(bar_w)), 150))
                bar_rect = scaled_bar.get_rect(midleft=(280, HEIGHT // 2))
                screen.blit(A["loading_bg"], loading_bg_rect)
                screen.blit(scaled_bar, bar_rect)
            else:
                screen.blit(finished, finished_rect)
                pygame.display.update()
                pygame.time.wait(1000)
                state = MAIN_MENU

        elif state == MAIN_MENU:
            screen.blit(A["main_menu_bg"], (0, 0))
            hovered = draw_image_button(screen, A["play_idle"], A["play_hover"], play_button_rect, mouse_pos)

        elif state == INSTRUCTIONS:
            screen.blit(A["instructions_bg"], (0, 0))
            hovered = draw_image_button(screen, A["ready_idle"], A["ready_hover"], ready_button_rect, mouse_pos)

        elif state == WEAPON_SELECT:
            screen.blit(A["select_bg"], (0, 0))
            if weapon_reveal_time and pygame.time.get_ticks() - weapon_reveal_time < REVEAL_DELAY_MS:
                cat_text = A["FONT"].render(" ", True, "white")
                screen.blit(cat_text, (380, 100))
            else:
                # three hoverable cards
                draw_image_button(screen, A["rock"], A["rock_h"], rock_rect, mouse_pos)
                draw_image_button(screen, A["paper"], A["paper_h"], paper_rect, mouse_pos)
                draw_image_button(screen, A["scissors"], A["scissors_h"], scissors_rect, mouse_pos)

        elif state == FIGHT:
            screen.blit(A["fight_bg"], (0, 0))
            now = pygame.time.get_ticks()
            countdown_elapsed = now - fight_start_time

            # one short beep at start
            if countdown_elapsed < 100 and not countdown_sound_played:
                if A["countdown_beep"]: A["countdown_beep"].play()
                countdown_sound_played = True

            if countdown_elapsed < COUNTDOWN_TOTAL_MS:
                # animated VS during countdown
                scale = 1.2 + 0.1 * math.sin(pygame.time.get_ticks() / 100)
                vs_scaled = pygame.transform.rotozoom(A["vs_icon"], 0, scale)
                vs_rect_scaled = vs_scaled.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                screen.blit(vs_scaled, vs_rect_scaled)

                # show 3..2..1..go!
                countdown_num = 3 - countdown_elapsed // 1000
                if countdown_num > 0:
                    text = str(countdown_num)
                elif countdown_elapsed < 3500:
                    text = "GO!"
                else:
                    text = ""
                countdown_text = A["FONT"].render(text, True, "white")
                screen.blit(countdown_text, (600, 100))

            else:
                # sliding cards reveal
                slide_elapsed = countdown_elapsed - COUNTDOWN_TOTAL_MS
                t = min(1, slide_elapsed / SLIDE_MS)

                player_img = A["rock"] if player_choice == "rock" else A["paper"] if player_choice == "paper" else A["scissors"]
                comp_img = A["rock"] if computer_choice == "rock" else A["paper"] if computer_choice == "paper" else A["scissors"]

                player_x = -300 + (320 + 300) * t
                comp_x = 1280 + 300 - (1280 + 300 - 960) * t
                screen.blit(player_img, player_img.get_rect(center=(player_x, 360)))
                screen.blit(comp_img, comp_img.get_rect(center=(comp_x, 360)))

                # static VS
                screen.blit(A["vs_icon"], vs_rect)

                if t >= 1:
                    nonlocal_result = rps_outcome(player_choice, computer_choice)
                    if result_shown_time is None:
                        result_text = nonlocal_result
                        result_shown_time = pygame.time.get_ticks()

                    result_display = A["FONT"].render(result_text, True, "white")
                    screen.blit(result_display, (520, 600))

                    if now - result_shown_time > RESULT_SHOW_MS:
                        if result_text == "YOU WIN":
                            player_score += 1
                        elif result_text == "YOU LOSE":
                            computer_score += 1
                        round_number += 1
                        player_choice = None
                        computer_choice = None
                        result_text = ""
                        fight_start_time = None
                        result_shown_time = None
                        if round_number > 3:
                            state = FINAL_RESULTS
                        else:
                            state = WEAPON_SELECT
                            weapon_reveal_time = pygame.time.get_ticks()

        elif state == FINAL_RESULTS:
            if player_score > computer_score:
                screen.blit(A["final_win"], (0, 0))
            elif computer_score > player_score:
                screen.blit(A["final_lose"], (0, 0))
            else:
                screen.blit(A["final_tie"], (0, 0))

            draw_image_button(screen, A["play_again_idle"], A["play_again_hover"], play_again_rect, mouse_pos)

        # music icon
        screen.blit(A["music_on"] if music_playing else A["music_off"], music_button_rect)

        pygame.display.update()
        CLOCK.tick(60)