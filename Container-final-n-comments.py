import random


class Bow: pass
class Sword: pass

CONTAINERS = {}
WEAPONS = [Bow, Sword]
NAMES = ["Раз", "Два", "Три"]


class Container:
    def __init__(self, coords):
        self.capacity = random.choice((10, 20, 30, 40, 50)) # Размер сундука
        self.current = 0 # Счетчик вещей в сундуке
        self.items = [] # Сами вещи
        # Заполняем сундук рандомными вещами
        for i in range(random.randint(0, self.capacity)):
            self.items.append(random.choice(WEAPONS)(random.choice(NAMES), random.randint(10, 100), random.randint(1, 15), random.randint(40, 200)))
            self.current += 1
        # закидываем контейнер в голбальный список контейнеров
        CONTAINERS[coords] = self

    # >> 
    def put(self, item, hero):
        if self.current < self.capacity:
            self.current += 1
            self.items.append(item)
            del hero.inventory[hero.inventory.index(item)]

    # << 
    def take(self, item, hero):
        self.current -= 1
        del self.items[self.items.index(item)]
        hero.inventory.append(item)
