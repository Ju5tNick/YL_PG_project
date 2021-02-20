import os
import sys
import pygame
import schedule

from random import randrange, choice
from math import asin, radians, degrees, sin

X, Y, FIELD_X, FIELD_Y = 40, 20, 5, 5
TILE_WIDTH, TILE_HEIGT = 25, 25

#  +-------TILES------+
#  | 0 - 5   -- grass |
#  | 6 - 8   -- water |
#  | 9 - 11  -- sand  |
#  +------------------+

class Tile_can_go(pygame.sprite.Sprite):

    def __init__(self, way, x, y):
        super().__init__(all_sprites)
        self.image = load_image(way)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x * TILE_WIDTH, y * TILE_HEIGT


class Tile_cant_go(pygame.sprite.Sprite):

    def __init__(self, way, x, y):
        super().__init__(all_sprites)
        self.image = load_image(way)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x, self.rect.y = x * TILE_WIDTH, y * TILE_HEIGT


class MainHero(pygame.sprite.Sprite):

    def __init__(self, coords, name, hp):
        super().__init__(all_sprites)
        self.coords, self.hp, self.name, self.weapon, self.weapons = coords, hp, name, None, []
        self.rect, self.animation_counter, self.balance, self.xp_progress = pygame.Rect(coords[0], coords[1], 19, 31), 0, 0, 0
        self.required_xp, self.level, self.max_hp = 100, 0, hp

        self.moves = {
            "up": (0, -4), "down": (0, 4),
            "left": (-4, 0), "right": (4, 0)
            }

        self.still = {
            "up": load_image("data/images/mainhero/knight11.png"),
            "down": load_image("data/images/mainhero/knight2.png"),
            "left": load_image("data/images/mainhero/knight5.png"),
            "right": load_image("data/images/mainhero/knight8.png")
            }

        self.directions = {
            "up": [load_image("data/images/mainhero/knight9.png"), load_image("data/images/mainhero/knight10.png")],
            "down": [load_image("data/images/mainhero/knight0.png"), load_image("data/images/mainhero/knight1.png")],
            "left": [load_image("data/images/mainhero/knight3.png"), load_image("data/images/mainhero/knight4.png")],
            "right": [load_image("data/images/mainhero/knight7.png"), load_image("data/images/mainhero/knight6.png")]
            }

        self.cur_frame = 0
        self.image = load_image("data/images/mainhero/knight2.png")
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.rect.move(coords[0], coords[1])

    def move(self, direction, stop=False):
        self.rect = self.rect.move(*self.moves[direction])
        if stop:
            self.image = self.still[direction]
            self.mask = pygame.mask.from_surface(self.image)
        else:
            self.update(direction)

    def get_hp(self):
        return self.hp

    def get_max_hp(self):
        return self.max_hp

    def get_damage(self, damage):
        self.hp -= damage

    def update(self, direction):
        if self.animation_counter == 5:
            self.frames = self.directions[direction]
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.animation_counter = 0
            self.mask = pygame.mask.from_surface(self.image)
            if self.hp <= self.max_hp:
                self.hp += 1
        self.animation_counter += 1

    def is_alive(self):
        return True if self.hp > 0 else False

    def set_coords(self, new_x, new_y):
        self.rect.x, self.rect.y = new_x, new_y

    def get_coords(self):
        return self.rect.x, self.rect.y

    def get_info(self):
        weapons = ', '.join([weapon.get_name().capitalize() for weapon in self.weapons])
        return f'{self.name}\nЗдоровья: {self.hp} hp\nОружие:\n{weapons}\n\nТекущее оружие: {self.get_weapon().get_info()}'

    def get_balance(self):
        return self.balance

    def add_weapon(self, weapon):
        if type(weapon) is Weapon:
            self.weapons.append(weapon)
            self.weapon = weapon
            weapons.add(weapon)

    def attack(self, enemy):
        enemy.get_damage(self.weapon.get_damage())

    def check_level(self):
        while self.xp_progress >= self.required_xp:
            self.level += 1
            self.xp_progress -= self.required_xp
            self.required_xp += 10


