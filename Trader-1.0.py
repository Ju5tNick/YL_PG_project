import random

class Trader:
    def __init__(self, name):
        self.name = name
        self.deals = {}
        for i in range(15):
            iname = ""
            for i in range(10):
                iname += str(random.randint(0, 9))
                self.deals[iname] = Weapon(*args, **kwargs)

    def sell(self, item, hero):
        if hero.get_balance() >= self.deals[item][0]:
            if len(hero.get_inventory()) < 40:  # inventory check
                # ok
                hero.add_item(item)  # item goes in >>
                hero.add_balance(-self.deals[item][0])  # balance goes wroom
                self.deals[item][1] -= 1  # stocks goes down

    def get_deals(self):
        return self.deals
