import random
from helper_functions import *
from gaming_cycle import menu_scr

pygame.init()

fail = pygame.sprite.Group()
score_lst = []

pygame.mixer.music.load('data/main_theme.wav')
pygame.mixer.music.play(-1)
menu_scr(score_lst)
# f = game_cycle()
# if f == 'fail':
#     fail_scr(fail, screen)