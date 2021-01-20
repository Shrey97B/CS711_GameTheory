# Game Theory Assignment - Computing Equilibrium in Games
In the given programming assignment, the NFG and EFG games are provided in the form of GAMBIT files. The objective is to prepare a program to programmatically compute the equilibriums like SDSE, WDSE, PSNE, SPNE and and converting EFG to NFG. The program has been written in python with driver code in `driver.py` and util components in `compute.py`. The code in driver is self explanatory for determining the util function.

The five components of the program are as follows:
1. SDSE: Given a Normal form game override the computeSDS function to compute the SDSE of the NFG. The output is in the form of an array of size player1_numstrategies + player2_numstrategies+ ... + playern_numstrategies and consists of 1 and 0 with 1 denoting the strategy of players which is a component of SDSE or is a strongly dominant strategy, otherwise 0.
2. WDSE: Given a Normal form game override the computeWDS function to compute the WDSE of the NFG. The output is in the form of an array of size player1_numstrategies + player2_numstrategies+ ... + playern_numstrategies and consists of 1 and 0 with 1 denoting the strategy of players which is a component of WDSE or is a weakly dominant strategy, otherwise 0.
3. PSNE: Given a Normal form game override the computePSNE function to compute the PSNE of the NFG. The output is in the form of a list of all possible PSNE with each PSNE also being a list describing the strategy number of players that are involved in equilibrium.
4. EFG to NFG: Given an EFG (PIEFG or IIEFG), the given function efg_NFG outputs a string representing the corresponding NFG of the game.
5. SPNE: Given a PIEFG, the function computeSPNE outputs the all the possible SPNE for the game in the form of a list denoting the strategy of players forming the SPNE.

## Running the Setup
In the `Driver.py` file, the appropriate function needs to be called present int he `compute.py` file which will return the corresponding list or string as per requirement.
The program can be executed using python3 as `python3 driver.py` command.
