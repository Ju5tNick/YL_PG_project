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
