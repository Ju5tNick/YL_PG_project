import os
import sys
import pygame
import schedule
import random

from random import randrange, choice

X, Y, FIELD_X, FIELD_Y = 40, 20, 5, 5

#  +-------TILES------+
#  | 0 - 5   -- grass |
#  | 6 - 8   -- water |
#  | 9 - 11  -- sand  |
#  | 12      -- trader|
#  | |
#  +------------------+


class MainHero(pygame.sprite.Sprite):
    def __init__(self, coords, name, hp, damage):
        super().__init__(all_sprites)
        self.coords, self.hp, self.damage, self.name, self.weapon, self.balance = coords, hp, damage, name, None, 0
        self.rect, self.animation_counter = pygame.Rect(coords[0], coords[1], 19, 31), 0
        

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
        # if something_happens():
            # self.barter()

    def update(self, direction):
        if self.animation_counter == 5:
            self.frames = self.directions[direction]
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.animation_counter = 0
            self.mask = pygame.mask.from_surface(self.image)
        self.animation_counter += 1

    def is_alive(self):
        return True if self.hp > 0 else False

    def set_coords(self, new_x, new_y):
        self.rect.x, self.rect.y = new_x, new_y

    def get_coords(self):
        return (self.rect.x, self.rect.y)

    def get_info(self):
        weapons = ', '.join([weapon.get_name().capitalize() for weapon in self.weapons])
        return f'{self.name}\nЗдоровья: {self.hp} hp\nОружие:\n{weapons}\n\nТекущее оружие: {self.get_weapon().get_info()}'
    
    def get_inventory(self):
        return self.inventory

    def get_balance(self):
        return self.balance

    def attack(self, enemy):
        if self.weapon:
            hx, hy = self.coords
            ex, ey = enemy.get_coords()
            if ((ex - hx) ** 2 + (ey - hy) ** 2) ** 0.5 <= self.weapon.get_range():
                # ok, do the thing
                pass
        else:
            hx, hy = self.coords
            ex, ey = enemy.get_coords()
            if ((ex - hx) ** 2 + (ey - hy) ** 2) ** 0.5 <= 1:
                # ok, do the thing
                pass  # damage = 10
            pass

    def put(self, item, container):
        if len(container.get_items()) < container.get_capacity():
            del self.inventory[self.inventory.index(item)]
            container.add_item(item)
    
    def check_level(self):
        while self.xp_progress >= self.required_xp:
            self.level += 1
            self.xp_progress -= self.required_xp
            self.required_xp += 10

    def add_hp(self, value):
        self.hp += value

    def add_damage(self, value):
        self.damage += value





