class Weapon:
    def __init__(self, name, damage, range, durability):
        self.name = name
        self.damage = damage
        self.range = range
        self.durability = durability

    def get_name(self):
        return self.name

    def get_damage(self):
        return self.damage

    def get_range(self):
        return self.range

    def get_durability(self):
        return self.durability
