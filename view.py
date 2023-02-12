import pygame, random

class Cat(pygame.sprite.Sprite): #создание кошки
    boredom_delta = 0.35 #с какой скоростью кошке становится скучно
    hunger_delta = 0.75 #с какой скоростью кошка проголодается
    tiredness_delta = 0.45 #с какой скоростью кошка устаёт

    boredom_threshold = 200 #с какого момента кошка заскучает
    hunger_threshold = 250 #с какого момента кошка проголодается
    tiredness_threshold = 100 #с какого момента кошка захочет есть
 
    max_char_value = 1000 #максимальное значение всех характеристик

    progress_bar_width = 300 #ширина полоски показателя
    progress_bar_height = 30 #высота полоски показателя

    action_time = 20 #сколько времени длится одно состояние кошки

    normal_cat = pygame.image.load("sprites_data/normal_cat.png") #нормальное состояние кошки
    sad_cat = pygame.image.load("sprites_data/sad_cat.png") #грустное состояние кошки

    play_cat = pygame.image.load("sprites_data/play_cat.png") #кошка играет
    feed_cat = pygame.image.load("sprites_data/eat_cat.png") #кошка ест
    sleep_cat = pygame.image.load("sprites_data/sleep_cat.png") #кошка спит

    def __init__(self, pos_x, pos_y): #создание кошки
        pygame.sprite.Sprite.__init__(self) #создание рисунка кошки
        self.image = self.normal_cat #кошка создаётся в нормальном состоянии
        self.rect = self.image.get_rect() #узнаём размеры рисунка кошки
        self.rect.center = (pos_x, pos_y) #задаём центр размещения кошки на экране
        self.boredom = random.randint(self.boredom_threshold, self.max_char_value) #задаём случайное значение скуки кошки в начале
        self.hunger = random.randint(self.hunger_threshold, self.max_char_value) #задаём случайное значение сытости кошки в начале
        self.tiredness = random.randint(self.tiredness_threshold, self.max_char_value) #задаём случайное значение усталости кошки в начале
        self.is_sleeping = False #кошка не спит
        #progress bars
        self.boredom_progress_bar = ProgressBar(self.progress_bar_width, self.progress_bar_height, 
                                                570, 50, self.max_char_value, self.boredom) #создаём полоску с прогрессом скуки
        self.hunger_progress_bar = ProgressBar(self.progress_bar_width, self.progress_bar_height, 
                                               570, 95, self.max_char_value, self.hunger) #создаём полоску с прогрессом голода
        self.tiredness_progress_bar = ProgressBar(self.progress_bar_width, self.progress_bar_height, 
                                                  570, 140, self.max_char_value, self.tiredness) #создаём полоску с прогрессом усталости
        self.actions = [] #создаём массив действий

    def update(self, surface) : #функция обновления состояния кошки
        self.boredom = max(1, self.boredom - self.boredom_delta) #все показатели должны быть неотрицательными
        self.hunger = max(1, self.hunger - self.hunger_delta) #все показатели должны быть неотрицательными
        if self.is_sleeping == False: #если кошка не спит
            self.tiredness = max(1, self.tiredness - self.tiredness_delta) #усталость всегда больше нуля
        else: #если кошка спит
            self.tiredness = self.max_char_value #усталость минимальна
        #update progress bar
        self.boredom_progress_bar.update(self.boredom) #обновляем полосочку скуки с новым значением
        self.hunger_progress_bar.update(self.hunger) #обновляем полосочку голода с новым значением
        self.tiredness_progress_bar.update(self.tiredness) #обновляем полосочку усталости с новым значением
        self.boredom_progress_bar.draw(surface, (174, 74, 87)) #рисуем полоску скуки
        self.hunger_progress_bar.draw(surface, (206, 134, 39)) #рисуем полоску голода
        self.tiredness_progress_bar.draw(surface, (125, 181, 205)) #рисуем полоску усталости
        #check actions and mood:
        if not(self.is_sleeping): #если кошка не спит
            if len(self.actions) == 0 : #если никаких действий нет
                if self.boredom <= self.boredom_threshold or \
                    self.hunger <= self.hunger_threshold or \
                    self.tiredness <= self.tiredness_threshold:
                    self.image = self.sad_cat #если какой-то из показателей меньше нужного, то кошке становится грустно
                else :
                    self.image = self.normal_cat #кошке прям норм
            else:
                action = self.actions[0] #достаём действие 
                if (action[0] == 0):
                    self.image = self.play_cat #кошка играет
                elif (action[0] == 1):
                    self.image = self.feed_cat #кошка ест
                self.actions[0][1] -= 1 
                if self.actions[0][1] == 0: #кошка спит, мы ей не мешаем
                    self.actions.pop(0)

 
    def play(self): #кошка играет
        if not(self.is_sleeping): #если кошка не спит
            self.boredom = self.max_char_value #характеристика на максимум
            self.boredom_progress_bar.update(self.boredom) #обновляем полосочку
            self.actions.append([0, self.action_time]) #добавляем действие
        

    def feed(self): #кошка ест
        if not(self.is_sleeping): #если кошка не спит
            self.hunger = self.max_char_value #характеристика на максимум
            self.hunger_progress_bar.update(self.hunger) #обновляем полосочку
            self.actions.append([1, self.action_time]) #добавляем действие
    
    def sleep(self): #кошка спит
        self.tiredness = self.max_char_value #характеристика на максимум
        self.tiredness_progress_bar.update(self.tiredness) #обновляем полосочку
        if self.is_sleeping: #если спит, то 
            self.is_sleeping = False #просыпаемся
            self.image = self.normal_cat #теперь мы норм кошка
        else : #если не спит
            self.is_sleeping = True #заснули 
            self.image = self.sleep_cat #теперь мы спящая кошка



