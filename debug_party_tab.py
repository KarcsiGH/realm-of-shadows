"""
Debug overlay: run this instead of python3 main.py
Opens camp UI on the Party tab and draws red outlines
around every clickable area so you can see them.
Press Q to quit, LEFT/RIGHT to cycle characters.
"""
import sys, os
sys.path.insert(0, os.path.expanduser('~/Documents/RealmOfShadows'))

import pygame
pygame.init()
screen = pygame.display.set_mode((1440, 900))
pygame.display.set_caption("Party Tab Debug")
clock = pygame.time.Clock()

from core.character import Character
from core.abilities import CLASS_ABILITIES

# Make a Fighter with some inventory and abilities
c = Character('Aldric', 'Fighter')
c.inventory = [
    {'name': 'Health Potion', 'type': 'consumable', 'identified': True, 'heal': 50},
    {'name': 'Iron Sword', 'type': 'weapon', 'slot': 'weapon', 'identified': True},
    {'name': 'Chain Mail', 'type': 'armor', 'slot': 'body', 'identified': True},
]
c.equipment = {'weapon': {'name': 'Short Sword', 'type': 'weapon', 'slot': 'weapon', 'identified': True}}
c.resources = {'HP': 60}
c.level = 3
c.abilities = [a.copy() for a in CLASS_ABILITIES.get('Fighter', []) if a.get('level',1) <= 3]

# Cleric with heal spell
c2 = Character('Sera', 'Cleric')
c2.inventory = [{'name': 'Scroll of Identify', 'type': 'consumable', 'subtype': 'scroll', 'identified': True}]
c2.equipment = {}
c2.resources = {'HP': 45, 'INT-MP': 20}
c2.level = 3
c2.abilities = [a.copy() for a in CLASS_ABILITIES.get('Cleric', []) if a.get('level',1) <= 3]

from camp_ui import CampUI
ui = CampUI([c, c2], location='dungeon')
ui.tab = 4  # Party tab

font_sm = pygame.font.Font(None, 18)

running = True
while running:
    mx, my = pygame.mouse.get_pos()
    for e in pygame.event.get():
        if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_q):
            running = False
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_LEFT and ui.selected_char > 0:
                ui.selected_char -= 1
            elif e.key == pygame.K_RIGHT and ui.selected_char < len(ui.party)-1:
                ui.selected_char += 1
        elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            result = ui.handle_click(mx, my)
            print(f"Click ({mx},{my}) → {result}, hit_map had {len(getattr(ui,'_stats_hit_map',{}))} keys")

    ui.draw(screen, mx, my)

    # Draw red outlines + labels over every hit zone
    hm = getattr(ui, '_stats_hit_map', {})
    for key, rect in hm.items():
        col = (255,80,80) if rect.collidepoint(mx,my) else (255,0,0)
        pygame.draw.rect(screen, col, rect, 2)
        label = font_sm.render(key[:20], True, (255,200,0))
        screen.blit(label, (rect.x+2, rect.y+1))

    # HUD
    hud = font_sm.render(
        f"Hit zones: {len(hm)}  |  selected_item: {ui._stats_inv_sel}  |  Q=quit  ←→=char",
        True, (200,200,80))
    screen.blit(hud, (4, 876))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
