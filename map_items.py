"""RPG - Map Item Classes.

Author: Caden VanV
Version: 10/4/2024
"""

import random
import entities
import math
import items


map_items = []


def print_map_items():
    """Print all map items."""
    for item in map_items:
        text = item.name
        if item.mobile:
            text += f' ({len(item.members)})'
        if not item.mobile:
            text += f'\n     Wealth: {item.wealth:,}'
        location = item.calculate_dir()
        text += f'\n     {location[0]:.1f} miles {location[1]}'
        print(text)


def print_map_item(item):
    """Print map item following above template.

    Args:
        item (MapItem): Map item being printed
    """
    text = item.name
    if item.mobile:
        text += f' ({len(item.members)})'
    if not item.mobile:
        text += f'\n     Wealth: {item.wealth:,}'
    location = item.calculate_dir()
    text += f'\n     {location[0]:.1f} miles {location[1]}'
    print(text)


class MapItem:
    """Stores a map item.

    Attributes:
        name (str): name
        x (int): location horizontally from player
        y (int): location vertically from player
        mobile (bool): can it move
        hostile (bool): hostile to player?
        player (bool): player controlled?
        leader (Entity): being in charge
    """

    def __init__(self):
        """Create generic map item."""
        self.name = 'City'
        self.x = random.randint(-100, 100)
        self.y = random.randint(-100, 100)
        while any((self.x == loc.x and self.y == loc.y and
                   not self == loc) for loc in map_items):
            self.x += 1
            self.y += 1
        self.mobile = False
        self.hostile = False
        self.player = False
        self.leader = entities.RPGCharacter()
        map_items.append(self)

    def __str__(self):
        """Print map item info.

        Returns:
            str: map item info
        """
        location = self.calculate_dir()
        result = f'{self.name}\n'
        result += f'     Leader: {self.leader.name}\n'
        result += f'     Hostile: {self.hostile}\n'
        result += f'     Location: {location[0]:.1f} miles {location[1]}\n'
        return result

    def debug_print_all(self):
        """Return all attributes.

        Returns:
            tuple: all attributes
        """
        return (self.name, self.x, self.y,
                self.mobile, self.hostile,
                self.player, self.leader.name)

    def calculate_dir(self):
        """Calculate dir from player.

        Returns:
            tuple: direction and distance
        """
        dist = (self.x*self.x + self.y*self.y)**0.5
        # atan2 gives angle from EAST in radians (-pi to pi),
        # then we normalize it to -1 to 1, then 0 to 8.
        # Rounding gives nearest cardinal direction,
        # then we spit that out as an index in the direction list.
        # We must have a second copy of "EAST" in the
        # list as 0-8 has 9 integer slots, and in this mod 8 system,
        # 0 = 8, similar to how circles work.
        theta = round((math.atan2(self.y, self.x)/math.pi) * 4 + 4)
        directions = ("E", "NE", "N", "NW",
                      "W", "SW", "S", "SE", "E")
        return (dist, directions[theta])


class Settlement(MapItem):
    """Stores a settlement.

    Attributes:
        name (str): name
        x (int): location horizontally from player
        y (int): location vertically from player
        mobile (bool): always False
        hostile (bool): always False
        player (bool): always False
        wealth (int): wealth in gold
        shop (list): list of items in stock
        recruitables (list): recruitable characters and their cost
        leader (Entity): being in charge
    """

    def __init__(self, name, wealth):
        """Create generic settlement.

        Args:
            name (str): Name of settlement
            wealth (int): Wealth
        """
        self.name = name
        self.wealth = wealth
        self.x = random.randint(-100, 100)
        self.y = random.randint(-100, 100)
        while any((self.x == loc.x and self.y == loc.y and
                   not self == loc) for loc in map_items):
            self.x += 1
            self.y += 1
        self.mobile = False
        self.hostile = False
        self.player = False
        self.leader = entities.RPGCharacter()
        self.shop = []
        self.recruitables = []
        self.generate_items()
        self.generate_recruitables()
        map_items.append(self)

    def __str__(self):
        """Print map item info.

        Returns:
            str: map item info
        """
        location = self.calculate_dir()
        result = f'{self.name}\n'
        result += f'     Leader: {self.leader.name}\n'
        result += f'     Wealth: {self.wealth}\n'
        result += f'     Location: {location[0]:.1f} miles {location[1]}\n'
        return result

    def generate_items(self):
        """Generate items for shop."""
        for _x in range(len(self.shop), 10):
            rar = random.random()
            if rar < 0.75:
                rand = random.randint(0, len(items.common_items) - 1)
                item = items.common_items[rand]
            elif rar < 0.9:
                rand = random.randint(0, len(items.well_made_items) - 1)
                item = items.well_made_items[rand]
            elif rar < 0.97:
                rand = random.randint(0, len(items.expert_items) - 1)
                item = items.expert_items[rand]
            else:
                rand = random.randint(0, len(items.masterwork_items) - 1)
                item = items.masterwork_items[rand]
            self.shop.append(item)

    def generate_recruitables(self):
        """Generate items for shop."""
        for _x in range(len(self.recruitables), 10):
            self.recruitables.append((entities.RPGCharacter(),
                                      random.randint(20, 100)))


