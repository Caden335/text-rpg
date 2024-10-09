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
    # Add new enemy parties, level scaling every 10 days
    type = random.randint(0, len(rpg_lists.generic_enemy_types) - 1)
    enemy_lvl = math.ceil(day / 10)
    if random.random() > 0.7:
        map_items.MonsterBand(rpg_lists.generic_enemy_types[type],
                              min(5, enemy_lvl), random.randint(2, 5))
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
        if actions == ['party', 'rest']:
            break
        print('-----------------\nPlayer Actions\n'
              '-----------------')
        for action in actions:
            print(f'{action.title()}')
        print('-----------------')
        # Pick action
        your_choice = "None"
        while your_choice.lower() not in actions:
            your_choice = input('Select Action: ')
            if your_choice == 'FULL CHEAT':
                print('CHEAT DONE')
                for member in player.members:
                    for _i in range(5 - member.lvl):
                        member.level_up()
                player.gold += 5000
                player.inv += items.all_items
            elif your_choice == 'MINOR CHEAT':
                print('CHEAT DONE')
                for member in player.members:
                    member.level_up()
                player.gold += 300
            if your_choice.lower() not in actions:
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
        elif your_choice.lower() == 'fight enemy':
            enemy = next(item for item in map_items.map_items
                         if item.x == 0 and item.y == 0 and
                         item.mobile and item.hostile)
            create_encounter(player, enemy)
            break
        elif your_choice.lower() == 'new move':
            back = new_move(player)
            if not back == 'back':
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
        if ((str(your_choice).lower() == 'back' or
             str(your_choice).lower() == 'finished')):
            return 'back'
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
    actions = ['recruit', 'shop']
    if len(player.members) == 5:
        actions[0] = actions[0] + ' (party full)'
    for action in actions:
        print(action.capitalize())
    print('-----------------')
    # Get action selection
    select = 'None'
    while select.lower() not in actions:
        select = input('What would you like to do? ')
        if select.lower() == 'back' or select.lower() == 'finished':
            return
        elif select.lower() not in actions:
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
    select = ''
    while select.lower() != 'finished' and select.lower() != 'back':
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
        if index_val.lower() == 'finished' or index_val.lower() == 'back':
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
        take_turn(team1.members, team2.members)
        team2.members = [char for char in team2.members if char.cur_hp > 0]
        if len(team2.members) > 0:
            take_turn(team2.members, team1.members)
            team1.members = [char for char in team1.members
                             if char.cur_hp > 0]
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
        for char in team1.members:
            for abil in char.abilities:
                abil.length_cur = 0
                if abil.activation == 'buff' or abil.activation == 'reaction':
                    abil.deactivate()
                abil.cooldown_cur = 0
        team1.leader = team1.members[0]
        print()
    else:
        print('-----------------\nWinners - Team 2\n-----------------')
        team2.gold += team1.gold
        team2.leader = team2.members[0]
        for char in team2.members:
            for abil in char.abilities:
                abil.length_cur = 0
                if abil.activation == 'buff' or abil.activation == 'reaction':
                    abil.deactivate()
                abil.cooldown_cur = 0
    print('Survivors')


def take_turn(team, enemy_team):
    """One team takes its turn.

    Args:
        team (list): The team going
        enemy_team (list): The team being targetted
    """
    for char in team:
        # Check is player controlled or not
        for abil in char.abilities:
            if abil.length_cur > 0:
                abil.length_cur -= 1
                if abil.length_cur == 0:
                    abil.deactivate()
            if abil.cooldown_cur > 0:
                abil.cooldown_cur -= 1
        if char.player:
            act_type = 'None'
            # Potential actions on turn
            actions = ['ability', 'attack']
            # Get input, run actions
            while act_type not in actions:
                act_type = input('Do you want to use an ability or attack? ')
                # Attack enemies
                if act_type == 'attack':
                    print('-----------------')
                    print(f'Who do you want {char.name} to target?')
                    for i, enemy in enumerate(enemy_team):
                        print(f'{i + 1}. {enemy.name}')
                    target = -1
                    while target not in range(len(enemy_team)):
                        target = int(input()) - 1
                        if target in range(len(enemy_team)):
                            char.attack(enemy_team[target])
                        else:
                            print('Invalid target, please try again')
                # Use ability, if you have usable ability
                elif (act_type == 'ability' and len(char.abilities) > 0 and
                      any(ability.is_usable() for ability in char.abilities)):
                    pick_use_ability(char, team, enemy_team)
                # Use ability, but none are available
                elif (act_type == 'ability' and
                      (len(char.ability) == 0 or
                       not any(ability.is_usable() for
                               ability in char.abilities))):
                    print('You have no usable abilities right now')
                else:
                    print('Invalid selection, try again')
            print()
        else:  # AI actions
            target = random.randint(0, len(enemy_team) - 1)
            char.attack(enemy_team[target])
    print()


