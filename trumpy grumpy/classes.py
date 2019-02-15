from helper_functions import *


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y, group):
        super().__init__(group)
        self.frames = []
        cut_sheet(self, sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.dir = 'down'

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]

    def change_img(self, sheet, columns, rows, x, y):
        self.frames = []
        cut_sheet(self, sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)


class AnimatedClimber(pygame.sprite.Sprite):

    def __init__(self, group):
        super().__init__(group)
        self.frames = []
        sheet = load_image('immigrant.png', -1)
        cut_sheet(self, sheet, 2, 1)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.dir = 'up'
        self.rect = self.rect.move(random.randrange(self.image.get_rect()[0], WIDTH - 50), HEIGHT)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]

        if self.dir == 'up':
            self.rect[1] -= 5
        else:
            self.rect[1] += 20

        if self.rect[1] >= HEIGHT:
            pygame.sprite.Sprite.kill(self)

    def fall(self, img, col, raw):
        self.dir = 'down'
        self.frames = []
        sheet = load_image(img, -1)
        rect = self.rect
        cut_sheet(self, sheet, col, raw)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = rect


class Sombrero(pygame.sprite.Sprite):

    def __init__(self, group, x, y, lvl):
        super().__init__(group)
        self.image = load_image('sombrero.png', -1)
        self.image = pygame.transform.scale(self.image, (90, 35))
        self.rect = [x, y]
        self.mask = pygame.mask.from_surface(self.image)
        self.lvl = lvl

    def update(self, corn, score):
        self.rect[1] -= 5
        for i in corn:
            if pygame.sprite.collide_mask(self, i):
                pygame.sprite.Sprite.kill(i)
                pygame.sprite.Sprite.kill(self)
                score += 100 / (self.lvl[0] + self.lvl[1])


class Corn(pygame.sprite.Sprite):
    def __init__(self, group, player):
        super().__init__(group)
        self.player = player
        self.image = load_image('Corn.png', -1)
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.dir = 'down'
        self.rect = [self.player.rect[0] + 40, self.player.rect[1] + 80]
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        if self.dir == 'down':
            self.rect[1] += 10
        else:
            self.rect[1] -= 10
        if 0 >= self.rect[1] >= HEIGHT:
            pygame.sprite.Sprite.kill(self)


class Trampoline(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = load_image('trampoline.png', -1)
        self.image = pygame.transform.scale(self.image, (WIDTH, 60))
        self.rect = [0, HEIGHT-50]
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, corn):
        for i in corn:
            if pygame.sprite.collide_mask(self, i):
                i.dir = 'up'


class Button(pygame.sprite.Sprite):
    def __init__(self, img, x, y, group):
        super().__init__(group)
        self.image = load_image(img)
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def check_click(self, mouse):
        if self.rect.collidepoint(mouse):
            return True

    def change_image(self, img):
        self.image = load_image(img)
        self.image = pygame.transform.scale(self.image, (100, 100))


class StaticSprite(pygame.sprite.Sprite):
    def __init__(self, img, group, x, y, width, height):
        super().__init__(group)
        self.image = load_image(img, -1)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect = [x, y]


class LevelButton(pygame.sprite.Sprite):
    def __init__(self, group, n):
        super().__init__(group)
        self.frames = []
        sheet = load_image('levels.png', -1)
        cut_sheet(self, sheet, 3, 1)
        self.image = self.frames[n - 1]
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.rect.move(100 * n, 360)

    def check_click(self, mouse):
        if self.rect.collidepoint(mouse):
            return True


class PauseIcon(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = load_image('pause.png')
        self.image = pygame.transform.scale(self.image, (200, 200))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(170, 170)


# class Scores():
#
#     def __init__(self):
#         self.lst = []
#
#     def append_score(self, score, corn_saved):
#         self.lst.append((score, corn_saved))
