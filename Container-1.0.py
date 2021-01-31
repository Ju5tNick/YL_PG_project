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
    
    # << OUT (MUST BE IN Hero)
    # def put(self, item, container):
    #     if len(container.get_items()) < container.get_capacity():
    #         del self.inventory[self.inventory.index(item)]
    #         container.add_item(item)
