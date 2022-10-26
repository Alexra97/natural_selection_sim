'''
Created on 13 oct 2022

@desc: Species generation and display functions
@author: Alejandro R. Lopez
'''

# Imports
from graphics import species
import numpy as np
import pygame as pg
from math import sqrt, ceil

# Biome RGB Values
GRASS = 0
SAND = 1
WATER = 2
RGBs = [(0,175,0), (255,204,153), (0,102,204)]

# Global variables
embryos = []

def euclidean_dist(p1, p2):
    """
    Calculates the euclidean distance between two points in a 2D or 3D space 
    
        Parameters:
            p1 (int tuple): First point
            p2 (int tuple): Second point
        
        Returns:
            Euclidean distance
    """
    
    if len(p1) == 2: return sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2) 
    elif len(p1) == 3: return sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2+(p1[2]-p2[2])**2)

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
    n_ind = 50
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
            pg.draw.circle(scr, i.colour, (i.location[0]-i.childhood_size/2, i.location[1]-i.childhood_size/2), i.childhood_size)
            pg.draw.circle(scr, (0,0,0), (i.location[0]-i.childhood_size/2, i.location[1]-i.childhood_size/2), i.childhood_size, 2)
        else:
            pg.draw.circle(scr, i.colour, (i.location[0]-i.size/2, i.location[1]-i.size/2), i.size)
            pg.draw.circle(scr, (0,0,0), (i.location[0]-i.size/2, i.location[1]-i.size/2), i.size, 2)
        
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
        # Growing up
        i.age += 1
        if i.age <= i.childhood: i.childhood_size += i.growth
        # Walking
        i.update_pos(n_squares, sq_size, bg_mat)
        # Conception
        if i.gender == "Female" and i.gestation_days == i.gestation_period:
            for _ in range(i.offspring_number):
                for e in embryos:
                    if e.mother == i: ind_list.append(e)
            i.gestation_days = 0
        # Reproduction
        if i.gender == "Female" and i.age >= i.childhood and i.gestation_days == 0:
            for j in ind_list:
                if j.name == i.name and j.gender == "Male" and euclidean_dist(j.location, i.location) <= sq_size:
                    i.gestation_days += 1
                    for _ in range(i.offspring_number):
                        embryos.append(species.Species(n_squares, sq_size, bg_mat, j, i))
                    break
        # Pregnancy
        if i.gestation_days > 0: i.gestation_days += 1
        # Death
        calculate_death_prob(i, bg_mat, sq_size)
        if i.death_prob*100 >= np.random.choice(100)+1: ind_list.remove(i)
                            
    
def calculate_death_prob(i, bg_mat, sq_size):
    # Define probabilities
    death_prob = 0.01
    child_prob = 0.001
    old_prob = 0.5
    size_prob = 0.001
    cammo_prob = 0.0001
        
    # Age
    if i.age <= i.childhood: death_prob += child_prob  
    elif i.age >= i.old_age_death: death_prob += old_prob  
    # Size
    if i.age <= i.childhood: death_prob -= i.childhood_size*size_prob
    else:
        if i.size > 0: death_prob -= i.size*size_prob
        
    
    # Camouflage
    habitat = bg_mat[ceil(i.location[0]/sq_size)-1][ceil(i.location[1]/sq_size)-1]
    cammo_diff = euclidean_dist(i.colour, RGBs[habitat])
    death_prob += cammo_diff*cammo_prob
    
    # Update probability
    i.death_prob = death_prob




