'''
Created on 30 oct 2022

@desc: Auxiliary functions related to the menu
@author: Alejandro R. Lopez
'''

# Imports
import pygame as pg

def get_dominant_species(ind_list):
    """
    Finds the dominant species (the one with the largest number of individuals) 
    
        Parameters:
            ind_list (Species list): List of individuals
        
        Returns:
            dominant_name (str): Taxonomical name of the dominant species
    """
    
    species_names = [i.name for i in ind_list]
    max_count = 0
    dominant_name = ""
    
    for n in set(species_names):
        n_occurrences = species_names.count(n)
        if n_occurrences > max_count:
            max_count = n_occurrences
            dominant_name = n
        
    return dominant_name
            
def get_dominant_info(dominant_name, ind_list):
    """
    Gets the mean information for all the individuals of the dominant species
    
        Parameters:
            dominant_name (str): Taxonomical name of the dominant species
            ind_list (Species list): List of individuals
        
        Returns:
            info (list): List of mean attributes of the dominant species
    """
    
    # Initialize all local variables
    info = []
    n_ind = n_fem = old_age_death = age = childhood = gestation_period = \
    offspring_size = offspring_number = terrestrials = aquatics = size = childhood_size = 0
    colour = [0,0,0]
    
    # Add up all the data to compute the means
    for i in ind_list:
        if i.name == dominant_name:
            n_ind += 1
            old_age_death += i.old_age_death
            age += i.age
            childhood += i.childhood
            if i.gender == "Female":
                n_fem += 1
                gestation_period += i.gestation_period
                offspring_size += i.offspring_size
                offspring_number += i.offspring_number
            colour[0] += i.colour[0]
            colour[1] += i.colour[1]
            colour[2] += i.colour[2]
            size += i.size
            childhood_size += i.childhood_size
            
            if i.s_type == "Terrestrial": terrestrials += 1
            elif i.s_type == "Aquatic": aquatics += 1
            
    # Append means to the list
    info.append(i.name)
    info.append(round(old_age_death/n_ind/365,2))
    info.append(round(age/n_ind/365,2))
    info.append(round(childhood/n_ind/30,2))
    if n_fem > 0:
        info.append(round(gestation_period/n_fem/30,2))
        info.append(round(offspring_size/n_fem,2))
        info.append(round(offspring_number/n_fem,2))
    else: 
        info.append(0)
        info.append(0)
        info.append(0)
    colour[0] = round(colour[0]/n_ind)
    colour[1] = round(colour[1]/n_ind)
    colour[2] = round(colour[2]/n_ind)
    info.append(tuple(colour))
    info.append(round(size/n_ind,2))
    info.append(round(childhood_size/n_ind,2))
    info.append(n_ind)
    if terrestrials > aquatics: info.append("Terrestrial")
    else: info.append("Aquatic")
    
    return info

def display_info(info, scr, win_size):
    """
    Displays information on the menu
    
        Parameters:
            info (list): List of mean attributes of the dominant species
            scr: Screen display of Pygame
    """
    
    # Define fonts
    title = pg.font.SysFont('Consolas Bold', round(win_size*0.06))
    subtitle = pg.font.SysFont('Consolas', round(win_size*0.03))
    
    # Generate text
    title_text = title.render("Dominant Species", True, (0,0,0))
    name = subtitle.render(str(info[0]), True, (0,0,0))
    oad = subtitle.render("Life expectancy: "+str(info[1])+" years.", True, (0,0,0))
    age = subtitle.render("Age: "+str(info[2])+" years.", True, (0,0,0))
    childhood = subtitle.render("Childhood period: "+str(info[3])+" months.", True, (0,0,0))
    gp = subtitle.render("Gestation period: "+str(info[4])+" months.", True, (0,0,0))
    off_size = subtitle.render("Offspring size: "+str(info[5])+" m.", True, (0,0,0))
    off_n = subtitle.render("Offspring number: "+str(info[6]), True, (0,0,0))
    size = subtitle.render("Size: "+str(info[8])+" m.", True, (0,0,0))
    childhood_size = subtitle.render("Childhood size: "+str(info[9])+" m.", True, (0,0,0))
    n_ind = subtitle.render("No. of individuals: "+str(info[10]), True, (0,0,0))
    s_type = subtitle.render("Type: "+str(info[11]), True, (0,0,0))
    
    # Display text on screen
    scr.blit(title_text, (win_size*0.15, win_size*0.14))
    scr.blit(name, (win_size*0.15, win_size*0.20))
    scr.blit(age, (win_size*0.18, win_size*0.26))
    scr.blit(size, (win_size*0.18, win_size*0.32))
    scr.blit(s_type, (win_size*0.18, win_size*0.38))
    scr.blit(oad, (win_size*0.18, win_size*0.44))
    scr.blit(off_n, (win_size*0.18, win_size*0.50))
    scr.blit(off_size, (win_size*0.18, win_size*0.56))
    scr.blit(gp, (win_size*0.18, win_size*0.62))
    scr.blit(childhood, (win_size*0.18, win_size*0.68))
    scr.blit(childhood_size, (win_size*0.18, win_size*0.74))
    scr.blit(n_ind, (win_size*0.18, win_size*0.80))
    
    # Display images for size comparison
    if info[8] > 1:
        tree = pg.image.load(".\\img\\tree.png").convert_alpha()
        tree = pg.transform.scale(tree, (win_size*0.18, win_size*0.18))
        scr.blit(tree, (win_size*0.65, win_size*0.20)) 
        
        new_size = info[8]*win_size*0.18/15
        pg.draw.circle(scr, info[7], (win_size*0.65-new_size/3, win_size*0.38-new_size/2), new_size/2)
        pg.draw.circle(scr, (0,0,0), (win_size*0.65-new_size/3, win_size*0.38-new_size/2), new_size/2, 3)
    else:
        stone = pg.image.load(".\\img\\stone.png").convert_alpha()
        stone = pg.transform.scale(stone, (win_size*0.1, win_size*0.1))
        scr.blit(stone, (win_size*0.73, win_size*0.20)) 
        
        new_size = info[8]*win_size*0.1
        pg.draw.circle(scr, info[7], (win_size*0.73-new_size/2-3, win_size*0.30-new_size/2-3), new_size/2)
        pg.draw.circle(scr, (0,0,0), (win_size*0.73-new_size/2-3, win_size*0.30-new_size/2-3), new_size/2, 3)          
    
    
    
    
    
    
    


