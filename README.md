# Natural Selection Simulator
A 2D simulation of the evolution and natural selection processes.  
Alejandro R. López

## Goal
This independent project aims to check if theoretical organisms can develop their characteristics in a simple rule system environment. If there is evidence of natural selection and evolution of the species, we can assume that these processes are also occurring in the complex natural ecosystem, as Charles Darwin postulated in 1859.

## Hypothesis
Given the appropriate initial conditions, as well as rules that direct the survival probability of each individual, the hypothesis is that any species will reach the best properties for its survival in an infinite time, approaching the limits allowed by the rule system, such as the maximum size, the minimum period of gestation, etc.

## Files
Scripts are organized according to the following structure:  

* **PROJECT**
	* **graphics [package]**  
		* menu_info.py: Functions to get data of the species and display it on the screen.  
		* species.py: Class that defines the Species structure and functions.  
		* species_gen.py: Species generation and updating functions.  
		* world_gen.py: World generation functions.  
	* **img [folder]**: Graphical resources.  
	* **main.py**: Main loop with data initialitation.
	* **tax_first.txt**: List of possible first taxonomical names.
	* **tax_sec.txt**: List of possible second taxonomical names.