class Weapon(pygame.sprite.Sprite):

    def __init__(self, damage, coords, range):
        super().__init__(all_sprites)
        self.image, self.default_image = load_image("data/images/sword/sword.png"), load_image("data/images/sword/sword.png")
        self.mask, self.range, self.damage = pygame.mask.from_surface(self.image), range, damage
        self.rect, self.crossing = self.image.get_rect(), True

        self.flips = {"++": -90, "=+": -135, "-+": -180, "-=": 135, "": -1,
                      "--": 90, "=-": 45, "+-": 0, "+=": -45, "==": -1}

    def move(self, x, y, del_x, del_y):
        if self.flips[''.join(self.check(del_x, del_y))] != -1:
            self.image = pygame.transform.rotate(self.default_image, self.flips[''.join(self.check(del_x, del_y))])
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x, self.rect.y = x, y
        hurt_enemies = pygame.sprite.spritecollide(self, enemies, False)
        if self.crossing:
            for enemy in hurt_enemies:
                hero.attack(enemy)
        self.crossing = True if not pygame.sprite.spritecollide(self, enemies, False) else False

    def get_range(self):
        return self.range

    def get_damage(self):
        return self.damage

    def check(self, x, y):
        result = ["", ""]
        result[0] = "+" if x > 0 else "-"
        result[1] = "+" if y > 0 else "-"
        result[0] = "=" if x in range(-3, 4) else result[0]
        result[1] = "=" if y in range(-3, 4) else result[1]
        return result


