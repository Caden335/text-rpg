"""RPG - Item Classes.

Author: Caden VanV
Version: 10/4/2024
"""

import random
import entities
import map_items


all_items = []


def print_map_item_list():
    """Print all map items."""
    for item in all_items:
        text = item.name
        text += f' ({item.type}) ({item.rarity}):'
        text += f'{item.effects}: {item.cost}'
        print(text)


class Item:
    """Stores a unique item.

    Attributes:
        name (str): name
        type (str): type (weapon, chest, head, hands, feet, accessory)
        rarity (str): rarity (common, well-made, expert, masterwork)
        effects (tuple): effects (atk, ac, dge, hp)
        cost (int): gold cost to buy
        owner (Band): owner
        equipt (RPGCharacter): person wearing
    """

    def __init__(self, name='Spear', type='weapon',
                 rarity='common', effects=(2, 0, 0, 0)):
        """Create item.

        Args:
            name (str): name
            type (str): type (see above)
            rarity (str): rarity (see above)
            effects (tuple): effects
        """
        self.name = name
        self.type = type
        self.rarity = rarity
        self.effects = effects
        self.owner = None
        self.equipt = None
        # Calculate cost
        if rarity == 'common':
            cost_base = 10
        elif rarity == 'well-made':
            cost_base = 50
        elif rarity == 'expert':
            cost_base = 100
        elif rarity == 'masterwork':
            cost_base = 1000
        else:
            cost_base = 10
        cost_mod = 1
        if type == 'chest':
            cost_mod = 1.5
        elif type == 'accessory':
            cost_mod = 0.8
        elif type == 'head':
            cost_mod = 1.2
        elif type == 'weapon':
            cost_mod = 1.2
        self.cost = int(cost_base * cost_mod)
        all_items.append(self)

    def __str__(self):
        """Print item info.

        Returns:
            str: map item info
        """
        result = f'{self.name}\n'
        result += f'     Type: {self.type}\n'
        result += f'     Rarity: {self.rarity}\n'
        result += f'     Cost: {self.cost}\n'
        # Adds in the effects as needed
        bonus_order = ('Atk', 'AC', 'Dge', 'HP')
        for i, effect in enumerate(self.effects):
            if effect != 0:
                print(f'     {bonus_order[i]}: {effect}\n')
        return result

    def equip(self, person):
        """Equip item.

        Args:
            person (RPGCharacter): new wearer
        """
        if person.items[self.type] is not None:
            person.item[self.type].unequip()
        person.items[self.type] = self
        self.equipt = person
        self.equipt.atk += self.effects[0]
        self.equipt.ac += self.effects[1]
        self.equipt.dge += self.effects[2]
        self.equipt.hp += self.effects[3]
        print(f'{self.equipt.name} equipt {self.name}')

    def unequip(self):
        """Unequip self."""
        self.equipt.items[self.type] = None
        self.equipt.atk -= self.effects[0]
        self.equipt.ac -= self.effects[1]
        self.equipt.dge -= self.effects[2]
        self.equipt.hp -= self.effects[3]
        print(f'Unequipt {self.name} from {self.equipt.name}')
        self.equipt = None