class Band(MapItem):
    """Stores a party of entities.

    Attributes:
        name (str): name
        x (int): location horizontally from player
        y (int): location vertically from player
        mobile (bool): can it move
        hostile (bool): hostile to player?
        player (bool): player controlled?
        leader (Entity): being in charge, equals members[0]
        members (list): list of all members
        movement (int): movement in miles per/turn
        gold (int): gold stored
        inv (list): items
    """

    def __init__(self, leader):
        """Create party.

        Args:
            leader (Entity): leader and first member of party.
        """
        self.name = f'{leader.name}\'s Band'
        self.x = random.randint(-100, 100)
        self.y = random.randint(-100, 100)
        while any((self.x == loc.x and self.y == loc.y and
                   not self == loc) for loc in map_items):
            self.x += 1
            self.y += 1
        self.mobile = True
        self.hostile = False
        self.player = False
        self.leader = leader
        self.members = [leader]
        map_items.append(self)
        self.movement = 10
        self.gold = 0
        self.inv = []

    def __str__(self):
        """Print map item info.

        Returns:
            str: map item info
        """
        location = self.calculate_dir()
        result = f'{self.name}\n'
        result += f'     Leader: {self.leader.name}\n'
        result += f'     Hostile: {self.hostile}\n'
        result += f'     Location: {location[0]:.1f} miles {location[1]}\n'
        result += f'     Member Count: {len(self.members)}'
        return result

    def move(self, x, y):
        """Move band by amount.

        Args:
            x (int): Moves horizontally
            y (int): Moves vertically
        """
        self.x += x
        self.y += y

    def wander(self, say):
        """Randomly move in any direction.

        Args:
            say (bool): Print or not
        """
        x = random.randint(-self.movement, self.movement)
        y = self.movement - abs(x)
        if random.random() < 0.5:
            y = -y
        self.move(x, y)
        if say:
            ns = 'S'
            ew = 'W'
            if y > 0:
                ns = 'N'
            if x > 0:
                ew = 'E'
            loc = self.calculate_dir()
            print(f'{self.name} has moved {y} {ns} and {x} {ew} '
                  f'and is now {loc[0]:.1f} miles {loc[1]}')
        while any((self.x == loc.x and self.y == loc.y and
                   not self == loc) for loc in map_items):
            self.x += 1
            self.y += 1


