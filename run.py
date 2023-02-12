from view import Cat, Button, Cursor #из файла view достаём реализацию кота, кнопки и курсора
import pygame, sys #добавляем бибилтеки pygame, sys

pygame.init() #создаём игру
clock = pygame.time.Clock() #создаём часы для игры

#Game parameters
screen_width = 900 #ширина экрана игры
screen_height = 1000 #высота экрана игры
screen = pygame.display.set_mode((screen_width, screen_height)) #создаём экран размера ширина * длину 
background = pygame.image.load("sprites_data/background.png") #загружаем картинку заднего фона
pygame.mouse.set_visible(False) #делаем мышку невидимой
night = pygame.image.load("sprites_data/night.png") #загрузка серого режима
update_time = 30 #сколько раз обновляется рисунок

cat = Cat(450, 550) #создание кота размера 450 * 670
cat_group = pygame.sprite.Group() #создание группы рисунков кота
cat_group.add(cat) #добавление рисунка кота в группа

#Activities
play = Button(150, 915, "sprites_data/play.png") #создание кнопки играть
feed = Button(480, 915, "sprites_data/food.png") #создание кнопки есть
sleep = Button(750, 915, "sprites_data/sleep.png") #создание кнпоки спать 
buttons_group = pygame.sprite.Group() #создать группу кнопок
buttons_group.add(play) #добавление кнпоки играть в группу
buttons_group.add(feed) #добавление кнпоки есть в группу
buttons_group.add(sleep) #добавление кнопки спать в группу

#Cursor
cursor = Cursor() #создание курсора
cursor_group = pygame.sprite.Group() #создание группы для курсора
cursor_group.add(cursor) #добавление курсора в группу

#Game loop
while(True): #бесконечный цикл игры
    for event in pygame.event.get(): #смотрим все появляющиеся события
        if event.type == pygame.QUIT: #нажатие на кнопку закрытия окна игры
            pygame.quit() #завершение игры
            sys.exit() #завершение работы программы 
        if event.type == pygame.MOUSEBUTTONDOWN: #нажатие на мышку
            pos = pygame.mouse.get_pos() #получение координат, где была нажата мышка
            clicked_sprites = [s for s in buttons_group if s.rect.collidepoint(pos)] #список всех объектов, на которые нажимали мышкой
            for sp in clicked_sprites: #просматриваем все такие объекты по одному
                if sp == play: #была нажата кнопка играть
                    cat.play() #кошка играет
                if sp == feed: #была нажата кнопка кормить
                    cat.feed() #кошка кушает
                if sp == sleep: #была нажата кнопка спать
                    cat.sleep() #кошка спит

    pygame.display.flip() #отображаем экран
    screen.blit(background, (0, 0)) #рисуем картинку на заднем фоне

    cat_group.update(screen) #обновляем состояние кошки
    cat_group.draw(screen) #отрисовываем изображение кошки на фоне

    if cat.is_sleeping: #если кошка спит
        screen.blit(night, (0, 0)) #то в комнате темно (на фон накладывается серый фильтр)
    
 
    buttons_group.draw(screen) #отрисовываем все кнопки на экране

    cursor.update() #обновляем положение курсора на экране
    cursor_group.draw(screen) #рисуем курсор

    clock.tick(update_time) #сколько времени будет отображаться текущая картинка