'''
Created on 13 oct 2022

@desc: Species class definition
@author: Alejandro R. Lopez
'''

# Imports
import numpy as np
from math import ceil
from os import listdir
from os.path import isfile, join

# Global variables
tax_first = open("tax_first.txt", "r")
tax_sec = open("tax_sec.txt", "r")
names1 = tax_first.read().split("\n")
names2 = tax_sec.read().split("\n")
genders = ["Male", "Female"]
types = ["Terrestrial", "Aquatic", "Aerial"]
sprites_terr = [f for f in listdir(".\\sprites\\terrestrial\\") if isfile(join(".\\sprites\\terrestrial\\", f))]
sprites_aq = [f for f in listdir(".\\sprites\\aquatic\\") if isfile(join(".\\sprites\\aquatic\\", f))]
sprites_aer = [f for f in listdir(".\\sprites\\aerial\\") if isfile(join(".\\sprites\\aerial\\", f))]
species = []

tax_first.close()
tax_sec.close()

def set_position(s_type, n_squares, sq_size, bg_mat, prev_pos = None):
    """
    Creates a new position or modifies a previous one for an individual
    
        Parameters:
            s_type (str): Type of individual based on his habitat
            n_squares (int): Tiles of each side of the world
            sq_size (int): Size of squares
            bg_mat (int 2d array): Numerical info of the world
            prev_pos (int tuple): Previous location of the individual
            
        Returns:
            New position in form of a two element tuple
    """
    
    # First position of specimen case
    if prev_pos is None:
        x = np.random.choice(n_squares*sq_size-1)
        y = np.random.choice(n_squares*sq_size-1)
                
        # Detect habitat borders
        if s_type == "Terrestrial":
            while bg_mat[ceil(x/sq_size)-1][ceil(y/sq_size)-1] == 2:
                x = np.random.choice(n_squares*sq_size-1)
                y = np.random.choice(n_squares*sq_size-1)
        elif s_type == "Aquatic":
            while bg_mat[ceil(x/sq_size)-1][ceil(y/sq_size)-1] != 2:
                x = np.random.choice(n_squares*sq_size-1)
                y = np.random.choice(n_squares*sq_size-1)
    
    # First position of normal individuals or walking case
    else:
        max_move_frwd = round(sq_size*0.33)
        max_move_bkwd = round(sq_size*-0.33)
        x = prev_pos[0] + np.random.choice(range(max_move_bkwd, max_move_frwd))
        y = prev_pos[1] + np.random.choice(range(max_move_bkwd, max_move_frwd))
        
        # Check window limits
        if x > n_squares*sq_size: x = n_squares*sq_size
        if y > n_squares*sq_size: y = n_squares*sq_size
        if x < 0: x = 0
        if y < 0: y = 0
                
        # Detect habitat borders
        if s_type == "Terrestrial":
            while bg_mat[ceil(x/sq_size)-1][ceil(y/sq_size)-1] == 2:
                x = prev_pos[0] + np.random.choice(range(max_move_bkwd, max_move_frwd))
                y = prev_pos[1] + np.random.choice(range(max_move_bkwd, max_move_frwd))
                
                # Check window limits
                if x > n_squares*sq_size: x = n_squares*sq_size
                if y > n_squares*sq_size: y = n_squares*sq_size
                if x < 0: x = 0
                if y < 0: y = 0
        elif s_type == "Aquatic":
            while bg_mat[ceil(x/sq_size)-1][ceil(y/sq_size)-1] != 2:
                x = prev_pos[0] + np.random.choice(range(max_move_bkwd, max_move_frwd))
                y = prev_pos[1] + np.random.choice(range(max_move_bkwd, max_move_frwd))
                
                # Check window limits
                if x > n_squares*sq_size: x = n_squares*sq_size
                if y > n_squares*sq_size: y = n_squares*sq_size
                if x < 0: x = 0
                if y < 0: y = 0
            
    return (x, y)

def create_tax_name():
    """
    Creates a new taxonomical name for a species
            
        Returns:
            tax_name (str): Taxonomical name
    """
    
    # Check limit of possible unique names (44*44 = 1936)
    if len(species) == 1936:
        print("ATTENTION: You have reached the limit of species.")
    else:
        tax_name = names1[np.random.choice(len(names1))] + names2[np.random.choice(len(names2))]
        
        # Check that the name is unique
        while tax_name in species:
            tax_name = names1[np.random.choice(len(names1))] + names2[np.random.choice(len(names2))]
        
        species.append(tax_name)
        return tax_name

def get_species_names():
    """
    Returns the list of species
            
        Returns:
            species (str list): List of species names
    """
    
    return species

