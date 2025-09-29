import os
import pygame

_bgm_path = os.path.join(os.path.dirname(__file__), "sounds", "Pinapple Rag Techno Remake.mp3")
_playing = False
_paused = False


def init_music():
    global _playing, _paused
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(_bgm_path)
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)
        _playing = True
        _paused = False
        return True
    except pygame.error:
        _playing = False
        _paused = False
        return False


def music_toggle():
    global _paused
    if not pygame.mixer.get_init():
        return
    if _paused:
        pygame.mixer.music.unpause()
        _paused = False
    else:
        pygame.mixer.music.pause()
        _paused = True


def music_is_playing():
    return pygame.mixer.get_init() is not None and not _paused
