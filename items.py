"""RPG - Item Classes.

Author: Caden VanV
Version: 10/4/2024
"""


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

    def one_line(self):
        """One line version of above.

        Returns:
            str: String
        """
        result = f'{self.name} ({self.rarity}): '
        bonus_order = ('Atk', 'AC', 'Dge', 'HP')
        for i, effect in enumerate(self.effects):
            if effect != 0:
                result += f'{effect} {bonus_order[i]}, '
        result = result[:-2]
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


all_items = (Item('Ring of Health', 'accessory', 'common', (0, 0, 0, 1)),
             Item('Ring of Armor', 'accessory', 'common', (0, 1, 0, 0)),
             Item('Ring of Speed', 'accessory', 'common', (0, 0, 1, 0)),
             Item('Ring of Damage', 'accessory', 'common', (1, 0, 0, 0)),
             Item('Emerald Ring', 'accessory', 'well-made', (0, 1, 0, 1)),
             Item('Ruby Ring', 'accessory', 'well-made', (2, 0, 0, 0)),
             Item('Amethyst Ring', 'accessory', 'well-made', (0, 0, 2, 0)),
             Item('Jade Ring', 'accessory', 'well-made', (0, 0, 0, 2)),
             Item('Sapphire Ring', 'accessory', 'well-made', (0, 2, 0, 0)),
             Item('Ring of Protection', 'accessory', 'expert', (0, 2, 1, 0)),
             Item('Diamong Ring', 'accessory', 'expert', (3, 0, 0, 0)),
             Item('All-Ring', 'accessory', 'masterwork', (1, 1, 1, 1)),
             Item('Buckler', 'weapon', 'common', (0, 1, 0, 0)),  # Shields
             Item('Heater Shield', 'weapon', 'well-made', (0, 2, 0, 0)),
             Item('Kite Shield', 'weapon', 'expert', (0, 3, 0, 0)),
             Item('Tower Shield', 'weapon', 'masterwork', (0, 4, 0, 0)),
             Item('Spear', 'weapon', 'common', (1, 0, 0, 0)),  # Spears
             Item('Steel Spear', 'weapon', 'well-made', (2, 0, 0, 0)),
             Item('Spear and Buckler', 'weapon', 'well-made', (1, 1, 0, 0)),
             Item('Ornate Spear', 'weapon', 'expert', (3, 0, 0, 0)),
             Item('Spear and Shield', 'weapon', 'expert', (2, 1, 0, 0)),
             Item('Gungnir', 'weapon', 'masterwork', (4, 0, 0, 0)),
             Item('Sword', 'weapon', 'common', (1, 0, 0, 0)),  # Swords
             Item('Greatsword', 'weapon', 'well-made', (2, 0, 0, 0)),
             Item('Sword and Shield', 'weapon', 'well-made', (1, 1, 0, 0)),
             Item('Zweihander', 'weapon', 'expert', (3, 0, 0, 0)),
             Item('Sword and Shield', 'weapon', 'expert', (2, 1, 0, 0)),
             Item('Gram', 'weapon', 'masterwork', (4, 0, 0, 0)),
             Item('Kopis and Aegis', 'weapon', 'masterwork', (2, 2, 0, 0)),
             Item('Axe', 'weapon', 'common', (1, 0, 0, 0)),  # Axes
             Item('Greataxe', 'weapon', 'well-made', (2, 0, 0, 0)),
             Item('Khopesh and Shield', 'weapon', 'well-made', (1, 1, 0, 0)),
             Item('Battleaxe', 'weapon', 'expert', (3, 0, 0, 0)),
             Item('Axe and Shield', 'weapon', 'expert', (2, 1, 0, 0)),
             Item('Labrys', 'weapon', 'masterwork', (4, 0, 0, 0)),
             Item('Axe and Roundshield', 'weapon', 'masterwork', (2, 2, 0, 0)),
             Item('Hunting Bow', 'weapon', 'common', (1, 0, 0, 0)),  # Bows
             Item('Shortbow', 'weapon', 'well-made', (2, 0, 0, 0)),
             Item('Longbow', 'weapon', 'expert', (3, 0, 0, 0)),
             Item('Fail-not Bow', 'weapon', 'masterwork', (4, 0, 0, 0)),
             Item('Stick', 'weapon', 'common', (1, 0, 0, 0)),  # Staffs
             Item('Staff', 'weapon', 'well-made', (2, 0, 0, 0)),
             Item('Oaken Staff', 'weapon', 'expert', (3, 0, 0, 0)),
             Item('Archmage\'s Staff', 'weapon', 'masterwork', (4, 0, 0, 0)),
             Item('Tunic', 'chest', 'common', (0, 1, 0, 0)),  # T1C Armor
             Item('Robe', 'chest', 'common', (0, 1, 0, 0)),
             Item('Gambeson', 'chest', 'common', (0, 2, -1, 0)),
             Item('Leather Armor', 'chest', 'common', (0, 2, 0, 0)),
             Item('Studded Armor', 'chest', 'well-made', (0, 3, -1, 0)),  # T2C
             Item('Hide Armor', 'chest', 'well-made', (0, 2, 0, 0)),
             Item('Chainmail', 'chest', 'well-made', (0, 4, -2, 0)),
             Item('Scale Mail', 'chest', 'expert', (0, 3, 0, 0)),  # T3C
             Item('Breastplate', 'chest', 'expert', (0, 4, -1, 0)),
             Item('Half-Plate', 'chest', 'expert', (0, 5, -2, 0)),
             Item('Plate Armor', 'chest', 'masterwork', (0, 6, -2, 0)),  # T4C
             Item('Ring Mail', 'chest', 'masterwork', (0, 5, -1, 0)),
             Item('Splint Armor', 'chest', 'masterwork', (0, 4, 0, 0)),
             Item('Sandals', 'feet', 'common', (0, 0, 1, 0)),  # Feet
             Item('Shoes', 'feet', 'common', (0, 0, 1, 0)),
             Item('Boots', 'feet', 'common', (0, 0, 1, 0)),
             Item('Cobbled Shoes', 'feet', 'common', (0, 0, 1, 0)),
             Item('Leather Boots', 'feet', 'well-made', (0, 0, 2, 0)),
             Item('Greaves', 'feet', 'expert', (0, 0, 3, 0)),
             Item('Plate Books', 'feet', 'masterwork', (0, 0, 4, 0)),
             Item('Gloves', 'hands', 'common', (0, 1, 0, 0)),  # Hands
             Item('Bracelets', 'hands', 'common', (1, 0, 0, 0)),
             Item('Bracers', 'hands', 'well-made', (1, 1, 0, 0)),
             Item('Gauntlets', 'hands', 'expert', (1, 2, 0, 0)),
             Item('Steel Gauntlets', 'hands', 'masterwork', (2, 2, 0, 0)),
             Item('Hood', 'head', 'common', (0, 1, 0, 0)),  # Head
             Item('Steel Cap', 'head', 'well-made', (0, 2, 0, 0)),
             Item('Helmet', 'head', 'expert', (0, 3, 0, 0)),
             Item('Sallet', 'head', 'masterwork', (0, 4, 0, 0)),
             Item('Circlet', 'head', 'well-made', (0, 0, 0, 2)),
             Item('Crown', 'head', 'masterwork', (0, 0, 0, 5)),
             Item('Cap', 'head', 'well-made', (0, 3, 0, 0)))
common_items = [item for item in all_items if item.rarity == 'common']
well_made_items = [item for item in all_items if item.rarity == 'well-made']
expert_items = [item for item in all_items if item.rarity == 'expert']
masterwork_items = [item for item in all_items if item.rarity == 'masterwork']


def print_map_item_list():
    """Print all map items."""
    for item in all_items:
        text = item.name
        text += f' ({item.type}) ({item.rarity}):'
        text += f' {item.effects}: {item.cost}'
        print(text)
