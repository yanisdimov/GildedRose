# Base class which cannot be changed
class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
         return "%s, %s, %s" % (self.name, self.sell_in, self.quality)

# Since Item class cannot be changed BaseItem class inherits from Item and the domain logic is expressed here
class BaseItem(Item):
    max_quality = 50


    def __init__(self, item):
        self.item = item
        
    def increase_quality(self):
        if self.item.quality < self.max_quality:
            self.item.quality = self.item.quality + 1

    def decrease_quality(self):
        if self.item.quality > 0:
            self.item.quality = self.item.quality - 1

    def decrease_sell_in(self):
        self.item.sell_in = self.item.sell_in - 1

    def update_quality(self):
        self.decrease_quality()
    
        if self.item.sell_in <= 0:
            self.decrease_quality()

# Every item that Gilded Rose has, inherits from the BaseItem class and extends it based on the specific item requirements                
class AgedBrie(BaseItem):
    def update_quality(self):   
        self.increase_quality()

        if self.item.sell_in <= 0:
            self.increase_quality()

class Sulfuras(BaseItem):
    
    def update_quality(self):
        self.item.quality = 80
    
    def decrease_sell_in(self):
        pass


class BackStage(BaseItem):
    first_increase = 10
    second_increase = 5

    def drop_quality(self):
        self.item.quality = 0

    def update_quality(self):
        self.increase_quality()
        if self.item.sell_in <= self.first_increase:
            self.increase_quality()
        if self.item.sell_in <= self.second_increase:
            self.increase_quality()
        if self.item.sell_in <= 0:
            self.drop_quality()
            
class Conjured(BaseItem):
    def update_quality(self):
        BaseItem.update_quality(self)
        BaseItem.update_quality(self)
        
         
class ItemFactory:
    item_dict = {
        "Aged Brie": AgedBrie,
        "Sulfuras, Hand of Ragnaros": Sulfuras,
        "Backstage passes to a TAFKAL80ETC concert" :BackStage,
        "Conjured Mana Cake": Conjured
        }

    @classmethod
    def create(cls, item):
        if item.name in cls.item_dict:
            return cls.item_dict[item.name](item)
        return BaseItem(item)


class GildedRose:
    
    def __init__(self, items):
        self.items = items

    def update_quality(self):
        for item in self.items:
            gilded_rose_item = ItemFactory.create(item)
            gilded_rose_item.update_quality()
            gilded_rose_item.decrease_sell_in()