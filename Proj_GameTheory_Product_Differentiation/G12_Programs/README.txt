Alliance_CopelandWinner.py and Alliance_KemenyYoung.py
------------------------------------------------------

The above codes implement the Copeland Winner and Kemeny Young Winner to compute the Conorcet Winner alliance.
To run the above files use:

python3 Alliance_CopelandWinner.py
or
python3 Alliance_KemenyYoung.py

Edit the variable FILE_PATH to point to the input file

The format of the data required is as follows:

N L K
M1 M2 .... MN
P11 P12 .... P1N
P21 P22 .... P2N
.
.
PL1 PL2 .... PLN

N -> Number of mobile products being considered
L -> Number of preferences
K -> Length of alliance or number of mobiles that can be manufactured
In next line space delimited N model names are provided
L lines follow each describing a preference.
Each line contains some order of the model

File Data_1.txt and Data_2.txt are sample for the same.

Game_theory.py
----------------------------------------------------------------------

The above script implements the static equilibrium plot as mentioned in the report.

Following commands can be used in order to run the project for desired outputs

Running Requirements:
1. Python3
note- kindly check the python executable (.exe) file in the location where python is installed. The executable file must be named "python3.exe". If that is not the case, kindly rename the executable file to "python3.exe" before running the assign2.sh
2. numpy
Install command:
pip install numpy
3. Matplotlib
Install command:
pip install matplotlib
4. Math
Install command:
pip install python-math

Steps:-
Run following commands on Linux:
chmod +x run.sh
./run.sh

dynamic_pricing.py
--------------------------------------------------------

The above script implements the dynamic equilibrium plot as mentioned in the report.
python3 dynamic_pricing.py