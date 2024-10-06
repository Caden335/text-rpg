"""RPG - Entity Classes.

Author: Caden VanV
Version: 10/4/2024
"""

import random
import rpg_lists


class RPGClass:
    """Stores a class.

    Attributes:
        name (str): name
        desc (str): description
        subclasses (tuple): subclasses
    """

    def __init__(self, name, desc, subclasses):
        """Create class.

        Args:
            name (str): name
            desc (str): description
            subclasses (tuple): subclasses
        """
        self.name = name
        self.desc = desc
        self.subclasses = subclasses

    def __str__(self):
        """Return class for printing.

        Returns:
            str: class for printing
        """
        return self.name


class RPGSubclass:
    """Stores a subclass.

    Attributes:
        name (str): name
        stats (tuple): stats
        stats_lvl (tuple): stats gained per lvl
    """

    def __init__(self, name, stats, stats_lvl):
        """Create class.

        Args:
            name (str): name
            stats (tuple): stats
            stats_lvl (tuple): stats per level
        """
        self.name = name
        self.stats = stats
        self.stats_lvl = stats_lvl

    def __str__(self):
        """Return class for printing.

        Returns:
            str: class for printing
        """
        text = self.name
        bonus_order = ('Atk', 'AC', 'Dge', 'HP')
        for i in range(len(self.stats) - 1):
            text += f'\n     {bonus_order[i]}: {self.stats[i]} '
            text += f'+ {self.stats_lvl[i]}/lvl'
        return text


class RPGRace:
    """Stores a race.

    Attributes:
        name (str): name
        stats (tuple): stats per lvl
    """

    def __init__(self, name, stats):
        """Create race.

        Args:
            name (str): name
            stats (tuple): stats per lvl
        """
        self.name = name
        self.stats = stats

    def __str__(self):
        """Return class for printing.

        Returns:
            str: class for printing
        """
        return self.name


# Stores General Information
# Classes contains class name, subclasses, and their stats
# Stores info as (base, per/lvl)
rpg_classes = (RPGClass('Warrior', 'Damage and armor focused class',
                        (RPGSubclass('Knight',
                                     (8, 15, 5, 40),
                                     (2, 2, 1, 6)),
                         RPGSubclass('Berserker',
                                     (15, 6, 5, 40),
                                     (3, 0, 1, 5)),
                         RPGSubclass('Ranger',
                                     (12, 8, 10, 30),
                                     (2, 1, 2, 6)))),
               RPGClass('Rogue', 'Damage and dodge focused class',
                        (RPGSubclass('Thief',
                                     (10, 5, 15, 25),
                                     (2, 0, 3, 4)),
                         RPGSubclass('Assassin',
                                     (14, 5, 12, 25),
                                     (3, 0, 2, 4)),
                         RPGSubclass('Duelist',
                                     (12, 10, 8, 30),
                                     (2, 2, 2, 5)))),
               RPGClass('Magus', 'Health and damage focused class',
                        (RPGSubclass('Elemental Caster',
                                     (13, 5, 6, 30),
                                     (3, 0, 1, 5)),
                         RPGSubclass('Light Mage',
                                     (9, 10, 7, 35),
                                     (1, 2, 1, 6)),
                         RPGSubclass('Dark Mage',
                                     (13, 6, 9, 30),
                                     (3, 0, 1, 5)))),
               RPGClass('Priest', 'Armor and health focused class',
                        (RPGSubclass('Cleric',
                                     (7, 12, 7, 50),
                                     (1, 2, 1, 7)),
                         RPGSubclass('Paladin',
                                     (10, 13, 6, 40),
                                     (2, 2, 1, 7)),
                         RPGSubclass('Zealot',
                                     (14, 5, 8, 30),
                                     (3, 0, 2, 5)))))

