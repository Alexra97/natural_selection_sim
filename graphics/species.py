'''
Created on 13 oct 2022

@desc: Species class definition
@author: Alejandro R. Lopez
'''

# Imports
import random
from math import ceil

# Global variables
tax_first = open("tax_first.txt", "r")
tax_sec = open("tax_sec.txt", "r")
names1 = tax_first.read().split("\n")
names2 = tax_sec.read().split("\n")
genders = ["Male", "Female"]
types = ["Terrestrial", "Aquatic"]
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
        x = random.randint(0, n_squares*sq_size-1)
        y = random.randint(0, n_squares*sq_size-1)
                
        # Detect habitat borders
        if s_type == "Terrestrial":
            while bg_mat[ceil(x/sq_size)-1][ceil(y/sq_size)-1] == 2:
                x = random.randint(0, n_squares*sq_size-1)
                y = random.randint(0, n_squares*sq_size-1)
        elif s_type == "Aquatic":
            while bg_mat[ceil(x/sq_size)-1][ceil(y/sq_size)-1] != 2:
                x = random.randint(0, n_squares*sq_size-1)
                y = random.randint(0, n_squares*sq_size-1)
    
    # First position of normal individuals or walking case
    else:
        max_move_frwd = round(sq_size*0.5)
        max_move_bkwd = round(sq_size*-0.5)
        x = prev_pos[0] + random.randint(max_move_bkwd, max_move_frwd)
        y = prev_pos[1] + random.randint(max_move_bkwd, max_move_frwd)
        
        # Check window limits
        if x > n_squares*sq_size: x = n_squares*sq_size
        if y > n_squares*sq_size: y = n_squares*sq_size
        if x < 0: x = 0
        if y < 0: y = 0
                
        # Detect habitat borders
        if s_type == "Terrestrial":
            while bg_mat[ceil(x/sq_size)-1][ceil(y/sq_size)-1] == 2:
                x = prev_pos[0] + random.randint(max_move_bkwd, max_move_frwd)
                y = prev_pos[1] + random.randint(max_move_bkwd, max_move_frwd)
                
                # Check window limits
                if x > n_squares*sq_size: x = n_squares*sq_size
                if y > n_squares*sq_size: y = n_squares*sq_size
                if x < 0: x = 0
                if y < 0: y = 0
        elif s_type == "Aquatic":
            while bg_mat[ceil(x/sq_size)-1][ceil(y/sq_size)-1] != 2:
                x = prev_pos[0] + random.randint(max_move_bkwd, max_move_frwd)
                y = prev_pos[1] + random.randint(max_move_bkwd, max_move_frwd)
                
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
        tax_name = names1[random.randint(0, len(names1)-1)] + names2[random.randint(0, len(names2)-1)]
        
        # Check that the name is unique
        while tax_name in species:
            tax_name = names1[random.randint(0, len(names1)-1)] + names2[random.randint(0, len(names2)-1)]
        
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
            offspring_size : float
                Size of embryos
            offspring_number : int
                Number of embryos
            s_type : str
                Individual type based on its habitat
            colour : int tuple
                Colour of the individual
            size : float
                Size of the individual
            location : int tuple
                Position of the individual
            childhood_size : float
                Size of hatchling during its childhood
            growth : float
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
        
        # Specimen attributes
        if specimen is None:
            self.name = create_tax_name()
            self.s_type = types[random.randint(0,1)]
            self.colour = list(random.sample(range(0, 255), 3))
            self.size = random.uniform(0, sq_size*0.4) 
            self.location = set_position(self.s_type, n_squares, sq_size, bg_mat)
            self.old_age_death = random.randint(60,365)
            self.childhood = round(random.uniform(0.1,0.5) * self.old_age_death)+1
            self.age = random.randint(self.childhood, self.old_age_death)
            self.childhood_size = random.uniform(0.1, self.size*0.4)
            self.growth = (self.size-self.childhood_size)/self.childhood
            self.mother = None
            self.offspring_size = random.uniform(0.1, 0.4)*self.size
            self.offspring_number = random.randint(1, round(self.size*0.4/self.offspring_size)+1)
            self.gestation_period = round(random.uniform(0.1, 0.3) * self.old_age_death)
                
        # Normal individual attributes
        elif specimen is not None and mother is None :
            self.name = specimen.name
            self.s_type = specimen.s_type
            self.colour = specimen.colour
            self.location = set_position(self.s_type, n_squares, sq_size, bg_mat, specimen.location)
            self.old_age_death = specimen.old_age_death
            self.mother = None
            self.size = specimen.size + random.uniform(-specimen.size*0.1, specimen.size*0.1)
            self.childhood = specimen.childhood
            self.age = random.randint(self.childhood, self.old_age_death)
            self.childhood_size = random.uniform(0.1, self.size*0.4)
            self.growth = (self.size-self.childhood_size)/self.childhood
            self.offspring_size = random.uniform(0.1, 0.4)*self.size
            self.offspring_number = random.randint(1, round(self.size*0.4/self.offspring_size)+1)
            self.gestation_period = round(random.uniform(0.1, 0.3) * self.old_age_death)
        
        # Offspring attributes
        else:
            mutation_prob = 0.1
            
            fathers = [specimen, mother]
            self.name = mother.name
            self.age = 0
            self.s_type = fathers[random.randint(0,1)].s_type
            self.location = mother.location
            self.old_age_death = fathers[random.randint(0,1)].old_age_death + random.randint(-30,30)
            self.mother = mother
            self.childhood_size = mother.offspring_size
            
            # Possible mutations
            if random.uniform(0,1) <= mutation_prob: self.colour = list(random.sample(range(0, 255), 3))
            else: self.colour = fathers[random.randint(0,1)].colour
            if random.uniform(0,1) <= mutation_prob: self.size = random.uniform(0, sq_size*0.4) 
            else: self.size = fathers[random.randint(0,1)].size
            if random.uniform(0,1) <= mutation_prob: self.offspring_size = random.uniform(0.1, 0.4)*self.size
            else: self.offspring_size = mother.offspring_size
            if random.uniform(0,1) <= mutation_prob: self.offspring_number = random.randint(1, round(self.size*0.4/self.offspring_size)+1)
            else: self.offspring_number = mother.offspring_number
            if random.uniform(0,1) <= mutation_prob: self.gestation_period = round(random.uniform(0.1, 0.3) * self.old_age_death)
            else: self.gestation_period = mother.gestation_period
            if random.uniform(0,1) <= mutation_prob: self.childhood = round(random.uniform(0.1,0.5) * self.old_age_death)+1
            else: self.childhood = fathers[random.randint(0,1)].childhood
            
            
            self.growth = (self.size-self.childhood_size)/self.childhood
        
        # Common attributes
        ## Death
        self.death_prob = 0.0 
        ## Reproduction
        self.gender = genders[random.randint(0,1)]
        self.gestation_days = 0     
                    
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
    