class ProgressBar(): #создаём полосочки
    def __init__(self, width, height, x_pos, y_pos, max_val, current_percent = 0): #функция создания полосочки
        self.width = width #задаём ширину полосочки
        self.height = height #задаём высоту полосчки
        self.current_percent = current_percent #какой процент характеристики
        self.x_pos = x_pos #узнаём x позицию
        self.y_pos = y_pos #узнаём y позицию
        self.max_value = max_val #задаём максимальное значение характеристики

    def update(self, current_val) : #функция обновления полосочки 
        self.current_percent = current_val / self.max_value #процент заполнения полосочки
    
    def draw(self, surface, color): #рисуем полосочку
        filled = self.current_percent * self.width #узнаём насколько она заполнена
        pygame.draw.rect(surface, color, pygame.Rect(self.x_pos, self.y_pos, filled, self.height)) #рисуем прямоугольник с цветом
        pygame.draw.rect(surface, (0, 0, 0), pygame.Rect(self.x_pos, self.y_pos, self.width, self.height), 5) #рисуем края



class Cursor(pygame.sprite.Sprite): #создаём курсор 
    def __init__(self): #функция создания курсора
        pygame.sprite.Sprite.__init__(self) #создаём картинку для курсора
        self.image = pygame.image.load("sprites_data/cursor.png") #загружаем картинку для курсора
        self.rect = self.image.get_rect() #узнаём размеры картинки курсора
    def update(self): #обновляем состояние курсора
        self.rect.center = pygame.mouse.get_pos() #узнаём позицию курсора на экране

    

class Button(pygame.sprite.Sprite): #создаём кнопочки
    def __init__(self, pos_x, pos_y, image_path) : #функция создания кнопочки
        pygame.sprite.Sprite.__init__(self) #создание рисунка кнопки
        self.image = pygame.image.load(image_path) #загружаем картинку анопки
        self.rect = self.image.get_rect() #узнаём размеры картинки
        self.rect.center = (pos_x, pos_y) #узнаём координаты центра картинки