# Races contains race name and their stat additions per level
rpg_races = (RPGRace('Human', (0, 0, 0, 1)),
             RPGRace('Elf', (0, 0, 2, -1)),
             RPGRace('Dwarf', (0, 2, -1, 0)),
             RPGRace('Orc', (0, -1, 0, 2)))


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
        # Hit chance, base chance 50% + 5% for each dif in atk and dge
        hit_chance = (self.atk - enemy.dge) / 20 + .5
        # Base damage is atk minus half enemy armor. Can't be below 0
        damage = max(0, (self.atk - (self.ac / 2)))
        # Damage range is 80% - 120% of base damage
        damage *= ((random.randint(3, 7) / 10) + 0.5)
        # Truncates to 1 decimal just in case math adds unecessary digits
        damage = float(f'{damage:.1f}')
        if random.random() <= hit_chance:
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
        rpg_class (RPGClass): class
        subclass (RPGSubclass): subclass
        race (RPGRace): race
        atk (int): attack
        ac (int): armor
        dge (int): dodge
        max_hp (int): maximum health
        cur_hp (int): current health
        lvl (int): Level (1-5)
        player (bool): player controlled?
        items (dict): items equipt
    """

    def __init__(self):
        """Create generic NPC character."""
        # Generate random numbers
        rn = random.randint(0, len(rpg_lists.rpg_names) - 1)
        rc = random.randint(0, len(rpg_classes) - 1)
        rsc = random.randint(0, 2)
        rr = random.randint(0, len(rpg_races) - 1)
        # Assign the basic attributes using random nums
        self.name = rpg_lists.rpg_names[rn]
        self.rpg_class = rpg_classes[rc]
        self.subclass = self.rpg_class.subclasses[rsc]
        self.race = rpg_races[rr]
        # Assign stats
        self.atk = self.subclass.stats[0] + self.race.stats[0]
        self.ac = self.subclass.stats[1] + self.race.stats[1]
        self.dge = self.subclass.stats[2] + self.race.stats[2]
        self.max_hp = self.subclass.stats[3] + self.race.stats[3]
        self.cur_hp = float(self.max_hp)
        # Assign the rest of the attributes
        self.player = False
        self.lvl = 1
        self.items = {'weapon': None, 'chest': None, 'head': None,
                      'hands': None, 'feet': None, 'accessory': None}

    def __str__(self):
        """Print character info.

        Returns:
            str: Character info
        """
        result = f'{self.name}\n     {self.subclass.name} '
        result += f'({self.rpg_class.name}) {self.lvl}\n'
        result += f'     Race: {self.race.name}\n     ATK: {self.atk}\n'
        result += f'     DEF: {self.ac + self.dge} ({self.ac} '
        result += f'AC + {self.dge} DGE)\n'
        result += f'     HP: {int(self.cur_hp)}/{self.max_hp}'
        return result

    def level_up(self):
        """Level up."""
        self.lvl += 1
        self.atk += self.subclass.stats_lvl[0] + self.race.stats[0]
        self.ac += self.subclass.stats_lvl[1] + self.race.stats[1]
        self.dge += self.subclass.stats_lvl[2] + self.race.stats[2]
        self.max_hp += self.subclass.stats_lvl[3] + self.race.stats[3]


class PlayerCharacter(RPGCharacter):
    """Stores a character.

    Attributes:
        name (str): name
        rpg_class (RPGClass): class
        subclass (RPGSubclass): subclass
        race (RPGRace): race
        atk (int): attack
        ac (int): armor
        dge (int): dodge
        max_hp (int): maximum health
        cur_hp (int): current health
        lvl (int): Level (1-5)
        player (bool): always True
        items (dict): items equipt
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
        self.lvl = 1
        self.items = {'weapon': None, 'chest': None, 'head': None,
                      'hands': None, 'feet': None, 'accessory': None}

    def __pick_class(self):
        """List and picks a class."""
        # Print options
        print('Select Class\n'
              '-----------------')
        for rpg_class in rpg_classes:
            print(rpg_class.name)
        print('-----------------')
        # Pick option
        select = "None"
        while not any(select == cl.name for cl in rpg_classes):
            select = input()
            if not any(select == cl.name for cl in rpg_classes):
                print('Invalid selection, try again')
        select = next(cl for cl in rpg_classes if cl.name == select)
        self.rpg_class = select

    def __pick_subclass(self, char_class):
        """Pick subclass.

        Args:
            char_class (str): Current char class
        """
        # Print options
        print('Select Subclass\n'
              '-----------------')
        for subclass in self.rpg_class.subclasses:
            print(f'{subclass.name}\n'
                  f'     Atk: {subclass.stats[0]} '
                  f'+ {subclass.stats_lvl[0]}/lvl\n'
                  f'     AC: {subclass.stats[1]} '
                  f'+ {subclass.stats_lvl[1]}/lvl\n'
                  f'     Dge: {subclass.stats[2]} '
                  f'+ {subclass.stats_lvl[2]}/lvl\n'
                  f'     HP: {subclass.stats[3]} '
                  f'+ {subclass.stats_lvl[3]}/lvl')
        print('-----------------')
        # Pick option
        select_name = "None"
        while not any(select_name in sc.name
                      for sc in self.rpg_class.subclasses):
            select_name = input()
            if not any(select_name in sc.name
                       for sc in self.rpg_class.subclasses):
                print('Invalid selection, try again')
            else:
                select = next(sc for sc in self.rpg_class.subclasses
                              if select_name in sc.name)
        self.subclass = select
        self.atk = select.stats[0]
        self.ac = select.stats[1]
        self.dge = select.stats[2]
        self.max_hp = select.stats[3]

    def __pick_race(self):
        """List and picks a race."""
        # Print options
        print('Select Race\n'
              '-----------------')
        bonus_order = ('Atk', 'AC', 'Dge', 'HP')
        races = rpg_races
        for race in races:
            print(race.name)
            for i, stat in enumerate(race.stats):
                if stat != 0:
                    print(f'     {bonus_order[i]}: {stat}/lvl')
        print('-----------------')
        # Pick option
        select_name = "None"
        while not any(select_name == rc.name for rc in races):
            select_name = input()
            if not any(select_name == rc.name for rc in races):
                print('Invalid selection, try again')
            else:
                select = next(rc for rc in races if select_name == rc.name)
        self.race = select
        self.atk += select.stats[0]
        self.ac += select.stats[1]
        self.dge += select.stats[2]
        self.max_hp += select.stats[3]
