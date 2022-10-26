'''
Created on 12 oct 2022

@desc: World generation and display functions
@author: Alejandro R. Lopez
'''

#Imports
import numpy as np
import pygame as pg

# Biome RGB Values
GRASS = 0
SAND = 1
WATER = 2
RGBs = [(0,175,0), (255,204,153), (0,102,204)]

def createBg(n_squares, sq_size):
    """
    Defines the background image of the generated world
    
        Parameters:
            n_squares (int): Tiles of each side of the world
            sq_size (int): Size of squares
        
        Returns:
            bg_mat (int 2d array): Numerical info of the world
    """
    
    # BG Matrix Generation
    bg_mat = [[np.random.choice(3, p=[0.1, 0.0, 0.9]) for _ in range(n_squares)] for _ in range(n_squares)]
    
    # Correct world
    checkWorld(bg_mat, n_squares)
    
    # Print world
    pg.display.init()
    screen = pg.display.set_mode((n_squares*sq_size, n_squares*sq_size))
    
    # Save .png image of the world
    matrix2Img(bg_mat, n_squares, sq_size, screen)
    pg.image.save(screen, "bg.png")
    
    # Save the numerical info of the world
    return bg_mat
    
def matrix2Img(m, n_squares, sq_size, scr):
    """
    Transforms a numerical matrix into an image
    
        Parameters:
            m (list of lists): Background matrix
            n_squares (int): Tiles of each side of the world
            sq_size (int): Size of squares
            scr: Screen display of Pygame
    """
    for x in range(n_squares):
        for y in range(n_squares):
            pg.draw.rect(scr, RGBs[m[x][y]], pg.Rect(x*sq_size, y*sq_size, sq_size, sq_size))
            
def checkWorld(m, n_squares):
    """
    Checks and corrects the world generation
    
        Parameters:
            m (list of lists): Background matrix
            n_squares (int): Tiles of each side of the world
    """
    
    amplifyBiome(m, n_squares)
    
    for x in range(n_squares):
        for y in range(n_squares):
            checkIsland(m, x, y, GRASS, n_squares)
            checkIsland(m, x, y, SAND, n_squares)
            checkPool(m, x, y, n_squares)
            genBeach(m, x, y, n_squares)
            
def amplifyBiome(m, n_squares):
    """
    Amplifies grass zones
    
        Parameters:
            m (list of lists): Background matrix
            n_squares (int): Tiles of each side of the world
    """
        
    for x in range(n_squares):
        for y in range(n_squares):
            if m[x][y] < 2:
                if y-1 >= 0: m[x][y-1] = np.random.choice(3, p=[0.8, 0, 0.2])
                if x-1 >= 0: m[x-1][y] = np.random.choice(3, p=[0.8, 0, 0.2]) 
                if y-1 >= 0 and x-1 >= 0: m[x-1][y-1] = np.random.choice(3, p=[0.6, 0, 0.4])

def checkIsland(m, x, y, i_type, n_squares):
    """
    Remove islands of only one square
    
        Parameters:
            m (list of lists): Background matrix
            x (int): Current row position
            y (int): Current column position
            type (int constant): Biome type of island to check
            n_squares (int): Tiles of each side of the world
    """
    
    lim = n_squares-1
    
    if m[x][y] == i_type:
        island = False
        if (y-1 >= 0 and m[x][y-1] == WATER) and (y+1 <= lim and m[x][y+1] == WATER) and \
           (x-1 >= 0 and m[x-1][y] == WATER) and (x+1 <= lim and m[x+1][y] == WATER): island = True
    
        if island: m[x][y] = WATER
        
def checkPool(m, x, y, n_squares):
    """
    Remove pools of only one square
    
        Parameters:
            m (list of lists): Background matrix
            x (int): Current row position
            y (int): Current column position
            n_squares (int): Tiles of each side of the world
    """
    
    lim = n_squares-1
    
    if m[x][y] == WATER:
        pool = True
        if (y-1 >= 0 and m[x][y-1] == WATER) or (y+1 <= lim and m[x][y+1] == WATER) or \
           (x-1 >= 0 and m[x-1][y] == WATER) or (x+1 <= lim and m[x+1][y] == WATER): pool = False
    
        if pool: m[x][y] = GRASS
        
def genBeach(m, x, y, n_squares):
    """
    Add sand to beach zones
    
        Parameters:
            m (list of lists): Background matrix
            x (int): Current row position
            y (int): Current column position
            n_squares (int): Tiles of each side of the world
    """
    
    lim = n_squares-1
    
    if m[x][y] == GRASS:
        if (y-1 >= 0 and m[x][y-1] == WATER) or (y+1 <= lim and m[x][y+1] == WATER) or \
           (x-1 >= 0 and m[x-1][y] == WATER) or (x+1 <= lim and m[x+1][y] == WATER): 
            m[x][y] = np.random.choice(3, p=[0.6, 0.3, 0.1])
            