def pick_use_ability(char, team, enemy_team):
    """One team takes its turn.

    Args:
        char (Entity): entity using their turn
        team (list): The team going
        enemy_team (list): The team being targetted
    """
    # Print abilities
    print('-----------------')
    for ability in char.abilities:
        if ability.is_usable():
            print(ability)
    print('-----------------')
    # Select ability
    abil_select = 'None'
    while not any(abil_select.lower() == abil.name.lower()
                  for abil in char.abilities):
        abil_select = input('Which ability do '
                            'you want to use? ')
        if not any(abil_select.lower() == abil.name.lower()
                   for abil in char.abilities):
            print('Invalid ability, try again')
        elif any(abil_select.lower() == abil.name.lower()
                 and not abil.is_usable()
                 for abil in char.abilities):
            print('You can\'t use that ability right now')
            abil_select = 'None'
        else:
            abil = next(abil for abil in char.abilities
                        if abil.name.lower() == abil_select.lower())
            if abil.target_type == 'self':
                abil.activate(char, [char])
            else:
                print(f'Who do you want {abil.name} to target?')
                your_targets = []
                your_targets_i = []
                if abil.target_type == 'enemy(ies)':
                    abil_targets = enemy_team
                else:
                    abil_targets = team
                for i, targ in enumerate(abil_targets):
                    print(f'{i + 1}. {targ.name}')
                targ_len = min(len(abil_targets), abil.target_count)
                while len(your_targets) < targ_len:
                    new_targ = int(input('Who do you want to target?')) - 1
                    if ((new_targ in range(len(abil_targets)) and
                         new_targ not in your_targets_i)):
                        your_targets.append(abil_targets[new_targ])
                        your_targets_i.append(new_targ)
                        print(f'({len(your_targets)}/{targ_len})')
                    elif new_targ not in range(len(abil_targets)):
                        print('Invalid target, try again')
                    elif new_targ in your_targets_i:
                        print('Already targeted, try again')
                abil.activate(char, your_targets)


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
    while not any(person.lower() == char.name.lower()
                  for char in player.members):
        person = input('Select character: ')
        if person == 'finished' or person == 'back':
            return
        if not any(person.lower() == char.name.lower()
                   for char in player.members):
            print('Invalid option, try again')
    person = next(char for char in player.members
                  if char.name.lower() == person.lower())
    select = 'None'
    # Keeps running while not finished
    while select.lower() != 'finished' and select.lower() != 'back':
        while select.lower() != 'equip' and select.lower() != 'unequip':
            select = input('Equip or Unequip? ')
            if select.lower() == 'finished' or select.lower() == 'back':
                return
        # Unequip objects
        if select.lower() == 'unequip':
            print(person.name)
            for key, val in person.items.items():
                if val is not None:
                    print(f'     {key.capitalize()}: {val.one_line()}')
            sel_item = ''
            while (sel_item.lower() != 'back' and
                   sel_item.lower() != 'finished'):
                while not any(person.items[val] is not None and
                              sel_item.lower() ==
                              person.items[val].name.lower()
                              for val in person.items):
                    sel_item = input('Which item do you want to unequip? ')
                    if ((sel_item.lower() == 'finished' or
                         sel_item.lower() == 'back')):
                        break
                    elif not any(person.items[val] is not None and
                                 sel_item.lower() ==
                                 person.items[val].name.lower()
                                 for val in person.items):
                        print('Invalid item, try again')
                    else:
                        item = next(person.items[val] for val in person.items
                                    if person.items[val] is not None and
                                    person.items[val].name.lower() ==
                                    sel_item.lower())
                        item.unequip()
                        player.inv.append(item)
                        sel_item = ''
                select = ''
        # Equip objects
        elif select.lower() == 'equip':
            sel_item = ''
            while (sel_item.lower() != 'back' and
                   sel_item.lower() != 'finished'):
                while not any(sel_item.lower() == item.name.lower()
                              for item in player.inv):
                    sel_item = input('Which item do you want to equip? ')
                    if ((sel_item.lower() == 'finished' or
                         sel_item.lower() == 'back')):
                        break
                    elif not any(sel_item.lower() == item.name.lower()
                                 for item in player.inv):
                        print('Invalid item, try again')
                    else:
                        item = next(item for item in player.inv
                                    if item.name.lower() == sel_item.lower())
                        item.equip(person)
                        player.inv.remove(item)
                        sel_item = ''
            select = ''
