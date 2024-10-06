"""RPG - Functions.

Author: Caden VanV
Version: 10/4/2024
"""
import random
import map_items
import rpg_lists
import math
import items


def create_world():
    """Generate settlements, and enemies."""
    for _i in range(random.randint(4, 8)):
        s_pref = [pref for pref in rpg_lists.rpg_names
                  if len(pref) <= 4]
        s_pref = s_pref + list(rpg_lists.settlement_pref)
        suf = random.randint(0, len(rpg_lists.settlement_suf) - 1)
        settlement_name = f'{s_pref[random.randint(0, len(s_pref) - 1)]}'
        settlement_name += f'{rpg_lists.settlement_suf[suf]}'
        map_items.Settlement(settlement_name, random.randint(1000, 10000))
    for _i in range(random.randint(12, 15)):
        type = random.randint(0, len(rpg_lists.generic_enemy_types) - 1)
        map_items.MonsterBand(rpg_lists.generic_enemy_types[type],
                              1, random.randint(2, 5))


def global_turn(player, day):
    """Global turn.

    Args:
        player (PlayerParty): player party
        day (int): day

    Returns:
        int: next day number
    """
    print(f'\n========================== Day {day} '
          '==========================')
    # AI Turns
    for item in map_items.map_items:
        if item.mobile:
            if item == player.target_move:
                item.wander(True)
            else:
                item.wander(False)
        else:
            item.generate_items()
            item.generate_recruitables()
            item.wealth = int(item.wealth * ((random.random() / 10) + 0.95))
    # Add new enemy parties, level scaling every 2.5 days
    type = random.randint(0, len(rpg_lists.generic_enemy_types) - 1)
    if random.random() > 0.7:
        map_items.MonsterBand(rpg_lists.generic_enemy_types[type],
                              math.ceil(day / 2.5), random.randint(2, 5))
    # Player goes
    select_options(player)
    # Increment day
    day += 1
    return day


def select_options(player):
    """Player turn options.

    Args:
        player (PlayerParty): Your party
    """
    can_move = True
    while True:
        # Print possible actions
        actions = get_actions(player, can_move)
        print('-----------------\nPlayer Actions\n'
              '-----------------')
        for action in actions:
            print(f'{action.capitalize()}')
        print('-----------------')
        # Pick action
        your_choice = -1
        while your_choice not in actions:
            your_choice = input('Select Action: ')
            if your_choice not in actions:
                print('Invalid selection, try again')
        # What happens
        if your_choice.lower() == 'rest':
            for char in player.members:
                char.heal(100)
            break
        elif your_choice.lower() == 'continue moving':
            print()
            player.move_to(player.target_move)
            can_move = False
        elif your_choice == 'Fight Enemy':
            enemy = next(item for item in map_items.map_items
                         if item.x == 0 and item.y == 0 and
                         item.mobile and item.hostile)
            create_encounter(player, enemy)
            break
        elif your_choice.lower() == 'new move':
            back = new_move(player)
            if not back.lower() == 'back':
                can_move = False
        elif your_choice.lower() == 'settlement':
            settlement_actions(player)
        elif your_choice.lower() == 'party':
            party_view(player)


def get_actions(player, can_move):
    """Get player actions.

    Args:
        player (PlayerParty): Your party
        can_move (bool): Has movement available

    Returns:
        list: Possible actions
    """
    actions = []
    if any(item.x == 0 and item.y == 0 and item.mobile and item.hostile
           for item in map_items.map_items):
        actions.append('fight enemy')
    if any(item.x == 0 and item.y == 0 and not item.mobile
           for item in map_items.map_items):
        actions.append('settlement')
    if player.target_move is not None and can_move:
        actions.append('continue moving')
    if can_move:
        actions.append('new move')
    actions.append('party')
    actions.append('rest')
    return actions


def new_move(player):
    """Create new movement.

    Args:
        player (PlayerParty): player party

    Returns:
        str: Back or not
    """
    print('-----------------\nNearby Locations\n-----------------')
    for i, loc in enumerate(map_items.map_items):
        if loc.calculate_dir()[0] < 50:
            print(i, end='. ')
            map_items.print_map_item(loc)
    your_choice = 'None'
    while not any(your_choice == i for i in range(len(map_items.map_items))):
        your_choice = int(input('Where do you want to go? (#) '))
        if your_choice == 'Back':
            return 'Back'
        if not any(your_choice == i for i in range(len(map_items.map_items))):
            print('Invalid selection, try again')
        else:
            select = map_items.map_items[your_choice]
    player.move_to(select)
    return 'Not'