class Species:
    """
    A class to represent a species.

        Attributes
        ----------
            death_prob : float
                Probability of death
            old_age_death : int
                Life expectancy
            age : int
                Days alive
            gender : str
                Gender of the individual
            childhood : int
                Duration of childhood
            gestation_days : int
                Current days of gestation since fertilization
            gestation_period: int
                Duration of gestation in females
            offspring_size : int
                Size of embryos
            offspring_number : int
                Number of embryos
            s_type : str
                Individual type based on its habitat
            colour : int tuple
                Colour of the individual
            size : int
                Size of the individual
            location : int tuple
                Position of the individual
            sprite_path : str
                Path to the sprite for the species
            childhood_size : int
                Size of hatchling during its childhood
            growth : int
                Size growth between days
            mother : Species
                Mother object of the individual if exists
        

        Methods
        -------
            update_pos(n_squares, sq_size, bg_mat):
                Sets a new position for the individual near the previous one
    """
    
    def __init__(self, n_squares, sq_size, bg_mat, specimen = None, mother = None):
        """
        Initializes all the attributes for the species object.

        Parameters
        ----------
            n_squares : int
                Tiles of each side of the world
            sq_size : int
                Size of squares
            bg_mat : int 2d array
                Numerical info of the world
            specimen : Species
                Specimen to imitate its properties if needed
        """
             
        # Common attributes
        self.childhood = np.random.choice(75)+15    
        
        # Specimen attributes
        if specimen is None:
            self.name = create_tax_name()
            self.age = np.random.choice(75)
            self.s_type = types[np.random.choice(3)]
            self.colour = list(np.random.choice(256, 3))
            self.size = np.random.choice(round(sq_size*0.25))+1  
            self.location = set_position(self.s_type, n_squares, sq_size, bg_mat)
            self.old_age_death = np.random.choice(2190)+730
            self.childhood_size = np.random.choice(round(self.size/3)+1)+1
            self.growth = round((self.size-self.childhood_size)/self.childhood)
            self.mother = None
            if self.s_type == "Terrestrial":   
                self.sprite_path = ".\\sprites\\terrestrial\\" + sprites_terr[np.random.choice(len(sprites_terr))] 
            elif self.s_type == "Aquatic":
                self.sprite_path = ".\\sprites\\aquatic\\" + sprites_aq[np.random.choice(len(sprites_aq))]
            elif self.s_type == "Aerial":
                self.sprite_path = ".\\sprites\\aerial\\" + sprites_aer[np.random.choice(len(sprites_aer))]
                
        # Normal individual attributes
        elif specimen is not None and mother is None :
            self.name = specimen.name
            self.age = np.random.choice(75)
            self.s_type = specimen.s_type
            self.colour = specimen.colour
            self.location = set_position(self.s_type, n_squares, sq_size, bg_mat, specimen.location)
            self.sprite_path = specimen.sprite_path
            self.old_age_death = specimen.old_age_death + np.random.choice(range(-700, 730))
            self.mother = None
            size_chg_pct = round(specimen.size/10)
            if size_chg_pct == 0: size_chg_pct = 1
            self.size = specimen.size + np.random.choice(range(-size_chg_pct, size_chg_pct))
            self.childhood_size = np.random.choice(round(self.size/3)+1)+1
            self.growth = round((self.size-self.childhood_size)/self.childhood)
        
        # Offspring attributes
        else:
            fathers = [specimen, mother]
            self.name = mother.name
            self.age = 0
            self.s_type = fathers[np.random.choice(2)].s_type
            self.colour = fathers[np.random.choice(2)].colour
            self.location = mother.location
            self.sprite_path = mother.sprite_path
            self.old_age_death = fathers[np.random.choice(2)].old_age_death + np.random.choice(range(-700, 730))
            self.size = fathers[np.random.choice(2)].size
            self.childhood_size = mother.offspring_size
            self.growth = round((self.size-self.childhood_size)/self.childhood)
            self.mother = mother
        
        # Common attributes
        ## Death
        self.death_prob = 0.0 
        ## Reproduction
        self.gender = genders[np.random.choice(2)]
        self.gestation_days = 0
        if self.gender == "Male": 
            self.gestation_period = None
            self.offspring_size = None
            self.offspring_number = None
        elif self.gender == "Female": 
            self.gestation_period = np.random.choice(150)+150
            self.offspring_size = np.random.choice(round(self.size/3)+1)+1
            max_offspring_n = round(round(self.size*0.33)/self.offspring_size)
            if max_offspring_n == 0: max_offspring_n = 1
            self.offspring_number = np.random.choice(max_offspring_n)+1
            
            
    def update_pos(self, n_squares, sq_size, bg_mat):
        """
        Sets a new position for the individual near the previous one 

        Parameters
        ----------
            n_squares : int
                Tiles of each side of the world
            sq_size : int
                Size of squares
            bg_mat : int 2d array
                Numerical info of the world
        """
        
        self.location = set_position(self.s_type, n_squares, sq_size, bg_mat, self.location)
    