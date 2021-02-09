import pygame
from random import randrange, choice

X, Y, FIELD_X, FIELD_Y = 40, 20, 5, 5

#  +-------TILES------+
#  | 0 - 5   -- grass |
#  | 6 - 8   -- water |
#  | 9 - 11  -- sand  |
#  +------------------+


class MainHero(pygame.sprite.Sprite):
    def __init__(self, coords, name, hp):
        super().__init__(all_sprites)
        self.coords, self.hp, self.name, self.weapons, self.weapon = coords, hp, name, [], None
        self.rect, self.animation_counter = pygame.Rect(coords[0], coords[1], 19, 31), 0

        self.moves = {
            "up": (0, -4), "down": (0, 4),
            "left": (-4, 0), "right": (4, 0)
            }

        self.still = {
            "up": pygame.image.load("data/images/mainhero/knight11.png"),
            "down": pygame.image.load("data/images/mainhero/knight2.png"),
            "left": pygame.image.load("data/images/mainhero/knight5.png"),
            "right": pygame.image.load("data/images/mainhero/knight8.png")
           }

        self.directions = {
            "up": [pygame.image.load("data/images/mainhero/knight9.png"), pygame.image.load("data/images/mainhero/knight10.png")],
            "down": [pygame.image.load("data/images/mainhero/knight0.png"), pygame.image.load("data/images/mainhero/knight1.png")],
            "left": [pygame.image.load("data/images/mainhero/knight3.png"), pygame.image.load("data/images/mainhero/knight4.png")],
            "right": [pygame.image.load("data/images/mainhero/knight7.png"), pygame.image.load("data/images/mainhero/knight6.png")]
            }

        self.cur_frame = 0
        self.image = pygame.image.load("data/images/mainhero/knight2.png")
        self.rect = self.rect.move(coords[0], coords[1])

    def move(self, direction, stop=False):
        self.rect = self.rect.move(*self.moves[direction])
        if stop:
            self.image = self.still[direction]
        else:
            self.update(direction)

    def update(self, direction):
        if self.animation_counter == 5:
            self.frames = self.directions[direction]
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.animation_counter = 0
        self.animation_counter += 1

    def is_alive(self):
        return True if self.hp > 0 else False
    
    def get_damage(self, amount):
        self.hp -= amount

    def set_coords(self, new_x, new_y):
        self.rect.x, self.rect.y = new_x, new_y

    def get_coords(self):
        return (self.rect.x, self.rect.y)

    def get_weapons(self):
        return self.weapons

    def get_name(self):
        return self.name

    def get_hp(self):
        return self.hp

    def get_image(self):
        return self.image

    def get_info(self):
        weapons = ', '.join([weapon.get_name().capitalize() for weapon in self.weapons])
        return f'{self.name}\nЗдоровья: {self.hp} hp\nОружие:\n{weapons}\n\nТекущее оружие: {self.get_weapon().get_info()}'

    def get_weapon(self):
        return self.weapons[0] if self.weapon == None else self.weapon

    def make_move(self, del_x=0, del_y=0):
        self.coords[0], self.coords[1] = self.coords[0] + del_x, self.coords[1] + del_y

    def add_weapon(self, weapon):
        if type(weapon) is Weapon:
            self.weapons.append(weapon)
            self.weapon = weapon
            return f'Подобрал {weapon.get_name().lower()}'
        return 'Это не оружие'
            
    def next_weapon(self):
        if self.get_weapon() == None:
            return 'Я безоружен'
        elif len(self.weapons) == 1:
            return 'У меня только одно оружие'
        else:
            a = self.weapons.index(self.weapon)
            if a + 1 == len(self.weapons):
                self.weapon = self.weapons[0]
            else:
                self.weapon = self.weapons[a + 1]
            return f'Сменил оружие на {self.weapon.get_name()}'
    
    def heal(self, amount):
        self.hp = 200 if self.hp + amount > 200 else self.hp + amount
        return f'Полечился, теперь здоровья {self.hp}'