def settlement_actions(player):
    """Create new movement.

    Args:
        player (PlayerParty): player party
    """
    # Get the settlement
    settlement = next(item for item in map_items.map_items
                      if item.x == 0 and item.y == 0)
    # Print out possible actions
    print(f'-----------------\n{settlement.name}\n-----------------')
    actions = ['Recruit', 'Shop']
    if len(player.members) == 5:
        actions[0] = actions[0] + ' (party full)'
    for action in actions:
        print(action)
    print('-----------------')
    # Get action selection
    select = 'None'
    while select not in actions:
        select = input('What would you like to do? ')
        if select.lower() == 'back':
            return
        elif select not in actions:
            print('Invalid option, try again')
    if select.lower() == 'recruit':
        pick_team(player, settlement)
    elif select.lower() == 'shop':
        settlement_shop(player, settlement)


def settlement_shop(player, settlement):
    """Buy items from shop.

    Args:
        player (PlayerParty): Your current team
        settlement (Settlement): settlement
    """
    # Print shop
    print('-----------------\nSettlement Shop\n-----------------')
    items.print_item_list(settlement.shop)
    print('-----------------')
    print('What do you want to buy?')
    select = None
    while select != 'finished':
        select = input('Type item name or '
                       'type "finished" to end: ')
        if any(select == item.name for item in settlement.shop):
            item = next(item for item in settlement.shop
                        if item.name == select)
            if item.cost <= player.gold:
                player.gold -= item.cost
                print(f'Successfully bought {item.name} for {item.cost} gold. '
                      f'You now have {player.gold} left')
                player.inv.append(item)
                settlement.shop.remove(item)
            else:
                print(f'You do not have enough gold to buy {item.name}, '
                      'try again')
        else:
            print('Invalid selection, try again')


def pick_team(player, settlement):
    """Recruit characters from settlement for team.

    Args:
        player (PlayerParty): Your current team
        settlement (Settlement): settlement
    """
    # Print intro and options
    print('--------------------- Recruit Party Members ---------------------')
    print(f'Select up to {5 - len(player.members)} available '
          'characters for your team:')
    print('--------------------------------------------------------------')
    for i, character in enumerate(settlement.recruitables):
        print(f'{i + 1}. {character[0].name} ({character[0].race.name} '
              f'{character[0].subclass.name} {character[0].lvl}): '
              f'{character[1]} gold')
    print('-----------------')
    # Recruit people
    print('Who Do You Want?')
    selected = []
    while len(player.members) < 5:
        index_val = input('Enter number for character '
                          'or type "finished" to end: ')
        if index_val.lower() == 'finished':
            break
        if index_val.isdigit():
            index_val = int(index_val) - 1
            if settlement.recruitables[index_val][1] <= player.gold:
                player.gold -= settlement.recruitables[index_val][1]
                print('Successfully recruited '
                      f'{settlement.recruitables[index_val][0].name} '
                      f'for {settlement.recruitables[index_val][1]} '
                      f'gold. You now have {player.gold} left')
                settlement.recruitables[index_val][0].player = True
                player.members.append(settlement.recruitables[index_val][0])
                selected.append(index_val)
                print(f'Team Capacity - {len(player.members)}/5')
            else:
                print('You do not have enough gold to recruit'
                      f'{settlement.recruitables[index_val][0].name}, '
                      'try again')
        else:
            print('Invalid pick, try again')
    settlement.recruitables = [char for i, char in
                               enumerate(settlement.recruitables)
                               if i not in selected]