class Enemy(pygame.sprite.Sprite):

    def __init__(self, name, base_damage, base_health, base_speed, range, gold_drops, xp_drops):
        super().__init__(all_sprites)
        self.name, self.damage, self.health, self.speed = name, base_damage, base_health, base_speed
        self.range, self.die_flag, self.max_health = range, False, base_health
        self.rect = pygame.Rect(*[randrange(50, X * TILE_WIDTH - 50), randrange(50, Y * TILE_HEIGT - 50)], 21, 24)
        while pygame.sprite.spritecollideany(self, cant_go_tiles):
            self.rect = pygame.Rect(*[randrange(50, X * TILE_WIDTH - 50), randrange(50, Y * TILE_HEIGT - 50)], 21, 24)
        
        self.get_angry = False
        self.animation_counter = 0

        self.still = [load_image("data/images/enemies/slime/static/0.png"), load_image("data/images/enemies/slime/static/1.png"),
                      load_image("data/images/enemies/slime/static/2.png"), load_image("data/images/enemies/slime/static/3.png"),
                      load_image("data/images/enemies/slime/static/4.png"), load_image("data/images/enemies/slime/static/5.png"),
                      load_image("data/images/enemies/slime/static/6.png")]
        self.moves = [load_image("data/images/enemies/slime/move/0.png"), load_image("data/images/enemies/slime/move/1.png"),
                      load_image("data/images/enemies/slime/move/2.png"), load_image("data/images/enemies/slime/move/3.png"),
                      load_image("data/images/enemies/slime/move/4.png"), load_image("data/images/enemies/slime/move/5.png"),
                      load_image("data/images/enemies/slime/move/6.png"), load_image("data/images/enemies/slime/move/7.png")]
        self.angry_moves = [load_image("data/images/enemies/slime/angry_move/0.png"), load_image("data/images/enemies/slime/angry_move/1.png")]
        self.gets_angry = [load_image("data/images/enemies/slime/gets_angry/0.png"), load_image("data/images/enemies/slime/gets_angry/1.png"),
                           load_image("data/images/enemies/slime/gets_angry/2.png"), load_image("data/images/enemies/slime/gets_angry/3.png"),
                           load_image("data/images/enemies/slime/gets_angry/4.png")]
        self.die_ani = [load_image("data/images/enemies/slime/die/0.png"), load_image("data/images/enemies/slime/die/1.png"),
                        load_image("data/images/enemies/slime/die/2.png"), load_image("data/images/enemies/slime/die/3.png"),
                        load_image("data/images/enemies/slime/die/4.png"), load_image("data/images/enemies/slime/die/5.png")]

        self.image = load_image("data/images/enemies/slime/static/0.png")
        self.cur_frame, self.frames = 0, []

        self.vision = Vision_for_enemy(100, (self.rect.x, self.rect.y), self)
        enemy_visions.add(self.vision)
        self.gold_drops, self.get_angry, self.angry = gold_drops, False, False
        self.xp_drops, self.flag, self.can_move = xp_drops, -1, True

    def move(self, hero_coords):
        flag = True
        if self.frames == self.die_ani:
            self.can_move = False
        if self.vision.check():
            if self.can_move:
                self.get_angry = True
                move = [self.speed, 0, -self.speed]                

                diff_y, diff_x = abs(hero_coords[0] - self.rect.x), abs(hero_coords[1] - self.rect.y)
                del_x, del_y = 0, 0
            
                if abs(hero_coords[0]) - abs(self.rect.x) != 10:
                    for elem in move:
                        if abs(hero_coords[0] - (self.rect.x + elem)) < diff_y:
                            del_y, flag = elem, False
                            
                if abs(hero_coords[1]) - abs(self.rect.y) != 20:
                    for elem in move:
                        if abs(hero_coords[1] - (self.rect.y + elem)) < diff_x:
                            del_x, flag = elem, False
                        
                self.vision.move(del_y, del_x)
                self.rect = self.rect.move(del_y, del_x)
        else:
            if self.angry and self.get_angry:
                self.angry, self.get_angry = False, False
            if self.flag == 1 and not self.angry and not self.get_angry and self.direction != [0, 0] and self.can_move:
                flag = False
                if self.rect.x + 1 >= X * TILE_WIDTH - 50:
                    self.direction[0] = -1
                elif self.rect.x - 1 <= 50:
                    self.direction[0] = 1
                if self.rect.y + 1 >= Y * TILE_HEIGT - 50:
                    self.direction[1] = -1
                elif self.rect.y - 1 <= 50:
                    self.direction[1] = 1
                self.rect = self.rect.move(self.direction[0], self.direction[1])
                self.vision.move(self.direction[0], self.direction[1])

        

        self.update(stop=flag)

    def update(self, stop=False):
        if self.animation_counter == 5:
            if not self.die_flag:
                if self.angry:
                    self.frames, self.speed, self.can_move = self.angry_moves, 3, True
                    self.angry = False if not self.vision.check() else True
                elif self.get_angry:
                    self.frames, self.can_move = self.gets_angry, False
                    if self.cur_frame == 3:
                        self.angry, self.get_angry = True, False
                else:
                    self.speed = 2
                    self.frames = self.still if stop else self.moves
            else:
                if self.image == self.die_ani[-1]:
                    self.kill()
                self.frames = self.die_ani
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.animation_counter = 0
            if self.health <= self.max_health:
                self.health += 1

            if abs(hero.get_coords()[0] - self.rect.x) <= 10 and abs(hero.get_coords()[1] - self.rect.y) <= 10:
                self.hit(hero)

        self.animation_counter += 1

    def set_flag(self):
        self.direction = [choice([1, 0, -1]), choice([1, 0, -1])]
        self.flag = -self.flag

    def get_damage(self, damage):
        self.health -= damage
        if -25 <= self.health <= -1:
            self.die(hero)

    def get_coords(self):
        return self.rect.x, self.rect.y

    def get_health(self):
        return self.health

    def get_max_health(self):
        return self.max_health
        
    def die(self, hero):
        if self.health <= 0:
            hero.balance += self.gold_drops
            hero.xp_progress += self.xp_drops
            hero.check_level()
            self.vision.kill()
            self.cur_frame, self.die_flag = 0, True
    
    def hit(self, hero):
        hero.get_damage(self.damage + __import__("random").randint(-(self.damage // 10), self.damage // 10))
        
    def get_stats(self):
        return (self.name, self.damage, self.health, self.speed, self.range)


class Vision_for_enemy(pygame.sprite.Sprite):

    def __init__(self, range, coords, enemy):
        super().__init__(all_sprites)
        self.host, self.range = enemy, range
        self.image = pygame.Surface((3 * self.range, 3 * self.range), pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, (70, 79, 21), (self.range, self.range), self.range, 1)
        pygame.draw.rect(self.image, (255, 0, 0), (self.range - 10, self.range - 16, 22, 5))
        self.rect = pygame.Rect(coords[0] - self.range + 10.5, coords[1] - self.range + 12, 1.85 * self.range, 1.85 * self.range)

    def update(self):
        pygame.draw.rect(self.image, (0, 0, 0), (self.range - 10, self.range - 16, 22, 5))
        pygame.draw.rect(self.image, (255, 0, 0), (self.range - 9, self.range - 15, (self.host.get_health() / self.host.get_max_health() * 22 - 2), 3))

    def move(self, del_x, del_y):
        self.rect = self.rect.move(del_x, del_y)

    def check(self):
        return pygame.sprite.spritecollideany(self, mainhero)
        
        
def render_map(chunk: list):
    cant_go = pygame.sprite.Group()
    can_go = pygame.sprite.Group()
    for rrow in range(Y):
        for rcol in range(X):
            flag = False
            if chunk[rrow][rcol] in range(6):
                tile = Tile_can_go(f"data/images/tiles/grass/grass{chunk[rrow][rcol] + 1}.png", rcol, rrow)  
            elif chunk[rrow][rcol] in range(6, 9):
                tile, flag = Tile_cant_go(f"data/images/tiles/water/water3{chunk[rrow][rcol] - 5}.png", rcol, rrow), True
            elif chunk[rrow][rcol] in range(9, 12):
                tile = Tile_can_go(f"data/images/tiles/sand/sand{chunk[rrow][rcol] - 8}.png", rcol, rrow)  

            if flag:
                cant_go.add(tile)
            else:
                can_go.add(tile)
    return can_go, cant_go


def load_image(name, colorkey=None):
    if not os.path.isfile(name):
        print(f"Файл с изображением '{name}' не найден")
        sys.exit()
    return pygame.image.load(name)


def generate():
    other_object = pygame.sprite.Group()
    chunk, flag = [], False
    for i in range(Y):
        intermediate = []
        for j in range(X): 
         
            if randrange(300) in range(1) and flag == False: # 0.33% шанс что новый тайл будет "началом" водоема
                if 2 < i < Y - 12:
                    r_lenght, r_width, flag = randrange(2, 4), randrange(7, 14), True  # длина и ширина будущего водоема
                    r_lenght_2, loc_x, r_width_2 = r_lenght, randrange(13, X - 15), r_width 
         
            if flag and r_lenght_2 != 0 and sum([intermediate.count(i) for i in range(6)]) == loc_x:
                intermediate.append(randrange(6, 9))
                if randrange(100) in range(5):
                    tile = pygame.sprite.Sprite()
                    image = pygame.transform.rotate(load_image(f"data/images/objects/water_lily.png"), randrange(1, 361))  
                    tile.image = image
                    tile.rect = image.get_rect()
                    tile.rect.x, tile.rect.y = (j) * TILE_WIDTH + randrange(10), (i) * TILE_WIDTH + randrange(10)
                    other_object.add(tile)
                r_lenght_2 -= 1
            
            elif len(intermediate) != X:
                intermediate.append(randrange(6))
                if randrange(100) in range(50):
                    tile = pygame.sprite.Sprite()
                    image = load_image(f"data/images/objects/tall_grass.png")  
                    tile.image = image
                    tile.rect = image.get_rect()
                    tile.rect.x, tile.rect.y = (j - 0.5) * 26 + randrange(10), (i - 0.5) * 26 + randrange(10)
                    other_object.add(tile)
                
        if flag:
            if r_width - r_width_2 in range(0, int(r_width / 2)):
                r_lenght, loc_x = r_lenght + randrange(choice([1, 2]), 4), loc_x - randrange(1, 3)
            elif r_width - r_width_2 in range(int(r_width / 2) + 1, r_width):
                r_lenght, loc_x = r_lenght - randrange(choice([1, 2]), 4), loc_x + randrange(1, 3)

            r_width_2, r_lenght_2 = r_width_2 - 1, r_lenght
            flag = False if r_width_2 == 0 else True  

        chunk.append(intermediate)

    if choice([True, False, False]):  # 33% водоемов будyт с песком
        for i in range(Y):  # окантовка водоемов "песком"
            for j in range(X):
                if i < Y - 1 and chunk[i][j] in list(range(6)) + list(range(9, 12)) and chunk[i + 1][j] in list(range(6, 9)):
                    chunk[i][j] = randrange(9, 12)
                    chunk[i - 1][j] = randrange(9, 12) if i < Y - 2 else 1
                    chunk[i][j - 1] = randrange(9, 12) if j != X - 2 else 1
                    flag = True

                if i - 1 != 0 and chunk[i][j] in list(range(6)) + list(range(9, 12)) and chunk[i - 1][j] in list(range(6, 9)):
                    chunk[i][j] = randrange(9, 12)
                    if i + 1 < Y:
                        chunk[i + 1][j] = randrange(9, 12) 
                    chunk[i][j - 1] = randrange(9, 12) if j - 2 > 0 else 1
                    flag = True     

                if j < X - 1 and chunk[i][j] in list(range(6)) + list(range(9, 12)) and chunk[i][j + 1] in list(range(6, 9)):
                    chunk[i][j] = randrange(9, 12)
                    chunk[i][j - 1] = randrange(9, 12) if j < X - 2 else 1
                    flag = True

                if j - 1 > 0 and chunk[i][j] in list(range(6)) + list(range(9, 12)) and chunk[i][j - 1] in list(range(6, 9)):
                    chunk[i][j] = randrange(9, 12)
                    chunk[i][j + 1] = randrange(9, 12) if j - 2 > 0 else 1

                if i < Y - 2 and j < X - 2 and chunk[i][j] in list(range(6, 9)) and chunk[i + 1][j + 1] in list(range(6)):
                    chunk[i + 1][j + 1] = randrange(9, 12)
                    flag = True 
                if i - 2 != 0 and j < X - 2 and chunk[i][j] in list(range(6, 9)) and chunk[i - 1][j + 1] in list(range(6)):
                    chunk[i - 1][j + 1] = randrange(9, 12)
                    flag = True

                if chunk[i][j] in range(9, 12):
                    if randrange(100) in range(20):
                        tile = pygame.sprite.Sprite()
                        image = load_image(f"data/images/objects/rock{choice([1, 2])}.png")
                        tile.image = image
                        tile.rect = image.get_rect()
                        tile.rect.x, tile.rect.y = (j - 0.5) * 26 + randrange(-5, 6), (i - 0.5) * 26 + randrange(-5, 6)
                        other_object.add(tile) 

    return chunk, other_object


def save():
    pass


def enemy_move():
    global enemies
    [schedule.every(3).to(5).seconds.do(elem.set_flag) for elem in enemies]


def draw_interface():
    pygame.draw.rect(screen, (0, 0, 0), (X * TILE_WIDTH - 155, 5, 150, 10))
    pygame.draw.rect(screen, (255, 0, 0), (X * TILE_WIDTH - 154, 6, (hero.get_hp() / hero.get_max_hp() * 150 - 2), 8))
    screen.blit(pygame.font.Font(None, 17).render(str(hero.get_hp()).rjust(3, '0'), True, (255, 255, 255)), (X * TILE_WIDTH - 75, 5))
    screen.blit(load_image("data/images/objects/heart.png"), (X * TILE_WIDTH - 90, 3))
    screen.blit(font.render(str(hero.get_balance()).rjust(5, '0'), True, (254, 226, 66)), (X * TILE_WIDTH - 70, 20))
    screen.blit(load_image("data/images/objects/coin.png"), (X * TILE_WIDTH - 21, 17))

 
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((X * TILE_WIDTH, Y * TILE_HEIGT))
    font = pygame.font.Font(None, 25)
    pygame.mouse.set_visible(False)
    pygame.display.set_caption('PyRogue')
    pygame.display.set_icon(load_image("data/images/objects/logo.png"))

    all_sprites = pygame.sprite.Group()
    running, field = True, [[None for _ in range(FIELD_X)] for _ in range(FIELD_Y)]
    cur_x, cur_y = 2, 2
    clock = pygame.time.Clock()

    enemies = pygame.sprite.Group()
    mainhero = pygame.sprite.Group()
    enemy_visions = pygame.sprite.Group()
    weapons = pygame.sprite.Group()
    
    hero = MainHero([10, 10], 'name', 200)  # координаты окна
    hero.add_weapon(Weapon(10, [20, 10], 100))
    mainhero.add(hero)
    up, down, left, right = False, False, False, False 

    game_map, other_obj = generate()
    can_go_tiles, cant_go_tiles = render_map(game_map)
    can_go_tiles.draw(screen)
    cant_go_tiles.draw(screen)
    field[cur_y][cur_x] = (can_go_tiles, cant_go_tiles, other_obj, enemies, enemy_visions)
    mainhero.draw(screen)
    weapons.draw(screen)
    draw_interface()

    schedule.every(2).to(5).seconds.do(enemy_move)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #save()
                running = False

            if event.type == pygame.KEYDOWN:
                keys, flag = pygame.key.get_pressed(), True

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

            if event.type == pygame.MOUSEMOTION and pygame.mouse.get_focused():
                [sword.move(*event.pos, *event.rel) for sword in weapons]

        if up:
            hero.move("up")
        elif down:
            hero.move("down")
        elif left:
            hero.move("left")
        elif right:
            hero.move("right")

        x, y = hero.get_coords()[0], hero.get_coords()[1]

        if X * TILE_WIDTH <= x or x <= 0 or Y * TILE_HEIGT <= y or y <= 0:

            if X * TILE_WIDTH <= x:
                cur_x += 1
            if x <= 0:
                cur_x -= 1
            if Y * TILE_HEIGT <= y:
                cur_y += 1
            if  y <= 0:
                cur_y -= 1

            cur_x = FIELD_X - 1 if cur_x < 0 else cur_x
            cur_y = FIELD_Y - 1 if cur_y < 0 else cur_y
            cur_x = 0 if cur_x >= FIELD_X else cur_x
            cur_y = 0 if cur_y >= FIELD_Y else cur_y

            if field[cur_y][cur_x] is None:
                game_map, other_obj = generate()
                can_go_tiles, cant_go_tiles = render_map(game_map)
                enemy_visions = pygame.sprite.Group()
                enemies = pygame.sprite.Group()
                for _ in range(randrange(10, 20)):
                    enemies.add(Enemy("name", 10, 100, 2, 5, randrange(5, 15), 100))
                field[cur_y][cur_x] = (can_go_tiles, cant_go_tiles, other_obj, enemies, enemy_visions)
            else:
                can_go_tiles, cant_go_tiles, other_obj, enemies, enemy_visions = field[cur_y][cur_x]

        if X * TILE_WIDTH <= hero.get_coords()[0]:
            hero.set_coords(0 , hero.get_coords()[1])

        elif hero.get_coords()[0] <= 0:
            hero.set_coords(X * TILE_WIDTH, hero.get_coords()[1])

        if Y * TILE_HEIGT <= hero.get_coords()[1]:
            hero.set_coords(hero.get_coords()[0], 0)

        elif hero.get_coords()[1] <= 0:
            hero.set_coords(hero.get_coords()[0], Y * TILE_HEIGT)

        schedule.run_pending()

        [elem.update() for elem in enemy_visions]
        [elem.move(hero.get_coords()) for elem in enemies] 
        can_go_tiles.draw(screen)
        cant_go_tiles.draw(screen)
        other_obj.draw(screen)
        enemy_visions.draw(screen)
        enemies.draw(screen)
        mainhero.draw(screen)
        weapons.draw(screen)
        draw_interface()
        
        pygame.display.flip()
        clock.tick(120)
