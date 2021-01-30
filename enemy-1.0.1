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
        del self
        
    def move(self):
        for i in range(self.speed):
            pass
        pass  # <вставьте стратегию передвижения>
    
    def hit(self, hero):
        hero.base_hp -= self.damage + __import__("random").randint(-(self.damage // 10), self.damage // 10)
        
    def get_stats(self):
        return (self.name, self.damage, self.health, self.speed, self.range)
