"""RPG - Entity Classes.

Author: Caden VanV
Version: 10/4/2024
"""

import random
import rpg_lists
import items
import abilities


class RPGClass:
    """Stores a class.

    Attributes:
        name (str): name
        tabs (str): any tabs needs for alignment
        desc (str): description
        subclasses (tuple): subclasses
    """

    def __init__(self, name, tabs, desc, subclasses):
        """Create class.

        Args:
            name (str): name
            tabs (str): any tabs needs for alignment
            desc (str): description
            subclasses (tuple): subclasses
        """
        self.name = name
        self.tabs = tabs
        self.desc = desc
        self.subclasses = subclasses

    def __str__(self):
        """Return class for printing.

        Returns:
            str: class for printing
        """
        result = f'-----------------\n{self.name}\n'
        result += f'-----------------\n{self.desc}\n'
        result += '-----------------\n'
        for subclass in self.subclasses:
            result += f'{subclass}\n'
        return result


class RPGSubclass:
    """Stores a subclass.

    Attributes:
        name (str): name
        stats (tuple): stats
        stats_lvl (tuple): stats gained per lvl
        abilities (list): abilities gained from lvl 2-5
    """

    def __init__(self, name, stats, stats_lvl, abil):
        """Create class.

        Args:
            name (str): name
            stats (tuple): stats
            stats_lvl (tuple): stats per level
            abil (list): index of abilities in abilities.all_abilities
        """
        self.name = name
        self.stats = stats
        self.stats_lvl = stats_lvl
        self.abilities = []
        for i in range(abil[0], abil[1] + 1):
            self.abilities.append(abilities.all_abilities[i])

    def __str__(self):
        """Return class for printing.

        Returns:
            str: class for printing
        """
        text = self.name
        text += '\n     Stats:\n'
        for i in range(len(self.stats)):
            text += f'          {items.bonus_order[i]}: {self.stats[i]} '
            text += f'+ {self.stats_lvl[i]}/lvl\n'
        text += '     Abilities:\n'
        for i, ability in enumerate(self.abilities):
            text += f'          Level {i + 2}: {ability}\n'
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
# Descs come first so I can call them more easily
rpg_class_descs = ('The Warrior is a fairly solid allrounder class.\n'
                   'It has a good mixture of passive abilities and\n'
                   'damaging abilities, and its subclasses have a good\n'
                   'mixture of stats with relatively high health.',
                   'The Rogue is more of a glass cannon. It has high\n'
                   'damage and dodging abilities but lower armor and\n'
                   'health. Their abilities focus on buffing themselves\n'
                   'and dealing damage, with passives buffing dodge and atk.',
                   'The Magus is an exceptional damage dealer and \n'
                   'buffer. It has excellent buff and debuff skills,\n'
                   'alongside great damage. This comes at a cost of getting\n'
                   'hit more, though it has decent health to make up for\n'
                   'this loss.',
                   'The Priest can heal its teammates and damage its foes.\n'
                   'It has high armor and health, alongside a variety\n'
                   'of abilities that can deal damage and keep the party\n'
                   'alive. By far the tankiest class as well, with high hp.',
                   '(HARD) The Battlemage is a tough class to start with.\n'
                   'It has low stats to begin with, and awful health, but\n'
                   'it gains more per level than any other class and has\n'
                   'excellent and versatile abilities focused on buffing\n'
                   'itself and dealing damage quickly.')
