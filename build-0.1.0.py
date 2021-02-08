class Hero:
    def __init__(self, name):
        self.name = name
        self.level = 1
        self.xp_progress = 0
        self.required_xp = 100
        self.base_hp = 200
        self.base_damage = 20
        self.weapon = None
        self.inventory = []
        self.balance = 100
        self.coords = (0, 0)

    def get_info(self):
        return (self.name, self.level, self.xp_progress, self.required_xp, self.base_hp, self.base_damage, self.weapon)

    def get_inventory(self):
        return self.inventory

    def get_coords(self):
        return self.coords

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

    def move(self):
        pass  # двигать будем уже из pg части, тестовая будет допилена отдельно
    
    def check_level(self):
        while self.xp_progress >= self.required_xp:
            self.level += 1
            self.xp_progress -= self.required_xp
            self.required_xp += 10


class Item:
    """ITEM
    ITEMS HAVE 3 TYPES - HP-BASED, DAMAGE-BASED, SPEED-BASED
    HP - 0, DAMAGE - 1, SPEED - 2
    EFFECT VALUE MEANS HOW MUCH ITEM CHANGE HP/DAMAGE/SPEED
    EFFECT RANGE - RANGE OF EFFECT
    DURABILITY - USES OF ITEM"""
    # Initialization
    def __init__(self, name, effect_type, effect_value, effect_range=0, durability=-1):
        self.name = name
        self.effect_type = effect_type
        self.effect_value = effect_value
        self.effect_range = effect_range
        self.durability = durability
    
    # Getters
    def get_name(self):
        return self.name

    def get_effect(self):
        return (self.effect_type, self.effect_value, self.effect_range)

    def get_durability(self):
        return self.durability
    
    # Editable methods
    def use(self):
        self.durability -= 1
        if self.durability == 0:
            del self

            
class Enemy:
    def __init__(self, name, base_damage, base_health, base_speed, inventory, coords, range, gold_drops, xp_drops):
        self.name = name
        self.damage = base_damage
        self.health = base_health
        self.speed = base_speed
        self.inventory = inventory
        self.coords = coords
        self.range = range
        for item in inventory:
            if item.type == "health":
                self.health += item.effect_value
            if item.type == "damage":
                self.damage += item.effect_value
            if item.type == "speed":
                self.speed += item.effect_value
        self.gold_drops = gold_drops
        self.xp_drops = xp_drops
        
    def die(self, hero):
        for item in self.inventory:
            if len(hero.inventory) < 40:
                hero.inventory.append(item)
        hero.balance += self.gold_drops
        hero.xp_progress += self.xp_drops
        hero.check_level()
        del self
        
    def move(self):
        for i in range(self.speed):
            pass
        pass  # <вставьте стратегию передвижения>
    
    def hit(self, hero):
        hero.base_hp -= self.damage + __import__("random").randint(-(self.damage // 10), self.damage // 10)
        
    def get_stats(self):
        return (self.name, self.damage, self.health, self.speed, self.range)

    
class Trader:
    """Trader logic:
    - initializing trader with some deals, each deal has price and stock
    - trader can ONLY sell you something, if you have enough money AND item.stock > 0"""
    def __init__(self, name):
        self.name = name
        self.deals = {Item: [0, 0]}  # item: [price, size] (somehow generates randomly)

    def sell(self, item, hero):
        if hero.get_balance() >= self.deals[item][0]:  # balance check
            if len(hero.get_inventory()) < 40:  # inventory check
                # ok
                hero.add_item(item)  # item goes in >>
                hero.add_balance(-self.deals[item][0])  # balance goes wroom
                self.deals[item][1] -= 1  # stocks goes down

    def get_deals(self):
        return self.deals

    
class Container:
    """CONTAINER LOGIC
    INITIALIZING WITH SOME RANDOM ITEMS
    TAKE - APPENDING ITEM TO HERO'S INVENTORY
    PUT (HERO METHOD) - APPENDING ITEM TO CONTAINER'S INVENTORY"""
    def __init__(self, coords):
        self.capacity = random.choice((10, 20, 30, 40, 50))
        self.items = []
        for i in range(random.randint(0, self.capacity)):
            self.items.append()  # filling container with items
        self.coords = coords
    
    # Getters
    def get_capacity(self):
        return self.capacity
    
    def get_items(self):
        return self.items

    # >> IN
    def take(self, item, hero):
        if len(hero.get_inventory()) < 40:
            del self.items[self.items.index(item)]
            hero.add_item(item)
        
    def add_item(self, item):
        self.items.append(item)
