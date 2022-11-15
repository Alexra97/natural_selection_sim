'''
Created on 12 oct 2022

@desc: Simple simulation of evolving process and natural selection
@author: Alejandro R. Lopez
'''

# Imports
import pygame as pg
from graphics import world_gen as wg
from graphics import species_gen as sg
from graphics import menu_info as mi
import time

# Variables
## Screen size
n_squares = 25
sq_size = 35
## Main loop
finish = False
days = 0
individuals = []
pause_time = True
day_speed = 0.15
menu = False

# Pyhame display initialitation
pg.display.init()
screen = pg.display.set_mode((n_squares*sq_size, n_squares*sq_size))
pg.display.set_caption('Natural Selection Simulator')
pg.font.init()
font = pg.font.SysFont('Consolas', 30)

# Create a new random world and save it
bg_mat = wg.createBg(n_squares, sq_size)

# Load pre-saved images
bg = pg.image.load("bg.png").convert()
menu_img = pg.image.load(".\\img\\menu.png").convert_alpha()
menu_img = pg.transform.scale(menu_img, (n_squares*sq_size*0.8, n_squares*sq_size*0.8))

# Main loop
while not finish:
    for event in pg.event.get():
        # X event
        if event.type == pg.QUIT:
            finish = True
            
        # Key down events
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:                                                # Esc to exit
                finish = True
            elif event.key == pg.K_RIGHT and menu == False:                             # Right arrow to advance time
                pause_time = False    
            elif event.key == pg.K_UP:                                                  # Up arrow to increase advancing speed
                day_speed /= 2
            elif event.key == pg.K_DOWN:                                                # Down arrow to decrease advancing speed
                day_speed *= 2
            elif event.key == pg.K_SPACE and menu == False:                             # Space to generate new species
                sg.gen_individuals(n_squares, sq_size, bg_mat, individuals, 49) 
            elif event.key == pg.K_m:  
                if individuals: menu = not menu                                         # M to open or close the menu
                           
        # Key up events
        elif event.type == pg.KEYUP:
            if event.key == pg.K_RIGHT:
                    pause_time = True
  
    
    # Display world
    screen.blit(bg, (0, 0))
    
    # Display each individual
    sg.display_individuals(individuals, screen)  
    
    # Display menu
    if menu:
        screen.blit(menu_img, (n_squares*sq_size*0.1, n_squares*sq_size*0.1))   
        dominant_name = mi.get_dominant_species(individuals)
        info = mi.get_dominant_info(dominant_name, individuals)
        mi.display_info(info, screen, n_squares*sq_size)
    
    # When time is advancing
    if not pause_time:
        days += 1
        screen.blit(bg, (0, 0))
        sg.update_individuals(individuals, n_squares, sq_size, bg_mat) 
        sg.display_individuals(individuals, screen) 
        time.sleep(day_speed)
     
    # Display day counter   
    text = font.render("Day: "+str(days), True, (0,0,0), (255,255,230))
    screen.blit(text, (5,0))
    
    # Update display
    pg.display.flip()

# Free resources
del individuals[:]
pg.quit()
