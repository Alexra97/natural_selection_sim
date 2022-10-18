'''
Created on 12 oct 2022

@desc: Simple simulation of evolving process and natural selection
@author: Alejandro R. Lopez
'''

# Imports
import pygame as pg
from graphics import world_gen as wg
from graphics import species_gen as sg
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
day_speed = 0.3


# Pyhame display initialitation
pg.display.init()
screen = pg.display.set_mode((n_squares*sq_size, n_squares*sq_size))
pg.display.set_caption('Natural Selection Simulator')
pg.font.init()
font = pg.font.SysFont('Consolas', 30)

# Create a new random world
bg_mat = wg.createBg(n_squares, sq_size)

# Load it as an image
bg = pg.image.load("bg.png").convert()
screen.blit(bg, (0, 0))

# Main loop
while not finish:
    for event in pg.event.get():
        # X event
        if event.type == pg.QUIT:
            finish = True
            
        # Key down events
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:                                    # Esc to exit
                finish = True
            elif event.key == pg.K_RIGHT:                                   # Right arrow to advance time
                pause_time = False    
            elif event.key == pg.K_UP:                                      # Up arrow to increase advancing speed
                day_speed /= 2
            elif event.key == pg.K_DOWN:                                    # Down arrow to decrease advancing speed
                day_speed *= 2
            elif event.key == pg.K_SPACE:                                   # Space to generate new species
                sg.gen_individuals(n_squares, sq_size, bg_mat, individuals) 
        # Key up events
        elif event.type == pg.KEYUP:
            if event.key == pg.K_RIGHT:
                    pause_time = True
  
    # Display each individual
    sg.display_individuals(individuals, screen)  
    
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
