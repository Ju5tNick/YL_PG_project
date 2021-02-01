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
