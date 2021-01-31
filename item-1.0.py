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