class Enemy(pygame.sprite.Sprite):
    def __init__(self, name, base_damage, base_health, base_speed, inventory, coords, range, gold_drops, xp_drops):
        super().__init__(all_sprites)
        self.name, self.damage, self.health, self.speed, self.inventory = name, base_damage, base_health, base_speed, inventory
        self.coords, self.range = coords, range
        self.get_angry = False
        self.rect, self.animation_counter = pygame.Rect(coords[0], coords[1], 21, 24), 0

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

        self.image = load_image("data/images/enemies/slime/static/0.png")
        self.cur_frame = 0

        for item in inventory:
            if item.type == "health":
                self.health += item.effect_value
            if item.type == "damage":
                self.damage += item.effect_value
            if item.type == "speed":
                self.speed += item.effect_value

        self.vision = EnemyVision(100, (self.rect.x - 95, self.rect.y - 90))
        enemy_visions.add(self.vision)
        self.gold_drops, self.get_angry, self.angry = gold_drops, False, False
        self.xp_drops, self.flag, self.can_move = xp_drops, -1, True

    def move(self, hero_coords):
        flag = True
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
            if self.flag == 1 and not self.angry and not self.get_angry:
                flag = False
                self.rect = self.rect.move(self.direction[0], self.direction[1])
                self.vision.move(self.direction[0], self.direction[1])

        self.update(stop=flag)

    def update(self, stop=False):
        if self.animation_counter == 5:
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
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.animation_counter = 0
            
        self.animation_counter += 1

    def set_flag(self):
        self.direction = (choice([1, -1]), choice([1, -1]))
        self.flag = -self.flag
        
    def die(self, hero):
        for item in self.inventory:
            if len(hero.inventory) < 40:
                hero.inventory.append(item)
        hero.balance += self.gold_drops
        hero.xp_progress += self.xp_drops
        hero.check_level()
        del self
    
    def hit(self, hero):
        hero.base_hp -= self.damage + __import__("random").randint(-(self.damage // 10), self.damage // 10)
        
    def get_stats(self):
        return (self.name, self.damage, self.health, self.speed, self.range)


class EnemyVision(pygame.sprite.Sprite):
    def __init__(self, range, coords):
        super().__init__(all_sprites)
        self.image = pygame.Surface((2 * range + 50, 2 * range + 50), pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color("black"), (coords[0], coords[1]), range, 1)
        self.rect = pygame.Rect(coords[0], coords[1], 2 * range, 2 * range)

    def move(self, del_x, del_y):
        self.rect = self.rect.move(del_x, del_y)

    def check(self):
        return pygame.sprite.spritecollideany(self, mainhero)


def render_map(chunk: list):
    render_map = pygame.sprite.Group()
    for rrow in range(Y):
        for rcol in range(X):
            tile = pygame.sprite.Sprite()
            if chunk[rrow][rcol] in range(6):
                image = load_image(f"data/images/tiles/grass/grass{chunk[rrow][rcol] + 1}.png")  
            elif chunk[rrow][rcol] in range(6, 9):
                image = load_image(f"data/images/tiles/water/water3{chunk[rrow][rcol] - 5}.png") 
            elif chunk[rrow][rcol] in range(9, 12):
                image = load_image(f"data/images/tiles/sand/sand{chunk[rrow][rcol] - 8}.png")  

            tile.image = image
            tile.rect = image.get_rect()
            tile.rect.x, tile.rect.y = rcol * 25, rrow * 25
            render_map.add(tile)
    return render_map


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
                    tile.rect.x, tile.rect.y = (j) * 25 + randrange(10), (i) * 25 + randrange(10)
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


class Trader(pygame.sprite.Sprite):
    def __init__(self):
        self.trades = [] # (price, eff_type, eff_value, stock)
        for i in range(20):
            price = random.randint(100, 10000)
            eff_type = random.randint(0, 1)
            eff_value = int(price / 50 / (eff_type + 1))
            stock = int(200 / (eff_type + 1) / eff_value)
            self.trades.append([price, eff_type, eff_value, stock])

    def sell(self, hero, idx):
        if hero.balance >= self.trades[idx][0]:
            if self.trades[idx][3] > 0:
                if self.trades[idx][1] == 0:
                    hero.add_hp(self.trades[idx][2])
                else:
                    hero.add_damage(self.trades[idx][2])
                self.trades[idx][3] -= 1
                print("Sold!")

    def get_trades(self):
        return self.trades



if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((X * 25, Y * 25))

    all_sprites = pygame.sprite.Group()
    running, field = True, [[None for _ in range(FIELD_X)] for _ in range(FIELD_Y)]
    cur_x, cur_y = 2, 2
    clock = pygame.time.Clock()

    characters = pygame.sprite.Group()
    mainhero = pygame.sprite.Group()
    enemy_visions = pygame.sprite.Group()
    
    
    hero = MainHero([10, 10], 'name', 200, 100)  # координаты окна
    enemy = Enemy("name", 10, 100, 2, [], [200, 200], 5, 10, 100)
    mainhero.add(hero)
    characters.add(enemy)
    up, down, left, right = False, False, False, False
    is_trader = True
    current_page = 0
    nearest_trader = Trader()

    last_x, last_y, x, y, w, h = hero.get_coords()[0], hero.get_coords()[1], hero.get_coords()[0], hero.get_coords()[1], X, Y
    game_map, other_obj = generate()
    game_map = render_map(game_map)
    game_map.draw(screen)
    field[cur_y][cur_x] = (game_map, other_obj, characters, enemy_visions)
    mainhero.draw(screen)

    schedule.every(2).seconds.do(enemy.set_flag)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #save()
                running = False

            if event.type == pygame.KEYDOWN:
                keys, flag = pygame.key.get_pressed(), True
                last_x, last_y = hero.get_coords()[0], hero.get_coords()[1]

                if is_trader:
                    if keys[pygame.K_m]:
                        is_trader = False
                        current_page = 0
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
            if event.type == pygame.MOUSEBUTTONDOWN:
                if is_trader:
                    if 350 >= event.pos[0] >= 30:
                        if event.pos[1] <= 345 and 45 >= event.pos[1] % 100 >= 30:
                            print("OK")
                            nearest_trader.sell(hero, current_page * 4 + event.pos[1] // 100)
                    if 320 >= event.pos[0] >= 200 and 440 >= event.pos[1] >= 420:
                        if current_page > 0:
                            current_page -= 1
                    if 760 >= event.pos[0] >= 700 and 440 >= event.pos[1] >= 420:
                        if current_page < 4:
                            current_page += 1

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
            if y <= 0:
                cur_y -= 1

            cur_x = FIELD_X - 1 if cur_x < 0 else cur_x
            cur_y = FIELD_Y - 1 if cur_y < 0 else cur_y
            cur_x = 0 if cur_x >= FIELD_X else cur_x
            cur_y = 0 if cur_y >= FIELD_Y else cur_y

            if field[cur_y][cur_x] is None:
                game_map, other_obj = generate()
                game_map = render_map(game_map)
                characters = pygame.sprite.Group()
                enemy_visions = pygame.sprite.Group()
                field[cur_y][cur_x] = (game_map, other_obj, characters, enemy_visions)
            else:
                game_map, other_obj, characters, enemy_visions = field[cur_y][cur_x]

        if X * 25 <= hero.get_coords()[0]:
            hero.set_coords(0 , hero.get_coords()[1])

        elif hero.get_coords()[0] <= 0:
            hero.set_coords(X * 25, hero.get_coords()[1])

        if Y * 25 <= hero.get_coords()[1]:
            hero.set_coords(hero.get_coords()[0], 0)

        elif hero.get_coords()[1] <= 0:
            hero.set_coords(hero.get_coords()[0], Y * 25)

        schedule.run_pending()
        [elem.move(hero.get_coords()) for elem in characters] 
        game_map.draw(screen)
        other_obj.draw(screen)
        enemy_visions.draw(screen)
        characters.draw(screen)
        mainhero.draw(screen)
        if is_trader:
            screen.fill((102, 43, 0))
            for i in range(4):
                font = pygame.font.Font(None, 30)
                text = font.render(f"Price: {nearest_trader.get_trades()[current_page - 1 * 4 + i][0]}, effect: {('HP', 'damage')[nearest_trader.get_trades()[current_page * 4 + i][1]]}, effect value: {nearest_trader.get_trades()[current_page * 4 + i][2]}, stock: {nearest_trader.get_trades()[current_page * 4 + i][3]}", True, (0, 0, 0))
                text_x = 30
                text_y = 30 + 100 * i
                text_w = text.get_width()
                text_h = text.get_height()
                screen.blit(text, (text_x, text_y))
            font = pygame.font.Font(None, 40)
            text = font.render(
                f"Previous",
                True, (0, 0, 0))
            text_x = 200
            text_y = 420
            text_w = text.get_width()
            text_h = text.get_height()
            screen.blit(text, (text_x, text_y))
            font = pygame.font.Font(None, 40)
            text = font.render(
                f"Next",
                True, (0, 0, 0))
            text_x = 700
            text_y = 420
            text_w = text.get_width()
            text_h = text.get_height()
            screen.blit(text, (text_x, text_y))

        
        pygame.display.flip()
        clock.tick(120)


