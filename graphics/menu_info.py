'''
Created on 30 oct 2022

@desc: Auxiliary functions related to the menu
@author: Alejandro R. Lopez
'''

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
            