rpg_classes = (RPGClass('Warrior', '\t', rpg_class_descs[0],
                        (RPGSubclass('Knight',
                                     (8, 15, 5, 40),
                                     (2, 2, 1, 6),
                                     (0, 3)),
                         RPGSubclass('Berserker',
                                     (15, 6, 5, 40),
                                     (3, 0, 1, 5),
                                     (4, 7)),
                         RPGSubclass('Ranger',
                                     (12, 8, 10, 30),
                                     (2, 1, 2, 6),
                                     (8, 11)))),
               RPGClass('Rogue', '\t', rpg_class_descs[1],
                        (RPGSubclass('Thief',
                                     (10, 5, 15, 25),
                                     (2, 0, 3, 4),
                                     (12, 15)),
                         RPGSubclass('Assassin',
                                     (14, 5, 12, 25),
                                     (3, 0, 2, 4),
                                     (16, 19)),
                         RPGSubclass('Duelist',
                                     (12, 10, 8, 30),
                                     (2, 2, 2, 5),
                                     (20, 23)))),
               RPGClass('Magus', '\t', rpg_class_descs[2],
                        (RPGSubclass('Elemental Caster',
                                     (13, 5, 6, 30),
                                     (3, 0, 1, 5),
                                     (24, 27)),
                         RPGSubclass('Light Mage',
                                     (9, 10, 7, 35),
                                     (1, 2, 1, 6),
                                     (28, 31)),
                         RPGSubclass('Dark Mage',
                                     (13, 6, 9, 30),
                                     (3, 0, 1, 5),
                                     (32, 35)))),
               RPGClass('Priest', '\t', rpg_class_descs[3],
                        (RPGSubclass('Cleric',
                                     (7, 12, 7, 50),
                                     (1, 2, 1, 7),
                                     (36, 39)),
                         RPGSubclass('Paladin',
                                     (10, 13, 6, 40),
                                     (2, 2, 1, 7),
                                     (40, 43)),
                         RPGSubclass('Zealot',
                                     (14, 5, 8, 30),
                                     (3, 0, 2, 5),
                                     (44, 47)))),
               RPGClass('Battlemage', '', rpg_class_descs[4],
                        (RPGSubclass('Arcane Knight',
                                     (6, 10, 4, 25),
                                     (3, 4, 2, 6),
                                     (48, 51)),
                         RPGSubclass('Runesmith',
                                     (5, 13, 3, 28),
                                     (2, 6, 2, 8),
                                     (52, 55)),
                         RPGSubclass('Spellblade',
                                     (7, 6, 9, 22),
                                     (3, 2, 4, 5),
                                     (56, 59)))))

