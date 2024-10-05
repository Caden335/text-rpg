"""RPG - Entity Classes.

Author: Caden VanV
Version: 10/4/2024
"""

import random
import rpg_lists


class Entity:
    """Stores a character.

    Attributes:
        name (str): name
        atk (int): attack
        ac (int): armor
        dge (int): dodge
        max_hp (int): maximum health
        cur_hp (int): current health
        player (bool): player controlled?
    """

    def __init__(self, name='Wolf', atk=5, ac=5, dge=5, max_hp=10):
        """Create generic entity.

        Args:
            name (str): Entity name
            atk (int): attack
            ac (int): armor
            dge (int): dodge
            max_hp (int): maximum health
        """
        self.name = name
        self.atk = atk
        self.ac = ac
        self.dge = dge
        self.max_hp = max_hp
        self.cur_hp = float(max_hp)
        self.player = False

    def __str__(self):
        """Print entity info.

        Returns:
            str: entity info
        """
        result = f'{self.name}\n'
        result += f'     ATK: {self.atk}\n'
        result += f'     DEF: {self.ac + self.dge} ({self.ac} '
        result += f'AC + {self.dge} DGE)\n'
        result += f'     HP: {int(self.cur_hp)}/{self.max_hp}'
        return result

    def attack(self, enemy):
        """Attack enemy.

        Args:
            enemy (Entity): Target entity
        """
        hit = random.randint(1, 10)
        damage = (self.atk * ((random.randint(0, 10) / 10) + 0.5))
        damage = damage * ((10 - enemy.ac) / 10)
        damage = float(f'{damage:.1f}')  # Truncates to 1 decimal point
        if hit >= enemy.dge:
            print(f'{self.name} hit their attack against '
                  f'{enemy.name} for {damage} points')
            enemy.take_damage(damage)
        else:
            print(f'{self.name} missed their attack against {enemy.name}')

    def take_damage(self, dmg):
        """Take damage.

        Args:
            dmg (float): Amount of damage taken
        """
        self.cur_hp -= dmg
        if self.cur_hp <= 0:
            self.die()

    def die(self):
        """Entity dies."""
        print(f'{self.name} has died.')
        self.name = self.name + ' (Dead)'

    def heal(self, amt):
        """Heal entity.

        Args:
            amt (int): Heal amt
        """
        self.cur_hp += amt
        if self.cur_hp > self.max_hp:
            amt = self.max_hp - self.cur_hp
            self.cur_hp = float(self.max_hp)
        print(f'{self.name} heals by {int(amt)} hp'
              f'and is now at {self.cur_hp}/{self.max_hp}')


class RPGCharacter(Entity):
    """Stores a character.

    Attributes:
        name (str): name
        rpg_class (str): class
        subclass (str): subclass
        race (str): race
        atk (int): attack
        ac (int): armor
        dge (int): dodge
        max_hp (int): maximum health
        cur_hp (int): current health
        player (bool): player controlled?
        items (dict): items equipt
    """

    def __init__(self):
        """Create generic NPC character."""
        rn = random.randint(0, len(rpg_lists.rpg_names) - 1)
        rc = random.randint(0, len(rpg_lists.rpg_classes) - 1)
        rsc = random.randint(0, 2)
        rr = random.randint(0, len(rpg_lists.rpg_races) - 1)
        self.name = rpg_lists.rpg_names[rn]
        self.rpg_class = rpg_lists.rpg_classes[rc]['Class']
        self.subclass = rpg_lists.rpg_classes[rc]['Subclasses'][rsc]
        self.atk = rpg_lists.rpg_classes[rc]['Attacks'][rsc]
        self.ac = rpg_lists.rpg_classes[rc]['Armor'][rsc]
        self.dge = rpg_lists.rpg_classes[rc]['Dodge'][rsc]
        self.max_hp = rpg_lists.rpg_classes[rc]['Health'][rsc]
        self.race = rpg_lists.rpg_races[rr][0]
        self.atk += rpg_lists.rpg_races[rr][1]
        self.ac += rpg_lists.rpg_races[rr][2]
        self.dge += rpg_lists.rpg_races[rr][3]
        self.max_hp += rpg_lists.rpg_races[rr][4]
        self.cur_hp = float(self.max_hp)
        self.player = True
        self.items = {'weapon': None, 'chest': None, 'head': None,
                      'hands': None, 'feet': None, 'accessory': None}

    def __str__(self):
        """Print character info.

        Returns:
            str: Character info
        """
        result = f'{self.name}\n     {self.subclass} ({self.rpg_class})\n'
        result += f'     Race: {self.race}\n     ATK: {self.atk}\n'
        result += f'     DEF: {self.ac + self.dge} ({self.ac} '
        result += f'AC + {self.dge} DGE)\n'
        result += f'     HP: {int(self.cur_hp)}/{self.max_hp}'
        return result


