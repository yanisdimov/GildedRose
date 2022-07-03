# GildedRose

# Overview
This is an assignment which concerns the refactoring of the GildedRose assignment. In order to solve the assignment and improve the code quality I will use OOP principles and Design Patterns. Moreover, I will justify my decisions in the sections below. The code will be written in Python. 

# Motivation to Refactor
The given code contains all the logic in one single class where all the bussines requirements are represented by nested if-else statements. This makes it hard to read and maintain in the future. Moreover, most of the bussines logics that are required can be seperated in different classes (parent-child relationship), since they share same similar functionality e.g. increase, decrese. This will give better extendability and flexibility of the code (i.e. the creation of the new item *Conjured*). 

# Implementation
My first thought was to extend the *Item* class, but in the requirements it is stated that this is an immutable class, so I decided to pass it to the newly created class *BaseItem*. There I will implement the default methods with logic which can be further extended in every specific items' requirements. This gives single responsibilty and its easier to maintain and extend since if something breaks, or a new bussines rule is applied it can be defined, fixed there and all classes that will inherit *BaseClass* will have access to the new bussines logic.  

```python
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

```

In order to allow different classes of Items to be used, I created a factory class *ItemFactory*. This class also contains method *create* which allows the creation of new *BaseItem* object based on the input from the form in the *texttest_fixture.py* file. I used a dictionary *item_dict* to map the item name and the object itself. 

```python
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

```

Before implementing the methods for the different items, I tested the *BaseItem* class code via the unit test in the *test_gilded_rose.py* file. All of the tests ran successfully, so it was time to extend the base methods according the bussines logic of the different items. 

As I have mentioned earlier, I will inherit and override the method of the *BaseItem* class. In example item *AgedBrie* overrides method *update_quality* since *AgedBrie* needs to increase in quality the older it gets. 

```python
class AgedBrie(BaseItem):
   def update_quality(self):   
       self.increase_quality()

       if self.item.sell_in <= 0:
           self.increase_quality()
```
On the other hand, for *Sulfuras* we need to keep the quality 80 and method *decrease_sell_in* should do nothing since it has no sell by date. 

```python
class Sulfuras(BaseItem):
    
    def update_quality(self):
        self.item.quality = 80
    
    def decrease_sell_in(self):
        pass
```
Item *BackStage* has different logic aswell. It increases in quality as the sell in value approaches, like AgedBrie, but quality can increase by 2 if there are 10 days or less and by 3 if there are 5 days or less. To handle this requirement, I created two variables - *first_increase* and *second_increase* to keep the range of the days. Moreover, it is given that the quality drops to 0 after the concert, so method *drop_quality* was created to take care of it. 

```python
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
```
Lastly, the new item *Conjured* has only requirement that it degrades twice as fast as normal items, which to me means that it implements the standard base class logic. We know that the normal items degrade twice as fast after sell in, and *Conjured* degrades twice as fast than normal so it should degrade x4 times. I decided to call the *update_quality* method twice, which gives a lot of flexibilty due to the choice of pattern. Later, it can be chagned to degrade x2 which can be easily maintained. 

```python
class Conjured(BaseItem):
    def update_quality(self):
        BaseItem.update_quality(self)
        BaseItem.update_quality(self)
```

The class *GildedRose* simply calls the method *update_quality* where the *ItemFactory* handles the creation of the item and there we call the *update_quality* and *decrease_sell_in* methods. 

```python
class GildedRose:
    
    def __init__(self, items):
        self.items = items

    def update_quality(self):
        for item in self.items:
            gilded_rose_item = ItemFactory.create(item)
            gilded_rose_item.update_quality()
            gilded_rose_item.decrease_sell_in()
```

I also imported the *tabluate* in the *texttest_fixture.py* in order to present the items in better looking shape. 

```python
from tabulate import tabulate

```
```python
 import sys
    if len(sys.argv) > 1:
        days = int(sys.argv[1]) + 1 
    for day in range(days):
        print("-------- day %s --------" % day)
        print(
            tabulate(
                [(i.name, i.sell_in, i.quality) for i in items], headers=["name", "sell_in", "quality"],
            )
        )
        print("")
        GildedRose(items).update_quality()
```

In order to justify that the refactoring works according to the bussines logic/requriements, unit tests are present in the *test_gilded_rose.py* file. There I have implemented several unit tests scenarios like exceeding quality over 50, negative quality and correct functioning of increasing and decreasing.
