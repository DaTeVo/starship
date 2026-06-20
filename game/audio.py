from pathlib import Path

import pygame

from settings import MUSIC_VOLUME, SOUND_VOLUME


ASSET_ROOT = Path(__file__).resolve().parent.parent / "assets"
MUSIC_PATH = ASSET_ROOT / "music" / "background.wav"
SOUND_PATHS = {
    "explosion": ASSET_ROOT / "sounds" / "explosion.wav",
    "powerup": ASSET_ROOT / "sounds" / "powerup.wav",
}

audio_enabled = False
sounds = {}


def init_audio():
    global audio_enabled, sounds

    try:
        if not pygame.mixer.get_init():
            pygame.mixer.init()

        sounds = {
            name: pygame.mixer.Sound(str(path))
            for name, path in SOUND_PATHS.items()
        }

        for sound in sounds.values():
            sound.set_volume(SOUND_VOLUME)

        audio_enabled = True
    except (FileNotFoundError, pygame.error):
        audio_enabled = False
        sounds = {}


def start_music():
    if not audio_enabled:
        return

    try:
        pygame.mixer.music.load(str(MUSIC_PATH))
        pygame.mixer.music.set_volume(MUSIC_VOLUME)
        pygame.mixer.music.play(-1)
    except pygame.error:
        pass


def play_sound(name):
    if not audio_enabled:
        return

    sound = sounds.get(name)

    if sound is not None:
        sound.play()
