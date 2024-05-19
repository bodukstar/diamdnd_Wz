import pygame
import random

Run = True
window_x = 600
window_y = 700
window = pygame.display.set_mode((window_x, window_y))

background = pygame.image.load('img/background.png')  # фон вікна

hero_direction = 'STOP'
count_before_diamond_show = 0
count_before_bos_show = 0

# завантажуємо шрифти
pygame.font.init()
font = pygame.font.SysFont('Arial', 26)
white = (255, 255, 255)
dark = (47, 14, 51)
text_x = 10
text_y = 10


def draw_background(window, picture):  # вимальовуємо фон
    window.blit(picture, (0, 0))


class Wizard:
    main_picture = pygame.image.load('img/1_IDLE_000.png')
    main_left = pygame.image.load('img/3_RUN_001_l.png')
    main_right = pygame.image.load('img/3_RUN_000.png')
    speed = 2
    x = 10
    y = 500
    width = 140
    height = 150
    jump_speed = 150

    def stand(self, window):
        window.blit(self.main_picture, (self.x, self.y))

    def move_left(self, window):
        if self.x - self.speed >= 0:
            self.x -= self.speed
        else:
            self.x = 0
        window.blit(self.main_left, (self.x, self.y))

    def move_right(self, window):
        if self.x + self.speed <= window_x - self.width:
            self.x += self.speed
        else:
            self.x = window_x - self.width
        window.blit(self.main_right, (self.x, self.y))

    def move_up(self):
        if self.y - self.jump_speed >= 0:
            self.y -= self.jump_speed
        else:
            self.y = 0

    def fall(self):
        if self.y + self.jump_speed <= window_y - self.height:
            self.y += self.jump_speed
        else:
            self.y = window_y - self.height - 50

    def get_position(self):  # повертаємо координати
        return (self.x, self.y)

    def get_size(self):  # повертає розміри чарівника
        return (self.width, self.height)


class Diamants:
    diamand_picture_1 = pygame.image.load('img/11.png')
    diamand_picture_2 = pygame.image.load('img/9.png')
    diamand_picture_3 = pygame.image.load('img/8.png')
    diamand_picture = [diamand_picture_1, diamand_picture_2, diamand_picture_3]
    diamand_list = []

    def __init__(self):
        pass

    def add(self):
        random_rander = random.randint(0, 2)
        random_picture = self.diamand_picture[random_rander]
        new_diamond = Diamant(random_picture)
        self.diamand_list.append(new_diamond)

    def draw(self):
        for element in self.diamand_list:
            element.show()

    def fall(self):
        for element in self.diamand_list:
            element.down()

    def delete(self, x, y, width, height):  # видалення об'єктів після попадання на чарівника
        index = 0
        catch = 0
        lost = 0

        for el in self.diamand_list:
            diamant_position = el.get_position()
            d_x = diamant_position[0]
            d_y = diamant_position[1] + 47
            
            if d_x > x and d_x < x + width and d_y > y and d_y < y + height:
                del self.diamand_list[index]
                catch += 1
            elif d_y > 700:
                del self.diamand_list[index]
                lost += 1
        index += 1 
        return (catch, lost)


class Diamant:
    x = 0
    y = 0
    picture = 0
    speed = 0

    def __init__(self, picture):
        self.x = random.randint(13, window_x - 50)
        self.speed = random.randint(1, 1)
        self.picture = picture

    def show(self):
        window.blit(self.picture, (self.x, self.y))

    def down(self):
        self.y += self.speed
    
    def get_position(self):
        return (self.x, self.y)


class Boss:  # додав
    bos_picture = pygame.image.load('img/zubat.png')
    resiz_picture = pygame.transform.scale(bos_picture, (60, 60))
    bos_list = []

    def add(self):
        new_bos = Diamant(self.resiz_picture)
        self.bos_list.append(new_bos)

    def draw(self):
        for el in self.bos_list:
            el.show()

    def fall(self):
        for el in self.bos_list:
            el.down()


class SuperWizard(Wizard):  # дочірній клас чарівника
    main_picture = pygame.image.load('img/1_IDLE_000_i.png')
    main_left = pygame.image.load('img/3_RUN_000_il.png')
    main_right = pygame.image.load('img/3_RUN_000_i.png')
    main_jump = pygame.image.load('img/4_JUMP_003.png')

    height = 175
    width = 150

    def jump(self, window):
        window.blit(self.main_jump, (self.x, self.y - 70))


super_wizard = SuperWizard()
wizard = Wizard()  # зміна для візард класу

bos_in_game = Boss()
diamant_in_game = Diamants()
diamant_in_game.add()

catch = 0
lost = 0

run_level = True

while Run:
    while run_level:
        if count_before_diamond_show == 500:
            diamant_in_game.add()
            count_before_diamond_show = 0

        if count_before_bos_show == 800:
            bos_in_game.add()
            count_before_bos_show = 0

        draw_background(window, background)

        # переміщення чарівника
        if hero_direction == 'LEFT':
            super_wizard.move_left(window)
        elif hero_direction == 'RIGHT':
            super_wizard.move_right(window)
        elif hero_direction == 'UP':
            super_wizard.jump(window)
        else:
            super_wizard.stand(window)  # переміщення без руху

        diamant_in_game.draw()
        diamant_in_game.fall()

        bos_in_game.draw()
        bos_in_game.fall()

        pygame.display.update()

        message = f"Source: {catch} / {lost}"
        text = font.render(message, True, white)
        window.blit(text, (text_x, text_y))

        for event in pygame.event.get():  # для виходу з вікна
            if event.type == pygame.QUIT:
                Run = False

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                hero_direction = 'LEFT'

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                hero_direction = 'RIGHT'

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                hero_direction = 'UP'

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                super_wizard.fall()

            elif event.type == pygame.KEYUP:
                hero_direction = 'STOP'

        wizard_position = super_wizard.get_position()
        w_x = wizard_position[0]
        w_y = wizard_position[1]

        wizard_size = super_wizard.get_size()
        w_w = wizard_size[0]
        w_h = wizard_size[1]

        result = diamant_in_game.delete(w_x, w_y, w_w, w_h)

        catch += result[0]
        lost += result[1]

        if lost == 5:
            draw_background(window, background)
            run_level = False

        count_before_diamond_show += 1
        count_before_bos_show += 1

    font = pygame.font.SysFont('Arial', 46)
    message = f"Game over! Your Score: {catch}"
    text = font.render(message, True, white, dark)
    window.blit(text, (text_x, text_y))
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Run = False
