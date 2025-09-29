import os
import pygame

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "images")
SOUNDS_DIR = os.path.join(os.path.dirname(__file__), "sounds")

def _img(name, scale=None):
    p = os.path.join(ASSETS_DIR, name)
    try:
        s = pygame.image.load(p).convert_alpha()
        if scale:
            s = pygame.transform.smoothscale(s, scale)
        return s
    except Exception:
        f = pygame.Surface((1, 1), pygame.SRCALPHA)
        return f


def _snd(name, volume=0.8):
    p = os.path.join(SOUNDS_DIR, name)
    try:
        s = pygame.mixer.Sound(p)
        s.set_volume(volume)
        return s
    except Exception:
        return None


def load_assets():
    # fonts
    font_big = pygame.font.SysFont("Roboto", 60)

    # loading screen
    loading_bg = _img("Loading_Bar_Background.png")
    loading_bar = _img("Loading_Bar.png")

    # main menu
    main_menu_bg = _img("main_screen.png")
    play_idle = _img("main_scree_button_idle.png")
    play_hover = _img("main_scree_button_hover.png")

    # instructions
    instructions_bg = _img("instructions_screen.png")
    ready_idle = _img("ready_iddle.png")
    ready_hover = _img("ready_hover.png")

    # selection
    select_bg = _img("selection_screen.png")
    rock = _img("furball_card.png")
    paper = _img("paw_card.png")
    scissors = _img("claws_card.png")
    rock_h = _img("furball_card_hover.png")
    paper_h = _img("paw_card_hover.png")
    scissors_h = _img("claws_card_hover.png")

    # fight
    fight_bg = _img("fight_bg.png")
    vs_icon = _img("vs_icon.png")

    # results
    final_win = _img("final_win.png")
    final_lose = _img("final_lose.png")
    final_tie = _img("final_tie.png")

    # play again
    play_again_idle = _img("play_again_idle.png")
    play_again_hover = _img("play_again_hover.png")

    # music icons
    music_on = _img("music_on.png")
    music_off = _img("music_off.png")

    # sfx
    btn_click = _snd("mouse-click.mp3", 0.7)
    hover = _snd("hover_sound.mp3", 0.6)
    countdown_beep = _snd("countdown_beep.mp3", 0.7)

    return {
        # fonts
        "FONT": font_big,
        # loading
        "loading_bg": loading_bg,
        "loading_bar": loading_bar,
        # main
        "main_menu_bg": main_menu_bg,
        "play_idle": play_idle,
        "play_hover": play_hover,
        # instructions
        "instructions_bg": instructions_bg,
        "ready_idle": ready_idle,
        "ready_hover": ready_hover,
        # select
        "select_bg": select_bg,
        "rock": rock,
        "paper": paper,
        "scissors": scissors,
        "rock_h": rock_h,
        "paper_h": paper_h,
        "scissors_h": scissors_h,
        # fight
        "fight_bg": fight_bg,
        "vs_icon": vs_icon,
        # finals
        "final_win": final_win,
        "final_lose": final_lose,
        "final_tie": final_tie,
        # play again
        "play_again_idle": play_again_idle,
        "play_again_hover": play_again_hover,
        # music icons
        "music_on": music_on,
        "music_off": music_off,
        # sounds
        "btn_click": btn_click,
        "hover": hover,
        "countdown_beep": countdown_beep,
    }