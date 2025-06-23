import pygame

class AudioManager:
    def __init__(self):
        pygame.mixer.init()
       
        self.collision_sound = pygame.mixer.Sound("src/audio/shot.wav")
        self.background_music = "src/audio/music2.mp3"
    
    def play_background_music(self):
        pygame.mixer.music.load(self.background_music)
        pygame.mixer.music.play(-1)
    
    def play_collision_sound(self):
        self.collision_sound.play()
    
