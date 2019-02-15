from classes import *
from levels import *

fail = pygame.sprite.Group()
win = pygame.sprite.Group()


def game_cycle(n_level, screen, sc_lst):

    score = 0

    lvl = levels[n_level]
    n_climbers = lvl[0]
    n_supclimbers = lvl[1]
    n_corn = lvl[2]
    trampoline = lvl[3]

    all_sprites = pygame.sprite.Group()
    corn_sprites = pygame.sprite.Group()
    hats = pygame.sprite.Group()
    climbers = pygame.sprite.Group()
    statics = pygame.sprite.Group()
    trampoline_gr = pygame.sprite.Group()
    pause_sp = pygame.sprite.Group()

    trump = AnimatedSprite(load_image("trump-run-straight.png"), 6, 1, 100, 100, all_sprites)
    StaticSprite('wall.png', statics, 0, 150, 500, 350)
    PauseIcon(pause_sp)
    retry_btn = Button('retry.png', 400, 0, pause_sp)

    if trampoline:
        Trampoline(trampoline_gr)

    running = True
    fps = 10
    clock = pygame.time.Clock()
    new_dir = 'right'
    interval = 0
    pause = False

    while running:
        if not pause:  # обновление, отрисовка и проверка спрайтов
            screen.fill(pygame.Color('blue'))

            # обработка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.KEYDOWN:
                    # кидаем кукурузу если она есть в запасе
                    if event.key == pygame.K_DOWN:
                        if n_corn > 0:
                            Corn(corn_sprites, trump)
                            n_corn -= 1
                    # ставим игру на паузу
                    if event.key == pygame.K_SPACE:
                        pygame.mixer.music.pause()
                        pause = True

            # обработка зажимов стрелок на клавиатуре
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_LEFT]:
                trump.rect[0] -= 10
                new_dir = 'left'
            if keys_pressed[pygame.K_RIGHT]:
                trump.rect[0] += 10
                new_dir = 'right'

            # проверка на смену направления игрока
            # меняет картинку анимированного спрайта в соответствии с новым направлнием
            if new_dir != trump.dir:
                if new_dir == 'right':
                    trump.change_img(load_image("trump-run-right.png"), 6, 1, trump.rect[0], trump.rect[1])
                elif new_dir == 'left':
                    trump.change_img(load_image("trump-run-left.png"), 6, 1, trump.rect[0], trump.rect[1])
                trump.dir = new_dir

            # создаем климберов с разными интервалами
            # если рандомно сгенерированный интервал между предыдущим климбером и
            # следующим не закончился уменьшаем его
            if interval > 0:
                interval -= 1
            # создаем климбера
            elif (n_climbers > 0 or n_supclimbers > 0) and interval == 0:
                # все что связано с перемнной эр нужно для того, чтобы равномерно создавались супер климберы
                r = 1
                try:
                    k = int((n_climbers + n_supclimbers) // n_supclimbers)
                    r = random.randint(0, k)
                except Exception:
                    pass

                if r == 0 and n_supclimbers > 0:
                    climber = AnimatedClimber(climbers)
                    Sombrero(hats, climber.rect[0] - 10, climber.rect[1] - 10, lvl)
                    n_supclimbers -= 1
                elif n_climbers > 0:
                    AnimatedClimber(climbers)
                    n_climbers -= 1
                interval = random.randrange(40)

            statics.update()
            all_sprites.update()
            corn_sprites.update()
            climbers.update()
            hats.update(corn_sprites, score)
            trampoline_gr.update(corn_sprites)

            # проверяем всех климберов на пересечение стены
            for climber in climbers:
                if climber.rect[1] <= 90:
                    end_scr(fail, score, n_corn, screen, n_level, sc_lst)
                    running = False

            # проверка кукурузин на столкновение с климберами и игроком
            for corn in corn_sprites:
                for climber in climbers:
                    if pygame.sprite.collide_mask(climber, corn):
                        pygame.sprite.Sprite.kill(corn)
                        climber.fall('falling_immigrant.png', 4, 1)
                        score += 100/(lvl[0] + lvl[1])

                if pygame.sprite.collide_mask(trump, corn):
                    end_scr(fail, score, n_corn, screen, n_level, sc_lst)

            # проверка на выигрыш
            if len(climbers) == 0 and n_climbers <= 0 and n_supclimbers <= 0:
                end_scr(win, score, n_corn, screen, n_level, sc_lst)

            statics.draw(screen)
            all_sprites.draw(screen)
            corn_sprites.draw(screen)
            climbers.draw(screen)
            hats.draw(screen)
            trampoline_gr.draw(screen)

        else:  # экран паузы
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pygame.mixer.music.unpause()
                        pause = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if retry_btn.check_click(event.pos):
                        game_cycle(n_level, screen, sc_lst)

            pause_sp.draw(screen)

        pygame.display.flip()
        clock.tick(fps)


def end_scr(group, score, saved_corn, screen, n_level, sc_lst):
    # экран выигрыша или проигрыша в зависимости от передаваемой группы
    sc_lst.append((score, saved_corn, n_level))
    intro_text = ["YOU LOSE", "YOU WIN", int(score), "CORN SAVED:", saved_corn,
                  "RETRY", "NEXT LEVEL",
                  "MENU"]

    font = pygame.font.Font(None, 70)
    btn_x = WIDTH//2 + 30
    if group == fail:
        sound = pygame.mixer.Sound('data/angry_scream.wav')
        fon = pygame.transform.scale(load_image('fail.png'), (WIDTH, HEIGHT))
        msg = font.render(intro_text[0], 1, pygame.Color('red'))
    else:
        sound = pygame.mixer.Sound('data/troll_laugh.wav')
        fon = pygame.transform.scale(load_image('win.png'), (WIDTH, HEIGHT))
        msg = font.render(intro_text[1], 1, pygame.Color('green'))
        if n_level < 2:
            next_button = Button("next.png", btn_x, 250, group)

    screen.blit(fon, (0, 0))
    pygame.mixer.Sound.play(sound)
    msg_x = WIDTH//2
    msg_y = 70
    screen.blit(msg, (msg_x - 10, msg_y))

    score_text = pygame.font.Font(None, 40).render("YOUR SCORE:" + str(intro_text[2]), 1, pygame.Color('blue'))
    screen.blit(score_text, (msg_x, msg_y + 90))

    corns_text = pygame.font.Font(None, 40).render(intro_text[3] + str(intro_text[4]), 1, pygame.Color('blue'))
    screen.blit(corns_text, (msg_x, msg_y + 120))

    retry_button = Button("retry.png", btn_x, 350, group)
    quit_button = Button("menu.png", btn_x + 100, 350, group)
    score_button = Button("scores.png", btn_x + 100, 250, group)
    group.draw(screen)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if retry_button.check_click(event.pos):
                    game_cycle(n_level, screen, sc_lst)
                if quit_button.check_click(event.pos):
                    menu_scr(sc_lst)
                if group == win:
                    if next_button.check_click(event.pos):
                        game_cycle(n_level + 1, screen, sc_lst)
                if score_button.check_click(event.pos):
                    score_table(screen, sc_lst)


def menu_scr(sc_lst):
    # главное меню
    menu = pygame.sprite.Group()
    buttons = pygame.sprite.Group()
    size = WIDTH, HEIGHT = 500, 500
    screen = pygame.display.set_mode(size)

    StaticSprite('main_menu.png', menu, 150, 50, 400, 400)
    fon = pygame.transform.scale(load_image('main_menu.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))

    level1_btn = LevelButton(buttons , 1)
    level2_btn = LevelButton(buttons , 2)
    level3_btn = LevelButton(buttons , 3)

    soundbtn = Button('sound_btn.png', 40, 150, buttons )
    sound = True

    running = True
    while running:
        screen.fill(pygame.Color('white'))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:

                if level1_btn.check_click(event.pos):
                    game_cycle(0, screen, sc_lst)
                if level2_btn.check_click(event.pos):
                    game_cycle(1, screen, sc_lst)
                if level3_btn.check_click(event.pos):
                    game_cycle(2, screen, sc_lst)
                if soundbtn.check_click(event.pos):
                    sound = not sound
                    if sound:
                        soundbtn.change_image('sound_btn.png')
                        pygame.mixer.music.unpause()
                    else:
                        soundbtn.change_image('no_sound_btn.png')
                        pygame.mixer.music.pause()

        buttons.update()
        menu.update()
        menu.draw(screen)
        buttons.draw(screen)
        pygame.display.flip()


def score_table(screen, score_list):

    score_list.sort(key=lambda x: (x[2], x[0], x[1]))
    sprites = pygame.sprite.Group()
    menu_btn = Button('menu.png', 20, 400, sprites)

    large_text = pygame.font.Font('freesansbold.ttf', 60)
    text_surf, text_rect = text_objects('TOP SCORES', large_text)
    text_rect.center = (250, 50)

    text = '# ' + 'Score ' + 'Corn saved ' + 'level'
    tab_text = pygame.font.Font('freesansbold.ttf', 30)
    tab_surf, tab_rect = text_objects(text, tab_text)
    tab_rect.center = (250, 100)

    score_text = ''
    for i in range(len(score_list)):
        score_text += (str(i + 1) + '.  ' + str(int(score_list[i][0])) + ' ' * 15 +
                       str(score_list[i][1]) + ' ' * 15 + str(score_list[i][2]))
    score_font = pygame.font.Font('freesansbold.ttf', 20)
    sc_surf, sc_rect = text_objects(score_text, score_font)
    sc_rect.center = (250, 300)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if menu_btn.check_click(event.pos):
                    menu_scr(score_list)

        screen.fill(pygame.Color('black'))
        screen.blit(text_surf, text_rect)
        screen.blit(tab_surf, tab_rect)
        screen.blit(sc_surf, sc_rect)

        sprites.update()
        sprites.draw(screen)

        pygame.display.flip()