class PlayerCharacter(RPGCharacter):
    """Stores a character.

    Attributes:
        name (str): name
        rpg_class (str): class
        subclass (str): subclass
        race (str): race
        atk (int): attack
        ac (int): armor
        dge (int): dodge
        max_hp (int): maximum health
        cur_hp (int): current health
        player (bool): player controlled?
        items (dict): items
    """

    def __init__(self):
        """Create character."""
        self.name = input('Choose Character Name: ')
        print('-----------------')
        self.__pick_class()
        print('-----------------')
        self.__pick_subclass(self.rpg_class)
        print('-----------------')
        self.__pick_race()
        self.cur_hp = float(self.max_hp)
        self.player = True
        self.items = {'weapon': None, 'chest': None, 'head': None,
                      'hands': None, 'feet': None, 'accessory': None}

    def __pick_class(self):
        """List and picks a class."""
        # Print options
        print('Select Class\n'
              '-----------------')
        for rpg_class in rpg_lists.rpg_classes:
            print(rpg_class['Class'])
        print('-----------------')
        # Pick option
        select = "None"
        while not any(select == cl['Class'] for cl in rpg_lists.rpg_classes):
            select = input()
            if not any(select == cl['Class'] for cl in rpg_lists.rpg_classes):
                print('Invalid selection, try again')
        self.rpg_class = select

    def __pick_subclass(self, char_class):
        """Pick subclass.

        Args:
            char_class (str): Current char class
        """
        # Get index of class
        index = 0
        for i, rpg_class in enumerate(rpg_lists.rpg_classes):
            if rpg_class['Class'] == char_class:
                index = i
        # Print options
        print('Select Subclass\n'
              '-----------------')
        subclasses = []
        for i in range(len(rpg_lists.rpg_classes[index]['Subclasses'])):
            subclass = (rpg_lists.rpg_classes[index]['Subclasses'][i],
                        rpg_lists.rpg_classes[index]['Attacks'][i],
                        rpg_lists.rpg_classes[index]['Armor'][i],
                        rpg_lists.rpg_classes[index]['Dodge'][i],
                        rpg_lists.rpg_classes[index]['Health'][i])
            subclasses.append(subclass)
            print(f'{subclass[0]}\n'
                  f'     Atk: {subclass[1]}\n'
                  f'     Def: {subclass[2] + subclass[3]} ('
                  f'{subclass[2]} ac + {subclass[3]} dge)\n'
                  f'     HP: {subclass[4]}')
        print('-----------------')
        # Pick option
        select_name = "None"
        while not any(select_name in sc[0] for sc in subclasses):
            select_name = input()
            if not any(select_name in sc[0] for sc in subclasses):
                print('Invalid selection, try again')
            else:
                select = next(sc for sc in subclasses if select_name in sc[0])
        self.subclass = select[0]
        self.atk = select[1]
        self.ac = select[2]
        self.dge = select[3]
        self.max_hp = select[4]

    def __pick_race(self):
        """List and picks a race."""
        # Print options
        print('Select Race\n'
              '-----------------')
        bonus_order = ('Atk', 'AC', 'Dge', 'HP')
        races = rpg_lists.rpg_races
        for race in races:
            print(race[0])
            for i in range(len(race) - 1):
                if race[i + 1] != 0:
                    print(f'     {bonus_order[i]}: {race[i + 1]}')
        print('-----------------')
        # Pick option
        select_name = "None"
        while not any(select_name == rc[0] for rc in races):
            select_name = input()
            if not any(select_name == rc[0] for rc in races):
                print('Invalid selection, try again')
            else:
                select = next(rc for rc in races if select_name == rc[0])
        self.race = select[0]
        self.atk += select[1]
        self.ac += select[2]
        self.dge += select[3]
        self.max_hp += select[4]
