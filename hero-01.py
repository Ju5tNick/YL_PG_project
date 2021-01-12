import random


class Hero:
    def __init__(self, name):
        self.name = name
        self.base_hp = 100
        self.base_damage = 10
        self.xp_progress = 0
        self.level = 0
        self.current_weapon = None
        self.inventory = []
        self.coords = (0, 0)
        self.balance = 0
        
    def get_item(self, item, container):
        if len(self.inventory) < 40:
            self.inventory.append(item)
            del self.container.inventory[self.container.inventory.index(item)]
        else:
            print("Just no.")
            
    def hit(self, enemy):
        hx, hy = self.coords
        ex, ey = enemy.coords
        distance = ((ex - hx) ** 2 + (ey - hy) ** 2) ** 0.5
        if distance <= self.current_weapon.range:
            # Roll the dice!
            if random.randint(1, 100) <= 70:
                enemy.hp -= self.current_weapon.damage + random.randint(-self.current_weapon.damage // 20, self.current_weapon.damage // 20)
            else:
                print("Sorry, Link!")
            self.current_weapon.durability -= 1
        else:
            print("Just not.")
        if enemy.hp <= 0:
            self.xp_progress += enemy.kill_xp + random.randint(-enemy.kill_xp // 10, enemy.kill_xp // 10)
            self.xp_progress += enemy.kill_money + random.randint(-enemy.kill_money // 10, enemy.kill_money // 10)
            
    def buy(self, item, trader):
        trader.buy(item)
        
