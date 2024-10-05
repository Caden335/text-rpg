"""RPG - Main Script.

Author: Caden VanV
Version: 10/4/2024
"""

import actions
import entities
import map_items

if __name__ == "__main__":
    print(f'\n========================== Begin Campaign '
          '==========================')
    main_char = entities.PlayerCharacter()
    adv_party = map_items.PlayerParty(main_char)
    actions.create_world()
    startersburg = map_items.Settlement('Startersburg', 1000)
    startersburg.x = 0
    startersburg.y = 0
    day = 1
    while len(adv_party.members) > 0:
        day = actions.global_turn(adv_party, day)
    print('\n========================== Game Over '
          '==========================')