def render_map(chunk: list):
    render_map = pygame.sprite.Group()
    for rrow in range(Y):
        for rcol in range(X):
            tile = pygame.sprite.Sprite()
            if chunk[rrow][rcol] in range(6):
                image = pygame.image.load(f"data/images/tiles/grass/grass{chunk[rrow][rcol] + 1}.png")  
            elif chunk[rrow][rcol] in range(6, 9):
                image = pygame.image.load(f"data/images/tiles/water/water3{chunk[rrow][rcol] - 5}.png") 
            elif chunk[rrow][rcol] in range(9, 12):
                image = pygame.image.load(f"data/images/tiles/sand/sand{chunk[rrow][rcol] - 8}.png")  

            tile.image = image
            tile.rect = image.get_rect()
            tile.rect.x, tile.rect.y = rcol * 25, rrow * 25
            render_map.add(tile)
    return render_map


def load_image(name, colorkey=None):
    if not os.path.isfile(os.path.join('data', name)):
        print(f"Файл с изображением '{os.path.join('data', name)}' не найден")
        sys.exit()
    return pygame.image.load(os.path.join('data', name))


def generate():
    chunk, flag = [], False
    for i in range(Y):
        intermediate = []
        for j in range(X): 
         
            if randrange(100) in range(1) and flag == False: # 0.33% шанс что новый тайл будет "началом" водоема
                if 2 < i < Y - 12:
                    r_lenght, r_width, flag = randrange(2, 4), randrange(7, 14), True  # длина и ширина будущего водоема
                    r_lenght_2, loc_x, r_width_2 = r_lenght, randrange(13, X - 15), r_width 
         
            if flag and r_lenght_2 != 0 and sum([intermediate.count(i) for i in range(6)]) == loc_x:
                intermediate.append(randrange(6, 9))
                r_lenght_2 -= 1
            
            elif len(intermediate) != X:
                intermediate.append(randrange(6))
                if randrange(100) in range(1):
                    tile = pygame.sprite.Sprite()
                    image = pygame.image.load(f"data/images/objects/rock.png")  
                    tile.image = image
                    tile.rect = image.get_rect()
                    tile.rect.x, tile.rect.y = j * 26 + randrange(15), i * 26 + randrange(15)
                    other_object.add(tile)
                
        if flag:
            if r_width - r_width_2 in range(0, int(r_width / 2)):
                r_lenght, loc_x = r_lenght + randrange(choice([1, 2]), 4), loc_x - randrange(1, 3)
            elif r_width - r_width_2 in range(int(r_width / 2) + 1, r_width):
                r_lenght, loc_x = r_lenght - randrange(choice([1, 2]), 4), loc_x + randrange(1, 3)

            r_width_2, r_lenght_2 = r_width_2 - 1, r_lenght
            flag = False if r_width_2 == 0 else True  

        chunk.append(intermediate)

    if choice([True, False, False]):  # 33% водоем будyт с песком
        for i in range(Y):  # окантовка водоемов "песком"
            for j in range(X):
                if i < Y - 1 and chunk[i][j] in list(range(6)) + list(range(9, 12)) and chunk[i + 1][j] in list(range(6, 9)):
                    chunk[i][j] = randrange(9, 12)
                    chunk[i - 1][j] = randrange(9, 12) if i < Y - 2 else 1
                    chunk[i][j - 1] = randrange(9, 12) if j != X - 2 else 1

                if i - 1 != 0 and chunk[i][j] in list(range(6)) + list(range(9, 12)) and chunk[i - 1][j] in list(range(6, 9)):
                    chunk[i][j] = randrange(9, 12)
                    if i + 1 < Y:
                        chunk[i + 1][j] = randrange(9, 12) 
                    chunk[i][j - 1] = randrange(9, 12) if j - 2 > 0 else 1     

                if j < X - 1 and chunk[i][j] in list(range(6)) + list(range(9, 12)) and chunk[i][j + 1] in list(range(6, 9)):
                    chunk[i][j] = randrange(9, 12)
                    chunk[i][j - 1] = randrange(9, 12) if j < X - 2 else 1

                if j - 1 > 0 and chunk[i][j] in list(range(6)) + list(range(9, 12)) and chunk[i][j - 1] in list(range(6, 9)):
                    chunk[i][j] = randrange(9, 12)
                    chunk[i][j + 1] = randrange(9, 12) if j - 2 > 0 else 1

                if i < Y - 2 and j < X - 2 and chunk[i][j] in list(range(6, 9)) and chunk[i + 1][j + 1] in list(range(6)):
                    chunk[i + 1][j + 1] = randrange(9, 12) 
                if i - 2 != 0 and j < X - 2 and chunk[i][j] in list(range(6, 9)) and chunk[i - 1][j + 1] in list(range(6)):
                    chunk[i - 1][j + 1] = randrange(9, 12)
    return chunk


