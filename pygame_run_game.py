"""RPG - Main Script.

Author: Caden VanV
Version: 10/4/2024
"""

import actions
import entities
import map_items
import pygame

import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((2240, 1400))
clock = pygame.time.Clock()
running = True
startersburg = map_items.Settlement('Startersburg', 1000)
actions.create_world()
startersburg.x = 0
startersburg.y = -1
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
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
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("dark green")
    pygame.draw.circle(screen, 'black', player_pos, 10)
    for item in map_items.map_items:
        if abs(item.x) <= 56 and abs(item.y) < 35:
            if item.mobile:
                  pygame.draw.circle(screen, 'red', ((-(item.x) + 56) * 20, (-(item.y) + 35) * 20), 10)
            else:
                  r = pygame.Rect((-(item.x) + 56) * 20 - 10, (-(item.y) + 35) * 20 - 10, 20, 20)
                  pygame.draw.rect(screen, 'white', r)
    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
