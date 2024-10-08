"""RPG - Abilities.

Author: Caden VanV
Version: 10/4/2024
"""

import items


class Ability:
    """Stores a unique ability.

    Attributes:
        name (str): name
        activation (str): activation type (instant, buff, reaction, passive)
            instant are activated by the player in their turn
            buffs are activated and last multiple terms
            reactions are triggered in the attack block in entities
            passive are activated upon being gained
        effects (tuple): effects (atk, ac, dge, hp, dmg, heal)
        target_count (int): how many targets
        target_type (str): 'self', 'team', 'enemy'
            self targets only yourself, target_count should be 1
            team targets multiple team members
            enemy targets enemies
        targets_cur (list): current targets
        length (int): how many turns
        length_cur (int): how many turns currently have passed
        cooldown (int): cooldown
        cooldown_cur (int): current cooldown after activation
        active (bool): is the ability active
    """

    def __init__(self, name='Bite', activation='instant',
                 effects=(0, 0, 0, 0, 10, 0), target_count=1,
                 target_type='enemy', length=1, cooldown=2):
        """Store a unique ability.

        Args:
            name (str): name
            activation (str): type (instant, buff, reaction, passive)
            effects (tuple): effects (atk, ac, dge, hp, dmg, heal)
            target_count (int): how many targets
            target_type (str): 'self', 'teammate(s)', 'enemy(ies)'
            length (int): how many turns
            cooldown (int): cooldown
        """
        self.name = name
        self.activation = activation
        self.effects = effects
        self.target_count = target_count
        self.target_type = target_type
        self.targets_cur = []
        self.length = length
        self.length_cur = 0
        self.cooldown = cooldown
        self.cooldown_cur = 0
        self.active = False

    def __str__(self):
        """Print ability info.

        Returns:
            str: ability info
        """
        result = f'{self.name} '
        if self.activation == 'buff' and self.target_type != 'enemy(ies)':
            result += f'({self.activation.capitalize()}) '
        elif self.activation == 'buff':
            result += f'(De{self.activation}) '
        else:
            result += f'({self.activation.capitalize()}) '
        if self.activation != 'passive':
            result += '('
            if self.target_type != 'self':
                result += f'up to {self.target_count} '
            result += f'{self.target_type.capitalize()}) '
        for i, effect in enumerate(self.effects):
            if effect != 0:
                result += f'{effect} {items.bonus_order[i]}, '
        if self.activation == 'buff':
            result += f'lasts {self.length} turn(s), '
        if self.activation != 'passive':
            result += f'cooldown of {self.cooldown} turns'
        if result[-2:] == ', ':
            result = result[:-2]
        return result

    def activate(self, user, targets):
        """Activate ability.

        Args:
            user (Entity): ability user
            targets (List): list of targets
        """
        # Basic initialization
        self.targets_cur = targets
        self.length_cur = self.length + 1
        self.active = True
        # Apply effects
        if self.activation != 'passive':
            print(f'{user.name} used the ability {self.name}')
        for target in targets:
            for i in range(len(self.effects) - 2):
                if self.effects[i] != 0:
                    if self.effects[i] > 0:
                        print(f'{target.name}\'s {items.bonus_order[i]} '
                              f'was buffed by {self.effects[i]}')
                    else:
                        print(f'{target.name}\'s {items.bonus_order[i]} '
                              f'was debuffed by {self.effects[i]}')
            target.atk += self.effects[0]
            target.ac += self.effects[1]
            target.dge += self.effects[2]
            target.cur_hp += self.effects[3]
            target.max_hp += self.effects[3]
            if self.effects[4] != 0:
                print(f'{self.name} dealt {self.effects[4]} '
                      f'damage to {target.name}')
                target.take_damage(self.effects[4])
            if self.effects[5] != 0:
                target.heal(self.effects[5])
        if self.activation == 'instant':
            self.deactivate()

    def deactivate(self):
        """Deactivate ability."""
        self.active = False
        self.cooldown_cur = self.cooldown
        for target in self.targets_cur:
            if self.activation == 'buff':
                for i in range(len(self.effects) - 2):
                    if self.effects[i] != 0:
                        if self.effects[i] > 0:
                            print(f'The buff on {target.name}\'s '
                                  f'{items.bonus_order[i]} '
                                  f'for {self.effects[i]} wore off')
                        else:
                            print(f'The debuff of {target.name}\'s '
                                  f'{items.bonus_order[i]} '
                                  f'for {self.effects[i]} wore off')
            target.atk -= self.effects[0]
            target.ac -= self.effects[1]
            target.dge -= self.effects[2]
            target.take_damage(self.effects[3])
            target.max_hp -= self.effects[3]
        self.targets_cur = []

    def is_usable(self):
        """Test if the ability is usable in a turn.

        Returns:
            bool: Returns if useable on turn
        """
        usable = (not self.active and
                  self.cooldown_cur == 0 and
                  (self.activation == 'instant' or
                   self.activation == 'buff'))
        return usable


