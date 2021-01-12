class Enemy:
    def __init__(self):
        self.name = "Леонид"
        self.coords = ()  # ???
        self.hp = 100
        self.damage = 0
        self.range = 5

    def hit(self, hero):
        ex, ey = self.coords
        hx, hy = hero.coords
        distance = ((ex - hx) ** 2 + (ey - hy) ** 2) ** 0.5
        if distance <= self.range:
            enemy.hp -= self.damage + random.randint(-self.damage // 20,
                                                                    self.damage // 20)
    
    def move(self):
        # ???