# Races contains race name and their stat additions per level
rpg_races = (RPGRace('Edain', (1, 1, 1, 1)),
             RPGRace('Sindar', (1, -1, 4, 0)),
             RPGRace('Noldor', (2, 2, 0, 0)),
             RPGRace('Dwarf', (0, 3, -1, 2)),
             RPGRace('Orc', (2, -1, 0, 3)))


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
        lvl (int): level
        xp (int): xp
        abilities (list): abilities
    """

    def __init__(self, name='Wolf', lvl=1):
        """Create generic entity.

        Args:
            name (str): Entity name
            lvl (int): lvl
        """
        self.name = name
        self.atk = 5 + (3 * lvl)
        self.ac = 5 + (2 * lvl)
        self.dge = 5 + (2 * lvl)
        self.max_hp = 20 + (5 * lvl)
        self.cur_hp = float(self.max_hp)
        self.lvl = lvl
        self.xp = 0
        self.player = False
        self.abilities = []

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
        damage = max(0, (self.atk - (enemy.ac / 2)))
        # Damage range is 80% - 120% of base damage
        damage *= ((random.randint(3, 7) / 10) + 0.5)
        # Truncates to 1 decimal just in case math adds unecessary digits
        damage = float(f'{damage:.1f}')
        if random.random() <= hit_chance:
            print(f'{self.name} hit their attack against '
                  f'{enemy.name} for {damage} points')
            enemy.take_damage(damage)
            # Triggers reaction abilities
            for ability in enemy.abilities:
                # Added two (()) because otherwise alignment doesn't work
                if ((ability.activation == 'reaction' and
                     ability.cooldown_cur == 0)):
                    if ability.target_type == 'enemy(ies)':
                        ability.activate(self, [enemy])
                    elif ability.target_type == 'self':
                        ability.activate(self, [self])
            self.add_xp(1)
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
        if amt > self.max_hp - self.cur_hp:
            amt = self.max_hp - self.cur_hp
        self.cur_hp += amt
        if amt > 0:
            print(f'{self.name} heals by {int(amt)} hp'
                  f'and is now at {self.cur_hp}/{self.max_hp}')

    def level_up(self):
        """Level up."""
        self.atk += 3
        self.ac += 2
        self.dge += 2
        self.max_hp += 5
        self.cur_hp += 5

    def add_xp(self, amt):
        """Add xp.

        Args:
            amt (int): amt of xp gained
        """
        if self.player:
            if self.lvl < 5:
                self.xp += amt
            if self.xp >= self.lvl * 10:
                self.xp -= self.lvl * 10
                self.level_up()


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
        xp (int): xp had
        abilities (list): abilities
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
        self.xp = 0
        self.abilities = []
        self.items = {'weapon': None, 'chest': None, 'head': None,
                      'hands': None, 'feet': None, 'accessory': None}

    def __str__(self):
        """Print character info.

        Returns:
            str: Character info
        """
        result = f'{self.name} ({self.subclass.name} '
        result += f'{self.rpg_class.name} {self.lvl})\n'
        result += f'     Race: {self.race.name}\n     Stats:\n'
        result += f'          ATK: {self.atk}\n'
        result += f'          AC: {self.ac}\n'
        result += f'          DGE: {self.dge}\n'
        result += f'          HP: {int(self.cur_hp)}/{self.max_hp}'
        if len(self.abilities) > 0:
            result += '\n     Abilities:'
            for ability in self.abilities:
                result += f'\n          {ability}'
        if any(item is not None for item in self.items):
            result += '\n     Items:'
            for slot, item in self.items.items():
                if item is not None:
                    result += f'\n          {slot.capitalize()}:'
                    result += f' {item.one_line()}'
        return result

    def level_up(self):
        """Level up."""
        self.lvl += 1
        self.atk += self.subclass.stats_lvl[0] + self.race.stats[0]
        self.ac += self.subclass.stats_lvl[1] + self.race.stats[1]
        self.dge += self.subclass.stats_lvl[2] + self.race.stats[2]
        self.max_hp += self.subclass.stats_lvl[3] + self.race.stats[3]
        self.cur_hp += self.subclass.stats_lvl[3] + self.race.stats[3]
        print(f'{self.name} leveled up to level {self.lvl}')
        print('-----------------------------')
        # Add new ability
        new_ability = self.subclass.abilities[self.lvl - 2]
        print(f'{self.name} gained the ability {new_ability.name}')
        self.abilities.append(new_ability)
        # Activate passive abilities
        if new_ability.activation == 'passive':
            new_ability.activate(self, [self])
        print()


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
        abilities (list): abilities list
    """

    def __init__(self):
        """Create character."""
        self.name = input('Choose Character Name: ').capitalize()
        print('-----------------')
        self.__pick_class()
        print('-----------------')
        self.__pick_subclass(self.rpg_class)
        print('-----------------')
        self.__pick_race()
        self.cur_hp = float(self.max_hp)
        self.player = True
        self.lvl = 1
        self.xp = 0
        self.abilities = []
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
            print(rpg_class.desc)
            print()
        print('-----------------')
        # Pick option
        select = "None"
        while not any(select.lower() == cl.name.lower()
                      for cl in rpg_classes):
            select = input()
            if not any(select.lower() == cl.name.lower()
                       for cl in rpg_classes):
                print('Invalid selection, try again')
        select = next(cl for cl in rpg_classes
                      if cl.name.lower() == select.lower())
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
            print(subclass)
        print('-----------------')
        # Pick option
        select_name = "None"
        while not any(select_name.lower() in sc.name.lower()
                      for sc in self.rpg_class.subclasses):
            select_name = input()
            if not any(select_name.lower() in sc.name.lower()
                       for sc in self.rpg_class.subclasses):
                print('Invalid selection, try again')
            else:
                select = next(sc for sc in self.rpg_class.subclasses
                              if select_name.lower() == sc.name.lower())
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
        races = rpg_races
        for race in races:
            print(race.name)
            for i, stat in enumerate(race.stats):
                if stat != 0:
                    print(f'     {items.bonus_order[i]}: {stat}/lvl')
        print('-----------------')
        # Pick option
        select_name = "None"
        while not any(select_name.lower() == rc.name.lower()
                      for rc in races):
            select_name = input()
            if not any(select_name.lower() == rc.name.lower()
                       for rc in races):
                print('Invalid selection, try again')
            else:
                select = next(rc for rc in races
                              if select_name.lower() == rc.name.lower())
        self.race = select
        self.atk += select.stats[0]
        self.ac += select.stats[1]
        self.dge += select.stats[2]
        self.max_hp += select.stats[3]