all_abilities = (Ability('Hunker Down', 'buff', (0, +2, +1, 0, 0, 0),
                         1, 'self', 2, 3),
                 Ability('Steady Defense', 'passive', (0, 2, 0, 0, 0, 0),
                         1, 'self', 0, 0),
                 Ability('Careful Strike', 'instant', (0, 0, 0, 0, 10, 0),
                         1, 'enemy(ies)', 0, 3),
                 Ability('Unyielding', 'passive', (0, 0, 0, 10, 0, 0),
                         1, 'self', 0, 0),
                 # Berserker Abilities
                 Ability('Reckless Attack', 'instant', (0, 0, 0, 0, 8, 0),
                         1, 'enemy(ies)', 0, 3),
                 Ability('Raging', 'passive', (2, 1, 0, 0, 0, 0),
                         1, 'self', 0, 0),
                 Ability('Savage Assault', 'instant', (0, 0, 0, 0, 6, 0),
                         5, 'enemy(ies)', 0, 5),
                 Ability('Blood Fury', 'passive', (5, 0, 0, 0, 0, 0),
                         1, 'self', 0, 0),
                 # Ranger Abilities
                 Ability('Volley', 'instant', (0, 0, 0, 0, 5, 0),
                         2, 'enemy(ies)', 0, 3),
                 Ability('Quick Reflexes', 'passive', (0, 0, 2, 0, 0, 0),
                         1, 'self', 0, 0),
                 Ability('Precision Shot', 'instant', (0, 0, 0, 0, 15, 0),
                         1, 'enemy(ies)', 0, 3),
                 Ability('Flexible Fighter', 'passive', (3, 0, 2, 0, 0, 0),
                         1, 'self', 0, 0),
                 # Thief Abilities
                 Ability('Smoke Bomb', 'buff', (-2, 0, -2, 0, 0, 0),
                         4, 'enemy(ies)', 3, 8),
                 Ability('Elusive', 'passive', (0, 0, 2, 0, 0, 0),
                         1, 'self', 0, 0),
                 Ability('Dodge', 'buff', (0, 0, 30, 0, 0, 0),
                         1, 'self', 1, 5),
                 Ability('Shadowstep', 'passive', (0, 0, 5, 0, 0, 0),
                         1, 'self', 0, 0),
                 # Assassin Abilities
                 Ability('Precision Strike', 'instant', (0, 0, 0, 0, 10, 0),
                         1, 'enemy(ies)', 0, 2),
                 Ability('Nimble Movement', 'passive', (0, 0, 2, 0, 0, 0),
                         1, 'self', 0, 0),
                 Ability('Execution', 'instant', (0, 0, 0, 0, 25, 0),
                         1, 'enemy(ies)', 0, 5),
                 Ability('Lethal Precision', 'passive', (5, 0, 0, 0, 0, 0),
                         1, 'self', 0, 0),
                 # Duelist Abilities
                 Ability('Riposte', 'reaction', (0, 0, 0, 0, 5, 0),
                         1, 'enemy(ies)', 0, 0),
                 Ability('Offensive Stance', 'buff', (4, 0, 0, 0, 0, 0),
                         1, 'self', 2, 4),
                 Ability('Defensive Stance', 'buff', (0, 3, 2, 0, 0, 0),
                         1, 'self', 2, 4),
                 Ability('Master Duelist', 'passive', (4, 0, 2, 0, 0, 0),
                         1, 'self', 0, 0),
                 # Elemental Caster Abilities
                 Ability('Flame Burst', 'instant', (0, 0, 0, 0, 6, 0),
                         1, 'enemy(ies)', 0, 3),
                 Ability('Air Steps', 'passive', (0, 0, 2, 0, 0, 0),
                         1, 'self', 0, 0),
                 Ability('Frost Shield', 'buff', (0, 4, 0, 0, 0, 0),
                         1, 'teammate(s)', 2, 3),
                 Ability('Stone Form', 'passive', (0, 0, 0, 15, 0, 0),
                         1, 'self', 0, 0),
                 # Light Mage Abilities
                 Ability('Radiant Burst', 'instant', (0, 0, 0, 0, 5, 0),
                         3, 'enemy(ies)', 0, 4),
                 Ability('Blinding Light', 'buff', (-2, 0, -2, 0, 0, 0),
                         5, 'enemy(ies)', 2, 5),
                 Ability('Aura of Protection', 'buff', (0, 2, 1, 0, 0, 5),
                         3, 'teammate(s)', 3, 6),
                 Ability('Inner Strength', 'passive', (5, 0, 0, 5, 0, 0),
                         1, 'self', 0, 0),
                 # Dark Mage Abilities
                 Ability('Withering', 'buff', (-2, 0, -2, 0, 0, 0),
                         3, 'enemy(ies)', 2, 4),
                 Ability('Shadow Veil', 'passive', (0, 0, 3, 0, 0, 0),
                         1, 'self', 0, 0),
                 Ability('Darkened Armor', 'buff', (0, 4, 0, 4, 0, 0),
                         1, 'self', 3, 3),
                 Ability('Curse of Darkness', 'buff', (-13, 0, 0, 0, 0, 0),
                         5, 'enemy(ies)', 1, 6),
                 # Cleric Abilities
                 Ability('Purify', 'buff', (1, 1, 1, 3, 0, 0),
                         3, 'teammate(s)', 2, 5),
                 Ability('Divine Protection', 'passive', (0, 3, 0, 0, 0, 0),
                         1, 'self', 0, 0),
                 Ability('Mass Heal', 'instant', (0, 0, 0, 0, 0, 10),
                         5, 'teammate(s)', 0, 3),
                 Ability('Shine', 'instant', (0, 0, 0, 0, 10, 0),
                         3, 'enemy(ies)', 0, 4),
                 # Paladin Abilities
                 Ability('Smite', 'instant', (0, 0, 0, 0, 8, 0),
                         1, 'enemy(ies)', 0, 3),
                 Ability('Righteousness', 'passive', (2, 2, 0, 0, 0, 0),
                         1, 'self', 0, 0),
                 Ability('Divine Shield', 'buff', (0, 15, 0, 0, 0, 0),
                         1, 'teammate(s)', 1, 4),
                 Ability('Holy Chosen', 'passive', (0, 6, 0, 8, 0, 0),
                         1, 'self', 0, 0),
                 # Zealot Abilities
                 Ability('Faithful Fury', 'buff', (6, 0, 0, 0, 0, 0),
                         1, 'self', 2, 5),
                 Ability('Zealous Endurance', 'passive', (0, 0, 0, 8, 0, 0),
                         1, 'self', 0, 0),
                 Ability('Holy Wrath', 'instant', (0, 0, 0, 0, 20, 0),
                         1, 'enemy(ies)', 0, 4),
                 Ability('Unbreakable Will', 'passive', (0, 5, 5, 0, 0, 0),
                         1, 'self', 0, 0),
                 # Arcane Knight Abilities
                 Ability('Arcane Slash', 'instant', (0, 0, 0, 0, 6, 0),
                         1, 'enemy(ies)', 0, 2),
                 Ability('Mana Shield', 'buff', (0, 5, 0, 0, 0, 0),
                         1, 'teammate(s)', 3, 5),
                 Ability('Arcane Barrage', 'instant', (0, 0, 0, 0, 10, 0),
                         1, 'teammate(s)', 0, 3),
                 Ability('Arcane Resilience', 'passive', (0, 4, 0, 15, 0, 0),
                         1, 'self', 0, 0),
                 # Runesmith Abilities
                 Ability('Rune of Flame', 'instant', (0, 0, 0, 0, 10, 0),
                         1, 'enemy(ies)', 0, 4),
                 Ability('Rune of Earth', 'buff', (0, 3, 0, 6, 0, 0),
                         1, 'self', 3, 5),
                 Ability('Rune of Wind', 'buff', (6, 0, 0, 0, 0, 0),
                         1, 'self', 2, 4),
                 Ability('Rune Explosion', 'instant', (0, 0, 0, 0, 12, 0),
                         7, 'enemy(ies)', 0, 6),
                 # Spellblade Abilities
                 Ability('Arcane Blade', 'instant', (0, 0, 0, 0, 8, 0),
                         1, 'enemy(ies)', 0, 3),
                 Ability('Arcane Agility', 'buff', (2, 0, 4, 0, 0, 0),
                         1, 'self', 2, 4),
                 Ability('Swift Strikes', 'instant', (0, 0, 0, 0, 10, 0),
                         2, 'enemy(ies)', 0, 4),
                 Ability('Spellblade Precision', 'passive', (8, 0, 0, 0, 0, 0),
                         1, 'self', 0, 0),)