def create_encounter(team1, team2):
    """Combat between 2 sides.

    Args:
        team1 (Band): Player side
        team2 (Band): Enemy side
    """
    # Print sides
    print('----------------- Battle Lineup -----------------')
    print('-----------------\nTeam 1\n-----------------')
    for char in team1.members:
        print(f'{char.name}: {int(char.cur_hp)}/{char.max_hp} hp')
    print('-----------------\nTeam 2\n-----------------')
    for char in team2.members:
        print(f'{char.name}: {int(char.cur_hp)}/{char.max_hp} hp')
    # The battle begins
    print('----------------- The Battle Begins -----------------')
    turn_count = 1
    while len(team1.members) > 0 and len(team2.members) > 0:
        print(f'-----------------\nTurn {turn_count}\n-----------------')
        dead = take_turn(team1.members, team2.members)
        team2.members = [char for i, char in
                         enumerate(team2.members) if i not in dead]
        if len(team2.members) > 0:
            dead = take_turn(team2.members, team1.members)
            team1.members = [char for i, char in
                             enumerate(team1.members) if i not in dead]
        turn_count += 1
    # Ending
    print('----------------- Encounter Over -----------------')
    if len(team1.members) > 0:
        print('-----------------\nWinners - Team 1\n-----------------')
        team1.gold += team2.gold
        map_items.map_items.remove(team2)
        # Print loot
        print('Loot:')
        print(f'    {team2.gold} gold')
        for item in team2.inv:
            team1.inv.append(item)
            print('   ', item.one_line())
        team1.leader = team1.members[0]
        print()
    else:
        print('-----------------\nWinners - Team 2\n-----------------')
        team2.gold += team1.gold
        team2.leader = team2.members[0]
    print('Survivors')


def take_turn(team, enemy_team):
    """One team takes its turn.

    Args:
        team (list): The team going
        enemy_team (list): The team being targetted

    Returns:
        list: Any dead enemies, if any
    """
    dead_enemies = []
    for char in team:
        possible_targets = list(range(len(enemy_team)))
        if char.player:
            print(f'Who do you want {char.name} to target?')
            for i, enemy in enumerate(enemy_team):
                print(f'{i + 1}. {enemy.name}')
            target = -1
            while target not in possible_targets:
                target = int(input()) - 1
                if target in possible_targets:
                    char.attack(enemy_team[target])
                    if enemy_team[target].cur_hp <= 0:
                        dead_enemies.append(target)
                else:
                    print('Invalid target, please try again')
            print()
        else:
            target = random.randint(0, len(enemy_team) - 1)
            char.attack(enemy_team[target])
            if enemy_team[target].cur_hp <= 0:
                dead_enemies.append(target)
        if dead_enemies == possible_targets:
            return dead_enemies
    print()
    return dead_enemies


def party_view(player):
    """Party view.

    Args:
        player (PlayerParty): Your current team
    """
    # Print party members
    print('-----------------\nParty Members\n-----------------')
    for char in player.members:
        print(char)
        print()
    # Print party inventory
    print('-----------------\nParty Inventory\n-----------------')
    items.print_item_list(player.inv)
    # Char item actions
    print('-----------------\nItem Actions\n-----------------')
    person = 'None'
    while not any(person == char.name for char in player.members):
        person = input('Select character: ')
        if person == 'finished':
            return
        if not any(person == char.name for char in player.members):
            print('Invalid option, try again')
    person = next(char for char in player.members if char.name == person)
    select = 'None'
    while select.lower() != 'finished':  # Keeps running while not finished
        while select.lower() != 'equip' and select.lower() != 'unequip':
            select = input('Equip or Unequip? ')
            if select == 'finished':
                return
        # Unequip objects
        if select.lower() == 'unequip':
            print(person.name)
            for key, val in person.items.items():
                if val is not None:
                    print(f'     {key.capitalize()}: {val.name}')
            while not any(person.items[val] is not None and
                          select == person.items[val].name
                          for val in person.items):
                select = input('Which item do you want to unequip? ')
                if select.lower() == 'finished':
                    return
                if not any(person.items[val] is not None and
                           select == person.items[val].name
                           for val in person.items):
                    print('Invalid item, try again')
            item = next(person.items[val] for val in person.items
                        if person.items[val] is not None and
                        person.items[val].name == select)
            item.unequip()
            player.inv.append(item)
        # Equip objects
        elif select.lower() == 'equip':
            while not any(select == item.name for item in player.inv):
                select = input('Which item do you want to equip? ')
                if select.lower() == 'finished':
                    return
                if not any(select == item.name for item in player.inv):
                    print('Invalid item, try again')
            item = next(item for item in player.inv if item.name == select)
            item.equip(person)
            player.inv.remove(item)
