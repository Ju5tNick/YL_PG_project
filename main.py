import pygame
import numpy
from random import randrange, choice

X, Y = 40, 20

#  +------TILES------+
#  | 0 - 5   -- grass|
#  | 6 - 8   -- water|
#  | 9 - 11  -- sand |
#  +-----------------+


class MainHero:
    def __init__(self, coords, name, hp):
        self.coords, self.hp, self.name, self.weapons, self.weapon = coords, hp, name, [], None
        self.image = pygame.image.load(f"data/images/mainhero/knight.png")

    def is_alive(self):
        return True if self.hp > 0 else False
    
    def get_damage(self, amount):
        self.hp -= amount

    def set_coords(self, new_x, new_y):
        self.coords = [new_x, new_y]
        
    def get_coords(self):
        return self.coords

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
        if self.coords[0] >= X * 25:
            self.coords[0] = 0
        elif self.coords[0] <= 0:
            self.coords[0] = X * 25 - 20

        if self.coords[1] >= Y * 25:
            self.coords[1] = 0
        elif self.coords[1] <= 0:
            self.coords[1] = Y * 25 - 29
            
    def add_weapon(self, weapon):
        if type(weapon) is Weapon:
            self.weapons.append(weapon)
            self.weapon = weapon
            return f'Подобрал {weapon.get_name().lower()}'
        else:
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


def render_map(chunk: list, flag=False):
    render_map = pygame.sprite.Group()
    if flag:
        for rrow in range(Y):
            for rcol in range(X):
                tile = pygame.sprite.Sprite()
                if chunk[rrow][rcol] in range(6):
                    image = pygame.image.load(f"data/images/grass/grass{chunk[rrow][rcol] + 1}.png")  # {str(choice(list(range(1, 7))))}.png")
                elif chunk[rrow][rcol] in range(6, 9):
                    image = pygame.image.load(f"data/images/water/water3{chunk[rrow][rcol] - 5}.png")  # {str(choice(list(range(1, 4))))}.png")
                elif chunk[rrow][rcol] in range(9, 12):
                    image = pygame.image.load(f"data/images/sand/sand{chunk[rrow][rcol] - 8}.png")  # {str(choice(list(range(1, 4))))}.png")
                else:
                    image = pygame.image.load(f"data/images/water/water1.png")

                tile.image = image
                tile.rect = image.get_rect()
                tile.rect.x, tile.rect.y = rcol * 25, rrow * 25
                render_map.add(tile)
    return render_map


def render_character(characters):
    loc_of_char = pygame.sprite.Group()
    for char in characters:
        tile = pygame.sprite.Sprite()
        tile.image = char.get_image()
        tile.rect = tile.image.get_rect()
        tile.rect.x, tile.rect.y = char.get_coords()[0], char.get_coords()[1]
        loc_of_char.add(tile)
    loc_of_char.draw(screen)
    pygame.display.flip()


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
         
            if randrange(300) in range(300) and flag == False: # 0.33% шанс что новый тайл будет "началом" водоема
                if 2 < i < Y - 12:
                    r_lenght, r_width, flag = randrange(2, 4), randrange(7, 14), True  # длина и ширина будущего водоема
                    r_lenght_2, loc_x, r_width_2 = r_lenght, randrange(13, X - 15), r_width 
         
            if flag and r_lenght_2 != 0 and sum([intermediate.count(i) for i in range(6)]) == loc_x:
                intermediate.append(randrange(6, 9))
                r_lenght_2 -= 1
            
            elif len(intermediate) != X:
                intermediate.append(randrange(6))
            
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
    open("chunks.txt", "w").write(' '.join(chunks))


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((X * 25, Y * 25))

    characters = []
    chunks = open("chunks.txt", "r").read().split()
    running = True
    clock = pygame.time.Clock()
    
    hero = MainHero([0, 0], 'name', 200)  # координаты окна
    characters.append(hero)
    up, down, left, right = False, False, False, False 
    last_x, last_y, x, y, w, h, chunk = hero.get_coords()[0], hero.get_coords()[1], hero.get_coords()[0], hero.get_coords()[1], X, Y, generate()
    game_map = render_map(chunk, flag=True)
    game_map.draw(screen)
    render_character(characters)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save()
                running = False

            if event.type == pygame.KEYDOWN:
                keys, flag = pygame.key.get_pressed(), True
                last_x, last_y = hero.get_coords()[0], hero.get_coords()[1]

                if keys[pygame.K_w] :
                    up = True
                if keys[pygame.K_a]:
                    left = True 
                if keys[pygame.K_s]:
                    down = True
                if keys[pygame.K_d]:
                    right = True
                    
                x, y = hero.get_coords()[0], hero.get_coords()[1]

            if event.type == pygame.KEYUP:
                if keys[pygame.K_w] :
                    up = False 
                if keys[pygame.K_a]:
                    left = False
                if keys[pygame.K_s]:
                    down = False
                if keys[pygame.K_d]:
                    right = False

        if up:
            hero.make_move(del_y=-5)
        if down:
            hero.make_move(del_y=5)
        if left:
            hero.make_move(del_x=-5)
        if right:
            hero.make_move(del_x=5)

        '''if X * 25 < x or x < 0 or Y * 25 < y or y < 0:


            if f"{x // w}:{y // h}" not in chunks:
                chunk = generate()
                render_map(chunk)

                chunks.append(f"{x // w}:{y // h}")
                new_chunk = open(f"chunks/chunk{x // w}{y // h}.txt", "w")
                for i in range(Y):
                    new_chunk.write(' '.join(str(chunk[i])) + "\n")
            else:
                chunk = open(f"chunks/chunk{x // w}{y // h}.txt", "r").read().split()
                render_map(chunk)'''

        if up or down or left or right:
            game_map.draw(screen)
            render_character(characters)

        pygame.display.flip()
        clock.tick(120)