import os
import pygame

root_dir = os.path.dirname(os.path.abspath(__file__))

def play_music():
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(os.path.join(root_dir, "data", "library", "music", "megalovania.mid"))
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

def stop_music():
    pygame.mixer.music.stop()

def toggle_music():
    if pygame.mixer.music.get_busy():
        stop_music()
    else:
        play_music()