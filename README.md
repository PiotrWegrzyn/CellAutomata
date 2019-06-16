The App implements 3 types of Cell Automata:
* 1D Elementar with a user-specified Rule
* 2D with Life-Like Automata (default is the famous Game Of Life but you can specify any rule)
* 2D simulation of Crystallites (also refered as grains:  https://en.wikipedia.org/wiki/Crystallite ) nucleation. After nucleation we apply Monte Carlo method in order to smoothen their borders and after that is finished we Recrystallize ( https://en.wikipedia.org/wiki/Recrystallization_(metallurgy) ) the grains. 


After downloading download packages 
by running the following command *in project's directory* :
'python pip install -r requirements.txt'

To start the app run:
python main.py


The saved patterns from 2D liflike automata and the data exports from Recrystallization are in Patterns directory.
Loading state from files is still a work in progress (like the whole app) 
so you may find some bugs if you do some unordinary stuff with them.
