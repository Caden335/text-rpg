"""RPG - Functions.

Author: Caden VanV
Version: 10/4/2024
"""
import random
import entities
import map_items
import rpg_lists


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
                              random.randint(0, 4), random.randint(2, 5))


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
    select_options(player)
    for item in map_items.map_items:
        if item.mobile:
            item.wander()
        else:
            item.generate_items()
            item.generate_recruitables()
            item.wealth = int(item.wealth * ((random.random() / 10) + 0.95))
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
        print('-----------------\nPlayer Actions\n'
              '-----------------')
        actions = get_actions(player, can_move)
        for action in actions:
            print(f'{action}')
        print('-----------------')
        # Pick action
        your_choice = -1
        while your_choice not in actions:
            your_choice = input('Select Action: ')
            if your_choice not in actions:
                print('Invalid selection, try again')
        # What happens
        if your_choice == 'Rest':
            break
        elif your_choice == 'Continue Movement':
            print()
            player.move_to(player.target_move)
            can_move = False
        elif your_choice == 'Fight Enemy':
            enemy = next(item.x == 0 and item.y == 0 and
                         item.mobile and item.hostile
                         for item in map_items.map_items)
            create_encounter(player, enemy)
            break


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
        actions.append('Fight Enemy')
    if any(item.x == 0 and item.y == 0 and not item.mobile
           for item in map_items.map_items):
        actions.append('Interact With Settlement')
    if player.target_move is not None and can_move:
        actions.append('Continue Movement')
    if can_move:
        actions.append('New Movement')
    actions.append('Rest')
    return actions


def pick_team(team):
    """Create available characters and pick some for team.

    Args:
        team (list): Your current team

    Returns:
        list: Your team
    """
    available_characters = [entities.RPGCharacter(), entities.RPGCharacter(),
                            entities.RPGCharacter(), entities.RPGCharacter(),
                            entities.RPGCharacter(), entities.RPGCharacter(),
                            entities.RPGCharacter(), entities.RPGCharacter()]
    names = []
    print('----------------- Pick Your Party -----------------')
    print('Select 4 available characters for your team:')
    print('------------------------------------------------------')
    for character in available_characters:
        print(character)
        print()
        names.append(character.name)
    print('Who Do You Want')
    for i in range(5 - len(team)):
        name = input()
        index = names.index(name)
        team.append(available_characters.pop(index))
        names.pop(index)
        print(f'Team Capacity - {i + 2}/5')
    return team


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
    print('\n-----------------\nTeam 2\n-----------------')
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
        winning_team = team1.members
        team1.gold += team2.gold
        map_items.map_items.remove(team2)
    else:
        print('-----------------\nWinners - Team 2\n-----------------')
        winning_team = team2.members
        team2.gold += team1.gold
    print('Survivors')
    for char in winning_team:
        print(f'{char.name}: {char.cur_hp}/{char.max_hp} hp')
        char.cur_hp = char.max_hp


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
                    print()
                else:
                    print('Invalid target, please try again')
        else:
            target = random.randint(0, len(enemy_team) - 1)
            char.attack(enemy_team[target])
            if enemy_team[target].cur_hp <= 0:
                dead_enemies.append(target)
            print()
        if dead_enemies == possible_targets:
            return dead_enemies
    return dead_enemies
