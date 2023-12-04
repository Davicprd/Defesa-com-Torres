# Defense Towers Game Solver

This program uses Z3 library to solve the Defense Towers game, where towers equipped with cannons need to be strategically placed to defend against attackers.

## Description

The Defense Towers game is played on a grid-like map where towers ('T') need to be equipped with cannons to fend off attackers ('n'). The cannons have four possible orientations:
1. Left and Down
2. Down and Right
3. Right and Up
4. Up and Left

The goal is to position the cannons in such a way that, when fired, they destroy all attackers without damaging any towers. The program takes a map as input, representing the layout of the towers, attackers, and castles. It then uses Z3 solver to find the optimal orientations for the cannons to achieve the objective.

## Usage

The main code is contained in the file `defense_towers_solver.py`. To use the program:
1. Provide the map layout in the specified format within the code or through user input.
2. Run the script.
3. The program will output the optimized map with cannon orientations.

## Dependencies

The program relies on the Z3 library for solving the logical constraints.

## Installation

1. Clone the repository: ```git clone https://github.com/Davicprd/Defesa-com-Torres```
2. Install Z3 library (if not installed): ```pip install z3-solver```
3. Run the program using Python: ```python defense_towers_solver.py```

