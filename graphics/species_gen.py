'''
Created on 13 oct 2022

@desc: Species generation and display functions
@author: Alejandro R. Lopez
'''

# Imports
from graphics import species
import numpy as np
import pygame as pg
from math import sqrt

# Global variables
embryos = []

def euclidean_dist(p1, p2):
    """
    Calculates the euclidean distance between two points in a 2D space 
    
        Parameters:
            p1 (int tuple): First point
            p2 (int tuple): Second point
        
        Returns:
            Euclidean distance
    """
    
    return sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2) 

def gen_individuals(n_squares, sq_size, bg_mat, ind_list):
    """
    Generates between 11 and 20 individuals of an species
    
        Parameters:
            n_squares (int): Tiles of each side of the world
            sq_size (int): Size of squares
            bg_mat (int 2d array): Numerical info of the world
            ind_list (list of Species): List of the individuals
    """
    
    # Generate the specimen
    specimen = species.Species(n_squares, sq_size, bg_mat)
    ind_list.append(specimen)
    
    # Generate the normal individuals
    n_ind = np.random.choice(10)+1
    for _ in range(n_ind):
        i = species.Species(n_squares, sq_size, bg_mat, specimen)
        ind_list.append(i)        
    
def display_individuals(ind_list, scr):
    """
    Display each individual as a circle on screen
    
        Parameters:
            ind_list (list of Species): List of the individuals
            scr: Screen display of Pygame
    """
    
    for i in ind_list:
        if i.age <= i.childhood:
            pg.draw.circle(scr, i.colour, (i.location[0]-i.size/4, i.location[1]-i.size/4), i.size/2)
            pg.draw.circle(scr, (0,0,0), (i.location[0]-i.size/4, i.location[1]-i.size/4), i.size/2, 2)
        else:
            pg.draw.circle(scr, i.colour, (i.location[0]-i.size/2, i.location[1]-i.size/2), i.size)
            pg.draw.circle(scr, (0,0,0), (i.location[0]-i.size/2, i.location[1]-i.size/2), i.size, 2)
        #sprite = pg.image.load(i.sprite_path).convert_alpha()
        #sprite = pg.transform.scale(sprite, (i.size, i.size))
        #scr.blit(sprite, (i.location[0]-i.size/2, i.location[1]-i.size/2))
        
def update_individuals(ind_list, n_squares, sq_size, bg_mat):
    """
    Updates individual info for the following day
    
        Parameters:
            ind_list (list of Species): List of the individuals
            n_squares (int): Tiles of each side of the world
            sq_size (int): Size of squares
            bg_mat (int 2d array): Numerical info of the world
    """
    
    for i in ind_list:
        # Growth
        i.age += 1
        # Walking
        i.update_pos(n_squares, sq_size, bg_mat)
        # Conception
        if i.gender == "Female" and i.gestation_days == i.gestation_period:
            for _ in range(i.offspring_number):
                for e in embryos:
                    if e.mother == i: ind_list.append(e)
            i.gestation_days = 0
        # Reproduction
        if i.age >= i.childhood and i.gestation_days == 0:
            for j in ind_list:
                if j.name == i.name and j.gender != i.gender and euclidean_dist(j.location, i.location) <= sq_size:
                    if j.gender == "Female": 
                        j.gestation_days += 1
                        for _ in range(j.offspring_number):
                            embryos.append(species.Species(n_squares, sq_size, bg_mat, i, j))
                    else: 
                        i.gestation_days += 1
                        for _ in range(i.offspring_number):
                            embryos.append(species.Species(n_squares, sq_size, bg_mat, j, i))
                            
    
def death():
    return