def save():
    pass


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((X * 25, Y * 25))

    all_sprites = pygame.sprite.Group()
    running, field = True, [[None for _ in range(FIELD_X)] for _ in range(FIELD_Y)]
    cur_x, cur_y = 2, 2
    clock = pygame.time.Clock()

    characters = pygame.sprite.Group()
    mainhero = pygame.sprite.Group()
    other_object = pygame.sprite.Group()
    
    hero = MainHero([10, 10], 'name', 200)  # координаты окна
    mainhero.add(hero)
    up, down, left, right = False, False, False, False 

    last_x, last_y, x, y, w, h = hero.get_coords()[0], hero.get_coords()[1], hero.get_coords()[0], hero.get_coords()[1], X, Y
    game_map = render_map(generate())
    game_map.draw(screen)
    field[cur_y][cur_x] = game_map
    mainhero.draw(screen)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #save()
                running = False

            if event.type == pygame.KEYDOWN:
                keys, flag = pygame.key.get_pressed(), True
                last_x, last_y = hero.get_coords()[0], hero.get_coords()[1]

                if keys[pygame.K_w]:
                    up, down = True, False
                if keys[pygame.K_a]:
                    left, right = True, False
                if keys[pygame.K_s]:
                    down, up = True, False
                if keys[pygame.K_d]:
                    right, left = True, False
                    
                    
            if event.type == pygame.KEYUP:
                if keys[pygame.K_w]:
                    up = False
                    hero.move("up", stop=True) 
                if keys[pygame.K_a]:
                    left = False
                    hero.move("left", stop=True)
                if keys[pygame.K_s]:
                    down = False
                    hero.move("down", stop=True)
                if keys[pygame.K_d]:
                    right = False
                    hero.move("right", stop=True)

        if up:
            hero.move("up")
        elif down:
            hero.move("down")
        elif left:
            hero.move("left")
        elif right:
            hero.move("right")

        x, y = hero.get_coords()[0], hero.get_coords()[1]

        if X * 25 <= x or x <= 0 or Y * 25 <= y or y <= 0:
            if X * 25 <= x:
                cur_x += 1
            if x <= 0:
                cur_x -= 1
            if Y * 25 <= y:
                cur_y += 1
            if  y <= 0:
                cur_y -= 1

            cur_x = FIELD_X - 1 if cur_x < 0 else cur_x
            cur_y = FIELD_Y - 1 if cur_y < 0 else cur_y
            cur_x = 0 if cur_x >= FIELD_X else cur_x
            cur_y = 0 if cur_y >= FIELD_Y else cur_y

            if field[cur_y][cur_x] is None:
                game_map = render_map(generate())
                field[cur_y][cur_x] = game_map
            else:
                game_map = field[cur_y][cur_x]
            print(*field, sep="\n")
            print()

        if X * 25 <= hero.get_coords()[0]:
            hero.set_coords(0 , hero.get_coords()[1])

        elif hero.get_coords()[0] <= 0:
            hero.set_coords(X * 25, hero.get_coords()[1])

        if Y * 25 <= hero.get_coords()[1]:
            hero.set_coords(hero.get_coords()[0], 0)

        elif hero.get_coords()[1] <= 0:
            hero.set_coords(hero.get_coords()[0], Y * 25)


        game_map.draw(screen)
        mainhero.draw(screen)
        other_object.draw(screen)

        pygame.display.flip()
        clock.tick(120)