"""RPG - Main Script.

Author: Caden VanV
Version: 10/4/2024
"""

import actions
import entities
import map_items

if __name__ == "__main__":
    # Intro text
    print('____________________________________________________________\n'
          '========================== TEXTRPG ==========================\n'
          '‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾')
    print('Welcome to my weekend obsession '
          'video game creation. This is a text rpg\nusing the most generic'
          'possible systems I could think of, like classes ripped\nstraight '
          'from original dnd with subclasses named after DND classes of Fin '
          'al\nFantasy, and races based off of LotR, as is only proper. This '
          'combination of\nADHD and boredom is fully functional however, and '
          'is questionably engaging\nat best. If you are in a menu and want'
          'to go back, you can enter the word\n"back" or "finished" to'
          'return.\n\nThe combt system in this game is based off of 4 stats: '
          'attack, armor, dodge,\nand hp. The chance to hit is based off of '
          'your attack compared to enemy\ndefense, and damage is based off of '
          'your attack minus half of their armor.\nHP is fairly obvious, as '
          'it determines your health.\n\nSettlements allow recruitment of new '
          'party members, at a max of 5 as well\nas buying items to buff your '
          'stats. Items can be equipt and unequipt in the\nparty view. You '
          'can choose to move towards a settlement or enemy party\nevery your '
          'turn, and you can continue to do so every turn as needed.\n\n'
          'Wandering bands are your main source of income, and will also each '
          'drop an\nitem that you can equip. Enemy bands will start off low '
          'level but higher level\nbands will spawn as the game continues.\n')
    input('Are you ready to begin? ')
    # Start game
    print('__________________________________________________________________'
          '\n========================== Begin Campaign '
          '==========================\n'
          '‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾')
    main_char = entities.PlayerCharacter()
    adv_party = map_items.PlayerParty(main_char)
    startersburg = map_items.Settlement('Startersburg', 1000)
    actions.create_world()
    startersburg.x = 0
    startersburg.y = 0
    day = 1
    while len(adv_party.members) > 0:
        day = actions.global_turn(adv_party, day)
    print('\n========================== Game Over '
          '==========================')
