class Hero:
    def __init__(self, name):
        self.name = name
        self.base_hp = 100
        self.base_damage = 10
        self.current_item = None
        self.coords = (0, 0)
            
    def hit(self, enemy):
        hx, hy = self.coords
        ex, ey = enemy.coords
        distance = ((ex - hx) ** 2 + (ey - hy) ** 2) ** 0.5
        if distance <= self.current_weapon.range:
            enemy.hp -= self.current_weapon.damage + random.randint(-self.current_weapon.damage // 20, self.current_weapon.damage // 20)
            self.current_weapon.durability -= 1
        else:
            print("Just not.")
