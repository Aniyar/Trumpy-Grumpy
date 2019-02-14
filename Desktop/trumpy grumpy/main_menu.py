from classes import *


def main_menu():
    menu = pygame.sprite.Group()
    size = WIDTH, HEIGHT = 500, 500
    screen = pygame.display.set_mode(size)

    level1 = LevelButton(menu)
    level2 = LevelButton(menu)
    level3 = LevelButton(menu)

    level1.unlock()



    running = True
    while running:
        screen.fill(pygame.Color('blue'))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if level1.check_click(event.pos):
                    game_cycle(1)
                if level2.check_click(event.pos):
                    game_cycle(2)
                if level3.check_click(event.pos):
                    game_cycle(3)
                if quit_button.check_click(event.pos):
                    menu_scr(screen)