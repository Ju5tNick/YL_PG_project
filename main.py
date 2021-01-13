import pygame
from random import randrange, choice

X, Y = 40, 20


class MainHero:
    def __init__(self, coords, name, hp):
        self.coords, self.hp, self.name, self.weapons, self.weapon = coords, hp, name, [], None
        self.image = pygame.image.load(f"data/images/mainhero/knight.png")

    def is_alive(self):
        return True if self.hp > 0 else False
    
    def get_damage(self, amount):
        self.hp -= amount
        
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
        self.coords[0] += del_x
        self.coords[1] += del_y
            
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


def render_map(chunk: list):
    render_map = pygame.sprite.Group()
    for rrow in range(Y):
        for rcol in range(X):
            tile = pygame.sprite.Sprite()
            if chunk[rrow][rcol] == 1:
                image = pygame.image.load(f"data/images/grass/grass{str(choice(list(range(1, 7))))}.png")
            elif chunk[rrow][rcol] == 3:
                image = pygame.image.load(f"data/images/sand/sand{str(choice(list(range(1, 4))))}.png")
            elif chunk[rrow][rcol] == 0:
                image = pygame.image.load(f"data/images/water/water3{str(choice(list(range(1, 4))))}.png")
            else:
                image = pygame.image.load(f"data/images/water/water1.png")

            tile.image = image
            tile.rect = image.get_rect()
            tile.rect.x, tile.rect.y = rcol * 25, rrow * 25
            render_map.add(tile)
    render_map.draw(screen)
    pygame.display.flip()


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
         
            if randrange(300) in range(1) and flag == False: # 0.33% шанс что новый тайл будет "началом" водоема
                if 2 < i < Y - 12:
                    r_lenght, r_width, flag = randrange(2, 4), randrange(7, 14), True  # длина и ширина будущего водоема
                    r_lenght_2, loc_x, r_width_2 = r_lenght, randrange(13, X - 15), r_width 
         
            if flag and r_lenght_2 != 0 and intermediate.count(1) == loc_x:
                intermediate.append(0)
                r_lenght_2 -= 1
            
            elif len(intermediate) != X:
                intermediate.append(1)
            
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
                if i < Y - 1 and chunk[i][j] in [1, 3] and chunk[i + 1][j] == 0:
                    chunk[i][j] = 3
                    chunk[i - 1][j] = 3 if i < Y - 2 else 1
                    chunk[i][j - 1] = 3 if j != X - 2 else 1

                if i - 1 != 0 and chunk[i][j] in [1, 3] and chunk[i - 1][j] == 0:
                    chunk[i][j] = 3
                    if i + 1 < Y:
                        chunk[i + 1][j] = 3 
                    chunk[i][j - 1] = 3 if j - 2 > 0 else 1     

                if j < X - 1 and chunk[i][j] in [1, 3] and chunk[i][j + 1] == 0:
                    chunk[i][j] = 3
                    chunk[i][j - 1] = 3 if j < X - 2 else 1

                if j - 1 > 0 and chunk[i][j] in [1, 3] and chunk[i][j - 1] == 0:
                    chunk[i][j] = 3
                    chunk[i][j + 1] = 3 if j - 2 > 0 else 1

                if i < Y - 2 and j < X - 2 and chunk[i][j] == 0 and chunk[i + 1][j + 1] == 1:
                    chunk[i + 1][j + 1] = 3 
                if i - 2 != 0 and j < X - 2 and chunk[i][j] == 0 and chunk[i - 1][j + 1] == 1:
                    chunk[i - 1][j + 1] = 3
    return chunk


def save():
    chunks_file = open("chunks.txt", "w")
    for elem in chunks:
        chunks_file.write(''.join(elem) + "\n")


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((X * 25, Y * 25))
    
    chunks_file = open("chunks.txt", "r")
    flag, characters = False, []
    chunks = list(chunks_file.read())
    running = True
    clock = pygame.time.Clock()
    
    hero = MainHero([0, 0], 'name', 200)  # координаты окна
    characters.append(hero)
    last_x, last_y, x, y, w, h, chunk = hero.get_coords()[0], hero.get_coords()[1], hero.get_coords()[0], hero.get_coords()[1], X, Y, generate()
    render_map(chunk)
    render_character(characters)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #save()
                running = False
            if event.type == pygame.KEYDOWN:
                flag = True
                keys = pygame.key.get_pressed()
                last_x, last_y = hero.get_coords()[0], hero.get_coords()[1]
                if keys[pygame.K_w]:
                    hero.make_move(del_y=-25)
                if keys[pygame.K_a]:
                    hero.make_move(del_x=-25)
                if keys[pygame.K_s]:
                    hero.make_move(del_y=25)
                if keys[pygame.K_d]:
                    hero.make_move(del_x=25)
                x, y = hero.get_coords()[0], hero.get_coords()[1]
        '''if (x // w, y // h) != (last_x // w, last_y // h):
            if f"{x // w}:{y // h}" not in chunks:
                chunk = generate()
                render_map(chunk)

                chunks.append(f"{x // w}:{y // h}")
                new_chunk = open(f"chunks/chunk{x // w}{y // h}.txt", "w")
                for i in range(Y):
                    new_chunk.write(''.join(str(chunk[i])) + "\n")
            else:
                chunk = open(f"chunks/chunk{x // w}{y // h}.txt", "r").read().split("\n")
                render_map(chunk)'''
        if flag:
            render_map(chunk)
            render_character(characters)
            last_x, last_y = hero.get_coords()[0], hero.get_coords()[1]
            pygame.display.flip()
            clock.tick(100)
            flag = False