class PlayerParty(Band):
    """Stores the player's party.

    Attributes:
        name (str): name
        x (int): always 0
        y (int): always 0
        mobile (bool): always True
        hostile (bool): always False
        player (bool): always True
        leader (Entity): player character
        members (list): list of all members
        movement (int): movement in miles per/turn
        target_move (MapItem): target to move towards
        gold (int): gold
        inv (list): items
    """

    def __init__(self, leader):
        """Create player party.

        Args:
            leader (Entity): leader and first member of party.
        """
        self.name = f'{leader.name}\'s Party'
        self.x = 0
        self.y = 0
        self.mobile = True
        self.hostile = False
        self.player = True
        self.leader = leader
        self.members = [leader]
        self.movement = 10
        self.gold = 100
        self.inv = []
        self.target_move = None

    def __str__(self):
        """Print map item info.

        Returns:
            str: map item info
        """
        result = f'{self.name}\n'
        result += f'     Leader: {self.leader.name}\n'
        result += '     Members:\n'
        for member in self.members:
            result += f'        {member.name}\n'
        result += f'     Capacity: {len(self.members)}/5'
        return result

    def move(self, x, y):
        """Move all other items by negative amount.

        Args:
            x (int): Moves horizontally
            y (int): Moves vertically
        """
        for map_item in map_items:
            map_item.x -= x
            map_item.y -= y

    def move_to(self, target):
        """Move towards something.

        Args:
            target (MapItem): target to move towards
        """
        dist_x = target.x - self.x
        dist_y = target.y - self.y
        total_dist = math.sqrt(dist_x**2 + dist_y**2)
        if total_dist == 0:
            print(f"You are already at {target.name}.")
            return
        if total_dist <= self.movement:
            self.move(dist_x, dist_y)
            self.target_move = None
            print(f'You have arrived at {target.name}.')
        else:
            move_fraction = self.movement / total_dist
            move_x = int(dist_x * move_fraction)
            move_y = int(dist_y * move_fraction)
            # Makes sure we're staying under the total movement
            total_move = abs(move_x) + abs(move_y)
            if total_move > self.movement:
                scale_factor = self.movement / total_move
                move_x = int(move_x * scale_factor)
                move_y = int(move_y * scale_factor)
            self.move(move_x, move_y)
            self.target_move = target
            print(f'You have moved towards {target.name}\n'
                  f'Trip will take an additional '
                  f'{self.calculate_travel_time(target)} days')

    def calculate_travel_time(self, target):
        """Calculate how long it will take to move towards something.

        Args:
            target (MapItem): target to test

        Returns:
            int: Turns to reach target
        """
        dist_x = target.x - self.x
        dist_y = target.y - self.y
        total_dist = math.sqrt(dist_x ** 2 + dist_y ** 2)
        turns = math.ceil(total_dist / self.movement)
        return turns


class MonsterBand(Band):
    """Create a band of monsters.

    Attributes:
        name (str): name
        x (int): distance from player horizontally
        y (int): distance from player vertically
        mobile (bool): always True
        hostile (bool): always True
        player (bool): always False
        leader (Entity): main monster
        members (list): list of all members
        movement (int): movement in miles per/turn
        diff (int): difficulty
        inv (list): items
    """

    def __init__(self, type, lvl, amt):
        """Create band of monsters.

        Args:
            type (str): What type of enemies
            lvl (int): Level of enemies
            amt (int): Amount of enemies
        """
        # Basic stats for all
        atk = 5 + (2 * lvl)
        ac = 5 + (2 * lvl)
        dge = 5 + (2 * lvl)
        hp = 20 + (5 * lvl)
        # Elite monster in charge
        prefixes = ('Raging ', 'Vicious ', 'Bloodthirsty ',
                    'Alpha ', 'Great ', 'Giant ')
        prefix = prefixes[random.randint(0, len(prefixes) - 1)]
        self.leader = entities.Entity(prefix + type,
                                      atk + 6, ac + 2, dge + 1, hp + lvl)
        super().__init__(self.leader)
        # Generate generic monsters
        for i in range(amt - 1):
            self.members.append(entities.Entity(type, atk, ac, dge, hp))
            self.gold += 10 + (10 * lvl)
        # Unique setup
        self.hostile = True
        self.diff = lvl
        # Drops
        self.gold += 30 + ((20 * lvl) * amt)
        if lvl == 1 or lvl == 2:
            item_pool = items.common_items
        elif lvl == 3:
            item_pool = items.well_made_items
        elif lvl == 4:
            item_pool = items.expert_items
        elif lvl == 5:
            item_pool = items.masterwork_items
        rand = random.randint(0, len(items.common_items) - 1)
        self.inv = [item_pool[rand]]

    def __str__(self):
        """Print map item info.

        Returns:
            str: map item info
        """
        location = self.calculate_dir()
        result = f'{self.name}\n'
        result += f'     Leader: {self.leader.name}\n'
        result += f'     Hostile: {self.hostile}\n'
        result += f'     Location: {location[0]:.1f} miles {location[1]}\n'
        result += f'     Member Count: {len(self.members)}'
        result += f'     Difficulty: {self.diff}'
        return result
